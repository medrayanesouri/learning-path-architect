import json
import os
import random
import re
import requests
from datetime import date, datetime

import streamlit as st

st.set_page_config(page_title="Learning Path Architect", page_icon="🧭")

# ─── Persistence ──────────────────────────────────────────────────────────────

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

_SAFE_ID_RE = re.compile(r"[^a-zA-Z0-9_\-]")


def sanitize_user_id(user_id: str) -> str:
    """Strip any characters that are not safe for use in a filename."""
    return _SAFE_ID_RE.sub("", user_id)


def profile_path(user_id: str) -> str:
    # Remove unsafe characters, then take only the basename to prevent traversal
    safe_id = os.path.basename(sanitize_user_id(user_id))
    abs_data = os.path.realpath(DATA_DIR)
    resolved = os.path.realpath(os.path.join(abs_data, f"{safe_id}.json"))
    if not resolved.startswith(abs_data + os.sep):
        raise ValueError("user_id resolves to a path outside the data directory")
    return resolved


def load_profile(user_id: str):
    p = profile_path(user_id)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_profile(profile: dict) -> None:
    with open(profile_path(profile["user_id"]), "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


# ─── Domain knowledge ─────────────────────────────────────────────────────────

DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "Python": ["python"],
    "Data Science": ["data", "pandas", "numpy", "analyse"],
    "Machine Learning": ["ml", "machine learning", "ia", "ai", "sklearn", "deep learning"],
    "Développement Web": ["web", "html", "css", "javascript", "react", "frontend", "backend"],
    "Cybersécurité": ["security", "sécurité", "hacking", "owasp", "cybersecurity"],
    "Prompt Engineering": ["prompt", "chatgpt", "gpt", "llm", "openai"],
    "Anglais": ["anglais", "english"],
    "Français": ["français", "french", "grammaire"],
}

MODULES: dict[str, list[str]] = {
    "Machine Learning": [
        "Fondamentaux ML + vocabulaire",
        "Préparation de données (NumPy/Pandas)",
        "Régression & classification",
        "Évaluation & métriques",
        "Mini-projet ML",
        "Amélioration & présentation",
        "Portfolio / extension",
        "Consolidation",
    ],
    "Data Science": [
        "Data exploration",
        "Nettoyage & préparation",
        "Visualisation",
        "Statistiques de base",
        "Mini-projet data",
        "Storytelling data",
        "Portfolio / extension",
        "Consolidation",
    ],
    "Python": [
        "Bases Python",
        "Structures de données",
        "Fonctions",
        "Fichiers & modules",
        "Mini-projet",
        "Tests / bonnes pratiques",
        "Consolidation",
        "Extension",
    ],
    "Développement Web": [
        "HTML basics",
        "CSS basics",
        "Responsive design",
        "JavaScript basics",
        "Mini-projet web",
        "Amélioration UI",
        "Consolidation",
        "Extension",
    ],
    "Cybersécurité": [
        "Concepts sécurité web",
        "Reconnaissance & collecte d'infos",
        "Tests auth & sessions",
        "Input validation",
        "Mini-audit",
        "Rapport & remédiation",
        "Consolidation",
        "Extension",
    ],
    "Prompt Engineering": [
        "Concepts de prompts",
        "Clarté & contexte",
        "Format & contraintes",
        "Itération & amélioration",
        "Mini-projet prompts",
        "Évaluation qualité",
        "Consolidation",
        "Extension",
    ],
    "Anglais": [
        "Listening basics",
        "Vocabulary building",
        "Grammar focus",
        "Speaking practice",
        "Mini-projet (journal audio)",
        "Writing practice",
        "Consolidation",
        "Extension",
    ],
    "Français": [
        "Compréhension orale",
        "Vocabulaire",
        "Grammaire",
        "Expression écrite",
        "Mini-projet (journal)",
        "Expression orale",
        "Consolidation",
        "Extension",
    ],
}

