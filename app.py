import streamlit as st
import os
from openai import OpenAI
import json
import logging
from logging.handlers import RotatingFileHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Tuple, Dict, Any
import importlib.util
from collections import Counter, defaultdict
import time
from datetime import datetime, timedelta
import threading
import random

# Constantes pour le rate limiting global
MAX_GLOBAL_REQUESTS = 100  # Maximum de requêtes globales
RESET_INTERVAL = 600     # 10 minutes en secondes

def display_analysis_summary(question: str, detailed_analysis: str):
    """
    Affiche un résumé de l'analyse en termes accessibles aux non-juristes
    """
    st.info(f"""
    📋 Notre compréhension de votre situation :
    
    {detailed_analysis}
    
    Sur la base de cette analyse, nous allons maintenant vous proposer une estimation adaptée à votre situation.
    """)

def check_global_limit() -> Tuple[bool, int]:
    """
    Vérifie la limite globale de requêtes
    Retourne (peut_continuer, requetes_restantes)
    """
    current_time = time.time()

    # Initialisation des variables globales si nécessaires
    if 'global_request_count' not in st.session_state:
        st.session_state.global_request_count = 0
    if 'last_reset_time' not in st.session_state:
        st.session_state.last_reset_time = current_time

    # Vérifier si on doit réinitialiser le compteur
    if current_time - st.session_state.last_reset_time > RESET_INTERVAL:
        st.session_state.global_request_count = 0
        st.session_state.last_reset_time = current_time

    # Vérifier si on a atteint la limite
    if st.session_state.global_request_count >= MAX_GLOBAL_REQUESTS:
        time_until_reset = RESET_INTERVAL - (current_time - st.session_state.last_reset_time)
        minutes_left = int(time_until_reset / 60)
        return False, minutes_left

    # Incrémenter le compteur
    st.session_state.global_request_count += 1
    return True, MAX_GLOBAL_REQUESTS - st.session_state.global_request_count

def get_session_id():
    """Obtient ou crée un ID de session unique"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(time.time())
    return st.session_state.session_id

class SimpleRateLimiter:
    def __init__(self, max_requests=3, time_window_minutes=5):
        self.max_requests = max_requests
        self.time_window = timedelta(minutes=time_window_minutes)
        self.requests = defaultdict(list)

    def check_limit(self, session_id: str) -> Tuple[bool, int]:
        """
        Vérifie si la limite est atteinte
        Retourne (peut_continuer, temps_attente_en_minutes)
        """
        if 'requests' not in st.session_state:
            st.session_state.requests = []

        current_time = datetime.now()
        cutoff_time = current_time - self.time_window
        
        # Nettoyer les anciennes requêtes
        st.session_state.requests = [
            time for time in st.session_state.requests
            if time > cutoff_time
        ]
        
        if len(st.session_state.requests) >= self.max_requests:
            # Calculer le temps restant avant la prochaine utilisation possible
            if st.session_state.requests:
                temps_attente = max(0, (st.session_state.requests[0] + self.time_window - current_time).seconds // 60)
                return False, temps_attente
            return False, self.time_window.seconds // 60
            
        # Ajouter la nouvelle requête
        st.session_state.requests.append(current_time)
        return True, 0

# Créer l'instance globale du rate limiter
rate_limiter = SimpleRateLimiter(max_requests=3, time_window_minutes=5)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ajout d'un handler pour écrire dans un fichier
file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=5)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def timeout_handler(func, timeout_seconds=30):
    """
    Exécute une fonction avec un timeout en utilisant threading
    """
    result = [None]
    error = [None]
    
    def worker():
        try:
            result[0] = func()
        except Exception as e:
            error[0] = e
    
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()
    thread.join(timeout=timeout_seconds)
    
    if thread.is_alive():
        logger.error(f"Timeout lors de l'exécution de {func.__name__}")
        return None, True
        
    if error[0] is not None:
        logger.error(f"Erreur lors de l'exécution de {func.__name__}: {str(error[0])}")
        return None, True
        
    return result[0], False

def execute_with_timeout(func, *args, timeout_seconds=30):
    """
    Wrapper pour exécuter une fonction avec des arguments et un timeout
    """
    def wrapped_func():
        return func(*args)
    return timeout_handler(wrapped_func, timeout_seconds)

def log_question(question: str, client_type: str, urgency: str, estimation: dict = None):
    """
    Journalise une question avec l'estimation si disponible
    """
    if estimation:
        log_message = f"""
