#!/usr/bin/env python3
"""
Policy Structure Scanner - ISO/IEC 27701:2025
Deterministic verification tool for privacy policies (Clause 5.2, A.3.3)
and privacy notices to data subjects (A.1.3.3, A.1.3.4).

Usage:
    python policy_structure_scanner.py --file <path_to_policy_file> [--type <notice|internal_policy|auto>] [--format <text|json|markdown>]
"""

import sys
import os
import re
import json
import argparse
from typing import Dict, List, Any, Tuple

# Patterns for Privacy Notices (A.1.3.3, A.1.3.4)
NOTICE_REQUIREMENTS = {
    "RESPONSIBLE_IDENTITY": {
        "name": "Identidad y Datos de Contacto del Responsable",
        "iso_control": "A.1.3.3 a)",
        "mandatory": True,
        "keywords": [
            r"responsable (del tratamiento|de los datos)",
            r"identidad del responsable",
            r"razón social",
            r"domicilio social",
            r"datos de contacto",
            r"correo electr[oó]nico de contacto",
            r"cif\b|nif\b|rfc\b|rut\b|nit\b|cnpj\b",
            r"data controller",
            r"identity of the controller",
        ],
    },
    "DPO_CONTACT": {
        "name": "Datos de Contacto del DPO / Delegado de Protección de Datos",
        "iso_control": "A.1.3.3 b)",
        "mandatory": True,
        "keywords": [
            r"delegado de protecci[oó]n de datos",
            r"\bdpo\b",
            r"oficial de privacidad",
            r"privacy officer",
            r"contacto (del )?dpo",
            r"data protection officer",
            r"encargado de privacidad",
        ],
    },
    "PURPOSES": {
        "name": "Finalidades Explícitas y Específicas del Tratamiento",
        "iso_control": "A.1.3.3 c) / A.1.2.2",
        "mandatory": True,
        "keywords": [
            r"finalidad(es)? (del|para el) tratamiento",
            r"para qu[eé] utilizamos (sus|los) datos",
            r"fines del tratamiento",
            r"purposes of (the )?processing",
            r"c[oó]mo usamos su informaci[oó]n",
            r"objetivos del tratamiento",
        ],
    },
    "LAWFUL_BASIS": {
        "name": "Base Jurídica / Licitud del Tratamiento",
        "iso_control": "A.1.3.3 d) / A.1.2.3",
        "mandatory": True,
        "keywords": [
            r"base (legal|jur[ií]dica)",
            r"licitud del tratamiento",
            r"legitimaci[oó]n",
            r"consentimiento",
            r"ejecuci[oó]n de un contrato",
            r"obligaci[oó]n legal",
            r"inter[eé]s leg[ií]timo",
            r"lawful basis",
            r"legal basis",
        ],
    },
    "DATA_CATEGORIES": {
        "name": "Categorías de Datos Personales Recabados",
        "iso_control": "A.1.3.3 e)",
        "mandatory": True,
        "keywords": [
            r"categor[ií]as de datos",
            r"qu[eé] datos recopilamos",
            r"datos que recogemos",
            r"datos identificativos",
            r"datos de contacto",
            r"datos bancarios|financieros",
            r"datos sensibles|categor[ií]as especiales",
            r"categories of personal data",
            r"data collected",
        ],
    },
    "DATA_SOURCES": {
        "name": "Origen y Fuentes de Obtención de Datos",
        "iso_control": "A.1.3.3 f)",
        "mandatory": False,
        "keywords": [
            r"origen de los datos",
            r"fuentes de informaci[oó]n",
            r"obtenidos directamente",
            r"fuentes p[uú]blicas",
            r"terceros proveedores",
            r"source of data",
            r"indirect collection",
        ],
    },
    "CONSEQUENCES_REFUSAL": {
        "name": "Carácter Obligatorio/Facultativo y Consecuencias de Negativa",
        "iso_control": "A.1.3.3 g)",
        "mandatory": True,
        "keywords": [
            r"car[aá]cter (obligatorio|facultativo)",
            r"consecuencia(s)? de no facilitar",
            r"necesarios para la prestaci[oó]n",
            r"consequences of failing to provide",
            r"requisito (contractual|legal)",
        ],
    },
    "RECIPIENTS_THIRD_PARTIES": {
        "name": "Destinatarios o Categorías de Terceros Receptores",
        "iso_control": "A.1.3.3 h)",
        "mandatory": True,
        "keywords": [
            r"destinatarios",
            r"comunicaci[oó]n de datos",
            r"cesi[oó]n a terceros",
            r"proveedores de servicios",
            r"encargados del tratamiento",
            r"recipients of personal data",
            r"third parties",
            r"compartir (sus )?datos",
        ],
    },
    "CROSS_BORDER_TRANSFERS": {
        "name": "Transferencias Internacionales y Salvaguardas",
        "iso_control": "A.1.3.3 i) / A.1.5.2",
        "mandatory": True,
        "keywords": [
            r"transferencias internacionales",
            r"flujos transfronterizos",
            r"fuera del (eee|espacio econ[oó]mico europeo)",
            r"cl[aá]usulas contractuales tipo|cct|scc",
            r"decisi[oó]n de adecuaci[oó]n",
            r"normas corporativas vinculantes|bcr",
            r"international transfers",
            r"cross-border data flows",
        ],
    },
    "RETENTION_PERIODS": {
        "name": "Plazos de Conservación o Criterios Objetivos de Borrado",
        "iso_control": "A.1.3.3 j) / A.1.4.8",
        "mandatory": True,
        "keywords": [
            r"plazo(s)? de conservaci[oó]n",
            r"durante cu[aá]nto tiempo conservamos",
            r"criterios de conservaci[oó]n",
            r"retenci[oó]n de datos",
            r"bloqueo de datos",
            r"periodo de retenci[oó]n",
            r"retention period",
            r"data retention",
        ],
    },
    "PRINCIPAL_RIGHTS": {
        "name": "Derechos de los Titulares (ARCO/DSAR) y Canales de Ejercicio",
        "iso_control": "A.1.3.3 k) / A.1.3.7",
        "mandatory": True,
        "keywords": [
            r"derechos (del interesado|del titular|arco)",
            r"acceso, rectificaci[oó]n, supresi[oó]n",
            r"oposici[oó]n y limitaci[oó]n",
            r"portabilidad de datos",
            r"c[oó]mo ejercer sus derechos",
            r"data subject rights",
            r"right to access|erasure|rectification",
        ],
    },
    "CONSENT_WITHDRAWAL": {
        "name": "Mecanismo para Revocar el Consentimiento",
        "iso_control": "A.1.3.3 l) / A.1.3.5",
        "mandatory": True,
        "keywords": [
            r"revocar (el )?consentimiento",
            r"retirar el consentimiento",
            r"retirada del consentimiento",
            r"withdraw (your )?consent",
            r"revocaci[oó]n de autorizaci[oó]n",
            r"dar(se)? de baja",
        ],
    },
    "AUTOMATED_DECISIONS": {
        "name": "Decisiones Automatizadas y Elaboración de Perfiles",
        "iso_control": "A.1.3.3 m) / A.1.3.11",
        "mandatory": True,
        "keywords": [
            r"decisiones automatizadas",
            r"elaboraci[oó]n de perfiles",
            r"profiling",
            r"algoritmo(s)?",
            r"l[oó]gica aplicada",
            r"automated decision-making",
        ],
    },
    "COMPLAINT_AUTHORITY": {
        "name": "Derecho a Reclamar ante la Autoridad de Control",
        "iso_control": "A.1.3.3 n)",
        "mandatory": True,
        "keywords": [
            r"autoridad de control",
            r"agencia (espa[nñ]ola )?de protecci[oó]n de datos|aepd",
            r"reclamaci[oó]n ante",
            r"supervisory authority",
            r"presentar una reclamaci[oó]n",
            r"inai\b|anpd\b|sic\b|ico\b",
        ],
    },
}