RESOURCES: dict[str, list[tuple[str, str]]] = {
    "Machine Learning": [
        ("Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course/"),
        ("scikit-learn Getting Started", "https://sklearn.org/stable/getting_started.html"),
        ("Pandas Intro Tutorials", "https://pandas.pydata.org/docs/getting_started/intro_tutorials/"),
        ("Python Tutorial (officiel)", "https://docs.python.org/3/tutorial/index.html"),
    ],
    "Data Science": [
        ("Pandas Intro Tutorials", "https://pandas.pydata.org/docs/getting_started/intro_tutorials/"),
        ("scikit-learn Getting Started", "https://sklearn.org/stable/getting_started.html"),
        ("Python Tutorial (officiel)", "https://docs.python.org/3/tutorial/index.html"),
    ],
    "Python": [
        ("Python Tutorial (officiel)", "https://docs.python.org/3/tutorial/index.html"),
    ],
    "Développement Web": [
        ("MDN Learn Web Development", "https://developer.mozilla.org/en-US/docs/Learn"),
        ("Khan Academy HTML/CSS", "https://www.khanacademy.org/computing/computer-programming/html-css"),
    ],
    "Cybersécurité": [
        ("OWASP Web Security Testing Guide", "https://owasp.org/www-project-web-security-testing-guide/"),
    ],
    "Prompt Engineering": [
        ("OpenAI Academy – Prompting Fundamentals", "https://openai.com/academy/prompting/"),
        ("OpenAI Help – Prompting Best Practices", "https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt"),
    ],
    "Anglais": [
        ("BBC Learning English", "https://www.bbc.co.uk/learningenglish"),
    ],
    "Français": [
        ("TV5MONDE Apprendre le français", "https://apprendre.tv5monde.com/"),
    ],
}

DEVTO_TAG_MAP: dict[str, str] = {
    "Python": "python",
    "Data Science": "datascience",
    "Machine Learning": "machinelearning",
    "Développement Web": "webdev",
    "Cybersécurité": "security",
    "Prompt Engineering": "ai",
    "Anglais": "beginners",
    "Français": "beginners",
}

QUIZ_BANK: dict[str, list[tuple[str, str]]] = {
    "Machine Learning": [
        ("Différence entre régression et classification ?", "Régression = valeur continue, classification = classe."),
        ("Pourquoi séparer train/test ?", "Évaluer la généralisation."),
        ("Qu'est-ce qu'un sur-apprentissage ?", "Le modèle apprend trop le train et généralise mal."),
    ],
    "Data Science": [
        ("À quoi sert pandas ?", "Manipulation et analyse de données tabulaires."),
        ("Pourquoi nettoyer les données ?", "Qualité des résultats."),
        ("Qu'est-ce qu'une variable cible ?", "La variable à prédire."),
    ],
    "Python": [
        ("Différence liste / tuple ?", "Liste modifiable, tuple immuable."),
        ("À quoi sert un dictionnaire ?", "Association clé-valeur."),
        ("Pourquoi utiliser une fonction ?", "Réutilisation et clarté."),
    ],
    "Développement Web": [
        ("Rôle de HTML ?", "Structure du contenu."),
        ("Rôle de CSS ?", "Style et mise en page."),
        ("Rôle de JS ?", "Interaction et logique côté client."),
    ],
    "Cybersécurité": [
        ("C'est quoi une attaque XSS ?", "Injection de script dans une page web."),
        ("Pourquoi tester la sécurité ?", "Réduire les vulnérabilités."),
        ("C'est quoi l'OWASP ?", "Organisation de bonnes pratiques sécurité web."),
    ],
    "Prompt Engineering": [
        ("Pourquoi être précis dans un prompt ?", "Pour réduire l'ambiguïté."),
        ("C'est quoi l'itération de prompts ?", "Améliorer progressivement le résultat."),
        ("Donne un exemple d'instruction claire.", "Ex : Résume en 5 points."),
    ],
    "Anglais": [
        ("Pourquoi pratiquer l'écoute ?", "Améliorer compréhension orale."),
        ("Que signifie 'consistency' ?", "Régularité."),
        ("Donne un objectif SMART.", "Spécifique, Mesurable, Atteignable, Réaliste, Temporel."),
    ],
    "Français": [
        ("Pourquoi écouter du contenu natif ?", "Améliorer l'oreille et le vocabulaire."),
        ("Que signifie 'grammaire' ?", "Règles de la langue."),
        ("Donne un objectif SMART.", "Spécifique, Mesurable, Atteignable, Réaliste, Temporel."),
    ],
}

DAY_NAMES = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


# ─── Pure helpers ─────────────────────────────────────────────────────────────