Nouvelle question posée :
Client : {client_type}
Urgence : {urgency}
Question : {question}

Estimation : {estimation['forfait']}€ HT
Domaine : {estimation['domaine']}
Prestation : {estimation['prestation']}
"""
    else:
        log_message = f"""
Nouvelle question posée :
Client : {client_type}
Urgence : {urgency}
Question : {question}
"""
    
    logger.info(log_message)
    
    # Envoi de l'email avec les secrets Streamlit
    subject = "Nouvelle question posée sur Estim'IA"
    to_email = st.secrets["EMAIL_TO"]
    send_log_email(subject, log_message, to_email)

st.set_page_config(page_title="Estim'IA - Obtenez une estimation grâce à l'IA", page_icon="⚖️", layout="wide")

# Fonction pour envoyer des emails
def send_log_email(subject, body, to_email):
    from_email = os.getenv('EMAIL_FROM')
    password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Ajustez selon votre fournisseur d'email
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
        logger.info(f"Log email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send log email: {str(e)}")

# Fonction pour appliquer le CSS personnalisé
def apply_custom_css():
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stApp > header {
                background-color: transparent;
            }
            .stApp {
                margin-top: -80px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .loading-icon {
                animation: spin 1s linear infinite;
                display: inline-block;
                margin-right: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

# Configuration du client OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY n'est pas défini dans les variables d'environnement")

client = OpenAI(api_key=OPENAI_API_KEY)

# Chargement des modules
def load_py_module(file_path: str, module_name: str):
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        logger.error(f"Erreur lors du chargement du module {module_name}: {e}")
        return None

# Chargement des modules personnalisés
prestations_module = load_py_module('./prestations.py', 'prestations')
instructions_module = load_py_module('./chatbot-instructions.py', 'consignes_chatbot')

# Initialisation des variables globales
prestations = prestations_module.get_prestations() if prestations_module else {}
instructions = instructions_module.get_chatbot_instructions() if instructions_module else ""



def analyze_question(question: str, client_type: str, urgency: str) -> Tuple[str, str, float, bool]:
    options = [f"{domaine}: {', '.join(prestations_domaine['prestations'].keys())}" for domaine, prestations_domaine in prestations.items()]
    prompt = f"""Analysez la question suivante et déterminez si elle concerne un problème juridique. Si c'est le cas, identifiez le domaine juridique et la prestation la plus pertinente.

Question : {question}
Type de client : {client_type}
Degré d'urgence : {urgency}

Options de domaines et prestations :
{' '.join(options)}

