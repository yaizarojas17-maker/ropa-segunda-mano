"""
👗 Dashboard: Ropa de Segunda Mano 2000–2026
Dataset normalizado: 1 fila por País × Año
Deploy en: https://share.streamlit.io/
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Ropa de Segunda Mano 2000–2026",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  .metric-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 1rem; border-radius: 14px; color: white;
    text-align: center; margin: 4px;
  }
  .metric-val { font-size: 1.9rem; font-weight: 800; }
  .metric-lbl { font-size: .8rem; opacity: .85; }
  h1, h2, h3  { color: #4a4a8a; }
</style>
""", unsafe_allow_html=True)


# ── CARGA ─────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Cargando datos…")
def load():
    df = pd.read_csv("dataset_normalizado.csv")
    df["Año_Compra"] = df["Año_Compra"].astype(int)
    return df

df = load()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filtros")

años_r   = st.sidebar.slider("📅 Años", 2000, 2026, (2000, 2026))
paises_s = st.sidebar.multiselect("🌎 País", sorted(df.País.unique()), default=sorted(df.País.unique()))

dff = df[df.Año_Compra.between(*años_r) & df.País.isin(paises_s)].copy()

st.sidebar.divider()
st.sidebar.markdown(f"**Registros:** `{len(dff):,}` filas\n\n`1 fila = 1 país × 1 año`")

# ── TÍTULO ────────────────────────────────────────────────────────────────────
st.title("👗 Compradores de Ropa de Segunda Mano")
st.markdown("#### Dataset Normalizado 2000–2026 · 1 fila por País × Año")
st.divider()