def suggest_domains(interests_text: str) -> list:
    """Return up to 3 domain suggestions based on keyword matching."""
    interests_lower = interests_text.lower()
    suggested = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in interests_lower:
                if domain not in suggested:
                    suggested.append(domain)
                break
    return suggested[:3] if suggested else ["Python", "Data Science", "Machine Learning"]


def recommend_weeks(hours: int, level: str, goal: str) -> int:
    weeks = 4
    if goal == "Faire un mini-projet":
        weeks = 6
    elif goal == "Créer un portfolio":
        weeks = 8
    if hours <= 4:
        weeks += 1
    if level == "Débutant":
        weeks += 1
    return min(max(weeks, 4), 10)


def week_plan(week_title: str) -> dict:
    return {
        "Lundi": f"Lecture/vidéo sur {week_title} + prise de notes",
        "Mardi": f"Exercice guidé sur {week_title}",
        "Mercredi": f"Mini-exercice pratique lié à {week_title}",
        "Jeudi": f"Quiz court + correction sur {week_title}",
        "Vendredi": f"Synthèse + fiche mémo de {week_title}",
        "Samedi": f"Révision générale de la semaine ({week_title})",
        "Dimanche": f"Contrôle hebdomadaire sur {week_title}",
    }


def weekly_quiz_questions(week_title: str) -> list:
    return [
        f"Explique le concept clé vu cette semaine : {week_title}",
        f"Donne un exemple pratique lié à : {week_title}",
        "Quelle difficulté as-tu rencontrée et comment l'as-tu résolue ?",
    ]


def task_key(week_num: int, day: str) -> str:
    return f"{week_num}-{day}"


# ─── Dev.to integration ───────────────────────────────────────────────────────

def fetch_devto(tag: str) -> list:
    """Fetch Dev.to articles for a tag with a 1-hour session cache."""
    cache_key = f"devto_{tag}"
    now = datetime.now()
    cached = st.session_state.get(cache_key)
    if cached and (now - cached["ts"]).total_seconds() < 3600:
        return cached["data"]
    try:
        resp = requests.get(
            f"https://dev.to/api/articles?tag={tag}&per_page=10",
            timeout=5,
        )
        data = resp.json() if resp.ok else []
    except Exception:
        data = []
    st.session_state[cache_key] = {"ts": now, "data": data}
    return data


# ─── Session initialisation ───────────────────────────────────────────────────

def init_session() -> None:
    if "step" not in st.session_state:
        st.session_state.step = "user_id"
    if "profile" not in st.session_state:
        st.session_state.profile = {}


# ─── Conversation flow ────────────────────────────────────────────────────────

