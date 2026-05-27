app_code = '''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(
    page_title="Tableau de Bord Académique",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #ffffff;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f, #2563a8, #1e3a5f);
        border-right: 3px solid #2563a8;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    .main .block-container {
        padding-top: 1.5rem;
        background: #ffffff;
    }
    h1, h2, h3, h4 { color: #1e3a5f !important; }
    p, label, .stMarkdown { color: #1a1a1a !important; }
    .metric-card {
        background: #f0f4ff;
        border: 1px solid #2563a8;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-card h2 { font-size: 2.2rem; color: #2563a8 !important; margin: 0; }
    .metric-card p  { font-size: 0.9rem; color: #444 !important; margin: 0; }
    .section-title {
        color: #1e3a5f !important;
        border-left: 4px solid #2563a8;
        padding-left: 12px;
        margin-bottom: 1rem;
    }
    .stDataFrame { background: #ffffff; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

COLORS = ["#2563a8","#e94560","#f5a623","#0f9b8e","#7b68ee","#50c878","#ff6b6b","#ffd93d"]
sns.set_theme(style="whitegrid")

@st.cache_data
def load_data():
    return pd.read_csv("dataset_academique.csv")

df = load_data()
ordre_niveau = ["Licence 1","Licence 2","Licence 3","Master 1","Master 2"]

# ── SIDEBAR ──────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/graduation-cap.png", width=80)
st.sidebar.title("🎓 Tableau de Bord\\nAcadémique")
st.sidebar.markdown("---")

menu = st.sidebar.radio("📌 Navigation", [
    "🏠 Accueil & KPIs",
    "📊 Analyse des Notes",
    "🏫 Filières & Niveaux",
    "👥 Genre & Assiduité",
    "🔍 Exploration des Données"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Filtres globaux")

filieres_dispo = sorted(df["Filiere"].unique())
filieres_sel = st.sidebar.multiselect("Filières", filieres_dispo, default=filieres_dispo)
niveaux_sel   = st.sidebar.multiselect("Niveaux", ordre_niveau, default=ordre_niveau)
genre_sel     = st.sidebar.multiselect("Genre", df["Genre"].unique().tolist(), default=df["Genre"].unique().tolist())

df_f = df[
    df["Filiere"].isin(filieres_sel) &
    df["Niveau"].isin(niveaux_sel) &
    df["Genre"].isin(genre_sel)
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"<small>📋 {len(df_f)} étudiants sélectionnés</small>", unsafe_allow_html=True)
st.sidebar.markdown("<small>© 2025 Dashboard Académique</small>", unsafe_allow_html=True)

# ── PAGE 1 — ACCUEIL ─────────────────────────────────────────
if menu == "🏠 Accueil & KPIs":
    st.markdown("<h1 style=\\'text-align:center; color:#1e3a5f;\\'>🎓 Tableau de Bord Académique</h1>", unsafe_allow_html=True)
    st.markdown("<p style=\\'text-align:center; font-size:1.1rem; color:#444;\\'>Analyse de la performance des étudiants</p>", unsafe_allow_html=True)
    st.markdown("---")

    total     = len(df_f)
    admis     = (df_f["Statut"] == "Admis").sum()
    taux      = admis / total * 100 if total > 0 else 0
    moy_gen   = df_f["Moyenne"].mean()

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in zip(
        [c1, c2, c3, c4],
        [total, admis, f"{taux:.1f}%", f"{moy_gen:.2f}/20"],
        ["👨‍🎓 Étudiants", "✅ Admis", "📈 Taux de réussite", "⭐ Moyenne générale"]
    ):
        col.markdown(f"""<div class="metric-card"><h2>{val}</h2><p>{label}</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 class=\\'section-title\\'>Répartition des Statuts</h3>", unsafe_allow_html=True)
        statut_counts = df_f["Statut"].value_counts()
        fig, ax = plt.subplots(figsize=(5,5), facecolor="white")
        ax.set_facecolor("white")
        wedges, texts, autotexts = ax.pie(
            statut_counts, labels=statut_counts.index,
            autopct="%1.1f%%", colors=COLORS[:len(statut_counts)],
            startangle=140, wedgeprops=dict(edgecolor="white", linewidth=2))
        for t in texts: t.set_color("#1a1a1a")
        for t in autotexts: t.set_color("white")
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown("<h3 class=\\'section-title\\'>Top Filières par Effectif</h3>", unsafe_allow_html=True)
        top_fil = df_f["Filiere"].value_counts()
        fig, ax = plt.subplots(figsize=(6,5), facecolor="white")
        ax.set_facecolor("white")
        bars = ax.barh(top_fil.index[::-1], top_fil.values[::-1], color=COLORS[:len(top_fil)])
        for bar, v in zip(bars, top_fil.values[::-1]):
            ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2, str(v), va="center", color="#1a1a1a")
        ax.tick_params(colors="#1a1a1a")
        st.pyplot(fig); plt.close()

# ── PAGE 2 — ANALYSE DES NOTES ───────────────────────────────
elif menu == "📊 Analyse des Notes":
    st.markdown("<h2 class=\\'section-title\\'>📊 Analyse des Notes</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Distribution des Moyennes")
        fig, ax = plt.subplots(figsize=(6,4), facecolor="white")
        ax.set_facecolor("white")
        sns.histplot(df_f["Moyenne"], bins=20, kde=True, color=COLORS[0], ax=ax)
        ax.axvline(10, color="red", linestyle="--", label="Seuil 10/20")
        ax.tick_params(colors="#1a1a1a"); ax.set_xlabel("Moyenne", color="#1a1a1a")
        ax.set_ylabel("Effectif", color="#1a1a1a"); ax.legend()
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown("#### Boxplot par Niveau")
        fig, ax = plt.subplots(figsize=(6,4), facecolor="white")
        ax.set_facecolor("white")
        niv_present = [n for n in ordre_niveau if n in df_f["Niveau"].unique()]
        sns.boxplot(data=df_f, x="Niveau", y="Moyenne", order=niv_present, palette=COLORS[:5], ax=ax)
        ax.axhline(10, color="red", linestyle="--", alpha=0.7)
        ax.tick_params(colors="#1a1a1a"); plt.xticks(rotation=30, ha="right")
        st.pyplot(fig); plt.close()

    st.markdown("#### Assiduité vs Moyenne")
    fig, ax = plt.subplots(figsize=(10,4), facecolor="white")
    ax.set_facecolor("white")
    color_map = {"Admis": COLORS[0], "Ajourné": COLORS[1], "Absent": COLORS[2]}
    for statut, grp in df_f.groupby("Statut"):
        ax.scatter(grp["Assiduite_pct"], grp["Moyenne"], label=statut,
                   alpha=0.6, color=color_map.get(statut,"gray"), s=35)
    ax.axhline(10, color="red", linestyle="--", alpha=0.5)
    ax.tick_params(colors="#1a1a1a"); ax.set_xlabel("Assiduité (%)", color="#1a1a1a")
    ax.set_ylabel("Moyenne /20", color="#1a1a1a"); ax.legend()
    st.pyplot(fig); plt.close()

# ── PAGE 3 — FILIÈRES & NIVEAUX ──────────────────────────────
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
                    f"{v:.1f}%", va="center", color="#1a1a1a", fontsize=9)
        ax.set_xlim(0, 115); ax.tick_params(colors="#1a1a1a")
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

    st.markdown("#### 🌡️ Heatmap : Moyenne par Filière × Niveau")
    niv_present = [n for n in ordre_niveau if n in df_f["Niveau"].unique()]
    pivot = df_f.pivot_table(values="Moyenne", index="Filiere", columns="Niveau", aggfunc="mean")[niv_present]
    fig, ax = plt.subplots(figsize=(10,5), facecolor="white")
    ax.set_facecolor("white")
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=0.5, ax=ax)
    ax.tick_params(colors="#1a1a1a"); plt.xticks(rotation=30, ha="right")
    st.pyplot(fig); plt.close()

# ── PAGE 4 — GENRE & ASSIDUITÉ ───────────────────────────────
elif menu == "👥 Genre & Assiduité":
    st.markdown("<h2 class=\\'section-title\\'>👥 Genre & Assiduité</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Répartition Genre par Filière")
        g_fil = df_f.groupby(["Filiere","Genre"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(6,5), facecolor="white")
        ax.set_facecolor("white")
        g_fil.plot(kind="bar", ax=ax, color=[COLORS[0], COLORS[1]], edgecolor="white")
        ax.tick_params(colors="#1a1a1a"); ax.set_ylabel("Effectif", color="#1a1a1a")
        ax.legend(); plt.xticks(rotation=90, ha="right")
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown("#### Assiduité moyenne par Niveau")
        assid_niv = df_f.groupby("Niveau")["Assiduite_pct"].mean().reindex(
            [n for n in ordre_niveau if n in df_f["Niveau"].unique()])
        fig, ax = plt.subplots(figsize=(6,5), facecolor="white")
        ax.set_facecolor("white")
        ax.bar(assid_niv.index, assid_niv.values, color=COLORS[2], edgecolor="white")
        ax.tick_params(colors="#1a1a1a"); ax.set_ylabel("Assiduité (%)", color="#1a1a1a")
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig); plt.close()

    st.markdown("#### Comparaison Moyenne & Assiduité par Genre")
    comp = df_f.groupby("Genre")[["Moyenne","Assiduite_pct"]].mean()
    fig, axes = plt.subplots(1, 2, figsize=(10,4), facecolor="white")
    for ax_i, col_i, color in zip(axes, ["Moyenne","Assiduite_pct"], [COLORS[0], COLORS[1]]):
        ax_i.set_facecolor("white")
        ax_i.bar(comp.index, comp[col_i], color=color, edgecolor="white")
        ax_i.set_title(col_i.replace("_pct"," (%)"), color="#1a1a1a")
        ax_i.tick_params(colors="#1a1a1a")
    plt.tight_layout()
    st.pyplot(fig); plt.close()

# ── PAGE 5 — EXPLORATION ─────────────────────────────────────
elif menu == "🔍 Exploration des Données":
    st.markdown("<h2 class=\\'section-title\\'>🔍 Exploration des Données</h2>", unsafe_allow_html=True)

    st.markdown("#### Statistiques descriptives")
    st.dataframe(df_f.describe().style.background_gradient(cmap="Blues"), use_container_width=True)

    st.markdown("#### Tableau des données filtrées")
    st.dataframe(df_f.reset_index(drop=True), use_container_width=True, height=350)

    st.markdown("#### Télécharger les données filtrées")
    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Télécharger CSV", csv, "data_filtree.csv", "text/csv")
'''

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("✅ app.py mis à jour — fond blanc, textes noirs !")
