import streamlit as st
import os
from openai import OpenAI
import json
import logging
from typing import Tuple, Dict, Any
import importlib.util
from collections import Counter

st.set_page_config(page_title="Estim'IA - Obtenez une estimation grâce à l'IA", page_icon="⚖️", layout="wide")

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

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Fonction pour obtenir une réponse de l'API OpenAI
def get_openai_response(prompt: str, model: str = "gpt-3.5-turbo", num_iterations: int = 3) -> list:
    try:
        responses = []
        for _ in range(num_iterations):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            content = response.choices[0].message.content.strip()
            responses.append(content)
        
        return responses
    except Exception as e:
        logger.error(f"Erreur lors de l'appel à l'API OpenAI: {e}")
        raise

def analyze_question(question: str, client_type: str, urgency: str) -> Tuple[str, str, float, bool]:
    prestations_data = get_prestations()
    
    prompt = f"""Analysez la question suivante et déterminez le domaine juridique et la prestation la plus pertinente.

Question : {question}
Type de client : {client_type}
Degré d'urgence : {urgency}

Voici les domaines et prestations disponibles avec leurs mots-clés associés :

{json.dumps(prestations_data, indent=2)}

Répondez au format JSON strict suivant :
{{
    "domaine": "nom_du_domaine",
    "prestation": "nom_de_la_prestation",
    "explication": "Brève explication de votre choix",
    "indice_confiance": 0.0 à 1.0
}}
"""

    response = client.chat.completions.create(
        model="gpt-4",  # Utilisation de GPT-4
        messages=[
            {"role": "system", "content": "Vous êtes un assistant juridique spécialisé dans l'analyse de questions et la recommandation de prestations juridiques."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    try:
        result = json.loads(response.choices[0].message.content)
        domain = result['domaine']
        prestation = result['prestation']
        confidence = result['indice_confiance']
        is_relevant = domain in prestations_data and prestation in prestations_data[domain]['prestations']
        
        return domain, prestation, confidence, is_relevant
    except (json.JSONDecodeError, KeyError):
        logger.error("Erreur dans l'analyse de la réponse de l'API")
        return "", "", 0.0, False

# Utilisation de la fonction
domain, prestation, confidence, is_relevant = analyze_question(question, client_type, urgency)

def check_response_relevance(response: str, options: list) -> bool:
    response_lower = response.lower()
    return any(option.lower().split(':')[0].strip() in response_lower for option in options)

def calculate_estimate(domaine: str, prestation: str, urgency: str) -> Tuple[int, int, list, Dict[str, Any]]:
    try:
        prestation_info = prestations.get(domaine, {}).get(prestation, {})
        forfait = prestation_info.get('tarif')

        if not forfait:
            return None, None, ["Aucun forfait trouvé pour cette prestation."], {}

        calcul_details = [
            f"Forfait pour la prestation '{prestation}': {forfait} €"
        ]

        if urgency == "Urgent":
            facteur_urgence = prestation_info.get('facteur_urgence', 1.5)
            forfait_urgent = round(forfait * facteur_urgence)
            calcul_details.extend([
                f"Facteur d'urgence appliqué: x{facteur_urgence}",
                f"Forfait après application du facteur d'urgence: {forfait_urgent} €"
            ])
            forfait = forfait_urgent

        estimation_basse, estimation_haute = forfait, forfait

        tarifs_utilises = {
            "forfait_prestation": forfait,
            "facteur_urgence": facteur_urgence if urgency == "Urgent" else "Non appliqué"
        }

        return estimation_basse, estimation_haute, calcul_details, tarifs_utilises
    except Exception as e:
        logger.exception(f"Erreur dans calculate_estimate: {str(e)}")
        raise

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
        responses = get_openai_response(prompt)
        response = responses[0] if responses else ""
        logger.info(f"Réponse brute de l'API : {response}")

        parts = response.split('\n\n')
        
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
    
    st.title("🏛️ View Avocats - Estimateur de devis")

    client_type = st.selectbox("Vous êtes :", ("Particulier", "Entreprise"))
    urgency = st.selectbox("Degré d'urgence :", ("Normal", "Urgent"))
    question = st.text_area("Expliquez brièvement votre cas, notre intelligence artificielle s'occupe du reste !", height=150)

    if st.button("Obtenir une estimation grâce à l'intelligence artificielle"):
        if question:
            try:
                loading_placeholder = st.empty()
                with loading_placeholder:
                    display_loading_animation()
                
                # Effectuer toutes les analyses et calculs
                domaine, prestation, confidence, is_relevant = analyze_question(question, client_type, urgency)
                estimation_basse, estimation_haute, calcul_details, tarifs_utilises = calculate_estimate(domaine, prestation, urgency)
                detailed_analysis, elements_used, sources = get_detailed_analysis(question, client_type, urgency, domaine, prestation)

                # Une fois que tout est prêt, supprimer l'animation de chargement
                loading_placeholder.empty()

                # Afficher les résultats
                if estimation_basse is not None:
                    st.success("Analyse terminée. Voici votre estimation :")
                    
                    # Mise en valeur du forfait
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
                        <h2 style="color: #1f618d;">Forfait estimé</h2>
                        <p style="font-size: 28px; font-weight: bold; color: #2c3e50;">
                            <span style="color: #e74c3c;">{estimation_basse} €HT</span>
                        </p>
                        <p style="font-style: italic;">Domaine : {domaine if domaine else 'Non déterminé'}</p>
                        <p style="font-style: italic;">Prestation : {prestation if prestation else 'Non déterminée'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Aucun forfait n'a été trouvé pour cette prestation spécifique.")

                st.markdown("---")

                st.subheader("Indice de confiance de l'analyse")
                st.progress(confidence)
                st.write(f"Confiance : {confidence:.2%}")

                if confidence < 0.5:
                    st.warning("⚠️ Attention : Notre IA a eu des difficultés à analyser votre question avec certitude. L'estimation ci-dessus peut manquer de précision.")
                elif not is_relevant:
                    st.info("Nous ne sommes pas sûr qu'il s'agisse d'une question d'ordre juridique. L'estimation ci-dessus est fournie à titre indicatif.")

                st.subheader("Détails du calcul")
                for detail in calcul_details:
                    st.write(detail)

                st.subheader("Analyse détaillée")
                st.write(detailed_analysis)

                expander = st.expander("Voir les éléments spécifiques pris en compte")
                with expander:
                    if isinstance(elements_used, dict) and "domaine" in elements_used and "prestation" in elements_used:
                        st.json(elements_used)
                    else:
                        st.warning("Les éléments spécifiques n'ont pas pu être analysés de manière optimale.")
                        st.json(elements_used)

                if sources and sources != "Aucune source spécifique mentionnée.":
                    expander = st.expander("Voir les sources d'information")
                    with expander:
                        st.write(sources)

                st.markdown("---")
                st.markdown("### 💡 Alternative Recommandée")
                st.info("**Consultation initiale d'une heure** - Tarif fixe : 100 € HT")

            except Exception as e:
                st.error(f"Une erreur s'est produite : {str(e)}")
                logger.exception("Erreur dans le processus d'estimation")
        else:
            st.warning("Veuillez décrire votre cas avant de demander une estimation.")

    st.markdown("---")
    st.write("© 2024 View Avocats. Tous droits réservés.")

if __name__ == "__main__":
    main()
