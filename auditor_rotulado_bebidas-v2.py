#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
SISTEMA INTERACTIVO DE AUDITORÍA Y VALIDACIÓN DE RÓTULOS DE BEBIDAS ANALCOHÓLICAS
Normativa: Código Alimentario Argentino (CAA) & Ley N° 27.642 (Etiquetado Frontal)
===============================================================================
"""

import sys
import os

def print_header(title):
    print("\n" + "=" * 80)
    print(f" {title.center(78)} ")
    print("=" * 80)

def get_float_input(prompt, default=0.0):
    while True:
        try:
            val_str = input(f"{prompt} [Predeterminado: {default}]: ").strip()
            if not val_str:
                return float(default)
            return float(val_str.replace(",", "."))
        except ValueError:
            print("❌ Entrada inválida. Ingrese un número válido.")

def get_sino_input(prompt, default="NO"):
    while True:
        val_str = input(f"{prompt} (SI/NO) [Predeterminado: {default}]: ").strip().upper()
        if not val_str:
            return default
        if val_str in ["SI", "S", "YES"]:
            return "SI"
        if val_str in ["NO", "N"]:
            return "NO"
        print("❌ Por favor ingrese 'SI' o 'NO'.")

def auditoria_rotulado():
    print_header("AUDITORÍA REGULATORIA DE RÓTULO DE BEBIDAS - CAA Y LEY 27.642")
    print("Este programa permite validar de forma interactiva el etiquetado nutricional,")
    print("sellos frontales, leyendas y cumplimiento del Código Alimentario Argentino.")
    
    print_header("MÓDULO 1: IDENTIFICACIÓN DEL PRODUCTO")
    nombre_comercial = input("1.1. Nombre Comercial / Marca de la bebida: ").strip() or "Bebida Analcohólica X"
    denominacion = input("1.2. Denominación Técnica de Venta (ej. Bebida sin alcohol con 10% jugo): ").strip() or "Bebida sin alcohol saborizada"
    porcion_ml = get_float_input("1.3. Volumen de la porción en ml", 200.0)
    
    print_header("MÓDULO 2: INFORMACIÓN NUTRICIONAL (VALORES POR 100 ML)")
    vet_100ml = get_float_input("2.1. Valor Energético Total (VET) en kcal por 100 ml", 32.0)
    azucar_100ml = get_float_input("2.2. Azúcares Añadidos / Libres en g por 100 ml", 7.5)
    sodio_100ml = get_float_input("2.3. Sodio en mg por 100 ml", 15.0)
    grasas_100ml = get_float_input("2.4. Grasas Totales en g por 100 ml", 0.0)
    grasas_sat_100ml = get_float_input("2.5. Grasas Saturadas en g por 100 ml", 0.0)
    
    print_header("MÓDULO 3: ADITIVOS Y COMPONENTES SENSIBLES")
    edulcorantes = get_sino_input("3.1. ¿Contiene edulcorantes no nutritivos (Acesulfamo, Sucralosa, Stevia, etc.)?", "SI")
    cafeina = get_sino_input("3.2. ¿Contiene cafeína añadida o por extractos?", "NO")
    aspartamo = get_sino_input("3.3. ¿Contiene Aspartamo (INS 951)?", "NO")
    
    print_header("MÓDULO 4: CUMPLIMIENTO DE ROTULADO CAA (CAPÍTULO V Y XVIII)")
    rne_presente = get_sino_input("4.1. ¿Figura el número de R.N.E. en el rótulo?", "SI")
    rnpa_presente = get_sino_input("4.2. ¿Figura el número de R.N.P.A. en el rótulo?", "SI")
    origen_presente = get_sino_input("4.3. ¿Declara Razón Social, Domicilio Legal y País de Origen?", "SI")
    lote_vto = get_sino_input("4.4. ¿Están claramente impresos el Lote y Fecha de Vencimiento?", "SI")
    ingredientes_orden = get_sino_input("4.5. ¿Lista de ingredientes en orden decreciente de peso?", "SI")
    aditivos_ins = get_sino_input("4.6. ¿Aditivos declarados con Función + (INS o Nombre)?", "SI")
    alergenos = get_sino_input("4.7. ¿Alérgenos/sustancias sensibles declarados en mayúsculas y negrita?", "SI")
    sobrepegado = get_sino_input("4.8. ¿Hay alguna etiqueta autoadhesiva de descuento TAPANDO la tabla o sellos?", "NO")
    claims_presentes = get_sino_input("4.9. ¿El rótulo o envase presenta dibujos infantiles, personajes o claims nutricionales?", "NO")

    # =========================================================================
    # EVALUACIÓN LÓGICA DE PERFIL DE NUTRIENTES (LEY 27.642 / OPS)
    # =========================================================================
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
    # IMPRESIÓN DEL INFORME FINAL DE AUDITORÍA
    # =========================================================================
    print_header("DICTAMEN FINAL DE AUDITORÍA DE RÓTULO")
    print(f"📌 Producto Evaluado: {nombre_comercial}")
    print(f"📌 Denominación Técnica: {denominacion}")
    print(f"📌 Porción: {porcion_ml} ml | VET: {vet_100ml} kcal/100ml")
    
    print("\n--- 1. EVALUACIÓN DE SELLOS OCTOGONALES FRONTALES (LEY 27.642) ---")
    if sellos_requeridos:
        print("⚠️ EL PRODUCTO DEBE EXHIBIR OBLIGATORIAMENTE LOS SIGUIENTES SELLOS NEGROS:")
        for s in sellos_requeridos:
            print(f"   [OCTÓGONO]: {s}")
    else:
        print("✅ El producto NO requiere sellos octogonales de exceso en nutrientes críticos.")

    print("\n--- 2. EVALUACIÓN DE LEYENDAS PRECAUTORIAS RECTANGULARES ---")
    if leyendas_requeridas:
        print("⚠️ EL PRODUCTO DEBE EXHIBIR OBLIGATORIAMENTE LAS SIGUIENTES LEYENDAS:")
        for l in leyendas_requeridas:
            print(f"   [RECTÁNGULO]: {l}")
    else:
        print("✅ El producto NO requiere leyendas precautorias rectangulares.")

    print("\n--- 3. RESTRICCIÓN DE CLAIMS Y PUBLICIDAD (ART. 235 QUINTO CAA) ---")
    if tiene_advertencias_frontales:
        print("🚫 PROHIBICIÓN ABSOLUTA: Al presentar sellos o leyendas, el producto TIENE PROHIBIDO:")
        print("   - Incluir Declaraciones de Propiedades Nutricionales (Claims) tipo 'Rico en...', 'Fuente de...'")
        print("   - Incluir personajes infantiles, dibujos animados, mascotas comerciales o deportistas.")
        print("   - Incluir avales de sociedades científicas, médicas o de nutrición.")
    else:
        print("🟢 PERMITIDO: Al no presentar sellos ni leyendas, puede incluir claims nutricionales bajo el Art. 235 quinto.")

    print("\n--- 4. EVALUACIÓN DE INFRACCIONES AL CÓDIGO ALIMENTARIO Y DEFENSA DEL CONSUMIDOR ---")
    if infracciones_caa:
        print("❌ SE DETECTARON LAS SIGUIENTES INFRACCIONES Y ERRORES EN EL RÓTULO:")
        for inf in infracciones_caa:
            print(f"   • {inf}")
    else:
        print("🎉 CUMPLE TOTALMENTE con los requisitos formales de rotulado del CAA Cap. V y XVIII.")

    print("\n--- 5. ORGANISMOS Y AUTORIDADES DE CONTROL PARA RADICAR DENUNCIAS ---")
    print("Si se detectan infracciones (ej. sobrepegados o falta de datos), se puede denunciar ante:")
    print("   1. Dirección de Bromatología Municipal de la jurisdicción del comercio.")
    print("   2. SENASA (Servicio Nacional de Sanidad y Calidad Agroalimentaria) - Decreto 697/2026.")
    print("   3. Dirección de Defensa del Consumidor (Ventanilla Única Federal - Ley 24.240).")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    auditoria_rotulado()