def conversation_ui() -> None:
    step = st.session_state.step

    st.title("🧭 Learning Path Architect")

    if step == "user_id":
        st.write("Bonjour ! Commençons par t'identifier.")
        st.caption("L'identifiant ne doit contenir que des lettres, chiffres, tirets et underscores.")
        uid = st.text_input("Entrez votre identifiant utilisateur (ex : jean42)", key="input_uid")
        if st.button("Continuer", key="btn_uid"):
            safe_uid = sanitize_user_id(uid.strip())
            if not safe_uid:
                st.warning("L'identifiant ne peut pas être vide et ne doit contenir que des lettres, chiffres, - et _.")
            else:
                existing = load_profile(safe_uid)
                if existing:
                    st.session_state.profile = existing
                    st.session_state.step = "main"
                    st.rerun()
                else:
                    st.session_state.profile = {"user_id": safe_uid}
                    st.session_state.step = "name"
                    st.rerun()

    elif step == "name":
        uid = st.session_state.profile.get("user_id", "")
        st.write(f"Identifiant : **{uid}** — Profil non trouvé, créons-le ensemble !")
        name = st.text_input("Quel est ton prénom ?", key="input_name")
        if st.button("Continuer", key="btn_name"):
            if not name.strip():
                st.warning("Le prénom ne peut pas être vide.")
            else:
                st.session_state.profile["name"] = name.strip()
                st.session_state.step = "age"
                st.rerun()

    elif step == "age":
        name = st.session_state.profile.get("name", "")
        st.write(f"Bonjour **{name}** ! Quel est ton âge ?")
        age = st.number_input("Âge", min_value=10, max_value=100, value=25, key="input_age")
        if st.button("Continuer", key="btn_age"):
            st.session_state.profile["age"] = int(age)
            st.session_state.step = "gender"
            st.rerun()

    elif step == "gender":
        gender = st.selectbox(
            "Quel est ton genre ?",
            ["Homme", "Femme", "Autre / Préfère ne pas dire"],
            key="input_gender",
        )
        if st.button("Continuer", key="btn_gender"):
            st.session_state.profile["gender"] = gender
            st.session_state.step = "level"
            st.rerun()

    elif step == "level":
        level = st.selectbox(
            "Quel est ton niveau actuel ?",
            ["Débutant", "Intermédiaire", "Avancé"],
            key="input_level",
        )
        if st.button("Continuer", key="btn_level"):
            st.session_state.profile["level"] = level
            st.session_state.step = "goal"
            st.rerun()

    elif step == "goal":
        goal = st.selectbox(
            "Quel est ton objectif ?",
            ["Comprendre les bases", "Faire un mini-projet", "Créer un portfolio"],
            key="input_goal",
        )
        if st.button("Continuer", key="btn_goal"):
            st.session_state.profile["goal"] = goal
            st.session_state.step = "hours"
            st.rerun()

    elif step == "hours":
        hours = st.slider(
            "Combien d'heures par semaine peux-tu y consacrer ?",
            min_value=2,
            max_value=20,
            value=6,
            key="input_hours",
        )
        if st.button("Continuer", key="btn_hours"):
            st.session_state.profile["hours_per_week"] = int(hours)
            st.session_state.step = "interests"
            st.rerun()

    elif step == "interests":
        st.write("Décris tes intérêts en quelques mots (ex : python, web, prompt engineering, français…)")
        interests = st.text_area("Tes centres d'intérêt", key="input_interests", height=100)
        if st.button("Continuer", key="btn_interests"):
            if not interests.strip():
                st.warning("Décris au moins un intérêt.")
            else:
                st.session_state.profile["interests"] = interests.strip()
                suggestions = suggest_domains(interests)
                st.session_state.profile["suggested_domains"] = suggestions
                st.session_state.step = "confirm_domains"
                st.rerun()

    elif step == "confirm_domains":
        suggestions = st.session_state.profile.get("suggested_domains", [])
        all_domains = list(MODULES.keys())
        st.write("Sur la base de tes intérêts, je te recommande ces domaines :")
        for s in suggestions:
            st.write(f"  ✅ {s}")
        st.write("---")
        selected = st.multiselect(
            "Confirme ou modifie ta sélection (choisis 1 à 3 domaines) :",
            options=all_domains,
            default=suggestions,
            key="input_domains",
        )
        if st.button("Valider et créer mon parcours", key="btn_domains"):
            if not selected:
                st.warning("Sélectionne au moins un domaine.")
            else:
                profile = st.session_state.profile
                profile["domains"] = selected[:3]
                domain = selected[0]
                weeks = recommend_weeks(
                    profile.get("hours_per_week", 6),
                    profile.get("level", "Débutant"),
                    profile.get("goal", "Comprendre les bases"),
                )
                profile["weeks"] = weeks
                profile["primary_domain"] = domain
                profile["start_date"] = str(date.today())
                profile["completed_tasks"] = []
                profile["created_at"] = datetime.now().isoformat()
                save_profile(profile)
                st.session_state.step = "main"
                st.rerun()


# ─── Main tabbed UI ───────────────────────────────────────────────────────────

