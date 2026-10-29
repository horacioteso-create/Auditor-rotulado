import streamlit as st

st.set_page_config(
    page_title="Auditoría de Rótulo de Bebidas - CAA y Ley 27.642",
    page_icon="🧪",
    layout="wide"
)

# Estilos CSS para simular octógonos y rectángulos de advertencia
st.markdown("""
<style>
    .octogono {
        background-color: #000000;
        color: #FFFFFF;
        padding: 12px 18px;
        margin: 8px 0;
        border-radius: 6px;
        font-weight: bold;
        font-size: 15px;
        text-align: center;
        border: 2px solid #ffffff;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.3);
    }
    .rectangulo {
        background-color: #000000;
        color: #FFFFFF;
        padding: 10px 15px;
        margin: 6px 0;
        border-radius: 4px;
        font-weight: bold;
        font-size: 14px;
        text-align: center;
        border: 1px solid #ffffff;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.25);
    }
    .infractor {
        background-color: #ffebe9;
        color: #d9381e;
        padding: 10px 15px;
        border-left: 5px solid #d9381e;
        margin: 6px 0;
        border-radius: 4px;
        font-weight: bold;
    }
    .cumple {
        background-color: #e6f4ea;
        color: #137333;
        padding: 10px 15px;
        border-left: 5px solid #137333;
        margin: 6px 0;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔍 Sistema de Auditoría Regulatoria de Rótulo de Bebidas")
st.subheader("Normativa: Código Alimentario Argentino (CAA) & Ley N° 27.642 (Etiquetado Frontal)")

st.markdown("""
Esta herramienta evalúa automáticamente el perfil de nutrientes, sellos de advertencia frontales, 
leyendas precautorias e infracciones al Código Alimentario Argentino para bebidas analcohólicas.
---
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📋 Datos del Producto")
    
    with st.expander("📌 Módulo 1: Identificación del Producto", expanded=True):
        nombre_comercial = st.text_input("1.1. Nombre Comercial / Marca:", value="Bebida Analcohólica X")
        denominacion = st.text_input("1.2. Denominación Técnica de Venta:", value="Bebida sin alcohol saborizada con 10% jugo")
        porcion_ml = st.number_input("1.3. Volumen de la porción (ml):", min_value=1.0, value=200.0, step=10.0)

    with st.expander("🥗 Módulo 2: Información Nutricional (por 100 ml)", expanded=True):
        vet_100ml = st.number_input("2.1. Valor Energético Total (VET) [kcal/100 ml]:", min_value=0.0, value=32.0, step=1.0)
        azucar_100ml = st.number_input("2.2. Azúcares Añadidos / Libres [g/100 ml]:", min_value=0.0, value=7.5, step=0.1)
        sodio_100ml = st.number_input("2.3. Sodio [mg/100 ml]:", min_value=0.0, value=15.0, step=1.0)
        grasas_100ml = st.number_input("2.4. Grasas Totales [g/100 ml]:", min_value=0.0, value=0.0, step=0.1)
        grasas_sat_100ml = st.number_input("2.5. Grasas Saturadas [g/100 ml]:", min_value=0.0, value=0.0, step=0.1)

    with st.expander("🧪 Módulo 3: Aditivos y Componentes Sensibles", expanded=True):
        edulcorantes = st.radio("3.1. ¿Contiene edulcorantes no nutritivos (Acesulfamo, Sucralosa, Stevia, etc.)?:", ["SI", "NO"], index=0)
        cafeina = st.radio("3.2. ¿Contiene cafeína añadida o por extractos?:", ["SI", "NO"], index=1)
        aspartamo = st.radio("3.3. ¿Contiene Aspartamo (INS 951)?:", ["SI", "NO"], index=1)

with col2:
    st.header("⚖️ Requisitos CAA y Ley 27.642")
    
    with st.expander("🏷️ Módulo 4: Cumplimiento de Rotulado General (Cap. V y XVIII CAA)", expanded=True):
        rne_presente = st.radio("4.1. ¿Figura el número de R.N.E. en el rótulo?:", ["SI", "NO"], index=0)
        rnpa_presente = st.radio("4.2. ¿Figura el número de R.N.P.A. en el rótulo?:", ["SI", "NO"], index=0)
        origen_presente = st.radio("4.3. ¿Declara Razón Social, Domicilio Legal y País de Origen?:", ["SI", "NO"], index=0)
        lote_vto = st.radio("4.4. ¿Están claramente impresos el Lote y Fecha de Vencimiento?:", ["SI", "NO"], index=0)
        ingredientes_orden = st.radio("4.5. ¿Lista de ingredientes en orden decreciente de peso?:", ["SI", "NO"], index=0)
        aditivos_ins = st.radio("4.6. ¿Aditivos declarados con Función + (INS o Nombre)?:", ["SI", "NO"], index=0)
        alergenos = st.radio("4.7. ¿Alérgenos/sustancias sensibles declarados en mayúsculas y negrita?:", ["SI", "NO"], index=0)
        sobrepegado = st.radio("4.8. ¿Hay alguna etiqueta autoadhesiva de descuento TAPANDO la tabla o sellos?:", ["SI", "NO"], index=1)
        claims_presentes = st.radio("4.9. ¿El rótulo o envase presenta dibujos infantiles, personajes o claims nutricionales?:", ["SI", "NO"], index=1)

st.markdown("---")

# EVALUACIÓN LÓGICA DE PERFIL DE NUTRIENTES (LEY 27.642 / OPS)
cal_azucar = azucar_100ml * 4.0
pct_azucar = (cal_azucar / vet_100ml) if vet_100ml > 0 else 0.0

rel_sodio_cal = (sodio_100ml / vet_100ml) if vet_100ml > 0 else 0.0

cal_grasas = grasas_100ml * 9.0
pct_grasas = (cal_grasas / vet_100ml) if vet_100ml > 0 else 0.0

cal_grasas_sat = grasas_sat_100ml * 9.0
pct_grasas_sat = (cal_grasas_sat / vet_100ml) if vet_100ml > 0 else 0.0

sellos_requeridos = []
leyendas_requeridas = []
infracciones_caa = []

# Sellos Octogonales
if pct_azucar >= 0.10:
    sellos_requeridos.append("EXCESO EN AZÚCARES (Azúcares añadidos aportan ≥ 10% del VET)")

if rel_sodio_cal >= 1.0 or sodio_100ml >= 300.0:
    sellos_requeridos.append("EXCESO EN SODIO (Sodio/Kcal ≥ 1.0 mg/kcal o ≥ 300 mg/100ml)")

if pct_grasas >= 0.30:
    sellos_requeridos.append("EXCESO EN GRASAS TOTALES (Grasas totales aportan ≥ 30% del VET)")

if pct_grasas_sat >= 0.10:
    sellos_requeridos.append("EXCESO EN GRASAS SATURADAS (Grasas saturadas aportan ≥ 10% del VET)")

if len(sellos_requeridos) > 0 and vet_100ml >= 25.0:
    sellos_requeridos.append("EXCESO EN CALORÍAS (Presenta sello previo y VET ≥ 25 kcal/100ml)")

# Leyendas Rectangulares
if edulcorantes == "SI":
    leyendas_requeridas.append("CONTIENE EDULCORANTES, NO RECOMENDABLE EN NIÑOS/AS")

if cafeina == "SI":
    leyendas_requeridas.append("CONTIENE CAFEÍNA. EVITAR EN NIÑOS/AS")

if aspartamo == "SI":
    leyendas_requeridas.append("CONTIENE FENILALANINA. CONTRAINDICADO PARA FENILCETONÚRICOS (Art. 1349 CAA)")

# Infracciones CAA y Ley 27.642
if rne_presente == "NO":
    infracciones_caa.append("Falta número de R.N.E. en rótulo (Infracción Art. 220 Cap. V CAA)")
if rnpa_presente == "NO":
    infracciones_caa.append("Falta número de R.N.P.A. en rótulo (Infracción Art. 220 Cap. V CAA)")
if origen_presente == "NO":
    infracciones_caa.append("Falta identificación de Razón Social / Origen (Infracción Cap. V CAA)")
if lote_vto == "NO":
    infracciones_caa.append("Falta lote o fecha de vencimiento clara (Infracción Cap. V CAA)")
if ingredientes_orden == "NO":
    infracciones_caa.append("Lista de ingredientes no está ordenada en forma decreciente")
if aditivos_ins == "NO":
    infracciones_caa.append("Aditivos omiten función o código INS/Nombre (Infracción Cap. XVIII CAA)")
if alergenos == "NO":
    infracciones_caa.append("Alérgenos no están declarados en mayúsculas/negrita (Infracción Art. 235 séptimo)")
if sobrepegado == "SI":
    infracciones_caa.append("CRÍTICA: Etiqueta sobrepegada tapa datos nutricionales o sellos (Infracción Art. 220 CAA, Ley 24.240 y DNU 274/2019)")

tiene_advertencias_frontales = (len(sellos_requeridos) > 0 or len(leyendas_requeridas) > 0)
if tiene_advertencias_frontales and claims_presentes == "SI":
    infracciones_caa.append("CRÍTICA: Producto con sellos/leyendas incluye claims, personajes o avales prohibidos (Infracción Art. 235 quinto CAA y Ley 27.642)")

# =========================================================================
# PRESENTACIÓN DE RESULTADOS / DICTAMEN FINAL
# =========================================================================
st.header("📊 DICTAMEN FINAL DE AUDITORÍA DE RÓTULO")

res_col1, res_col2 = st.columns([1, 1])

with res_col1:
    st.subheader("1. Sellos Octogonales Requeridos (Ley 27.642)")
    if sellos_requeridos:
        st.warning("⚠️ El producto DEBE exhibir obligatoriamente los siguientes sellos negros:")
        for s in sellos_requeridos:
            st.markdown(f'<div class="octogono">🛑 {s}</div>', unsafe_allow_html=True)
    else:
        st.success("✅ El producto NO requiere sellos octogonales de exceso en nutrientes críticos.")

    st.subheader("2. Leyendas Precautorias Rectangulares")
    if leyendas_requeridas:
        st.warning("⚠️ El producto DEBE exhibir obligatoriamente las siguientes leyendas:")
        for l in leyendas_requeridas:
            st.markdown(f'<div class="rectangulo">⚠️ {l}</div>', unsafe_allow_html=True)
    else:
        st.success("✅ El producto NO requiere leyendas precautorias rectangulares.")

with res_col2:
    st.subheader("3. Restricción de Claims y Publicidad (Art. 235 Quinto CAA)")
    if tiene_advertencias_frontales:
        st.error("""
        🚫 **PROHIBICIÓN ABSOLUTA:** Al presentar sellos o leyendas, el producto TIENE PROHIBIDO:
        - Incluir Declaraciones de Propiedades Nutricionales (Claims) tipo 'Rico en...', 'Fuente de...'.
        - Incluir personajes infantiles, dibujos animados, mascotas comerciales o deportistas.
        - Incluir avales de sociedades científicas, médicas o de nutrición.
        """)
    else:
        st.success("🟢 **PERMITIDO:** Al no presentar sellos ni leyendas, puede incluir claims nutricionales autorizados bajo el Art. 235 quinto.")

    st.subheader("4. Infracciones Formales al Código Alimentario (CAA)")
    if infracciones_caa:
        st.error("❌ Se detectaron las siguientes infracciones y errores en el rótulo:")
        for inf in infracciones_caa:
            st.markdown(f'<div class="infractor">• {inf}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="cumple">🎉 CUMPLE TOTALMENTE con los requisitos formales de rotulado del CAA Cap. V y XVIII.</div>', unsafe_allow_html=True)

st.markdown("---")
st.info("""
📌 **Organismos y Autoridades de Control para radicar denuncias o consultas:**
1. **Dirección de Bromatología Municipal** de la jurisdicción de comercialización.
2. **SENASA** (Servicio Nacional de Sanidad y Calidad Agroalimentaria) - Decreto 697/2026.
3. **Dirección de Defensa del Consumidor** (Ventanilla Única Federal - Ley 24.240 y DNU 274/2019).
""")