# Patterns for Internal Governance Policies (Clause 5.2, A.3.3)
INTERNAL_POLICY_REQUIREMENTS = {
    "ORGANIZATIONAL_PURPOSE": {
        "name": "Alineación con el Propósito y Contexto de la Organización",
        "iso_control": "Cláusula 5.2 a)",
        "mandatory": True,
        "keywords": [
            r"prop[oó]sito de la organizaci[oó]n",
            r"contexto de la entidad",
            r"alcance del sgip",
            r"alcance del pims",
            r"modelo de negocio",
            r"organizational context",
            r"scope of the pims",
        ],
    },
    "OBJECTIVES_FRAMEWORK": {
        "name": "Marco de Referencia para Objetivos de Privacidad",
        "iso_control": "Cláusula 5.2 b) / Cláusula 6.2",
        "mandatory": True,
        "keywords": [
            r"objetivos de privacidad",
            r"marco para (el establecimiento de )?objetivos",
            r"metas de privacidad",
            r"indicadores de desempe[nñ]o",
            r"privacy objectives framework",
        ],
    },
    "LEGAL_COMPLIANCE_COMMITMENT": {
        "name": "Compromiso Expreso de Cumplimiento Legal y Contractual",
        "iso_control": "Cláusula 5.2 c)",
        "mandatory": True,
        "keywords": [
            r"compromiso de cumplir",
            r"requisitos legales aplicables",
            r"cumplimiento normativo",
            r"legislaci[oó]n de protecci[oó]n de datos",
            r"commitment to satisfy applicable requirements",
            r"legal and regulatory compliance",
        ],
    },
    "CONTINUAL_IMPROVEMENT": {
        "name": "Compromiso de Mejora Continua del PIMS / SGIP",
        "iso_control": "Cláusula 5.2 d) / Cláusula 10.2",
        "mandatory": True,
        "keywords": [
            r"mejora continua",
            r"continual improvement",
            r"eficacia del sgip",
            r"eficacia del pims",
            r"revisi[oó]n peri[oó]dica",
        ],
    },
    "DOCUMENTED_INFORMATION": {
        "name": "Información Documentada y Control de Aprobación",
        "iso_control": "Cláusula 5.2 / Cláusula 7.5",
        "mandatory": True,
        "keywords": [
            r"aprobaci[oó]n (de la|por la) alta direcci[oó]n",
            r"aprobado por",
            r"versi[oó]n|control de versiones",
            r"c[oó]digo de documento",
            r"fecha de vigencia|fecha de aprobaci[oó]n",
            r"approved by top management",
            r"document version",
        ],
    },
    "COMMUNICATION_AWARENESS": {
        "name": "Comunicación y Comprensión Interna",
        "iso_control": "Cláusula 5.2 / Cláusula 7.3",
        "mandatory": True,
        "keywords": [
            r"comunicada dentro de la organizaci[oó]n",
            r"difusi[oó]n interna",
            r"sensibilizaci[oó]n|concienciaci[oó]n",
            r"capacitaci[oó]n del personal",
            r"communicated within the organization",
            r"employee awareness",
        ],
    },
    "STAKEHOLDER_AVAILABILITY": {
        "name": "Disponibilidad para Partes Interesadas Pertinentes",
        "iso_control": "Cláusula 5.2",
        "mandatory": True,
        "keywords": [
            r"partes interesadas",
            r"disponible para (las )?partes interesadas",
            r"available to relevant interested parties",
            r"publicaci[oó]n accesible",
        ],
    },
    "SECURITY_INTEGRATION": {
        "name": "Políticas Temáticas de Seguridad Integradas con PII",
        "iso_control": "Control A.3.3",
        "mandatory": True,
        "keywords": [
            r"control de accesos a pii",
            r"cifrado de datos personales",
            r"pol[ií]tica de retenci[oó]n y destrucci[oó]n",
            r"copias de seguridad de pii",
            r"gesti[oó]n de incidentes de seguridad",
            r"information security policies for pii",
            r"segregaci[oó]n de funciones",
        ],
    },
}


