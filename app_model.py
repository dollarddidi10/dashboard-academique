app_code = '''
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

st.set_page_config(
    page_title="Tableau de Bord Académique",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #f8f9fa; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f, #2563a8);
        border-right: 3px solid #2563a8;
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    h1, h2, h3, h4 { color: #1e3a5f !important; }
    p, label, .stMarkdown { color: #1a1a1a !important; }
    .metric-card {
        background: #ffffff;
        border: 1px solid #2563a8;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(37,99,168,0.10);
    }
    .metric-card h2 { font-size: 2.2rem; color: #2563a8 !important; margin: 0; }
    .metric-card p  { font-size: 0.9rem; color: #555 !important; margin: 0; }
    .section-title {
        color: #1e3a5f !important;
        border-left: 4px solid #2563a8;
        padding-left: 12px;
        margin-bottom: 1rem;
    }
    .pred-admis {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border: 2px solid #28a745;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
    }
    .pred-ajourne {
        background: linear-gradient(135deg, #fff3cd, #ffeeba);
        border: 2px solid #ffc107;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
    }
    .pred-title { font-size: 1.3rem; font-weight: bold; color: #333 !important; margin-bottom: 8px; }
    .pred-result-admis  { font-size: 2.8rem; font-weight: 900; color: #155724 !important; }
    .pred-result-ajourne { font-size: 2.8rem; font-weight: 900; color: #856404 !important; }
    .conseil-box {
        background: #e8f4fd;
        border-left: 5px solid #2563a8;
        border-radius: 8px;
        padding: 16px 20px;
        margin-top: 16px;
    }
    .conseil-box p { color: #1a1a1a !important; margin: 4px 0; }
    .stButton > button {
        background: linear-gradient(135deg, #2563a8, #1e3a5f);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 14px 40px;
        font-size: 1.1rem;
        font-weight: bold;
        width: 100%;
        cursor: pointer;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.88; }
    .stSlider > div > div { background: #2563a8 !important; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

COLORS = ["#2563a8","#e94560","#f5a623","#0f9b8e","#7b68ee","#50c878","#ff6b6b","#ffd93d"]
sns.set_theme(style="whitegrid")

# ── Chargement données & modèle ──────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("dataset_academique.csv")

@st.cache_resource
def load_model():
    return {
        "model":      joblib.load("best_model.pkl"),
        "scaler":     joblib.load("scaler.pkl"),
        "le_filiere": joblib.load("le_filiere.pkl"),
        "le_niveau":  joblib.load("le_niveau.pkl"),
        "le_genre":   joblib.load("le_genre.pkl"),
        "le_statut":  joblib.load("le_statut.pkl"),
    }

df_raw = load_data()
df_raw["Statut"] = df_raw["Statut"].replace("Absent", "Ajourné")
ml = load_model()
ordre_niveau = ["Licence 1","Licence 2","Licence 3","Master 1","Master 2"]

# ── SIDEBAR ──────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/graduation-cap.png", width=75)
st.sidebar.title("🎓 Dashboard\\nAcadémique")
st.sidebar.markdown("---")

menu = st.sidebar.radio("📌 Navigation", [
    "🏠 Accueil & KPIs",
    "📊 Analyse des Notes",
    "🏫 Filières & Niveaux",
    "👥 Genre & Assiduité",
    "🤖 Prédiction IA",
    "🔍 Exploration des Données"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Filtres globaux")
filieres_dispo = sorted(df_raw["Filiere"].unique())
filieres_sel = st.sidebar.multiselect("Filières", filieres_dispo, default=filieres_dispo)
niveaux_sel  = st.sidebar.multiselect("Niveaux",  ordre_niveau,   default=ordre_niveau)
genre_sel    = st.sidebar.multiselect("Genre",    df_raw["Genre"].unique().tolist(),
                                       default=df_raw["Genre"].unique().tolist())

df_f = df_raw[
    df_raw["Filiere"].isin(filieres_sel) &
    df_raw["Niveau"].isin(niveaux_sel)   &
    df_raw["Genre"].isin(genre_sel)
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"<small>📋 {len(df_f)} étudiants sélectionnés</small>", unsafe_allow_html=True)
st.sidebar.markdown("<small>© 2025 Dashboard Académique</small>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
#  PAGE 1 — ACCUEIL
# ════════════════════════════════════════════════════════
if menu == "🏠 Accueil & KPIs":
    st.markdown("<h1 style=\\'text-align:center;\\'>🎓 Tableau de Bord Académique</h1>", unsafe_allow_html=True)
    st.markdown("<p style=\\'text-align:center; font-size:1.1rem; color:#555;\\'>Analyse & Prédiction de la performance étudiante</p>", unsafe_allow_html=True)
    st.markdown("---")

    total   = len(df_f)
    admis   = (df_f["Statut"]=="Admis").sum()
    taux    = admis/total*100 if total > 0 else 0
    moy_gen = df_f["Moyenne"].mean()
    assid   = df_f["Assiduite_pct"].mean()

    c1,c2,c3,c4,c5 = st.columns(5)
    for col, val, label in zip(
        [c1,c2,c3,c4,c5],
        [total, admis, f"{taux:.1f}%", f"{moy_gen:.2f}/20", f"{assid:.1f}%"],
        ["👨‍🎓 Étudiants","✅ Admis","📈 Taux réussite","⭐ Moyenne","📅 Assiduité moy."]
    ):
        col.markdown(f"""<div class="metric-card"><h2>{val}</h2><p>{label}</p></div>""",
                     unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 class=\\'section-title\\'>Répartition des Statuts</h3>", unsafe_allow_html=True)
        sc = df_f["Statut"].value_counts()
        fig, ax = plt.subplots(figsize=(5,5), facecolor="white")
        ax.set_facecolor("white")
        wedges, texts, autotexts = ax.pie(
            sc, labels=sc.index, autopct="%1.1f%%",
            colors=COLORS[:len(sc)], startangle=140,
            wedgeprops=dict(edgecolor="white", linewidth=2))
        for t in texts: t.set_color("#1a1a1a")
        for t in autotexts: t.set_color("white"); t.set_fontsize(11)
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown("<h3 class=\\'section-title\\'>Effectif par Filière</h3>", unsafe_allow_html=True)
        top = df_f["Filiere"].value_counts()
        fig, ax = plt.subplots(figsize=(6,5), facecolor="white")
        ax.set_facecolor("white")
        bars = ax.barh(top.index[::-1], top.values[::-1], color=COLORS[:len(top)])
        for bar, v in zip(bars, top.values[::-1]):
            ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
                    str(v), va="center", color="#1a1a1a")
        ax.tick_params(colors="#1a1a1a")
        st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════
#  PAGE 2 — ANALYSE DES NOTES
# ════════════════════════════════════════════════════════
elif menu == "📊 Analyse des Notes":
    st.markdown("<h2 class=\\'section-title\\'>📊 Analyse des Notes</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Distribution des Moyennes")
        fig, ax = plt.subplots(figsize=(6,4), facecolor="white")
        ax.set_facecolor("white")
        sns.histplot(df_f["Moyenne"], bins=20, kde=True, color=COLORS[0], ax=ax)
        ax.axvline(10, color="red", linestyle="--", label="Seuil 10/20")
        ax.tick_params(colors="#1a1a1a"); ax.legend()
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown("#### Boxplot par Niveau")
        fig, ax = plt.subplots(figsize=(6,4), facecolor="white")
        ax.set_facecolor("white")
        niv_p = [n for n in ordre_niveau if n in df_f["Niveau"].unique()]
        sns.boxplot(data=df_f, x="Niveau", y="Moyenne", order=niv_p, palette=COLORS[:5], ax=ax)
        ax.axhline(10, color="red", linestyle="--", alpha=0.7)
        ax.tick_params(colors="#1a1a1a"); plt.xticks(rotation=30, ha="right")
        st.pyplot(fig); plt.close()

    st.markdown("#### Assiduité vs Moyenne")
    fig, ax = plt.subplots(figsize=(10,4), facecolor="white")
    ax.set_facecolor("white")
    cmap = {"Admis": COLORS[0], "Ajourné": COLORS[1]}
    for s, g in df_f.groupby("Statut"):
        ax.scatter(g["Assiduite_pct"], g["Moyenne"], label=s,
                   alpha=0.6, color=cmap.get(s,"gray"), s=35)
    ax.axhline(10, color="red", linestyle="--", alpha=0.5)
    ax.set_xlabel("Assiduité (%)"); ax.set_ylabel("Moyenne /20"); ax.legend()
    st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════
#  PAGE 3 — FILIÈRES & NIVEAUX
# ════════════════════════════════════════════════════════
elif menu == "🏫 Filières & Niveaux":
    st.markdown("<h2 class=\\'section-title\\'>🏫 Filières & Niveaux</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Taux de Réussite par Filière")
        taux_fil = df_f.groupby("Filiere").apply(
            lambda x: (x["Statut"]=="Admis").sum()/len(x)*100
        ).reset_index(name="Taux").sort_values("Taux")
        fig, ax = plt.subplots(figsize=(6,5), facecolor="white")
        ax.set_facecolor("white")
        bars = ax.barh(taux_fil["Filiere"], taux_fil["Taux"], color=COLORS[3])
        for bar, v in zip(bars, taux_fil["Taux"]):
            ax.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2,
                    f"{v:.1f}%", va="center", fontsize=9)
        ax.set_xlim(0,115); ax.tick_params(colors="#1a1a1a")
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown("#### Moyenne par Filière")
        moy_fil = df_f.groupby("Filiere")["Moyenne"].mean().sort_values()
        fig, ax = plt.subplots(figsize=(6,5), facecolor="white")
        ax.set_facecolor("white")
        ax.barh(moy_fil.index, moy_fil.values, color=COLORS[4])
        ax.axvline(10, color="red", linestyle="--")
        ax.tick_params(colors="#1a1a1a")
        st.pyplot(fig); plt.close()

    st.markdown("#### 🌡️ Heatmap Filière × Niveau")
    niv_p = [n for n in ordre_niveau if n in df_f["Niveau"].unique()]
    pivot = df_f.pivot_table(values="Moyenne", index="Filiere", columns="Niveau", aggfunc="mean")[niv_p]
    fig, ax = plt.subplots(figsize=(10,5), facecolor="white")
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=0.5, ax=ax)
    plt.xticks(rotation=30, ha="right"); plt.tight_layout()
    st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════
#  PAGE 4 — GENRE & ASSIDUITÉ
# ════════════════════════════════════════════════════════
elif menu == "👥 Genre & Assiduité":
    st.markdown("<h2 class=\\'section-title\\'>👥 Genre & Assiduité</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Répartition Genre par Filière")
        g_fil = df_f.groupby(["Filiere","Genre"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(6,5), facecolor="white")
        g_fil.plot(kind="bar", ax=ax, color=[COLORS[0],COLORS[1]], edgecolor="white")
        ax.tick_params(colors="#1a1a1a"); ax.legend()
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown("#### Assiduité par Niveau")
        an = df_f.groupby("Niveau")["Assiduite_pct"].mean().reindex(
            [n for n in ordre_niveau if n in df_f["Niveau"].unique()])
        fig, ax = plt.subplots(figsize=(6,5), facecolor="white")
        ax.bar(an.index, an.values, color=COLORS[2], edgecolor="white")
        ax.set_ylabel("Assiduité (%)"); ax.tick_params(colors="#1a1a1a")
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig); plt.close()

    st.markdown("#### Comparaison par Genre")
    comp = df_f.groupby("Genre")[["Moyenne","Assiduite_pct"]].mean()
    fig, axes = plt.subplots(1,2, figsize=(10,4), facecolor="white")
    for ax_i, col_i, color in zip(axes,["Moyenne","Assiduite_pct"],[COLORS[0],COLORS[1]]):
        ax_i.set_facecolor("white")
        ax_i.bar(comp.index, comp[col_i], color=color, edgecolor="white")
        ax_i.set_title(col_i.replace("_pct"," (%)"))
        ax_i.tick_params(colors="#1a1a1a")
    plt.tight_layout(); st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════
#  PAGE 5 — PRÉDICTION IA
# ════════════════════════════════════════════════════════
elif menu == "🤖 Prédiction IA":
    st.markdown("<h2 class=\\'section-title\\'>🤖 Prédiction du Statut Académique</h2>", unsafe_allow_html=True)
    st.markdown("<p>Renseignez le profil de l\\'étudiant pour obtenir une prédiction instantanée.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_form, col_result = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown("### 📋 Profil de l\\'étudiant")

        filiere  = st.selectbox("🏫 Filière", sorted(df_raw["Filiere"].unique()))
        niveau   = st.selectbox("📚 Niveau", ordre_niveau)
        genre    = st.selectbox("👤 Genre",  ["Masculin","Féminin"])

        st.markdown("#### 📊 Résultats académiques")
        moyenne  = st.slider("⭐ Moyenne générale (/20)", 0.0, 20.0, 12.0, 0.5)

        color_moy = "#28a745" if moyenne >= 10 else "#dc3545"
        st.markdown(f"<p style=\\'color:{color_moy}; font-weight:bold;\\'>{'✅ Au-dessus du seuil' if moyenne >= 10 else '❌ En dessous du seuil (10/20)'}</p>",
                    unsafe_allow_html=True)

        assiduite = st.slider("📅 Taux d\\'assiduité (%)", 0.0, 100.0, 75.0, 1.0)

        color_ass = "#28a745" if assiduite >= 70 else "#ffc107" if assiduite >= 50 else "#dc3545"
        label_ass = "✅ Bonne assiduité" if assiduite >= 70 else "⚠️ Assiduité moyenne" if assiduite >= 50 else "❌ Assiduité faible"
        st.markdown(f"<p style=\\'color:{color_ass}; font-weight:bold;\\'>{label_ass}</p>",
                    unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("🔮 Lancer la Prédiction")

    with col_result:
        st.markdown("### 🎯 Résultat de la Prédiction")

        if predict_btn:
            data_input = pd.DataFrame([{
                "Filiere_enc":   ml["le_filiere"].transform([filiere])[0],
                "Niveau_enc":    ml["le_niveau"].transform([niveau])[0],
                "Genre_enc":     ml["le_genre"].transform([genre])[0],
                "Moyenne":       moyenne,
                "Assiduite_pct": assiduite
            }])
            data_sc  = ml["scaler"].transform(data_input)
            pred     = ml["model"].predict(data_sc)[0]
            proba    = ml["model"].predict_proba(data_sc)[0]
            statut   = ml["le_statut"].inverse_transform([pred])[0]
            classes  = ml["le_statut"].classes_

            # ── Carte résultat ────────────────────────────
            is_admis = statut == "Admis"
            css_card = "pred-admis" if is_admis else "pred-ajourne"
            css_txt  = "pred-result-admis" if is_admis else "pred-result-ajourne"
            emoji    = "🎉" if is_admis else "⚠️"

            st.markdown(f"""
            <div class="{css_card}">
                <div class="pred-title">Statut prédit pour cet étudiant</div>
                <div class="{css_txt}">{emoji} {statut}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Jauge de probabilités ─────────────────────
            st.markdown("#### 📊 Probabilités par classe")
            for cls, p in zip(classes, proba):
                color = "#28a745" if cls=="Admis" else "#ffc107"
                st.markdown(f"**{cls}** — `{p*100:.1f}%`")
                st.markdown(f"""
                <div style="background:#e9ecef; border-radius:8px; height:20px; margin-bottom:10px;">
                  <div style="background:{color}; width:{p*100:.1f}%; height:20px;
                              border-radius:8px; transition:width 0.5s;"></div>
                </div>""", unsafe_allow_html=True)

            # ── Graphe radar ──────────────────────────────
            st.markdown("#### 📈 Profil vs Moyennes de la promotion")
            moy_globale  = df_raw["Moyenne"].mean()
            assid_globale = df_raw["Assiduite_pct"].mean()

            categories = ["Moyenne\\n(/20)", "Assiduité\\n(%)"]
            etudiant   = [moyenne,   assiduite]
            promotion  = [moy_globale, assid_globale]

            fig, ax = plt.subplots(figsize=(5,3), facecolor="white")
            ax.set_facecolor("white")
            x = np.arange(len(categories))
            w = 0.3
            ax.bar(x - w/2, etudiant,  w, label="Étudiant",  color=COLORS[0])
            ax.bar(x + w/2, promotion, w, label="Promotion", color=COLORS[2], alpha=0.7)
            ax.set_xticks(x); ax.set_xticklabels(categories)
            ax.legend(); ax.set_ylim(0, 110)
            ax.tick_params(colors="#1a1a1a")
            st.pyplot(fig); plt.close()

            # ── Conseils ──────────────────────────────────
            st.markdown("#### 💡 Recommandations")
            conseils = []
            if moyenne < 10:
                conseils.append("📖 Renforcer l\\'encadrement pédagogique et les séances de tutorat.")
            if assiduite < 70:
                conseils.append("📅 Améliorer l\\'assiduité — en dessous de 70% le risque d\\'échec augmente fortement.")
            if moyenne >= 10 and assiduite >= 70:
                conseils.append("🌟 Bon profil ! Encourager la continuité dans le travail.")
            if moyenne >= 14:
                conseils.append("🏆 Excellent niveau — candidat potentiel pour une mention ou une bourse.")

            for c in conseils:
                st.markdown(f"""<div class="conseil-box"><p>{c}</p></div>""",
                            unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="background:#f0f4ff; border-radius:12px; padding:40px; text-align:center; margin-top:20px;">
                <div style="font-size:3rem;">🤖</div>
                <p style="color:#2563a8 !important; font-size:1.1rem; font-weight:bold;">
                    Remplissez le profil et cliquez sur<br><b>Lancer la Prédiction</b>
                </p>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
#  PAGE 6 — EXPLORATION
# ════════════════════════════════════════════════════════
elif menu == "🔍 Exploration des Données":
    st.markdown("<h2 class=\\'section-title\\'>🔍 Exploration des Données</h2>", unsafe_allow_html=True)

    st.markdown("#### Statistiques descriptives")
    st.dataframe(df_f.describe().style.background_gradient(cmap="Blues"), use_container_width=True)

    st.markdown("#### Données filtrées")
    st.dataframe(df_f.reset_index(drop=True), use_container_width=True, height=350)

    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Télécharger CSV", csv, "data_filtree.csv", "text/csv")
'''

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("✅ app.py mis à jour avec la page Prédiction IA !")
