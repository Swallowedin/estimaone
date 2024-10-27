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
from collections import Counter
import time
import signal

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ajout d'un handler pour écrire dans un fichier
file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=5)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def execute_with_timeout(func, *args, timeout_seconds=30):
    """
    Exécute une fonction avec un timeout simple
    Retourne (résultat, False) si succès
    Retourne (None, True) si timeout
    """
    def timeout_handler(signum, frame):
        raise TimeoutError("Timeout")

    # Mettre en place le gestionnaire de signal
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    
    try:
        result = func(*args)
        signal.alarm(0)  # Désactiver l'alarme
        return result, False
    except TimeoutError:
        logger.error(f"Timeout lors de l'exécution de {func.__name__}")
        return None, True
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution de {func.__name__}: {str(e)}")
        return None, True
    finally:
        signal.alarm(0)  # S'assurer que l'alarme est désactivée

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

# Fonction pour journaliser les questions
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

def display_loading_animation():
    return st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; flex-direction: column;">
        <svg class="loading-icon" width="50" height="50" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,19a8,8,1,1,1,8-8A8,8,0,0,1,12,20Z" opacity=".25"/>
            <path d="M12,4a8,8,0,0,1,7.89,6.7A1.53,1.53,0,0,0,21.38,12h0a1.5,1.5,0,0,0,1.48-1.75,11,11,0,0,0-21.72,0A1.5,1.5,0,0,0,2.62,12h0a1.53,1.53,0,0,0,1.49-1.3A8,8,0,0,1,12,4Z"/>
        </svg>
        <p style="margin-top: 10px; font-weight: bold;">Notre intelligence artificielle analyse votre demande...</p>
        <p>Votre estimation arrive dans quelques secondes !</p>
    </div>
    """, unsafe_allow_html=True)

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
        st.experimental_rerun()

    client_type = st.selectbox("Vous êtes :", ("Particulier", "Entreprise"))
    urgency = st.selectbox("Degré d'urgence :", ("Normal", "Urgent"))

    exemple_cas = """Exemple : Mon voisin a construit une extension de sa maison qui empiète de 50 cm sur mon terrain. J'ai essayé de lui en parler à l'amiable, mais il refuse de reconnaître le problème. Je souhaite connaître mes droits et les démarches possibles pour résoudre cette situation, si possible sans aller jusqu'au procès."""

    question = st.text_area(
        "Expliquez brièvement votre cas, notre intelligence artificielle s'occupe du reste !",
        height=150,
        placeholder=exemple_cas
    )

    if st.button("Obtenir une estimation grâce à l'intelligence artificielle"):
        if question and question != exemple_cas:
            loading_placeholder = st.empty()
            with loading_placeholder:
                display_loading_animation()
            
            # Analyse avec timeout
            result, timeout = execute_with_timeout(
                analyze_question,
                question, 
                client_type, 
                urgency,
                timeout_seconds=30
            )
            
            if timeout:
                loading_placeholder.empty()
                st.error("Désolé, l'analyse a pris trop de temps. Veuillez réessayer ou nous contacter directement.")
                return
                
            domaine, prestation, confidence, is_relevant = result
            
            if not domaine or not prestation:
                loading_placeholder.empty()
                st.error("Désolé, nous n'avons pas pu analyser votre demande. Veuillez réessayer avec plus de détails.")
                return

            forfait, _, calcul_details, tarifs_utilises, domaine_label, prestation_label = calculate_estimate(domaine, prestation, urgency)
            
            # Ajout du logging avec l'estimation
            if forfait is not None:
                estimation = {
                    'forfait': forfait,
                    'domaine': domaine_label,
                    'prestation': prestation_label
                }
                log_question(question, client_type, urgency, estimation)
            else:
                log_question(question, client_type, urgency)

            if forfait is None:
                loading_placeholder.empty()
                st.warning("Nous n'avons pas pu trouver un forfait précis pour cette prestation. Voici les détails :")
                for detail in calcul_details:
                    st.write(detail)
                st.info("Pour obtenir une estimation précise, veuillez nous contacter directement.")
                return

            detailed_analysis, elements_used, sources = get_detailed_analysis(question, client_type, urgency, domaine, prestation)

            loading_placeholder.empty()

            st.success("Analyse terminée. Voici votre estimation :")
            
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

            st.subheader("Indice de confiance de l'analyse")
            st.progress(confidence)
            st.write(f"Confiance : {confidence:.2%}")

            if confidence < 0.5:
                st.warning("⚠️ Attention : Notre IA a eu des difficultés à analyser votre question avec certitude. L'estimation ci-dessus peut manquer de précision.")
            elif not is_relevant:
                st.info("Nous ne sommes pas sûr qu'il s'agisse d'une question d'ordre juridique. L'estimation ci-dessus est fournie à titre indicatif.")

            st.markdown("### 💡 Recommandations")
            st.success("""
            **Consultation initiale recommandée** - Pour une analyse approfondie de votre situation et des conseils personnalisés, 
            nous vous recommandons de prendre rendez-vous pour une consultation initiale d'un montant de 200€HT. Cette première analyse de votre situation nous permettra de :
            - Évaluer précisément la complexité de votre cas
            - Vous fournir des conseils juridiques adaptés
            - Élaborer une stratégie sur mesure pour votre situation
            """)

            st.markdown("---")

            st.subheader("Détails du forfait")
            for detail in calcul_details:
                st.write(detail)

            st.subheader("Analyse détaillée")
            st.write(detailed_analysis)

            expander = st.expander("Voir les éléments spécifiques pris en compte")
            with expander:
                if isinstance(elements_used, dict) and "domaine" in elements_used and "prestation" in elements_used:
                    elements_used["domaine"]["nom"] = domaine_label
                    elements_used["prestation"]["nom"] = prestation_label
                    st.json(elements_used)
                else:
                    st.warning("Les éléments spécifiques n'ont pas pu être analysés de manière optimale.")
                    st.json(elements_used)

            if sources and sources != "Aucune source spécifique mentionnée.":
                expander = st.expander("Voir les sources d'information")
                with expander:
                    st.write(sources)

        else:
            st.warning("Veuillez décrire votre cas avant de demander une estimation. N'utilisez pas l'exemple fourni tel quel.")

    st.markdown("---")
    st.empty()  # Pour le keep-alive
    st.write("© 2024 View Avocats. Tous droits réservés.")

if __name__ == "__main__":
    main()
