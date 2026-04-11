import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go
import pandas as pd
import os

st.set_page_config(
    page_title="Prédiction Emploi — Tunisie",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background: #f0f4f8; }

[data-testid="stSidebar"] {
    background: #0a1628 !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.15);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

.sb-logo {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.3rem; font-weight: 800;
    color: #ffffff !important; line-height: 1.2;
}
.sb-sub { font-size: 0.72rem; color: #64748b !important; margin-top: 2px; }
.sb-divider { border: none; border-top: 1px solid #1e3a5f; margin: 14px 0; }
.sb-section {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    color: #0ea5e9 !important; margin: 18px 0 10px 0;
}
.sb-stat {
    background: #112240; border-radius: 10px;
    padding: 10px 14px; margin: 6px 0;
    border-left: 3px solid #0ea5e9;
}
.sb-stat-num {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.35rem; font-weight: 800; color: #e2e8f0 !important;
}
.sb-stat-lbl { font-size: 0.7rem; color: #64748b !important; margin-top: 1px; }

.page-header {
    background: linear-gradient(135deg, #0a1628 0%, #0f2d5c 50%, #1a4080 100%);
    border-radius: 20px; padding: 32px 40px; margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(10,22,40,0.2);
    position: relative; overflow: hidden;
}
.page-header::before {
    content: ''; position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(14,165,233,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.page-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.9rem; font-weight: 800; color: #ffffff; margin: 0;
}
.page-subtitle { font-size: 0.85rem; color: #7dd3fc; margin-top: 6px; }
.badge {
    display: inline-block;
    background: rgba(14,165,233,0.2); border: 1px solid rgba(14,165,233,0.4);
    color: #7dd3fc; font-size: 0.7rem; font-weight: 600;
    padding: 3px 10px; border-radius: 20px; margin-top: 12px;
}

.card {
    background: #ffffff; border-radius: 16px; padding: 24px;
    box-shadow: 0 2px 12px rgba(15,45,92,0.08), 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 20px; border: 1px solid #e2e8f0;
}
.card-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    color: #0ea5e9; margin-bottom: 16px;
    padding-bottom: 10px; border-bottom: 2px solid #f0f9ff;
}

.result-card-employe {
    background: linear-gradient(135deg,#ecfdf5,#d1fae5);
    border: 1.5px solid #10b981; border-radius: 16px; padding: 28px;
    text-align: center; box-shadow: 0 4px 20px rgba(16,185,129,0.15);
}
.result-card-chomeur {
    background: linear-gradient(135deg,#fff1f2,#ffe4e6);
    border: 1.5px solid #f43f5e; border-radius: 16px; padding: 28px;
    text-align: center; box-shadow: 0 4px 20px rgba(244,63,94,0.15);
}
.result-card-inactif {
    background: linear-gradient(135deg,#eff6ff,#dbeafe);
    border: 1.5px solid #3b82f6; border-radius: 16px; padding: 28px;
    text-align: center; box-shadow: 0 4px 20px rgba(59,130,246,0.15);
}
.result-icon { font-size: 2.5rem; margin-bottom: 8px; }
.result-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.8rem; font-weight: 800; margin: 4px 0;
}
.c-green { color: #059669; }
.c-red   { color: #e11d48; }
.c-blue  { color: #2563eb; }
.result-desc { font-size: 0.87rem; color: #475569; margin-top: 6px; }

.facteur {
    background: #f8faff; border: 1px solid #bfdbfe;
    border-left: 3px solid #3b82f6; border-radius: 8px;
    padding: 9px 14px; margin: 6px 0;
    font-size: 0.83rem; color: #1e40af;
}

.stButton > button {
    background: linear-gradient(135deg,#0369a1,#0ea5e9) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.95rem !important;
    padding: 14px 0 !important;
    box-shadow: 0 4px 16px rgba(3,105,161,0.35) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(3,105,161,0.5) !important;
}

label { color: #374151 !important; font-size: 0.82rem !important; font-weight: 500 !important; }
div[data-baseweb="select"] > div {
    background: #f8fafc !important; border-color: #e2e8f0 !important; border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Modèle ────────────────────────────────────────────────────────
@st.cache_resource
def charger_modele():
    return joblib.load("modele_final.pkl"), joblib.load("features.pkl")

try:
    modele, features = charger_modele()
    modele_charge = True
except Exception as e:
    modele_charge = False
    st.error(f"❌ Erreur chargement modèle : {e}")

# ════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-logo">📊 ML Dashboard</div><div class="sb-sub">ENPE 2017 · INS Tunisie</div><hr class="sb-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Informations modèle</div>', unsafe_allow_html=True)
    for num, lbl in [("XGBoost","Algorithme"),("452 928","Individus"),("65.1 %","Accuracy"),("0.648","F1-macro"),("14","Features")]:
        st.markdown(f'<div class="sb-stat"><div class="sb-stat-num">{num}</div><div class="sb-stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Distribution des classes</div>', unsafe_allow_html=True)
    fig_pie = go.Figure(go.Pie(
        labels=["Employé","Chômeur","Inactif"], values=[52.3,15.4,32.3], hole=0.58,
        marker_colors=["#10b981","#f43f5e","#3b82f6"],
        textinfo="label+percent", textfont=dict(size=10,color="#e2e8f0"),
    ))
    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)",margin=dict(t=8,b=8,l=8,r=8),height=200,showlegend=False,font_color="#94a3b8")
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('<div class="sb-section">Comparaison modèles</div>', unsafe_allow_html=True)
    df_m = pd.DataFrame({"M":["XGBoost","Rnd Forest","Log. Reg.","SVM","KNN"],"F1":[0.651,0.638,0.612,0.601,0.554]})
    fig_bm = go.Figure(go.Bar(
        x=df_m["F1"], y=df_m["M"], orientation="h",
        marker_color=["#0ea5e9","#1e3a5f","#1e3a5f","#1e3a5f","#1e3a5f"],
        text=[f"{v:.3f}" for v in df_m["F1"]], textposition="outside", textfont=dict(color="#94a3b8",size=10),
    ))
    fig_bm.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0.5,0.72],color="#475569",showgrid=True,gridcolor="#1e3a5f"),
        yaxis=dict(color="#94a3b8",tickfont=dict(size=10)),
        margin=dict(t=4,b=4,l=4,r=40),height=190,font_color="#94a3b8")
    st.plotly_chart(fig_bm, use_container_width=True)

    st.markdown('<div class="sb-section">Feature importance</div>', unsafe_allow_html=True)
    df_fi = pd.DataFrame({"F":["CSP","Secteur","Âge","Instruction","Groupe âge","Sexe","Gouvernorat","Milieu","Sit. mat.","Diplômé sup."],
                          "I":[0.21,0.18,0.14,0.12,0.09,0.07,0.06,0.05,0.04,0.04]}).sort_values("I")
    fig_fi = go.Figure(go.Bar(x=df_fi["I"],y=df_fi["F"],orientation="h",marker_color="#0ea5e9",marker_line_width=0))
    fig_fi.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#475569",showgrid=True,gridcolor="#1e3a5f"),
        yaxis=dict(color="#94a3b8",tickfont=dict(size=10)),
        margin=dict(t=4,b=4,l=4,r=10),height=270,font_color="#94a3b8")
    st.plotly_chart(fig_fi, use_container_width=True)

# ════════════════════════════════════════════════════
# PAGE PRINCIPALE
# ════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
    <div class="page-title">Prédiction du Statut d'Emploi</div>
    <div class="page-subtitle">Modèle XGBoost · Dataset ENPE 2017 · Institut National de la Statistique, Tunisie</div>
    <span class="badge">🎓 Projet Machine Learning</span>
</div>
""", unsafe_allow_html=True)

GOUVERNORATS = {"Tunis":11,"Ariana":12,"Ben Arous":13,"Manouba":14,"Nabeul":15,"Zaghouan":16,"Bizerte":17,
    "Beja":21,"Jendouba":22,"Kef":23,"Siliana":24,"Sousse":31,"Monastir":32,"Mahdia":33,"Sfax":34,
    "Kairouan":41,"Kasserine":42,"Sidi Bouzid":43,"Gabes":51,"Medenine":52,"Tataouine":53,"Gafsa":61,"Tozeur":62,"Kebili":63}
NIVEAUX    = {"Sans diplôme":1,"Enseignement de base":2,"Secondaire (Bac)":3,"Supérieur (Bac+)":4}
SITUATIONS = {"Célibataire":1,"Marié(e)":2,"Divorcé(e)":3,"Veuf/Veuve":4}
LIENS      = {"Chef de ménage":1,"Épouse du chef":2,"Fils/Fille":3,"Autre membre":4}

c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    st.markdown('<div class="card"><div class="card-header">📍 Localisation</div>', unsafe_allow_html=True)
    gouvernorat_nom  = st.selectbox("Gouvernorat", list(GOUVERNORATS.keys()))
    gouvernorat_code = GOUVERNORATS[gouvernorat_nom]
    milieu = st.radio("Milieu", ["Urbain","Rural"], horizontal=True)
    milieu_code = 1 if milieu == "Urbain" else 2
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card"><div class="card-header">👤 Profil Personnel</div>', unsafe_allow_html=True)
    sexe = st.radio("Sexe", ["Masculin","Féminin"], horizontal=True)
    sexe_code = 1 if sexe == "Masculin" else 2
    age = st.slider("Âge", 15, 75, 25)
    situation_nom = st.selectbox("Situation matrimoniale", list(SITUATIONS.keys()))
    situation_code = SITUATIONS[situation_nom]
    lien_nom = st.selectbox("Lien de parenté", list(LIENS.keys()))
    lien_code = LIENS[lien_nom]
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card"><div class="card-header">🎓 Emploi & Formation</div>', unsafe_allow_html=True)
    niveau_nom = st.selectbox("Niveau d'instruction", list(NIVEAUX.keys()))
    niveau_code = NIVEAUX[niveau_nom]
    secteur_code = st.selectbox("Secteur d'activité", [0,1,2,3,4],
        format_func=lambda x:{0:"Sans emploi",1:"Agriculture",2:"Industrie",3:"Commerce",4:"Services"}[x])
    csp_code = st.selectbox("Catégorie socioprofessionnelle", [0,1,2,3],
        format_func=lambda x:{0:"Sans emploi",1:"Cadre",2:"Technicien",3:"Ouvrier"}[x])
    st.markdown('</div>', unsafe_allow_html=True)

# Variables dérivées
REGIONS_INT = [21,22,23,24,41,42,43,53,61,62,63]
region_interieure = 1 if gouvernorat_code in REGIONS_INT else 0
groupe_age        = 0 if age<25 else (1 if age<35 else (2 if age<50 else 3))
diplome_superieur = 1 if niveau_code==4 else 0
femme_region_int  = 1 if (sexe_code==2 and region_interieure==1) else 0
jeune_diplome     = 1 if (age<35 and diplome_superieur==1) else 0

vecteur = np.array([[gouvernorat_code,milieu_code,lien_code,sexe_code,
                     situation_code,age,niveau_code,secteur_code,csp_code,
                     region_interieure,groupe_age,diplome_superieur,femme_region_int,jeune_diplome]])

_, bcol, _ = st.columns([1,2,1])
with bcol:
    predict = st.button("📊  PRÉDIRE LE STATUT D'EMPLOI", use_container_width=True)

if predict:
    if not modele_charge:
        st.error("Le modèle n'est pas chargé.")
    else:
        pred   = modele.predict(vecteur)[0]
        probas = modele.predict_proba(vecteur)[0]

        CLASSES = ["Employé","Chômeur","Inactif"]
        ICONS   = ["✅","⚠️","💼"]
        DESCS   = {0:"Bon profil d'insertion professionnelle.",
                   1:"Risque élevé de chômage.",
                   2:"Probablement hors du marché du travail."}
        CSS     = ["result-card-employe","result-card-chomeur","result-card-inactif"]
        CLRS    = ["c-green","c-red","c-blue"]
        GCLR    = ["#10b981","#f43f5e","#3b82f6"]
        RGB     = [(16,185,129),(244,63,94),(59,130,246)]

        st.markdown("<br>", unsafe_allow_html=True)
        left, right = st.columns(2, gap="large")

        with left:
            st.markdown(f"""
            <div class="{CSS[pred]}">
                <div class="result-icon">{ICONS[pred]}</div>
                <div class="result-title {CLRS[pred]}">{CLASSES[pred].upper()}</div>
                <div class="result-desc">{DESCS[pred]}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="card"><div class="card-header">⚡ Facteurs de vulnérabilité</div>', unsafe_allow_html=True)
            facteurs = []
            if region_interieure: facteurs.append("📍 Région intérieure — risque +15 pts")
            if diplome_superieur and pred==1: facteurs.append("🎓 Paradoxe du diplôme supérieur")
            if femme_region_int: facteurs.append("👩 Femme en région intérieure")
            if jeune_diplome and pred==1: facteurs.append("🕐 Jeune diplômé <35 ans")
            if not facteurs: facteurs.append("✔️ Aucun facteur de vulnérabilité majeur")
            for f in facteurs:
                st.markdown(f'<div class="facteur">{f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=round(probas[pred]*100,1),
                number={"suffix":"%","font":{"size":38,"color":GCLR[pred],"family":"Plus Jakarta Sans"}},
                title={"text":f"Confiance — {CLASSES[pred]}","font":{"size":12,"color":"#64748b"}},
                gauge={"axis":{"range":[0,100],"tickcolor":"#cbd5e1","tickfont":{"color":"#94a3b8","size":10}},
                       "bar":{"color":GCLR[pred],"thickness":0.28},"bgcolor":"#f8fafc","bordercolor":"#e2e8f0",
                       "steps":[{"range":[0,33],"color":"#f8fafc"},{"range":[33,66],"color":"#f1f5f9"},{"range":[66,100],"color":"#e8f0fe"}]}
            ))
            fig_g.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="#374151",margin=dict(t=30,b=5,l=20,r=20),height=215)
            st.plotly_chart(fig_g, use_container_width=True)

            fig_p = go.Figure(go.Bar(
                x=CLASSES, y=[p*100 for p in probas], marker_color=GCLR, marker_line_width=0,
                text=[f"{p:.1%}" for p in probas], textposition="outside",
                textfont=dict(color="#374151",size=12,family="Plus Jakarta Sans"),
            ))
            fig_p.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#f8fafc",
                xaxis=dict(color="#374151",showgrid=False),
                yaxis=dict(color="#94a3b8",showgrid=True,gridcolor="#e2e8f0",range=[0,115]),
                margin=dict(t=15,b=5,l=5,r=5),height=215,
                title=dict(text="Probabilités par classe (%)",font=dict(size=11,color="#64748b")),
                font_color="#374151")
            st.plotly_chart(fig_p, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-header">🕸️ Radar du profil individuel</div>', unsafe_allow_html=True)
        cats = ["Instruction","Âge norm.","Diplôme sup.","Région côtière","Milieu urbain","Jeune diplômé"]
        vals = [niveau_code/4, min(age/75,1), float(diplome_superieur),
                float(1-region_interieure), float(milieu_code==1), float(jeune_diplome)]
        v2 = vals+[vals[0]]; c2 = cats+[cats[0]]
        r,g,b = RGB[pred]
        fig_r = go.Figure(go.Scatterpolar(
            r=v2,theta=c2,fill="toself",
            fillcolor=f"rgba({r},{g},{b},0.12)",
            line_color=f"rgb({r},{g},{b})",line_width=2.5,
            marker=dict(size=6,color=f"rgb({r},{g},{b})")
        ))
        fig_r.update_layout(
            polar=dict(bgcolor="#f8fafc",
                radialaxis=dict(visible=True,range=[0,1],color="#94a3b8",gridcolor="#e2e8f0",tickfont=dict(size=9)),
                angularaxis=dict(color="#374151",gridcolor="#e2e8f0",tickfont=dict(size=11,family="Inter"))),
            paper_bgcolor="rgba(0,0,0,0)",font_color="#374151",
            margin=dict(t=20,b=20,l=50,r=50),height=320)
        st.plotly_chart(fig_r, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center;color:#94a3b8;font-size:0.72rem;padding:30px 0 10px">Projet Machine Learning · ENPE 2017 · INS Tunisie · XGBoost · F1-macro 0.648</div>', unsafe_allow_html=True)