def main_ui() -> None:
    profile = st.session_state.profile
    name = profile.get("name", "Utilisateur")
    domain = profile.get("primary_domain", list(MODULES.keys())[0])
    weeks = profile.get("weeks", 4)
    start_date = date.fromisoformat(profile.get("start_date", str(date.today())))
    completed_tasks: set = set(profile.get("completed_tasks", []))

    st.title(f"🧭 Learning Path — {name}")
    st.caption(
        f"Domaine principal : **{domain}** | Durée : **{weeks} semaines** | Début : {start_date}"
    )

    # Overall progress bar
    total_tasks = weeks * 7
    done_count = len(completed_tasks)
    pct = done_count / total_tasks if total_tasks else 0
    pct_display = f"{pct * 100:.0f} %"
    st.progress(pct, text=f"Progression globale : {done_count}/{total_tasks} tâches ({pct_display})")

    # Current week / day
    today = date.today()
    delta_days = max(0, (today - start_date).days)
    current_week = min(delta_days // 7, weeks - 1)
    current_day = DAY_NAMES[delta_days % 7]
    week_title = MODULES[domain][current_week % len(MODULES[domain])]

    tab1, tab2, tab3 = st.tabs(["📅 Aujourd'hui", "🗺️ Roadmap", "📊 Progression"])

    # ── Tab 1 : Aujourd'hui ───────────────────────────────────────────────────
    with tab1:
        st.subheader(f"Semaine {current_week + 1} — {current_day}")
        plan = week_plan(week_title)
        task_text = plan[current_day]
        tk = task_key(current_week + 1, current_day)
        checked = tk in completed_tasks
        new_checked = st.checkbox(task_text, value=checked, key=f"chk_{tk}")
        if new_checked != checked:
            if new_checked:
                completed_tasks.add(tk)
            else:
                completed_tasks.discard(tk)
            profile["completed_tasks"] = list(completed_tasks)
            save_profile(profile)
            st.rerun()

        # Dev.to dynamic articles
        st.divider()
        st.subheader("📰 Articles du jour (Dev.to)")
        tag = DEVTO_TAG_MAP.get(domain, "programming")
        articles = fetch_devto(tag)
        if articles:
            for art in articles[:5]:
                title = art.get("title", "")
                url = art.get("url", "#")
                st.markdown(f"- [{title}]({url})")
        else:
            st.info("Aucun article trouvé pour le moment (vérifie ta connexion).")

        # Static official resources
        st.divider()
        st.subheader("📚 Ressources officielles")
        for res_title, res_url in RESOURCES.get(domain, []):
            st.markdown(f"- [{res_title}]({res_url})")

    # ── Tab 2 : Roadmap (current week only) ───────────────────────────────────
    with tab2:
        st.subheader(f"Semaine {current_week + 1} sur {weeks} — {week_title}")
        wt = MODULES[domain][current_week % len(MODULES[domain])]
        plan = week_plan(wt)
        for day in DAY_NAMES:
            tk = task_key(current_week + 1, day)
            done_day = tk in completed_tasks
            icon = "✅" if done_day else "⬜"
            st.write(f"{icon} **{day}** : {plan[day]}")

        st.divider()
        st.subheader("🧪 Quiz de fin de semaine")
        for q_text in weekly_quiz_questions(wt):
            st.write(f"**Q :** {q_text}")

        domain_quiz = QUIZ_BANK.get(domain, [])
        if domain_quiz:
            st.divider()
            st.subheader("Questions de connaissance")
            # Seed by week number so questions are consistent within the same week
            rng = random.Random(current_week)
            sample = rng.sample(domain_quiz, min(3, len(domain_quiz)))
            for q, a in sample:
                st.write(f"**Q :** {q}")
                with st.expander("Voir la réponse"):
                    st.write(a)

    # ── Tab 3 : Progression ───────────────────────────────────────────────────
    with tab3:
        st.subheader("📊 Tes statistiques")
        col1, col2, col3 = st.columns(3)
        col1.metric("Tâches complétées", f"{done_count} / {total_tasks}")
        col2.metric("Semaine actuelle", f"{current_week + 1} / {weeks}")
        col3.metric("Progression", pct_display)
        st.progress(pct)

        st.divider()
        st.subheader("Détail par semaine")
        for w in range(weeks):
            wt = MODULES[domain][w % len(MODULES[domain])]
            w_done = sum(1 for d in DAY_NAMES if task_key(w + 1, d) in completed_tasks)
            st.write(f"**Semaine {w + 1}** ({wt}) : {w_done}/7 tâches ✅")

        st.divider()
        st.subheader("Ton profil")
        st.json({
            "Prénom": profile.get("name"),
            "Âge": profile.get("age"),
            "Genre": profile.get("gender"),
            "Niveau": profile.get("level"),
            "Objectif": profile.get("goal"),
            "Heures/semaine": profile.get("hours_per_week"),
            "Domaines": profile.get("domains"),
            "Date de début": profile.get("start_date"),
        })


# ─── Entry point ──────────────────────────────────────────────────────────────

init_session()

if st.session_state.step == "main":
    if not st.session_state.profile:
        st.session_state.step = "user_id"
        st.rerun()
    else:
        main_ui()
else:
    conversation_ui()
