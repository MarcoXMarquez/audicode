#!/usr/bin/env python3
"""
PIA Risk Scorer - Deterministic Privacy Impact Assessment Threshold Evaluator.

Aligned with ISO/IEC 27701:2025 (Control A.1.2.6, Clauses 6.1.2 & 8.2, Control A.2.2.2)
and ISO/IEC 29134:2017 guidelines.

Calculates a deterministic privacy risk score (0-100) based on 10 risk factors,
evaluates autonomous triggers, and emits a conclusive regulatory verdict:
- OBLIGATORIA (Mandatory PIA required prior to processing)
- RECOMENDADA (Recommended PIA / In-depth risk assessment)
- NO_REQUERIDA (PIA not required; document threshold screening)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


CRITERIA_CATALOG: Dict[str, Dict[str, Any]] = {
    "c1_profiling": {
        "id": "C1",
        "name": "Evaluación sistemática, exhaustiva o perfilado",
        "weight": 20,
        "autonomous": False,
        "description": "Profiling, credit scoring, evaluación continua de desempeño laboral o segmentación predictiva.",
        "iso_ref": "ISO/IEC 27701:2025 A.1.2.6 (B.1.2.6)",
    },
    "c2_automated_decisions": {
        "id": "C2",
        "name": "Toma de decisiones automatizadas con efectos jurídicos",
        "weight": 20,
        "autonomous": True,
        "description": "Decisiones algorítmicas sin intervención humana con impacto legal o significativo.",
        "iso_ref": "ISO/IEC 27701:2025 A.1.2.6 (B.1.2.6)",
    },
    "c3_sensitive_data": {
        "id": "C3",
        "name": "Tratamiento a gran escala de datos sensibles / biometría / salud",
        "weight": 20,
        "autonomous": True,
        "description": "Datos de salud, genéticos, biométricos para identificación, opiniones políticas, religión u origen.",
        "iso_ref": "ISO/IEC 27701:2025 A.1.2.6 & A.1.4.2",
    },
    "c4_public_surveillance": {
        "id": "C4",
        "name": "Monitoreo, observación o vigilancia sistemática a gran escala",
        "weight": 20,
        "autonomous": True,
        "description": "CCTV inteligente en zonas de acceso público, telemetría continua o geolocalización en tiempo real.",
        "iso_ref": "ISO/IEC 27701:2025 A.1.2.6 (B.1.2.6)",
    },
    "c5_vulnerable_subjects": {
        "id": "C5",
        "name": "Datos de colectivos vulnerables o en relación asimétrica",
        "weight": 15,
        "autonomous": False,
        "description": "Menores de edad, pacientes, ancianos dependientes o empleados sujetos a asimetría laboral.",
        "iso_ref": "ISO/IEC 27701:2025 A.1.2.6 & Cláusula 6.1.2",
    },
    "c6_emerging_tech_ai": {
        "id": "C6",
        "name": "Uso de tecnologías emergentes, IA o modelos predictivos",
        "weight": 15,
        "autonomous": False,
        "description": "IA generativa con PII, reconocimiento facial, machine learning sobre comportamiento o IoT masivo.",
        "iso_ref": "ISO/IEC 27701:2025 A.1.2.6 & ISO/IEC 42001",
    },
    "c7_data_matching": {
        "id": "C7",
        "name": "Cruce, combinación o correlación de bases de datos",
        "weight": 10,
        "autonomous": False,
        "description": "Cruce de datasets creados con finalidades distintas o enriquecimiento con brokers de datos externos.",
        "iso_ref": "ISO/IEC 27701:2025 A.1.2.6 & A.1.4.2",
    },
    "c8_prevent_rights_service": {
        "id": "C8",
        "name": "Exclusión o impedimento al ejercicio de derechos o servicios básicos",
        "weight": 15,
        "autonomous": True,
        "description": "Tratamientos que restringen o deniegan acceso a servicios financieros, sanitarios o empleo.",
        "iso_ref": "ISO/IEC 27701:2025 A.1.2.6 & Cláusula 6.1.2",
    },
    "c9_large_scale": {
        "id": "C9",
        "name": "Tratamiento masivo de titulares o cobertura territorial amplia",
        "weight": 10,
        "autonomous": False,
        "description": "Alto volumen de titulares (>10k activos), alcance geográfico múltiple o retención de metadatos masiva.",
        "iso_ref": "ISO/IEC 27701:2025 A.1.2.6",
    },
    "c10_cross_border_transfers": {
        "id": "C10",
        "name": "Transferencias internacionales sin decisión de adecuación",
        "weight": 10,
        "autonomous": False,
        "description": "Flujos hacia jurisdicciones de alto riesgo de vigilancia o sin garantías equivalentes.",
        "iso_ref": "ISO/IEC 27701:2025 A.1.5.2 & A.2.2.2",
    },
}


def score_project(answers: Dict[str, bool], project_name: str = "Proyecto Sin Nombre") -> Dict[str, Any]:
    """
    Score a project questionnaire against the 10 ISO 27701 PIA threshold criteria.

    Args:
        answers: Dictionary mapping criterion keys to boolean values.
        project_name: Optional descriptive project name.

    Returns:
        Structured evaluation dictionary with score, verdict, active factors, and recommendations.
    """
    total_score = 0
    active_criteria: List[Dict[str, Any]] = []
    autonomous_triggers: List[Dict[str, Any]] = []

    for key, criterion in CRITERIA_CATALOG.items():
        if answers.get(key, False):
            total_score += criterion["weight"]
            criterion_info = {
                "key": key,
                "id": criterion["id"],
                "name": criterion["name"],
                "weight": criterion["weight"],
                "autonomous": criterion["autonomous"],
                "iso_ref": criterion["iso_ref"],
                "description": criterion["description"],
            }
            active_criteria.append(criterion_info)
            if criterion["autonomous"]:
                autonomous_triggers.append(criterion_info)

    # Cap score at 100
    capped_score = min(total_score, 100)

    # Determine Verdict
    # 1. Mandatory if autonomous trigger is met OR >= 2 criteria OR score >= 30
    if len(autonomous_triggers) > 0 or len(active_criteria) >= 2 or capped_score >= 30:
        verdict = "OBLIGATORIA"
        verdict_reason = (
            f"Se activó {'un criterio autónomo mandatorio' if len(autonomous_triggers) > 0 else f'{len(active_criteria)} criterios de riesgo concurrentes (puntaje: {capped_score}/100)'}."
        )
    elif len(active_criteria) == 1 or capped_score >= 15:
        verdict = "RECOMENDADA"
        verdict_reason = (
            f"Se identificó 1 factor de riesgo no autónomo (puntaje: {capped_score}/100). Se aconseja realizar PIA o análisis de riesgos reforzado."
        )
    else:
        verdict = "NO_REQUERIDA"
        verdict_reason = (
            f"No se activaron factores de riesgo de alto impacto (puntaje: {capped_score}/100). Tratamiento de bajo riesgo residual."
        )

    # Actionable recommendations
    recommendations: List[str] = []
    if verdict == "OBLIGATORIA":
        recommendations.append("Detener o condicionar el despliegue a producción hasta completar y aprobar formalmente la PIA (Control A.1.2.6).")
        recommendations.append("Consultar preceptivamente al Delegado de Protección de Datos (DPO) o Responsable de Privacidad (Cláusula B.3.4).")
        recommendations.append("Elaborar Diagrama de Flujo de Datos (DFD) y matriz de impacto específica en derechos y libertades de titulares (Cláusula 6.1.2).")
        if any(c["key"] == "c10_cross_border_transfers" for c in active_criteria):
            recommendations.append("Exigir al proveedor cláusulas contractuales de asistencia técnica en PIA (Control A.2.2.2).")
        recommendations.append("Evaluar si tras mitigación subsiste un riesgo residual alto que requiera Consulta Previa a la Autoridad de Control.")
    elif verdict == "RECOMENDADA":
        recommendations.append("Ejecutar un análisis de proporcionalidad y necesidad abreviado previo al despliegue.")
        recommendations.append("Documentar y archivar la presente ficha de tamizaje como evidencia para auditorías ISO/IEC 27701 (Cláusula 8.2).")
        recommendations.append("Revisar si el tratamiento involucra a encargados y verificar su compromiso de soporte técnico (A.2.2.2).")
    else:
        recommendations.append("Archivar este registro de tamizaje (screening record) en el repositorio documental del SGIP (Cláusula 8.2).")
        recommendations.append("Reevaluar el tratamiento en caso de modificaciones funcionales, integración de nuevas APIs o cambios normativos.")

    return {
        "project_name": project_name,
        "score": capped_score,
        "raw_score": total_score,
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "active_criteria_count": len(active_criteria),
        "autonomous_triggers_count": len(autonomous_triggers),
        "active_criteria": active_criteria,
        "autonomous_triggers": autonomous_triggers,
        "recommendations": recommendations,
        "normative_references": [
            "ISO/IEC 27701:2025 Control A.1.2.6 (Privacy impact assessment)",
            "ISO/IEC 27701:2025 Cláusula 6.1.2 (Privacy risk assessment)",
            "ISO/IEC 27701:2025 Cláusula 8.2 (Operación de apreciación del riesgo)",
            "ISO/IEC 27701:2025 Control A.2.2.2 (Customer agreement - Assistance in PIA)",
            "ISO/IEC 29134:2017 (Privacy impact assessment methodology)",
        ],
    }


def format_text_report(results: Dict[str, Any]) -> str:
    """Format evaluation results into a clean human-readable audit report."""
    lines: List[str] = [
        "=" * 76,
        "  DICTAMEN DE UMBRAL DE EVALUACIÓN DE IMPACTO EN LA PRIVACIDAD (PIA)",
        "  Conforme a ISO/IEC 27701:2025 (A.1.2.6, Cláusulas 6.1.2 y 8.2, A.2.2.2)",
        "=" * 76,
        f"Proyecto: {results['project_name']}",
        f"Puntaje de Riesgo de Privacidad: {results['score']} / 100",
        f"Criterios Activos: {results['active_criteria_count']} de 10",
        f"Disparadores Autónomos: {results['autonomous_triggers_count']}",
        "",
        f">>> DICTAMEN FINAL: [ {results['verdict']} ] <<<",
        f"Motivo: {results['verdict_reason']}",
        "-" * 76,
        "CRITERIOS DE RIESGO IDENTIFICADOS:",
    ]

    if not results["active_criteria"]:
        lines.append("  (Ningún criterio de alto riesgo identificado)")
    else:
        for c in results["active_criteria"]:
            auton_tag = " [DISPARADOR AUTÓNOMO]" if c["autonomous"] else ""
            lines.append(f"  * [{c['id']}] {c['name']} (+{c['weight']} pts){auton_tag}")
            lines.append(f"    - Detalle: {c['description']}")
            lines.append(f"    - Control: {c['iso_ref']}")

    lines.extend([
        "-" * 76,
        "RECOMENDACIONES OBLIGATORIAS PARA EL PROYECTO:",
    ])
    for idx, rec in enumerate(results["recommendations"], 1):
        lines.append(f"  {idx}. {rec}")

    lines.extend([
        "-" * 76,
        "MARCO NORMATIVO APLICADO:",
    ])
    for ref in results["normative_references"]:
        lines.append(f"  * {ref}")

    lines.append("=" * 76)
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Calificador determinista de necesidad y umbral de PIA bajo ISO/IEC 27701:2025."
    )
    parser.add_argument(
        "--project",
        "-p",
        type=str,
        default="Sistema de Tratamiento Evaluado",
        help="Nombre descriptivo del proyecto o sistema auditado.",
    )
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        help="Ruta a archivo JSON con respuestas a los criterios (claves booleanas c1 a c10).",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Formato de salida del reporte (text por defecto, json para automatizaciones).",
    )

    # Boolean flags for individual criteria
    group = parser.add_argument_group("Criterios de Riesgo Evaluados (Flags individuales)")
    group.add_argument("--c1-profiling", action="store_true", help="C1: Evaluación sistemática o perfiles automatizados.")
    group.add_argument("--c2-decisions", action="store_true", help="C2: Toma de decisiones automatizadas con efectos jurídicos.")
    group.add_argument("--c3-sensitive", action="store_true", help="C3: Tratamiento a gran escala de datos sensibles / biometría.")
    group.add_argument("--c4-surveillance", action="store_true", help="C4: Monitoreo o vigilancia sistemática en zonas públicas.")
    group.add_argument("--c5-vulnerable", action="store_true", help="C5: Datos de menores, pacientes o empleados (asimetría).")
    group.add_argument("--c6-ai-tech", action="store_true", help="C6: Tecnologías emergentes, IA generativa o reconocimiento facial.")
    group.add_argument("--c7-matching", action="store_true", help="C7: Cruce de bases de datos o combinación no esperada.")
    group.add_argument("--c8-rights-denial", action="store_true", help="C8: Tratamiento que impide acceso a servicio básico o derecho.")
    group.add_argument("--c9-large-scale", action="store_true", help="C9: Tratamiento masivo a gran escala (>10k titulares).")
    group.add_argument("--c10-transfers", action="store_true", help="C10: Transferencias internacionales sin adecuación.")

    return parser


def main() -> int:
    """CLI execution entrypoint."""
    parser = build_arg_parser()
    args = parser.parse_args()

    answers: Dict[str, bool] = {}

    if args.file:
        if not args.file.exists():
            print(f"Error: El archivo especificado no existe: {args.file}", file=sys.stderr)
            return 1
        try:
            with open(args.file, "r", encoding="utf-8") as fp:
                file_data = json.load(fp)
            if not isinstance(file_data, dict):
                print("Error: El archivo JSON debe contener un objeto clave-valor.", file=sys.stderr)
                return 1
            # Normalize keys
            for k, v in file_data.items():
                norm_key = k.lower().replace("-", "_")
                if norm_key in CRITERIA_CATALOG:
                    answers[norm_key] = bool(v)
        except Exception as e:
            print(f"Error al leer archivo JSON: {e}", file=sys.stderr)
            return 1
    else:
        # Map arguments to catalog keys
        answers = {
            "c1_profiling": args.c1_profiling,
            "c2_automated_decisions": args.c2_decisions,
            "c3_sensitive_data": args.c3_sensitive,
            "c4_public_surveillance": args.c4_surveillance,
            "c5_vulnerable_subjects": args.c5_vulnerable,
            "c6_emerging_tech_ai": args.c6_ai_tech,
            "c7_data_matching": args.c7_matching,
            "c8_prevent_rights_service": args.c8_rights_denial,
            "c9_large_scale": args.c9_large_scale,
            "c10_cross_border_transfers": args.c10_transfers,
        }

    results = score_project(answers, project_name=args.project)

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_text_report(results))

    return 0


if __name__ == "__main__":
    sys.exit(main())