# ── KPIs ──────────────────────────────────────────────────────────────────────
k = st.columns(6)
kpis = [
    ("👥 Total Compradores",  f"{int(dff.Total_Compradores.sum()):,}"),
    ("💰 Gasto Total USD",    f"${dff.Gasto_USD_Total.sum():,.0f}"),
    ("📦 Items Totales",      f"{int(dff.Items_Total.sum()):,}"),
    ("🎂 Edad Prom. Global",  f"{dff.Edad_Promedio.mean():.1f} años"),
    ("😊 % Satisfechos",      f"{dff.Pct_Satisfechos.mean():.1f}%"),
    ("📣 % Recomiendan",      f"{dff.Pct_Recomienda.mean():.1f}%"),
]
for col, (lbl, val) in zip(k, kpis):
    col.markdown(f'<div class="metric-card"><div class="metric-val">{val}</div>'
                 f'<div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.divider()

# ── TABS ──────────────────────────────────────────────────────────────────────
t1, t2, t3, t4, t5, t6 = st.tabs([
    "📈 Tendencias",
    "🌍 Geografía",
    "💰 Economía",
    "😊 Satisfacción",
    "🗺️ Treemap",
    "📋 Dataset",
])

# ══════════ TAB 1 ════════════════════════════════════════════════════════════
with t1:
    st.subheader("📈 Evolución Temporal por País")

    c1, c2 = st.columns(2)
    with c1:
        tot = dff.groupby("Año_Compra")["Total_Compradores"].sum().reset_index()
        fig = px.area(tot, x="Año_Compra", y="Total_Compradores",
                      title="Total de Compradores por Año",
                      color_discrete_sequence=["#667eea"], template="plotly_white")
        fig.update_traces(fill="tozeroy")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.line(dff, x="Año_Compra", y="Gasto_USD_Promedio", color="País",
                       title="Gasto Promedio/Año por País (USD)",
                       markers=True, template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig3 = px.bar(dff, x="Año_Compra", y="Total_Compradores", color="País",
                      title="Compradores por País y Año (apilado)",
                      barmode="stack", template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        fig4 = px.line(dff, x="Año_Compra", y="Items_Promedio", color="País",
                       title="Items Promedio por Año y País",
                       markers=True, template="plotly_white")
        st.plotly_chart(fig4, use_container_width=True)

    # Heatmap compradores
    pivot = dff.pivot_table(index="País", columns="Año_Compra",
                            values="Total_Compradores", aggfunc="sum", fill_value=0)
    fig5 = px.imshow(pivot, title="Heatmap: Compradores por País × Año",
                     color_continuous_scale="Blues", aspect="auto", template="plotly_white",
                     text_auto=True)
    st.plotly_chart(fig5, use_container_width=True)

    # Canal más frecuente por año
    canal_yr = dff.groupby(["Año_Compra","Canal_Mas_Frecuente"]).size().reset_index(name="n")
    fig6 = px.bar(canal_yr, x="Año_Compra", y="n", color="Canal_Mas_Frecuente",
                  title="Canal Más Frecuente por Año",
                  barmode="stack", template="plotly_white")
    st.plotly_chart(fig6, use_container_width=True)


# ══════════ TAB 2 ════════════════════════════════════════════════════════════
with t2:
    st.subheader("🌍 Análisis Geográfico")

    c1, c2 = st.columns(2)
    with c1:
        pc = dff.groupby("País")["Total_Compradores"].sum().reset_index().sort_values("Total_Compradores", ascending=False)
        fig = px.bar(pc, x="País", y="Total_Compradores",
                     title="Total Compradores por País (todos los años)",
                     color="Total_Compradores", color_continuous_scale="Plasma",
                     template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        pg = dff.groupby("País")["Gasto_USD_Promedio"].mean().reset_index().sort_values("Gasto_USD_Promedio", ascending=False)
        fig2 = px.bar(pg, x="País", y="Gasto_USD_Promedio",
                      title="Gasto Promedio por País (USD)",
                      color="Gasto_USD_Promedio", color_continuous_scale="Viridis",
                      template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    iso = {"Perú":"PER","México":"MEX","Colombia":"COL","Argentina":"ARG","Chile":"CHL",
           "España":"ESP","Ecuador":"ECU","Venezuela":"VEN","Bolivia":"BOL","Uruguay":"URY"}
    pc["ISO"] = pc["País"].map(iso)
    fig3 = px.choropleth(pc, locations="ISO", color="Total_Compradores",
                         hover_name="País", color_continuous_scale="Reds",
                         title="Mapa de Calor: Total Compradores por País")
    st.plotly_chart(fig3, use_container_width=True)

    # Edad promedio por país
    ep = dff.groupby("País")["Edad_Promedio"].mean().reset_index().sort_values("Edad_Promedio")
    fig4 = px.bar(ep, x="Edad_Promedio", y="País", orientation="h",
                  title="Edad Promedio del Comprador por País",
                  color="Edad_Promedio", color_continuous_scale="Sunset",
                  template="plotly_white")
    st.plotly_chart(fig4, use_container_width=True)


# ══════════ TAB 3 ════════════════════════════════════════════════════════════
with t3:
    st.subheader("💰 Análisis Económico")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(dff, x="Gasto_USD_Promedio", nbins=30,
                           title="Distribución del Gasto Promedio (USD)",
                           color_discrete_sequence=["#f093fb"], template="plotly_white")
        fig.add_vline(x=dff.Gasto_USD_Promedio.mean(), line_dash="dash", line_color="red",
                      annotation_text=f"Media ${dff.Gasto_USD_Promedio.mean():.1f}")
        fig.add_vline(x=dff.Gasto_USD_Promedio.median(), line_dash="dash", line_color="blue",
                      annotation_text=f"Mediana ${dff.Gasto_USD_Promedio.median():.1f}")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.scatter(dff, x="Ingreso_Prom_USD", y="Gasto_USD_Promedio",
                          color="País", size="Total_Compradores", opacity=0.75,
                          title="Ingreso Promedio vs Gasto Promedio por País/Año",
                          trendline="ols", template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        gc = dff.groupby("Año_Compra")["Gasto_USD_Total"].sum().cumsum().reset_index()
        fig3 = px.area(gc, x="Año_Compra", y="Gasto_USD_Total",
                       title="Gasto Total Acumulado (USD)",
                       color_discrete_sequence=["#43e97b"], template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        fig4 = px.box(dff, x="País", y="Gasto_USD_Promedio", color="País",
                      title="Variabilidad del Gasto por País",
                      template="plotly_white",
                      color_discrete_sequence=px.colors.qualitative.Bold)
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    # Gasto por país a lo largo del tiempo (línea)
    fig5 = px.line(dff, x="Año_Compra", y="Gasto_USD_Total", color="País",
                   title="Gasto Total Anual por País (USD)",
                   markers=True, template="plotly_white")
    st.plotly_chart(fig5, use_container_width=True)

    # Items totales por año
    it = dff.groupby("Año_Compra")["Items_Total"].sum().reset_index()
    fig6 = px.bar(it, x="Año_Compra", y="Items_Total",
                  title="Total de Items Comprados por Año",
                  color="Items_Total", color_continuous_scale="Cividis",
                  template="plotly_white")
    st.plotly_chart(fig6, use_container_width=True)


# ══════════ TAB 4 ════════════════════════════════════════════════════════════
with t4:
    st.subheader("😊 Satisfacción y Comportamiento")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.line(dff, x="Año_Compra", y="Pct_Satisfechos", color="País",
                      title="% Satisfechos por Año y País",
                      markers=True, template="plotly_white")
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.line(dff, x="Año_Compra", y="Pct_Recomienda", color="País",
                       title="% Que Recomienda por Año y País",
                       markers=True, template="plotly_white")
        fig2.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        cp = dff.groupby("País")[["Pct_Satisfechos","Pct_Recomienda","Pct_Primera_Vez"]].mean().reset_index()
        fig3 = go.Figure()
        for col, color in zip(["Pct_Satisfechos","Pct_Recomienda","Pct_Primera_Vez"],
                               ["#667eea","#f093fb","#43e97b"]):
            fig3.add_trace(go.Bar(name=col.replace("Pct_","% "), x=cp.País, y=cp[col], marker_color=color))
        fig3.update_layout(barmode="group", title="KPIs de Comportamiento por País",
                           template="plotly_white", yaxis_title="%")
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        fig4 = px.scatter(dff, x="Pct_Satisfechos", y="Pct_Recomienda",
                          color="País", size="Total_Compradores",
                          title="Satisfacción vs Recomendación",
                          template="plotly_white", opacity=0.75)
        st.plotly_chart(fig4, use_container_width=True)

    # Canal más frecuente por país
    cn = dff.groupby(["País","Canal_Mas_Frecuente"]).size().reset_index(name="n")
    fig5 = px.bar(cn, x="País", y="n", color="Canal_Mas_Frecuente",
                  title="Canal Más Frecuente por País",
                  barmode="group", template="plotly_white",
                  color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig5, use_container_width=True)

    # Plataforma top
    pl = dff.groupby(["País","Plataforma_Top"]).size().reset_index(name="n")
    fig6 = px.bar(pl, x="País", y="n", color="Plataforma_Top",
                  title="Plataforma de Descubrimiento Top por País",
                  barmode="stack", template="plotly_white",
                  color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig6, use_container_width=True)


# ══════════ TAB 5 ════════════════════════════════════════════════════════════
with t5:
    st.subheader("🗺️ Treemap Jerárquico")

    # Treemap País → Canal → Categoría
    tree1 = dff.groupby(["País","Canal_Mas_Frecuente","Categoria_Top"]).agg(
        Compradores=("Total_Compradores","sum"),
        Gasto_Prom=("Gasto_USD_Promedio","mean")
    ).reset_index()
    fig_t1 = px.treemap(tree1,
        path=["País","Canal_Mas_Frecuente","Categoria_Top"],
        values="Compradores", color="Gasto_Prom",
        color_continuous_scale="RdYlGn",
        color_continuous_midpoint=tree1.Gasto_Prom.median(),
        title="País → Canal → Categoría Top | Color = Gasto Promedio USD",
        template="plotly_white")
    fig_t1.update_traces(textinfo="label+value+percent root")
    fig_t1.update_layout(height=550)
    st.plotly_chart(fig_t1, use_container_width=True)

    # Sunburst País → Motivación
    sun = dff.groupby(["País","Motivacion_Top"]).agg(
        Compradores=("Total_Compradores","sum")).reset_index()
    fig_s = px.sunburst(sun, path=["País","Motivacion_Top"], values="Compradores",
                        title="País → Motivación Principal",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_s.update_layout(height=500)
    st.plotly_chart(fig_s, use_container_width=True)

    # Scatter matrix numérico
    st.markdown("**🔍 Scatter Matrix de Variables Numéricas**")
    num_cols = ["Gasto_USD_Promedio","Items_Promedio","Edad_Promedio","Ingreso_Prom_USD","Pct_Satisfechos"]
    fig_sm = px.scatter_matrix(dff, dimensions=num_cols, color="País",
                                opacity=0.5, title="Scatter Matrix",
                                template="plotly_white",
                                color_discrete_sequence=px.colors.qualitative.Bold)
    fig_sm.update_traces(diagonal_visible=False)
    st.plotly_chart(fig_sm, use_container_width=True)

    # Correlación
    corr = dff[num_cols].corr()
    fig_c = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                      title="Matriz de Correlación", aspect="auto", template="plotly_white")
    st.plotly_chart(fig_c, use_container_width=True)


# ══════════ TAB 6 ════════════════════════════════════════════════════════════
with t6:
    st.subheader("📋 Dataset Normalizado")
    st.caption("1 fila por País × Año | Año en 4 dígitos | Sin letras en valores numéricos")

    c1, c2, c3 = st.columns(3)
    c1.metric("Filas",    f"{len(dff):,}")
    c2.metric("Columnas", len(dff.columns))
    c3.metric("Período",  f"{dff.Año_Compra.min()} – {dff.Año_Compra.max()}")

    st.dataframe(dff, use_container_width=True, height=420)

    csv = dff.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar CSV Normalizado",
                       csv, "dataset_normalizado.csv", "text/csv")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center;color:#888;font-size:.8rem'>"
    "👗 Dashboard Ropa de Segunda Mano 2000-2026 | "
    "Streamlit + Plotly | Dataset: 1 fila × País × Año"
    "</div>", unsafe_allow_html=True)