def analyze_text_against_rules(text: str, rules: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    text_lower = text.lower()
    results = {}
    found_count = 0
    mandatory_count = 0
    mandatory_found = 0

    for req_key, req_data in rules.items():
        is_mandatory = req_data.get("mandatory", True)
        if is_mandatory:
            mandatory_count += 1

        matches = []
        for kw in req_data["keywords"]:
            if re.search(kw, text_lower, re.IGNORECASE):
                matches.append(kw)

        status = "PRESENT" if len(matches) >= 2 else ("PARTIAL" if len(matches) == 1 else "MISSING")
        if status in ("PRESENT", "PARTIAL"):
            found_count += 1
            if is_mandatory:
                mandatory_found += 1

        results[req_key] = {
            "name": req_data["name"],
            "iso_control": req_data["iso_control"],
            "mandatory": is_mandatory,
            "status": status,
            "matched_patterns": len(matches),
            "sample_match": matches[0] if matches else None,
        }

    total_reqs = len(rules)
    coverage_pct = round((found_count / total_reqs) * 100, 2) if total_reqs > 0 else 0.0
    mandatory_pct = round((mandatory_found / mandatory_count) * 100, 2) if mandatory_count > 0 else 0.0

    return {
        "total_requirements": total_reqs,
        "found_requirements": found_count,
        "mandatory_total": mandatory_count,
        "mandatory_found": mandatory_found,
        "coverage_percentage": coverage_pct,
        "mandatory_percentage": mandatory_pct,
        "details": results,
    }


def compute_readability_metrics(text: str) -> Dict[str, Any]:
    words = re.findall(r"\b\w+\b", text)
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    word_count = len(words)
    sentence_count = len(sentences) if sentences else 1
    paragraph_count = len(paragraphs) if paragraphs else 1

    avg_sentence_len = round(word_count / sentence_count, 1) if sentence_count > 0 else 0
    avg_paragraph_len = round(word_count / paragraph_count, 1) if paragraph_count > 0 else 0

    # Layered structure hints
    has_summary_table = bool(re.search(r"(\|.*\|.*\n\|[-:\s|]+\n\|.*\|)", text))
    has_layered_headers = bool(re.search(r"(resumen|primera capa|capa b[aá]sica|informaci[oó]n b[aá]sica)", text, re.IGNORECASE))
    has_bullets = bool(re.search(r"(^\s*[-*+]\s+)", text, re.MULTILINE))

    readability_eval = "ALTA"
    if avg_sentence_len > 35 or avg_paragraph_len > 180:
        readability_eval = "BAJA (Oraciones o párrafos excesivamente largos; riesgo de opacidad)"
    elif avg_sentence_len > 25:
        readability_eval = "MEDIA (Requiere simplificación o estructuración adicional)"

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "avg_words_per_sentence": avg_sentence_len,
        "avg_words_per_paragraph": avg_paragraph_len,
        "has_summary_table": has_summary_table,
        "has_layered_headers": has_layered_headers,
        "has_bullet_lists": has_bullets,
        "readability_assessment": readability_eval,
    }


