# 👗 Ropa de Segunda Mano 2000–2026

Dashboard interactivo de compradores de ropa de segunda mano (2000–2026).

## 🚀 Deploy en Streamlit Cloud

1. Sube esta carpeta a un repositorio GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io/)
3. Conecta tu repo y selecciona `app.py`
4. ¡Listo!

## 📁 Archivos

| Archivo | Descripción |
|---|---|
| `app.py` | Aplicación Streamlit principal |
| `dataset_normalizado.csv` | Dataset: 1 fila por País × Año (270 filas) |
| `requirements.txt` | Dependencias Python |

## 📊 Dataset Normalizado

- **270 filas** (10 países × 27 años: 2000–2026)
- **1 sola fila por País por Año**
- **Año en 4 dígitos** (entero, sin letras)
- **19 columnas** con métricas agregadas

## 🗂️ Tabs del Dashboard

1. 📈 Tendencias — evolución temporal
2. 🌍 Geografía — mapa choropleth, ranking
3. 💰 Economía — gasto, ingreso, correlaciones
4. 😊 Satisfacción — KPIs de comportamiento
5. 🗺️ Treemap — jerarquía País→Canal→Categoría
6. 📋 Dataset — tabla interactiva + descarga