Répondez au format JSON strict suivant :
{{
    "est_juridique": true/false,
    "domaine": "nom du domaine juridique",
    "prestation": "nom de la prestation (pas le label)",
    "explication": "Brève explication de votre analyse",
    "indice_confiance": 0.0 à 1.0
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        result = json.loads(response.choices[0].message.content)
        
        domain = result['domaine']
        service = result['prestation']
        confidence = result['indice_confiance']
        is_relevant = result['est_juridique'] and domain in prestations and service in prestations[domain]['prestations']
        
        logger.info(f"Domaine identifié : {domain}")
        logger.info(f"Prestation identifiée : {service}")
        
        return domain, service, confidence, is_relevant
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse de la question: {e}")
        return "", "", 0.0, False

def check_response_relevance(response: str, options: list) -> bool:
    response_lower = response.lower()
    return any(option.lower().split(':')[0].strip() in response_lower for option in options)

def calculate_estimate(domaine: str, prestation: str, urgency: str) -> Tuple[int, int, list, Dict[str, Any], str, str]:
    try:
        # Récupérer les prestations pour le domaine spécifié
        domaine_info = prestations.get(domaine)
        if not domaine_info:
            logger.error(f"Domaine non trouvé : {domaine}")
            return None, None, [f"Aucun domaine trouvé pour : {domaine}"], {}, "", ""

        prestations_domaine = domaine_info.get('prestations', {})
        prestation_info = prestations_domaine.get(prestation)
        if not prestation_info:
            logger.error(f"Prestation non trouvée : {prestation} dans le domaine {domaine}")
            available_prestations = ", ".join(prestations_domaine.keys())
            return None, None, [f"Prestation '{prestation}' non trouvée dans le domaine '{domaine}'. Prestations disponibles : {available_prestations}"], {}, "", ""

        forfait = prestation_info.get('tarif')
        if not forfait:
            logger.error(f"Aucun tarif défini pour la prestation : {prestation}")
            return None, None, [f"Aucun forfait défini pour la prestation : {prestation}"], {}, "", ""

        calcul_details = [
            f"Forfait pour la prestation '{prestation_info['label']}': {forfait} €"
        ]

        # Définir directement le facteur d'urgence ici
        facteur_urgence = 1.5  # Vous pouvez ajuster cette valeur selon vos besoins

        if urgency == "Urgent":
            forfait_urgent = round(forfait * facteur_urgence)
            calcul_details.extend([
                f"Facteur d'urgence appliqué: x{facteur_urgence}",
                f"Forfait après application du facteur d'urgence: {forfait_urgent} €"
            ])
            forfait = forfait_urgent

        tarifs_utilises = {
            "forfait_prestation": forfait,
            "facteur_urgence": facteur_urgence if urgency == "Urgent" else "Non appliqué"
        }

        domaine_label = domaine_info['label']
        prestation_label = prestation_info['label']

        return forfait, forfait, calcul_details, tarifs_utilises, domaine_label, prestation_label
    except Exception as e:
        logger.exception(f"Erreur dans calculate_estimate: {str(e)}")
        return None, None, [f"Erreur lors du calcul de l'estimation : {str(e)}"], {}, "", ""

def get_detailed_analysis(question: str, client_type: str, urgency: str, domaine: str, prestation: str) -> Tuple[str, Dict[str, Any], str]:
    prompt = f"""En tant qu'assistant juridique virtuel pour View Avocats, analysez la question suivante et expliquez votre raisonnement pour le choix du domaine juridique et de la prestation.

Question : {question}
Type de client : {client_type}
Degré d'urgence : {urgency}
Domaine recommandé : {domaine}
Prestation recommandée : {prestation}

Structurez votre réponse en trois parties clairement séparées par des lignes vides :

1. Analyse détaillée :
Fournissez une analyse concise mais détaillée du cas, en tenant compte du type de client et du degré d'urgence.

2. Éléments spécifiques utilisés (format JSON strict) :
{{"domaine": {{"nom": "nom_du_domaine", "description": "description_du_domaine"}}, "prestation": {{"nom": "nom_de_la_prestation", "description": "description_de_la_prestation"}}}}

3. Sources d'information :
Listez les sources d'information utilisées pour cette analyse, si applicable.

Assurez-vous que chaque partie est clairement séparée et que le JSON dans la partie 2 est valide et strict."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        content = response.choices[0].message.content.strip()
        logger.info(f"Réponse brute de l'API : {content}")

        parts = content.split('\n\n')
        
        analysis = parts[0] if len(parts) > 0 else "Analyse non disponible."
        
        elements_used = {}
        if len(parts) > 1:
            try:
                json_part = next((part for part in parts if '{' in part and '}' in part), None)
                if json_part:
                    json_str = json_part[json_part.index('{'):json_part.rindex('}')+1]
                    elements_used = json.loads(json_str)
                else:
                    logger.warning("Aucun JSON valide trouvé dans la réponse.")
                    elements_used = {
                        "domaine": {"nom": domaine, "description": "Information non fournie par l'API"},
                        "prestation": {"nom": prestation, "description": "Information non fournie par l'API"}
                    }
            except json.JSONDecodeError as e:
                logger.error(f"Erreur de décodage JSON : {e}")
                elements_used = {
                    "domaine": {"nom": domaine, "description": "Erreur dans l'analyse de la réponse"},
                    "prestation": {"nom": prestation, "description": "Erreur dans l'analyse de la réponse"}
                }
        else:
            elements_used = {
                "domaine": {"nom": domaine, "description": "Information non disponible"},
                "prestation": {"nom": prestation, "description": "Information non disponible"}
            }
        
        sources = parts[2] if len(parts) > 2 else "Aucune source spécifique mentionnée."

        return analysis, elements_used, sources
    except Exception as e:
        logger.exception(f"Erreur lors de l'analyse détaillée : {e}")
        return "Une erreur s'est produite lors de l'analyse.", {
            "domaine": {"nom": domaine, "description": "Erreur dans l'analyse"},
            "prestation": {"nom": prestation, "description": "Erreur dans l'analyse"}
        }, "Non disponible en raison d'une erreur."

def display_analysis_progress():
    """
    Affiche une barre de progression avec les étapes de l'analyse
    """
    progress_placeholder = st.empty()
    
    steps = {
        1: "Analyse de votre demande...",
        2: "Identification du domaine juridique...",
        3: "Calcul de l'estimation...",
        4: "Génération du rapport d'analyse..."
    }
    
    for step_num, step_desc in steps.items():
        progress = step_num / len(steps)
        with progress_placeholder.container():
            st.progress(progress)
            st.write(f"⏳ {step_desc}")
        time.sleep(0.8)  # Délai entre chaque étape
    
    progress_placeholder.empty()

def send_contact_email(name: str, email: str, phone: str, message: str) -> bool:
    """
    Envoie un email de contact
    """
    try:
        from_email = os.getenv('EMAIL_FROM')
        to_email = st.secrets["EMAIL_TO"]
        password = os.getenv('EMAIL_PASSWORD')

        subject = f"Nouveau message de contact - Estim'IA"
        
        body = f"""
Nouveau message de contact reçu via Estim'IA :

Nom : {name}
Email : {email}
Téléphone : {phone}

Message :
{message}
"""

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            
        logger.info(f"Contact email sent from {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send contact email: {str(e)}")
        return False

class AntiSpam:
    def __init__(self, min_submit_delay: int = 10):
        self.min_submit_delay = min_submit_delay

    def generate_math_captcha(self) -> Tuple[int, int, int]:
        """Génère un captcha mathématique simple"""
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        return a, b, a + b

    def initialize_session(self):
        """Initialise les variables de session pour l'anti-spam"""
        if 'captcha' not in st.session_state:
            a, b, answer = self.generate_math_captcha()
            st.session_state.captcha = {
                'a': a,
                'b': b,
                'answer': answer
            }
        if 'last_submit_time' not in st.session_state:
            st.session_state.last_submit_time = 0

    def add_honeypot(self):
        """Ajoute un champ honeypot caché"""
        st.markdown("""
            <div style="display:none">
                <input type="text" name="website" id="website" tabindex="-1" autocomplete="off">
            </div>
        """, unsafe_allow_html=True)

    def verify_submission(self, captcha_answer: str, honeypot: str = '') -> Tuple[bool, str]:
        """
        Vérifie si la soumission est légitime
        Retourne (is_valid, error_message)
        """
        current_time = time.time()
        
        # Vérifier le délai minimum entre les soumissions
        if current_time - st.session_state.last_submit_time < self.min_submit_delay:
            return False, "Veuillez patienter quelques secondes avant de renvoyer un message."

        # Vérifier le honeypot
        if honeypot:
            return False, "Erreur de validation."

        # Vérifier le captcha
        try:
            if int(captcha_answer) != st.session_state.captcha['answer']:
                return False, "La réponse au calcul est incorrecte."
        except ValueError:
            return False, "Veuillez entrer un nombre valide pour le calcul."

        # Mettre à jour le timestamp de dernière soumission
        st.session_state.last_submit_time = current_time
        return True, ""

def display_contact_form():
    """
    Affiche et gère le formulaire de contact avec protection anti-spam
    """
    st.markdown("### 📬 Contactez-nous")
    st.write("""
    Vous souhaitez plus d'informations ou prendre rendez-vous ? 
    Remplissez le formulaire ci-dessous et nous vous recontacterons dans les plus brefs délais.
    """)
    
    # Initialiser l'anti-spam
    anti_spam = AntiSpam()
    anti_spam.initialize_session()
    
    # CSS pour cacher complètement le honeypot
    st.markdown("""
        <style>
            #honeypot { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

    # Container pour le message de succès
    success_message = st.empty()
    
    # Créer le formulaire
    with st.form(key="contact_form"):
        # Création de deux colonnes principales
        form_col1, form_col2 = st.columns([1, 1])
        
        with form_col1:
            name = st.text_input("Nom et Prénom *")
            email = st.text_input("Email *")
            phone = st.text_input("Téléphone")
            # Captcha sur une ligne
            st.text_input(f"{st.session_state.captcha['a']} + {st.session_state.captcha['b']} = ", 
                         key="captcha_input", 
                         label_visibility="visible",
                         max_chars=3)
            
            # Honeypot vraiment invisible
            st.markdown("""
                <div id="honeypot" style="display:none;">
                    <input type="text" name="website" value="">
                </div>
            """, unsafe_allow_html=True)
            honeypot = st.session_state.get('website', '')
        
        with form_col2:
            message = st.text_area(
                "Votre message *",
                height=200,
                placeholder="Décrivez brièvement votre situation et vos attentes..."
            )
        
        # Bouton de soumission
        submit_button = st.form_submit_button("Envoyer le message")
    
    if submit_button:
        captcha_answer = st.session_state.captcha_input
        
        # Vérifier les champs obligatoires
        if not name or not email or not message or not captcha_answer:
            st.error("Veuillez remplir tous les champs obligatoires (*)")
            return
        
        if "@" not in email or "." not in email:
            st.error("Veuillez entrer une adresse email valide")
            return
        
        # Vérifier l'anti-spam
        is_valid, error_message = anti_spam.verify_submission(captcha_answer, honeypot)
        if not is_valid:
            st.error(error_message)
            return
            
        # Envoyer le message
        with st.spinner("Envoi de votre message..."):
            success = send_contact_email(name, email, phone, message)
            
        if success:
            success_message.success("✅ Message envoyé")
        else:
            st.error("""
            ❌ Une erreur est survenue lors de l'envoi du message. 
            Veuillez réessayer ou nous contacter directement par téléphone.
            """)

def get_dynamic_client_type_fields():
    """
    Gère les champs dynamiques selon le type de client
    Retourne un dictionnaire avec toutes les informations collectées
    """
    client_info = {}
    
    client_type = st.selectbox("Vous êtes :", ("Particulier", "Professionnel"))
    client_info["type_principal"] = client_type
    
    if client_type == "Professionnel":
        sub_type = st.selectbox(
            "Type d'organisation :",
            [
                "Entreprise",
                "Profession libérale",
                "Association",
                "Administration",
                "Collectivité"
            ]
        )
        client_info["sous_type"] = sub_type
        
        if sub_type == "Entreprise":
            client_info["taille"] = st.selectbox(
                "Taille de l'entreprise :",
                [
                    "TPE (moins de 10 salariés)",
                    "PME (10 à 250 salariés)",
                    "ETI (250 à 5000 salariés)",
                    "Grande entreprise"
                ]
            )
            
        if sub_type in ["Entreprise", "Profession libérale"]:
            client_info["secteur"] = st.selectbox(
                "Secteur d'activité :",
                [
                    "Commerce",
                    "Services",
                    "Industrie",
                    "BTP",
                    "Tech",
                    "Autre"
                ]
            )
    
    return client_info

def main():
    apply_custom_css()
    
    st.title("🏛️ Estim'IA by View Avocats\nObtenez une première estimation du prix de nos services en quelques secondes grâce à l'IA")

    # Initialisation du compteur de keep-alive dans la session state
    if 'last_keep_alive' not in st.session_state:
        st.session_state['last_keep_alive'] = time.time()

    # Vérification et mise à jour du keep-alive
    current_time = time.time()
    if current_time - st.session_state['last_keep_alive'] > 3540:  # 59 minutes
        st.session_state['last_keep_alive'] = current_time
        st.rerun()

    # Collecte des informations client avec les champs dynamiques
    client_info = get_dynamic_client_type_fields()
    urgency = st.selectbox("Degré d'urgence :", ("Normal", "Urgent"))

    exemple_cas = """Exemple : Mon voisin a construit une extension de sa maison qui empiète de 50 cm sur mon terrain. J'ai essayé de lui en parler à l'amiable, mais il refuse de reconnaître le problème. Je souhaite connaître mes droits et les démarches possibles pour résoudre cette situation, si possible sans aller jusqu'au procès."""

    question = st.text_area(
        "Expliquez brièvement votre cas, notre intelligence artificielle s'occupe du reste !",
        height=150,
        placeholder=exemple_cas
    )

    if st.button("Obtenir une estimation grâce à l'intelligence artificielle"):
        # Vérification des limites
        peut_continuer_global, requetes_restantes = check_global_limit()
        if not peut_continuer_global:
            st.error(f"""
            ⚠️ Le nombre maximum de requêtes global a été atteint pour le moment.
            Le système sera à nouveau disponible dans {requetes_restantes} minutes.
            Pour une analyse urgente, vous pouvez nous contacter directement.
            """)
            return

        peut_continuer, temps_attente = rate_limiter.check_limit(get_session_id())
        if not peut_continuer:
            st.warning(f"""
            ⏳ Merci de patienter {temps_attente} minute{'s' if temps_attente > 1 else ''} avant de faire une nouvelle demande.
            Pour une analyse urgente, vous pouvez nous contacter directement.
            """)
            return

        if question and question != exemple_cas:
            progress_container = st.empty()
            
            with progress_container:
                # Afficher la progression à la place du spinner
                display_analysis_progress()
                
                # Préparation des informations client pour l'analyse
                client_type_desc = f"{client_info['type_principal']}"
                if client_info['type_principal'] == "Professionnel":
                    client_type_desc += f" - {client_info['sous_type']}"
                    if 'taille' in client_info:
                        client_type_desc += f" ({client_info['taille']})"
                    if 'secteur' in client_info:
                        client_type_desc += f" - Secteur {client_info['secteur']}"
                
                # Analyse avec timeout
                result, timeout = execute_with_timeout(
                    analyze_question,
                    question,
                    client_type_desc,
                    urgency,
                    timeout_seconds=30
                )
                
                if timeout:
                    progress_container.empty()
                    st.error("Désolé, l'analyse a pris trop de temps. Veuillez réessayer ou nous contacter directement.")
                    return
                    
                domaine, prestation, confidence, is_relevant = result
                
                if not domaine or not prestation:
                    progress_container.empty()
                    st.error("Désolé, nous n'avons pas pu analyser votre demande. Veuillez réessayer avec plus de détails.")
                    return

                detailed_analysis, elements_used, sources = get_detailed_analysis(
                    question, client_type_desc, urgency, domaine, prestation
                )

                # Calcul de l'estimation
                forfait, _, calcul_details, tarifs_utilises, domaine_label, prestation_label = calculate_estimate(
                    domaine, prestation, urgency
                )

                # Logging
                if forfait is not None:
                    estimation = {
                        'forfait': forfait,
                        'domaine': domaine_label,
                        'prestation': prestation_label
                    }
                    log_question(question, client_type_desc, urgency, estimation)
                else:
                    log_question(question, client_type_desc, urgency)

                if forfait is None:
                    progress_container.empty()
                    st.warning("Nous n'avons pas pu trouver un forfait précis pour cette prestation. Voici les détails :")
                    for detail in calcul_details:
                        st.write(detail)
                    st.info("Pour obtenir une estimation précise, veuillez nous contacter directement.")
                    return

                # Vider le container de progression
                progress_container.empty()
                
                # Container principal pour les résultats
                with st.container():
                    # 1. Résumé de l'analyse
                    st.info(f"""
                    📋 Notre compréhension de votre situation :
                    
                    {detailed_analysis}
                    
                    Sur la base de cette analyse, nous allons maintenant vous proposer une estimation adaptée à votre situation.
                    """)

                    # 2. Estimation
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
                        <h2 style="color: #1f618d;">Forfait estimé</h2>
                        <p style="font-size: 24px; font-weight: bold; color: #2c3e50;">
                            À partir de <span style="color: #e74c3c;">{forfait} €HT</span>
                        </p>
                        <p style="font-style: italic;">Domaine : {domaine_label}</p>
                        <p style="font-style: italic;">Prestation : {prestation_label}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.info("""
                    📌 Note importante : Cette estimation est fournie à titre indicatif et peut varier en fonction de la complexité spécifique de votre situation. 
                    Nous vous invitons à nous contacter pour une évaluation personnalisée qui prendra en compte tous les détails de votre cas. Pour les particuliers, il est possible de payer en plusieurs fois.
                    """)

                    st.markdown("---")

                    # 3. Indicateurs de confiance et avertissements
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.subheader("Indice de confiance")
                        st.progress(confidence)
                        st.write(f"Confiance : {confidence:.2%}")
                    with col2:
                        if confidence < 0.5:
                            st.warning("⚠️ Attention : Notre IA a eu des difficultés à analyser votre question avec certitude. L'estimation ci-dessus peut manquer de précision.")
                        elif not is_relevant:
                            st.info("Nous ne sommes pas sûr qu'il s'agisse d'une question d'ordre juridique. L'estimation ci-dessus est fournie à titre indicatif.")

                    # 4. Recommandations
                    st.markdown("### 💡 Recommandations")
                    st.success("""
                    **Consultation initiale recommandée** - Pour une analyse approfondie de votre situation et des conseils personnalisés, 
                    nous vous recommandons de prendre rendez-vous pour une consultation initiale d'un montant de 200€HT. Cette première analyse de votre situation nous permettra de :
                    - Évaluer précisément la complexité de votre cas
                    - Vous fournir des conseils juridiques adaptés
                    - Élaborer une stratégie sur mesure pour votre situation
                    """)

                    st.markdown("---")

                    # 5. Détails dans des colonnes
                    details_col1, details_col2 = st.columns(2)
                    
                    with details_col1:
                        st.subheader("Détails du forfait")
                        for detail in calcul_details:
                            st.write(detail)

                    with details_col2:
                        if isinstance(elements_used, dict) and "prestation" in elements_used:
                            st.subheader("Procédure suggérée")
                            st.write(elements_used['prestation'].get('description', 'Non spécifié'))

                    # 6. Informations supplémentaires
                    if sources and sources != "Aucune source spécifique mentionnée.":
                        with st.expander("Sources juridiques"):
                            st.write(sources)

        else:
            st.warning("Veuillez décrire votre cas avant de demander une estimation. N'utilisez pas l'exemple fourni tel quel.")
    
    st.markdown("---")
    display_contact_form()
    
    st.markdown("---")
    st.empty()
    st.write("© 2024 View Avocats. Tous droits réservés.")

if __name__ == "__main__":
    main()
