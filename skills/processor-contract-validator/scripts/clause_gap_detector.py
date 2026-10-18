#!/usr/bin/env python3
"""Clause Gap Detector - Deterministic DPA and Processor Contract Compliance Auditor.

This script parses and analyzes contract text or Data Processing Agreements (DPAs)
against mandatory privacy controls in ISO/IEC 27701:2025 (A.1.2.7, A.1.2.8,
Table A.2, A.2.5.7-9, A.3.10) and GDPR Article 28.

It deterministically identifies:
1. Presence and quality of mandatory privacy clauses.
2. Missing or deficient contractual stipulations.
3. Common contractual red flags (e.g. self-assigned AI training rights,
   audit prohibitions, passive subprocessor notices).
4. An overall contractual compliance score (0-100%).

Usage:
  python clause_gap_detector.py --file path/to/contract.txt [--json] [--report]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


MANDATORY_CRITERIA: Dict[str, Dict[str, Any]] = {
    "purpose_scope": {
        "title": "Objeto, Naturaleza, Duración y Finalidad",
        "iso_control": "A.1.2.7 / A.2.2.3",
        "gdpr_ref": "Art. 28.3",
        "weight": 8,
        "keywords": [
            r"objeto\s+del\s+tratamiento",
            r"naturaleza\s+y\s+finalidad",
            r"duración\s+del\s+tratamiento",
            r"finalidad(es)?\s+específica(s)?",
            r"scope\s+of\s+processing",
            r"nature\s+and\s+purpose",
            r"duration\s+of\s+processing",
            r"categories\s+of\s+data",
            r"categorías\s+de\s+datos",
        ],
        "description": "Especificación del objeto, naturaleza técnica, duración, tipos de PII y categorías de titulares.",
    },
    "documented_instructions": {
        "title": "Sujeción Estricta a Instrucciones Documentadas y No Uso Propio",
        "iso_control": "A.1.2.7 / A.2.2.3",
        "gdpr_ref": "Art. 28.3(a)",
        "weight": 12,
        "keywords": [
            r"instrucciones\s+documentadas",
            r"únicamente\s+siguiendo\s+instrucciones",
            r"instrucciones\s+del\s+responsable",
            r"documented\s+instructions",
            r"only\s+on\s+instructions",
            r"process\s+solely\s+on",
            r"prohibición\s+de\s+uso\s+propio",
            r"no\s+tratará\s+para\s+fines\s+propios",
        ],
        "description": "Obligación del encargado de tratar PII exclusivamente bajo directrices documentadas del cliente.",
    },
    "confidentiality": {
        "title": "Deber de Confidencialidad y Compromiso del Personal",
        "iso_control": "A.1.2.7 / A.3.10",
        "gdpr_ref": "Art. 28.3(b)",
        "weight": 10,
        "keywords": [
            r"confidencialidad",
            r"deber\s+de\s+secreto",
            r"personal\s+autorizado.*compromiso\s+de\s+confidencialidad",
            r"obligación\s+legal\s+de\s+secreto",
            r"confidentiality\s+commitment",
            r"duty\s+of\s+confidentiality",
            r"authorized\s+personnel.*confidential",
            r"statutory\s+obligation\s+of\s+secrecy",
        ],
        "description": "Compromiso expreso y vinculante de confidencialidad del personal con acceso a PII.",
    },
    "security_measures": {
        "title": "Medidas Técnicas y Organizativas de Seguridad",
        "iso_control": "A.1.2.7 / A.3.10",
        "gdpr_ref": "Art. 28.3(c) / Art. 32",
        "weight": 12,
        "keywords": [
            r"medidas\s+técnicas\s+y\s+organizativas",
            r"seguridad\s+del\s+tratamiento",
            r"cifrado\s+en\s+tránsito|cifrado\s+en\s+reposo|cifrado",
            r"autenticación\s+multifactor|mfa",
            r"copias\s+de\s+seguridad|resiliencia",
            r"technical\s+and\s+organizational\s+measures",
            r"security\s+measures",
            r"encryption\s+at\s+rest|in\s+transit",
            r"tabla\s+a\.3|iso\s*27001",
        ],
        "description": "Implementación obligatoria de salvaguardas de seguridad (cifrado, control de acceso, resiliencia).",
    },
    "subprocessor_authorization": {
        "title": "Régimen de Subcontratación y Autorización Previa",
        "iso_control": "A.2.5.7 / A.2.5.8",
        "gdpr_ref": "Art. 28.2 / Art. 28.4",
        "weight": 10,
        "keywords": [
            r"subencargad(o|os)|subcontratista(s)?|subprocesador(es)?",
            r"autorización\s+previa\s+por\s+escrito",
            r"autorización\s+general\s+por\s+escrito",
            r"prior\s+written\s+authorization",
            r"sub-?processor(s)?",
            r"subcontractor(s)?",
            r"traslado\s+de\s+obligaciones|cláusula\s+espejo|flow-?down",
            r"same\s+obligations",
        ],
        "description": "Prohibición de subcontratar sin autorización previa y traslado contractual vinculante (flow-down).",
    },
    "subprocessor_objection": {
        "title": "Gestión de Cambios de Subencargados y Derecho de Oposición",
        "iso_control": "A.2.5.9",
        "gdpr_ref": "Art. 28.2 / Art. 28.4",
        "weight": 8,
        "keywords": [
            r"notificará\s+con\s+antelación",
            r"incorporación\s+o\s+sustitución\s+de\s+subencargados",
            r"derecho\s+a\s+oponerse|derecho\s+de\s+oposición",
            r"rescindir\s+el\s+contrato|resolver\s+el\s+acuerdo",
            r"notice\s+of\s+changes|prior\s+notice",
            r"right\s+to\s+object|object\s+to\s+such\s+changes",
            r"terminate\s+the\s+agreement",
            r"días\s+(naturales|hábiles)\s+de\s+antelación|days\s+prior\s+notice",
        ],
        "description": "Preaviso formal de sustitución de subencargados y derecho de veto u oposición del cliente.",
    },
    "rights_assistance": {
        "title": "Asistencia en el Ejercicio de Derechos de Titulares",
        "iso_control": "A.1.2.7 / A.2.3.2",
        "gdpr_ref": "Art. 28.3(e)",
        "weight": 8,
        "keywords": [
            r"asistencia\s+al\s+responsable.*derechos",
            r"solicitudes\s+de\s+los\s+titulares|derechos\s+arco|dsar",
            r"acceso,\s+rectificación,\s+supresión|portabilidad|oposición",
            r"assist\s+the\s+controller.*data\s+subject",
            r"rights\s+of\s+data\s+subjects",
            r"access,\s+rectification,\s+erasure",
        ],
        "description": "Compromiso de asistir técnicamente al responsable para desahogar solicitudes ARCO/DSAR.",
    },
    "pia_assistance": {
        "title": "Asistencia en Evaluaciones de Impacto (PIA) y Consultas",
        "iso_control": "A.1.2.7 / A.2.2.2",
        "gdpr_ref": "Art. 28.3(f)",
        "weight": 6,
        "keywords": [
            r"evaluación\s+de\s+impacto|evaluaciones\s+de\s+impacto",
            r"privacy\s+impact\s+assessment|pia|dpia",
            r"consulta\s+previa|prior\s+consultation",
            r"asistirá\s+al\s+responsable.*evaluación\s+de\s+impacto",
            r"assist\s+with\s+data\s+protection\s+impact\s+assessments",
        ],
        "description": "Facilitar información técnica y arquitectónica para la elaboración de PIAs y consultas previas.",
    },
    "breach_notification": {
        "title": "Notificación Inmediata de Brechas de Seguridad",
        "iso_control": "A.1.2.7 / B.2.2.2 / B.3.12",
        "gdpr_ref": "Art. 28.3(f) / Art. 33.2",
        "weight": 12,
        "keywords": [
            r"notificación\s+de\s+brecha(s)?|violación\s+de\s+seguridad",
            r"notificará\s+sin\s+dilación|notificará\s+inmediatamente",
            r"24\s+horas|48\s+horas|72\s+horas",
            r"data\s+breach\s+notification|security\s+incident",
            r"without\s+undue\s+delay|promptly\s+notify",
            r"notify\s+the\s+controller\s+after\s+becoming\s+aware",
        ],
        "description": "Notificación inmediata por escrito al responsable tras conocer una brecha de datos con plazo perentorio.",
    },
    "data_disposal": {
        "title": "Destino Final de la PII (Devolución o Destrucción Segura)",
        "iso_control": "A.1.2.7 / A.2.4.3",
        "gdpr_ref": "Art. 28.3(g)",
        "weight": 10,
        "keywords": [
            r"devolución\s+o\s+destrucción",
            r"suprimir\s+o\s+devolver",
            r"certificado\s+de\s+destrucción|borrado\s+seguro",
            r"a\s+elección\s+del\s+responsable",
            r"return\s+or\s+delete",
            r"delete\s+or\s+return",
            r"at\s+the\s+choice\s+of\s+the\s+controller",
            r"secure\s+destruction|certificate\s+of\s+destruction",
        ],
        "description": "Obligación de devolver o destruir irreversiblemente la PII al finalizar la relación contractual.",
    },
    "audit_inspection": {
        "title": "Derecho de Auditoría, Inspección y Demostración de Cumplimiento",
        "iso_control": "A.1.2.7 / A.2.2.6",
        "gdpr_ref": "Art. 28.3(h)",
        "weight": 10,
        "keywords": [
            r"derecho\s+de\s+auditoría|permitirá\s+auditorías",
            r"auditorías\s+e\s+inspecciones",
            r"auditor\s+independiente",
            r"demostrar\s+el\s+cumplimiento",
            r"right\s+to\s+audit|permit\s+and\s+contribute\s+to\s+audits",
            r"audits\s+and\s+inspections",
            r"independent\s+auditor",
            r"demonstrate\s+compliance",
        ],
        "description": "Facultad de realizar inspecciones y auditorías directamente o mediante auditor externo acreditado.",
    },
}

RED_FLAGS_CRITERIA: List[Dict[str, Any]] = [
    {
        "id": "ai_training_self_use",
        "title": "Uso de Datos para Entrenamiento de IA / Fines Propios",
        "severity": "Crítica",
        "regex": r"(podrá|facultad\s+de|autoriza(do)?\s+a|se\s+reserva\s+el\s+derecho|may\s+use|right\s+to|entitled\s+to)[^.;\n]{0,80}(entrenar\s+(modelos|algoritmos|ia|inteligencia)|train(ing)?\s+(models|algorithms|ai)|fines\s+propios|own\s+commercial\s+purposes|desarrollar\s+nuevos\s+productos)",
        "issue": "El proveedor se arroga la facultad de explotar datos del cliente para enriquecimiento algorítmico, entrenamiento de modelos o propósitos propios sin mandato legal.",
        "recommendation": "Exigir prohibición expresa de uso secundario e incorporación de cláusula de prohibición total de minería y entrenamiento de IA sobre PII.",
    },
    {
        "id": "audit_prohibition_or_exorbitant_fees",
        "title": "Prohibición o Restricción Abusiva del Derecho de Auditoría",
        "severity": "Crítica",
        "regex": r"(no\s+se\s+(admiten|permiten|autorizan)\s+auditorías\s+in\s+situ|no\s+(on-?site\s+audits|physical\s+inspections)\s+allowed|tarifa\s+de\s+auditoría.*(\$|\bUSD\b|\bEUR\b)|audit\s+fee.*(\$|\bUSD\b|\bEUR\b))",
        "issue": "El contrato suprime de facto la facultad inspectora del responsable o impone costes exorbitantes como barrera disuasoria.",
        "recommendation": "Sustituir por cláusula que garantice auditorías anuales ordinarias sin coste adicional y con preaviso razonable (10 días).",
    },
    {
        "id": "passive_subprocessor_update",
        "title": "Notificación Pasiva de Subencargados sin Derecho Efectivo de Oposición",
        "severity": "Mayor",
        "regex": r"(actualizará\s+la\s+lista\s+en\s+el\s+sitio\s+web\s+sin\s+previo\s+aviso|update\s+the\s+list\s+on\s+(its\s+)?website\s+without\s+prior\s+notice|deberá\s+consultar\s+periódicamente\s+la\s+web|check\s+(our\s+)?website\s+periodically|aceptación\s+tácita\s+del\s+subcontratista|continued\s+use\s+constitutes\s+acceptance)",
        "issue": "El proveedor transfiere la carga de revisión a la web sin notificación activa individual, violando el control A.2.5.9.",
        "recommendation": "Obligar a notificación por correo electrónico con al menos 30 días de antelación y derecho expreso de rescisión sin penalización.",
    },
    {
        "id": "indefinite_breach_timeline",
        "title": "Plazo Indefinido o Discrecional de Notificación de Brechas",
        "severity": "Crítica",
        "regex": r"(tiempo\s+comercialmente\s+razonable\s+a\s+entera\s+discreción|commercially\s+reasonable\s+time\s+at\s+its\s+sole\s+discretion|una\s+vez\s+que\s+haya\s+concluido\s+de\s+forma\s+definitiva\s+la\s+investigación|after\s+investigation\s+is\s+fully\s+completed)",
        "issue": "Subordina el aviso a plazos subjetivos del proveedor, poniendo en riesgo el cumplimiento del plazo fatal de 72 horas.",
        "recommendation": "Fijar un plazo perentorio de notificación por escrito no superior a 24-48 horas tras tener conocimiento o sospecha fundada.",
    },
    {
        "id": "indefinite_backup_retention",
        "title": "Retención Indefinida de PII tras Rescisión",
        "severity": "Mayor",
        "regex": r"(conservará\s+copias\s+de\s+respaldo\s+por\s+tiempo\s+indefinido|retain\s+backup\s+copies\s+indefinitely|no\s+se\s+destruirán\s+las\s+copias\s+de\s+seguridad|will\s+not\s+delete\s+backups)",
        "issue": "El proveedor se niega a purgar o desidentificar las copias de seguridad a la extinción del contrato, violando A.2.4.3.",
        "recommendation": "Exigir ciclo de vida de backup definido (máximo 30 días) y certificado de destrucción segura según NIST SP 800-88.",
    },
]


class ContractAuditResult:
    """Encapsulates the audit findings for a DPA/contract text."""

    def __init__(self, filename: str, text: str) -> None:
        self.filename = filename
        self.text = text
        self.total_words = len(text.split())
        self.clauses_analysis: Dict[str, Dict[str, Any]] = {}
        self.red_flags_detected: List[Dict[str, Any]] = []
        self.overall_score: int = 0
        self.compliance_level: str = "NO CONFORME"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.filename,
            "word_count": self.total_words,
            "overall_score": self.overall_score,
            "compliance_level": self.compliance_level,
            "clauses_evaluated": len(self.clauses_analysis),
            "clauses_compliant": sum(1 for c in self.clauses_analysis.values() if c["status"] == "CONFORME"),
            "clauses_partial": sum(1 for c in self.clauses_analysis.values() if c["status"] == "PARCIAL"),
            "clauses_missing": sum(1 for c in self.clauses_analysis.values() if c["status"] == "AUSENTE"),
            "red_flags_count": len(self.red_flags_detected),
            "clauses_details": self.clauses_analysis,
            "red_flags": self.red_flags_detected,
        }


def analyze_contract_text(text: str, filename: str = "contract") -> ContractAuditResult:
    """Analyze contract text against mandatory privacy controls deterministically."""
    result = ContractAuditResult(filename, text)
    clean_text = text.lower()

    total_weight = sum(info["weight"] for info in MANDATORY_CRITERIA.values())
    accumulated_score = 0.0

    # 1. Audit mandatory clauses
    for key, info in MANDATORY_CRITERIA.items():
        matches = []
        for pattern in info["keywords"]:
            found = re.findall(pattern, clean_text, re.IGNORECASE)
            if found:
                matches.append(pattern)

        match_ratio = len(matches) / len(info["keywords"])

        if match_ratio >= 0.35 or len(matches) >= 2:
            status = "CONFORME"
            score_earned = info["weight"]
            evidence = f"Detectados {len(matches)} indicadores de concordancia normativa."
        elif len(matches) == 1:
            status = "PARCIAL"
            score_earned = info["weight"] * 0.45
            evidence = "Mención superficial o incompleta; carece de garantías operativas robustas."
        else:
            status = "AUSENTE"
            score_earned = 0.0
            evidence = "No se encontraron estipulaciones correspondientes a este control."

        accumulated_score += score_earned

        result.clauses_analysis[key] = {
            "title": info["title"],
            "iso_control": info["iso_control"],
            "gdpr_ref": info["gdpr_ref"],
            "weight": info["weight"],
            "status": status,
            "matches_count": len(matches),
            "evidence": evidence,
            "description": info["description"],
        }

    # 2. Audit Red Flags
    for rf in RED_FLAGS_CRITERIA:
        match = re.search(rf["regex"], clean_text, re.IGNORECASE)
        if match:
            # Extract surrounding snippet
            start = max(0, match.start() - 60)
            end = min(len(text), match.end() + 60)
            snippet = text[start:end].replace("\n", " ").strip()

            result.red_flags_detected.append({
                "id": rf["id"],
                "title": rf["title"],
                "severity": rf["severity"],
                "matched_snippet": f"...{snippet}...",
                "issue": rf["issue"],
                "recommendation": rf["recommendation"],
            })
            # Penalize overall score for critical red flags
            if rf["severity"] == "Crítica":
                accumulated_score = max(0.0, accumulated_score - 15)
            elif rf["severity"] == "Mayor":
                accumulated_score = max(0.0, accumulated_score - 8)

    # Normalize final score (0-100)
    final_score = int(round((accumulated_score / total_weight) * 100))
    result.overall_score = max(0, min(100, final_score))

    if result.overall_score >= 85 and not any(r["severity"] == "Crítica" for r in result.red_flags_detected):
        result.compliance_level = "CONFORME (APROBADO)"
    elif result.overall_score >= 60:
        result.compliance_level = "PARCIALMENTE CONFORME (REQUIERE ENMIENDA)"
    else:
        result.compliance_level = "NO CONFORME (RIESGO ALTO / RECHAZO)"

    return result


def generate_markdown_report(result: ContractAuditResult) -> str:
    """Generate a clean, professional Markdown audit report."""
    data = result.to_dict()

    lines = [
        f"# Dictamen de Auditoría Contractual: {result.filename}",
        "",
        f"- **Fecha de Evaluación**: 2026-10-01",
        f"- **Estándar**: ISO/IEC 27701:2025 (Tabla A.1, A.2, A.3) & RGPD Art. 28",
        f"- **Volumen del Documento**: {data['word_count']} palabras",
        f"- **Puntuación de Cumplimiento**: {data['overall_score']} / 100",
        f"- **Dictamen Global**: **{data['compliance_level']}**",
        "",
        "---",
        "",
        "## 1. Resumen de Cobertura de Cláusulas Obligatorias",
        "",
        f"- Cláusulas Conformes: **{data['clauses_compliant']}**",
        f"- Cláusulas Parciales / Débiles: **{data['clauses_partial']}**",
        f"- Cláusulas Ausentes: **{data['clauses_missing']}**",
        f"- Cláusulas Abusivas / Red Flags Detectadas: **{data['red_flags_count']}**",
        "",
        "| Control ISO 27701 | Cláusula Auditada | Estado | Ponderación | Evidencia Preliminar |",
        "|---|---|:---:|:---:|---|",
    ]

    for key, c in data["clauses_details"].items():
        status_badge = "[CONFORME]" if c["status"] == "CONFORME" else ("[PARCIAL]" if c["status"] == "PARCIAL" else "[AUSENTE]")
        lines.append(f"| `{c['iso_control']}` | {c['title']} | {status_badge} | {c['weight']} pts | {c['evidence']} |")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Detección de Cláusulas Abusivas y Factores de Riesgo (Red Flags)",
        "",
    ])

    if not data["red_flags"]:
        lines.append("*(No se detectaron red flags contractuales típicas).*")
    else:
        for rf in data["red_flags"]:
            lines.extend([
                f"### [ALERTA - {rf['severity'].upper()}] {rf['title']}",
                f"- **Fragmento Contractual**: `{rf['matched_snippet']}`",
                f"- **Riesgo Normativo**: {rf['issue']}",
                f"- **Acción Correctiva Sugerida**: {rf['recommendation']}",
                "",
            ])

    lines.extend([
        "---",
        "",
        "## 3. Próximos Pasos de Auditoría",
        "",
        "1. Para cada cláusula marcada como `AUSENTE` o `PARCIAL`, incorpore la redacción sugerida del catálogo `references/mandatory_clauses_dpa.md`.",
        "2. Negocie formalmente la supresión de las `Red Flags` detectadas antes de formalizar la firma del contrato.",
        "3. Si el proveedor almacena datos fuera del territorio nacional, derive el expediente a `pii-transfer-auditor` para auditar SCCs y TIA.",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    """CLI entrypoint."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Analizador determinista de cláusulas obligatorias en contratos DPA bajo ISO/IEC 27701:2025 y RGPD."
    )
    parser.add_argument(
        "--file", "-f", required=True, help="Ruta al archivo de texto o markdown del contrato/DPA."
    )
    parser.add_argument(
        "--json", action="store_true", help="Generar salida en formato JSON estructurado."
    )
    parser.add_argument(
        "--report", action="store_true", help="Generar reporte completo en formato Markdown."
    )
    parser.add_argument(
        "--threshold", type=int, default=70, help="Umbral mínimo de puntuación para aprobación (default: 70)."
    )

    args = parser.parse_args()
    contract_path = Path(args.file)

    if not contract_path.exists():
        print(f"Error: El archivo '{args.file}' no existe.", file=sys.stderr)
        sys.exit(1)

    try:
        content = contract_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = contract_path.read_text(encoding="latin-1")

    result = analyze_contract_text(content, filename=contract_path.name)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    elif args.report:
        print(generate_markdown_report(result))
    else:
        # Default brief summary
        data = result.to_dict()
        print(f"==================================================")
        print(f" DPA AUDIT SUMMARY: {data['file']}")
        print(f" Overall Score: {data['overall_score']} / 100")
        print(f" Compliance:    {data['compliance_level']}")
        print(f" Compliant: {data['clauses_compliant']} | Partial: {data['clauses_partial']} | Missing: {data['clauses_missing']}")
        print(f" Red Flags: {data['red_flags_count']}")
        print(f"==================================================")

    # Return exit code based on threshold
    if result.overall_score < args.threshold or any(r["severity"] == "Crítica" for r in result.red_flags_detected):
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