def detect_document_type(text: str) -> str:
    text_lower = text.lower()
    notice_hits = len(re.findall(r"(aviso de privacidad|privacy notice|titular|interesado|derechos arco|cookies)", text_lower))
    internal_hits = len(re.findall(r"(pol[ií]tica interna|sgip|pims|alta direcci[oó]n|revisi[oó]n por la direcci[oó]n|objetivos de privacidad)", text_lower))

    if notice_hits >= internal_hits:
        return "notice"
    return "internal_policy"


def scan_policy(file_path: str, doc_type: str = "auto") -> Dict[str, Any]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo '{file_path}' no existe.")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    detected_type = doc_type
    if doc_type == "auto":
        detected_type = detect_document_type(content)

    rules = NOTICE_REQUIREMENTS if detected_type == "notice" else INTERNAL_POLICY_REQUIREMENTS
    analysis = analyze_text_against_rules(content, rules)
    metrics = compute_readability_metrics(content)

    # Classify critical missing items
    critical_missing = []
    for req_k, d in analysis["details"].items():
        if d["mandatory"] and d["status"] == "MISSING":
            critical_missing.append(f"[{d['iso_control']}] {d['name']}")

    return {
        "file_path": file_path,
        "document_type_evaluated": detected_type,
        "analysis": analysis,
        "readability": metrics,
        "critical_missing": critical_missing,
    }


def format_text_report(scan_res: Dict[str, Any]) -> str:
    lines = []
    lines.append("=" * 78)
    lines.append(" INFORME DE ESCANEO ESTRUCTURAL - ISO/IEC 27701:2025")
    lines.append("=" * 78)
    lines.append(f"Archivo analizado: {scan_res['file_path']}")
    lines.append(f"Tipo documental evaluado: {scan_res['document_type_evaluated'].upper()}")
    a = scan_res["analysis"]
    lines.append(f"Cobertura Global: {a['coverage_percentage']}% ({a['found_requirements']}/{a['total_requirements']} requisitos)")
    lines.append(f"Cobertura Mandatoria: {a['mandatory_percentage']}% ({a['mandatory_found']}/{a['mandatory_total']} mandatorios)")
    lines.append("-" * 78)
    lines.append(f"{'CONTROL':<16} | {'ESTADO':<8} | {'REQUISITO NORMATIVO':<48}")
    lines.append("-" * 78)

    for k, v in a["details"].items():
        status_color = v["status"]
        lines.append(f"{v['iso_control']:<16} | {status_color:<8} | {v['name'][:48]:<48}")

    lines.append("-" * 78)
    r = scan_res["readability"]
    lines.append("MÉTRICAS DE LEGIBILIDAD Y ESTRUCTURA (A.1.3.4):")
    lines.append(f" - Palabras totales: {r['word_count']} | Oraciones: {r['sentence_count']} | Párrafos: {r['paragraph_count']}")
    lines.append(f" - Promedio palabras/oración: {r['avg_words_per_sentence']} (recomendado: < 25)")
    lines.append(f" - Presenta tabla resumen: {'SÍ' if r['has_summary_table'] else 'NO'}")
    lines.append(f" - Detecta capas de información: {'SÍ' if r['has_layered_headers'] else 'NO'}")
    lines.append(f" - Evaluación preliminar de legibilidad: {r['readability_assessment']}")
    lines.append("-" * 78)

    if scan_res["critical_missing"]:
        lines.append("ALERTA: REQUISITOS MANDATORIOS FALTANTES (SEVERIDAD CRÍTICA/MAYOR):")
        for item in scan_res["critical_missing"]:
            lines.append(f"  [!] {item}")
    else:
        lines.append("[OK] Todos los elementos mandatorios clave tienen presencia detectada.")

    lines.append("=" * 78)
    return "\n".join(lines)


def format_markdown_report(scan_res: Dict[str, Any]) -> str:
    lines = []
    lines.append("# Resultado de Escaneo Estructural - ISO/IEC 27701:2025")
    lines.append("")
    lines.append(f"- **Archivo**: `{scan_res['file_path']}`")
    lines.append(f"- **Tipo de documento**: `{scan_res['document_type_evaluated']}`")
    a = scan_res["analysis"]
    lines.append(f"- **Cobertura Global**: `{a['coverage_percentage']}%` ({a['found_requirements']}/{a['total_requirements']})")
    lines.append(f"- **Cobertura Mandatoria**: `{a['mandatory_percentage']}%` ({a['mandatory_found']}/{a['mandatory_total']})")
    lines.append("")
    lines.append("### Desglose de Controles")
    lines.append("")
    lines.append("| Control ISO | Estado | Requisito Mandatorio |")
    lines.append("|---|---|---|")
    for k, v in a["details"].items():
        lines.append(f"| {v['iso_control']} | **{v['status']}** | {v['name']} |")
    lines.append("")
    lines.append("### Métricas de Legibilidad y Transparencia")
    lines.append("")
    r = scan_res["readability"]
    lines.append(f"- **Palabras totales**: {r['word_count']}")
    lines.append(f"- **Promedio de palabras por oración**: {r['avg_words_per_sentence']}")
    lines.append(f"- **Estructura por capas identificada**: {'Sí' if r['has_layered_headers'] else 'No'}")
    lines.append(f"- **Tabla sinóptica de resumen**: {'Sí' if r['has_summary_table'] else 'No'}")
    lines.append(f"- **Evaluación sintética**: {r['readability_assessment']}")
    lines.append("")
    if scan_res["critical_missing"]:
        lines.append("### Omisiones Críticas Detectadas")
        for item in scan_res["critical_missing"]:
            lines.append(f"- :warning: **{item}**")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Escáner determinista de estructura de políticas y avisos de privacidad (ISO/IEC 27701:2025)."
    )
    parser.add_argument("--file", required=True, help="Ruta al archivo de texto o markdown a analizar.")
    parser.add_argument(
        "--type",
        choices=["notice", "internal_policy", "auto"],
        default="auto",
        help="Tipo de documento a evaluar: 'notice' (aviso a titulares A.1.3.3), 'internal_policy' (política interna Cl. 5.2/A.3.3) o 'auto' (detección automática).",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "markdown"],
        default="text",
        help="Formato de salida del reporte.",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.0,
        help="Umbral mínimo de porcentaje de cobertura para retornar código de salida 0.",
    )

    args = parser.parse_args()

    try:
        scan_res = scan_policy(args.file, doc_type=args.type)
    except Exception as e:
        sys.stderr.write(f"Error al analizar el archivo: {e}\n")
        sys.exit(2)

    if args.format == "json":
        print(json.dumps(scan_res, indent=2, ensure_ascii=False))
    elif args.format == "markdown":
        print(format_markdown_report(scan_res))
    else:
        print(format_text_report(scan_res))

    if args.min_score > 0 and scan_res["analysis"]["mandatory_percentage"] < args.min_score:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
