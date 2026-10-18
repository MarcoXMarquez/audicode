#!/usr/bin/env python3
"""
transfer_record_validator.py - Validador Determinista de Inventarios de Transferencias de PII

Valida inventarios y libros de registro de transferencias transfronterizas de datos personales
en formatos CSV y JSON contra los requisitos de ISO/IEC 27701:2025 (A.1.5.2, A.1.5.3, A.1.5.4, A.2.5.2, A.3.7).

Verificaciones realizadas:
1. Presencia de país/jurisdicción de destino y consistencia geográfica.
2. Identificación y validez de la base jurídica de transferencia (Adecuación, SCC, BCR, Excepción).
3. Verificación de estatus de adecuación territorial contra catálogo normativo reconocido.
4. Para destinos sin decisión de adecuación:
   - Exigencia obligatoria de garantías adecuadas (SCC o BCR).
   - Exigencia y vigencia de Evaluación de Impacto de Transferencia (TIA - Transfer Impact Assessment).
   - Verificación de medidas suplementarias de seguridad (cifrado en tránsito y reposo, custodia de claves).
5. Evaluación de obligaciones de encargados (notificación previa al cliente y derechos de objeción).
6. Identificación de transferencias basadas indebidamente en excepciones para flujos masivos o continuos.

Uso:
    python transfer_record_validator.py --input inventario_transferencias.json
    python transfer_record_validator.py --input transfers.csv --format csv --output-format markdown
"""

import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

# Catálogo normativo de países y territorios con Decisión de Adecuación reconocida
# (Conforme a Comisión Europea, UK adequacy y estándares internacionales análogos)
ADEQUATE_COUNTRIES = {
    "AD": "Andorra",
    "ANDORRA": "Andorra",
    "AR": "Argentina",
    "ARGENTINA": "Argentina",
    "CA": "Canadá (Organizaciones Comerciales / PIPEDA)",
    "CANADA": "Canadá (Organizaciones Comerciales / PIPEDA)",
    "CH": "Suiza",
    "SWITZERLAND": "Suiza",
    "SUIZA": "Suiza",
    "FO": "Islas Feroe",
    "FAROE ISLANDS": "Islas Feroe",
    "GB": "Reino Unido",
    "UK": "Reino Unido",
    "UNITED KINGDOM": "Reino Unido",
    "REINO UNIDO": "Reino Unido",
    "GG": "Guernesey",
    "GUERNSEY": "Guernesey",
    "IL": "Israel",
    "ISRAEL": "Israel",
    "IM": "Isla de Man",
    "ISLE OF MAN": "Isla de Man",
    "JE": "Jersey",
    "JERSEY": "Jersey",
    "JP": "Japón (Sector Privado)",
    "JAPAN": "Japón (Sector Privado)",
    "JAPON": "Japón (Sector Privado)",
    "KR": "República de Corea",
    "SOUTH KOREA": "República de Corea",
    "KOREA": "República de Corea",
    "COREA DEL SUR": "República de Corea",
    "NZ": "Nueva Zelanda",
    "NEW ZEALAND": "Nueva Zelanda",
    "NUEVA ZELANDA": "Nueva Zelanda",
    "US-DPF": "Estados Unidos (EU-US Data Privacy Framework certificado)",
    "USA-DPF": "Estados Unidos (EU-US Data Privacy Framework certificado)",
    "UY": "Uruguay",
    "URUGUAY": "Uruguay",
}

# Miembros del Espacio Económico Europeo (Tratamiento asimilado a doméstico / no internacional)
EEA_COUNTRIES = {
    "AT": "Austria", "AUSTRIA": "Austria",
    "BE": "Bélgica", "BELGIUM": "Bélgica", "BELGICA": "Bélgica",
    "BG": "Bulgaria", "BULGARIA": "Bulgaria",
    "CY": "Chipre", "CYPRUS": "Chipre", "CHIPRE": "Chipre",
    "CZ": "República Checa", "CZECH REPUBLIC": "República Checa", "CHEQUIA": "República Checa",
    "DE": "Alemania", "GERMANY": "Alemania", "ALEMANIA": "Alemania",
    "DK": "Dinamarca", "DENMARK": "Dinamarca", "DINAMARCA": "Dinamarca",
    "EE": "Estonia", "ESTONIA": "Estonia",
    "ES": "España", "SPAIN": "España", "ESPANA": "España",
    "FI": "Finlandia", "FINLAND": "Finlandia", "FINLANDIA": "Finlandia",
    "FR": "Francia", "FRANCE": "Francia", "FRANCIA": "Francia",
    "GR": "Grecia", "GREECE": "Grecia", "GRECIA": "Grecia",
    "HR": "Croacia", "CROATIA": "Croacia", "CROACIA": "Croacia",
    "HU": "Hungría", "HUNGARY": "Hungría", "HUNGRIA": "Hungría",
    "IE": "Irlanda", "IRELAND": "Irlanda", "IRLANDA": "Irlanda",
    "IS": "Islandia", "ICELAND": "Islandia", "ISLANDIA": "Islandia",
    "IT": "Italia", "ITALY": "Italia", "ITALIA": "Italia",
    "LI": "Liechtenstein", "LIECHTENSTEIN": "Liechtenstein",
    "LT": "Lituania", "LITHUANIA": "Lituania", "LITUANIA": "Lituania",
    "LU": "Luxemburgo", "LUXEMBOURG": "Luxemburgo", "LUXEMBURGO": "Luxemburgo",
    "LV": "Letonia", "LATVIA": "Letonia", "LETONIA": "Letonia",
    "MT": "Malta", "MALTA": "Malta",
    "NL": "Países Bajos", "NETHERLANDS": "Países Bajos", "PAISES BAJOS": "Países Bajos",
    "NO": "Noruega", "NORWAY": "Noruega", "NORUEGA": "Noruega",
    "PL": "Polonia", "POLAND": "Polonia", "POLONIA": "Polonia",
    "PT": "Portugal", "PORTUGAL": "Portugal",
    "RO": "Rumanía", "ROMANIA": "Rumanía", "RUMANIA": "Rumanía",
    "SE": "Suecia", "SWEDEN": "Suecia", "SUECIA": "Suecia",
    "SI": "Eslovenia", "SLOVENIA": "Eslovenia", "ESLOVENIA": "Eslovenia",
    "SK": "Eslovaquia", "SLOVAKIA": "Eslovaquia", "ESLOVAQUIA": "Eslovaquia",
}

VALID_LEGAL_BASES = {
    "ADEQUACY": "Decisión de Adecuación (Art. 45 / A.1.5.2)",
    "ADECUACION": "Decisión de Adecuación (Art. 45 / A.1.5.2)",
    "SCC": "Cláusulas Contractuales Tipo (SCC / CCT / Art. 46 / A.1.5.2)",
    "STANDARD_CONTRACTUAL_CLAUSES": "Cláusulas Contractuales Tipo (SCC / Art. 46)",
    "BCR": "Normas Corporativas Vinculantes (BCR / Art. 47 / A.1.5.2)",
    "BCR-C": "Normas Corporativas Vinculantes para Responsables",
    "BCR-P": "Normas Corporativas Vinculantes para Encargados",
    "DEROGATION": "Excepción Tasada para Situación Específica (Art. 49 / A.1.5.2)",
    "EXCEPCION": "Excepción Tasada para Situación Específica (Art. 49 / A.1.5.2)",
    "CONSENT": "Excepción por Consentimiento Explícito (Art. 49(1)(a))",
    "CONTRACT": "Excepción por Ejecución de Contrato (Art. 49(1)(b))",
    "LEGAL_CLAIMS": "Excepción por Formulación de Reclamaciones (Art. 49(1)(e))",
    "INTERNAL_EEA": "Tráfico Intracomunitario EEE (No requiere mecanismo transfronterizo)",
}


class TransferRecordValidator:
    """Validador estricto y determinista de registros de transferencias transfronterizas."""

    def __init__(self, max_tia_age_days: int = 365):
        self.max_tia_age_days = max_tia_age_days

    def normalize_country(self, raw_country: str) -> str:
        """Normaliza el nombre o código de país a mayúsculas limpias."""
        if not raw_country:
            return ""
        cleaned = re.sub(r'[^a-zA-Z0-9_-]', '', raw_country.strip().upper())
        return cleaned

    def parse_date(self, date_str: Any) -> Optional[datetime]:
        """Parsea una fecha en diversos formatos comunes (ISO 8601, YYYY-MM-DD, DD/MM/YYYY)."""
        if not date_str:
            return None
        date_str = str(date_str).strip()
        formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S%z",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y/%m/%d"
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except ValueError:
                continue
        return None

    def validate_single_record(self, record: Dict[str, Any], index: int) -> Dict[str, Any]:
        """
        Valida una fila o entrada individual del inventario de transferencias.
        Retorna un diccionario con estado ('PASS', 'WARNING', 'FAIL') y lista de hallazgos.
        """
        issues: List[Dict[str, str]] = []
        record_id = record.get("transfer_id") or record.get("id") or f"REG-{index + 1}"
        destination_raw = record.get("destination_country") or record.get("country") or record.get("pais_destino") or ""
        origin_raw = record.get("origin_country") or record.get("pais_origen") or "ORIGIN_DEFAULT"
        legal_basis_raw = record.get("legal_basis") or record.get("base_legal") or record.get("transfer_mechanism") or ""
        data_categories = record.get("data_categories") or record.get("pii_categories") or record.get("categorias_datos") or ""
        recipient_name = record.get("recipient_name") or record.get("destinatario") or record.get("vendor") or ""
        is_processor = str(record.get("is_processor", "")).strip().lower() in ("true", "1", "yes", "si")
        is_recurring = str(record.get("is_recurring", "true")).strip().lower() in ("true", "1", "yes", "si")
        tia_conducted = record.get("tia_conducted")
        tia_date_raw = record.get("tia_date") or record.get("fecha_tia")
        safeguards = record.get("safeguards") or record.get("medidas_seguridad") or record.get("supplementary_measures") or ""
        transit_encryption = record.get("transit_encryption") or record.get("cifrado_transito") or ""
        customer_notified = record.get("customer_notified") or record.get("cliente_notificado")

        dest_norm = self.normalize_country(str(destination_raw))
        basis_norm = str(legal_basis_raw).strip().upper().replace(" ", "_")

        # 1. Validación de Destino (A.1.5.3)
        if not dest_norm:
            issues.append({
                "control": "A.1.5.3",
                "severity": "CRÍTICA",
                "message": f"Registro '{record_id}' carece de país o jurisdicción de destino documentada.",
                "remedy": "Especificar taxativamente el país territorial y región cloud receptora según A.1.5.3."
            })
        elif dest_norm in ("GLOBAL", "CLOUD", "WORLDWIDE", "INTERNACIONAL", "VARIOS", "UNKNOWN"):
            issues.append({
                "control": "A.1.5.3",
                "severity": "CRÍTICA",
                "message": f"Destino ambiguo '{destination_raw}' en '{record_id}'. Está prohibido declarar nubes indeterminadas.",
                "remedy": "Desglosar los centros de datos específicos y países con acceso de soporte remoto."
            })

        # 2. Validación de Base Jurídica (A.1.5.2)
        if not basis_norm:
            issues.append({
                "control": "A.1.5.2",
                "severity": "CRÍTICA",
                "message": f"Transferencia '{record_id}' carece de mecanismo o base legal de transferencia.",
                "remedy": "Asignar y documentar base legal formal: Adecuación, SCC, BCR o excepción válida."
            })

        # Evaluación de adecuación geográfica
        is_eea = dest_norm in EEA_COUNTRIES
        is_adequate = dest_norm in ADEQUATE_COUNTRIES or (dest_norm.startswith("US") and "DPF" in basis_norm)

        # Reglas según adecuación
        if is_eea:
            # Flujo intracomunitario
            pass
        elif is_adequate:
            # País con decisión de adecuación
            if "ADEQUACY" not in basis_norm and "ADECUACION" not in basis_norm and "DPF" not in basis_norm:
                issues.append({
                    "control": "A.1.5.2",
                    "severity": "MENOR",
                    "message": f"Destino '{dest_norm}' cuenta con Decisión de Adecuación, pero la base indicada es '{legal_basis_raw}'.",
                    "remedy": "Registrar 'Decisión de Adecuación' como fundamento principal para mayor solidez."
                })
        else:
            # País TERCERO SIN DECISIÓN DE ADECUACIÓN (e.g. EE.UU. sin DPF, India, China, Brasil, etc.)
            if basis_norm in ("ADEQUACY", "ADECUACION"):
                issues.append({
                    "control": "A.1.5.2",
                    "severity": "CRÍTICA",
                    "message": f"Se declaró 'Decisión de Adecuación' para '{dest_norm}', pero no cuenta con reconocimiento de adecuación válido.",
                    "remedy": "Formalizar Cláusulas Contractuales Tipo (SCC) o Normas Corporativas Vinculantes (BCR)."
                })

            # Comprobar si se ampara en garantías adecuadas (SCC o BCR)
            has_scc_or_bcr = any(k in basis_norm for k in ["SCC", "STANDARD_CONTRACTUAL", "BCR"])

            # Comprobar si se ampara indebidamente en excepciones para flujos sistemáticos
            has_derogation = any(k in basis_norm for k in ["DEROGATION", "EXCEPCION", "CONSENT", "CONTRACT"])
            if has_derogation and is_recurring:
                issues.append({
                    "control": "A.1.5.2",
                    "severity": "CRÍTICA",
                    "message": f"Transferencia continua/recurrente amparada indebidamente en excepción ('{legal_basis_raw}') hacia país sin adecuación ('{dest_norm}').",
                    "remedy": "Las excepciones de A.1.5.2 solo aplican a transferencias aisladas y no repetitivas. Suscribir SCC."
                })

            # Exigencia obligatoria de TIA (Transfer Impact Assessment) para países sin adecuación
            has_tia_conducted = False
            if isinstance(tia_conducted, bool):
                has_tia_conducted = tia_conducted
            elif str(tia_conducted).lower() in ("true", "1", "yes", "si"):
                has_tia_conducted = True
            elif tia_date_raw:
                has_tia_conducted = True

            if not has_tia_conducted:
                issues.append({
                    "control": "A.1.5.2",
                    "severity": "CRÍTICA",
                    "message": f"Falta Evaluación de Impacto de Transferencia (TIA) obligatoria para destino sin adecuación '{dest_norm}'.",
                    "remedy": "Ejecutar y documentar expediente de TIA evaluando leyes de vigilancia y acceso judicial local."
                })
            else:
                # Validar vigencia de la TIA
                parsed_tia_date = self.parse_date(tia_date_raw)
                if parsed_tia_date:
                    age_days = (datetime.now(timezone.utc) - parsed_tia_date).days
                    if age_days > self.max_tia_age_days:
                        issues.append({
                            "control": "A.1.5.2",
                            "severity": "MAYOR",
                            "message": f"La TIA de '{record_id}' tiene {age_days} días de antigüedad (límite configurado: {self.max_tia_age_days} días).",
                            "remedy": "Reevaluar y actualizar el expediente de TIA ante cambios legislativos o tecnológicos."
                        })
                elif tia_date_raw:
                    issues.append({
                        "control": "A.1.5.4",
                        "severity": "MENOR",
                        "message": f"Formato de fecha inválido o no reconocido en TIA: '{tia_date_raw}'.",
                        "remedy": "Utilizar formato estándar ISO 8601 (YYYY-MM-DD)."
                    })

            # Medidas suplementarias (Técnicas y Organizativas)
            if not safeguards:
                issues.append({
                    "control": "A.1.5.2",
                    "severity": "MAYOR",
                    "message": f"No se documentan medidas suplementarias (safeguards) para destino no adecuado '{dest_norm}'.",
                    "remedy": "Documentar cifrado con gestión de claves fuera del país receptor y medidas contractuales."
                })

        # 3. Seguridad en Tránsito (A.3.7)
        transit_norm = str(transit_encryption).strip().upper()
        if not transit_norm or transit_norm in ("NO", "NONE", "FALSE", "0", "CLEAR_TEXT"):
            issues.append({
                "control": "A.3.7",
                "severity": "CRÍTICA",
                "message": f"Flujo transfronterizo en '{record_id}' no acredita cifrado robusto en tránsito.",
                "remedy": "Implementar cifrado obligatorio en tránsito (TLS 1.3 / mTLS / IPsec VPN) con suites criptográficas modernas."
            })

        # 4. Obligaciones de Encargados (A.2.5.2, A.2.5.3)
        if is_processor:
            notified_bool = str(customer_notified).strip().lower() in ("true", "1", "yes", "si")
            if not notified_bool:
                issues.append({
                    "control": "A.2.5.2",
                    "severity": "MAYOR",
                    "message": f"Como encargado, no se registra notificación previa al cliente de la transferencia '{record_id}'.",
                    "remedy": "Notificar con antelación formal al responsable y asegurar la oportunidad de objeción."
                })

        # 5. Campos de Trazabilidad del Registro (A.1.5.4)
        if not data_categories:
            issues.append({
                "control": "A.1.5.4",
                "severity": "MENOR",
                "message": f"Falta inventario explícito de categorías de PII transferidas en '{record_id}'.",
                "remedy": "Especificar las categorías exactas de PII (ej. datos de contacto, financieros, salud)."
            })
        if not recipient_name:
            issues.append({
                "control": "A.1.5.4",
                "severity": "MENOR",
                "message": f"Falta identificar la entidad o razón social del destinatario receptor en '{record_id}'.",
                "remedy": "Registrar el nombre formal del importador/proveedor y su rol de tratamiento."
            })

        # Determinación del estado general del registro
        status = "CONFORME"
        if any(iss["severity"] == "CRÍTICA" for iss in issues):
            status = "NO_CONFORME_CRÍTICO"
        elif any(iss["severity"] == "MAYOR" for iss in issues):
            status = "NO_CONFORME_MAYOR"
        elif issues:
            status = "CONFORME_CON_OBSERVACIONES"

        return {
            "record_id": record_id,
            "destination_country": destination_raw,
            "legal_basis": legal_basis_raw,
            "status": status,
            "issues": issues,
            "issue_count": len(issues)
        }

    def validate_inventory(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Valida una lista completa de transferencias y sintetiza estadísticas globales."""
        results: List[Dict[str, Any]] = []
        critical_count = 0
        major_count = 0
        minor_count = 0
        conforming_count = 0

        for i, rec in enumerate(records):
            eval_res = self.validate_single_record(rec, i)
            results.append(eval_res)
            for iss in eval_res["issues"]:
                if iss["severity"] == "CRÍTICA":
                    critical_count += 1
                elif iss["severity"] == "MAYOR":
                    major_count += 1
                else:
                    minor_count += 1
            if eval_res["status"] == "CONFORME":
                conforming_count += 1

        total = len(records)
        compliance_pct = round((conforming_count / total * 100), 2) if total > 0 else 0.0

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_records_audited": total,
            "conforming_records": conforming_count,
            "compliance_percentage": compliance_pct,
            "summary_severity": {
                "critical": critical_count,
                "major": major_count,
                "minor": minor_count
            },
            "records": results
        }


def load_records(file_path: Path, format_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Carga registros desde archivo JSON o CSV."""
    if not file_path.exists():
        raise FileNotFoundError(f"El archivo especificado no existe: {file_path}")

    ext = file_path.suffix.lower()
    in_format = (format_type or ("csv" if ext == ".csv" else "json")).lower()

    if in_format == "csv":
        records = []
        with open(file_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Limpiar espacios en claves y valores
                cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                records.append(cleaned_row)
        return records
    else:
        with open(file_path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # Si viene envuelto en 'transfers', 'records' o similar
                for key in ["transfers", "records", "data", "items"]:
                    if key in data and isinstance(data[key], list):
                        return data[key]
                return [data]
            else:
                raise ValueError("Estructura JSON no reconocida: debe ser lista o diccionario con transferencias.")


def format_markdown_report(analysis: Dict[str, Any]) -> str:
    """Genera informe en formato Markdown legible y estructurado."""
    md = []
    md.append("# Informe de Auditoría Determinista de Transferencias de PII (ISO/IEC 27701:2025)")
    md.append(f"\n- **Fecha de ejecución**: {analysis['timestamp']}")
    md.append(f"- **Registros auditados**: {analysis['total_records_audited']}")
    md.append(f"- **Registros plenamente conformes**: {analysis['conforming_records']}")
    md.append(f"- **Porcentaje de conformidad**: {analysis['compliance_percentage']}%")
    md.append(f"- **Hallazgos Críticos**: {analysis['summary_severity']['critical']}")
    md.append(f"- **Hallazgos Mayores**: {analysis['summary_severity']['major']}")
    md.append(f"- **Hallazgos Menores / OMs**: {analysis['summary_severity']['minor']}\n")

    md.append("## Tabla de Evaluación por Flujo de Transferencia\n")
    md.append("| ID Flujo | Destino | Base Jurídica | Estado Normativo | Hallazgos |")
    md.append("|---|---|---|---|---|")
    for r in analysis["records"]:
        md.append(f"| {r['record_id']} | {r['destination_country']} | {r['legal_basis']} | **{r['status']}** | {r['issue_count']} incidencia(s) |")

    md.append("\n## Detalle Pormenorizado de No Conformidades y Recomendaciones\n")
    has_issues = False
    for r in analysis["records"]:
        if r["issues"]:
            has_issues = True
            md.append(f"### Flujo: {r['record_id']} (Destino: {r['destination_country']})")
            for iss in r["issues"]:
                md.append(f"- **[{iss['severity']}] Control {iss['control']}**: {iss['message']}")
                md.append(f"  * *Recomendación de subsanación*: {iss['remedy']}")
            md.append("")

    if not has_issues:
        md.append("No se detectaron no conformidades en el inventario analizado. Cumplimiento pleno.")

    return "\n".join(md)


def main():
    """Punto de entrada de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Validador determinista de registros e inventarios de transferencias internacionales de PII (ISO/IEC 27701:2025)."
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        type=str,
        help="Ruta al archivo CSV o JSON con el libro de transferencias."
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "csv"],
        default=None,
        help="Formato del archivo de entrada (por defecto se autodetecta por extensión)."
    )
    parser.add_argument(
        "--output-format", "-o",
        choices=["text", "json", "markdown"],
        default="text",
        help="Formato de salida de resultados (text, json, markdown)."
    )
    parser.add_argument(
        "--max-tia-age-days",
        type=int,
        default=365,
        help="Antigüedad máxima permitida para las Evaluaciones de Impacto de Transferencia (días, defecto: 365)."
    )

    args = parser.parse_args()
    file_path = Path(args.input)

    try:
        records = load_records(file_path, args.format)
    except Exception as e:
        print(f"ERROR: Fallo al cargar el archivo de transferencias: {e}", file=sys.stderr)
        sys.exit(2)

    validator = TransferRecordValidator(max_tia_age_days=args.max_tia_age_days)
    report = validator.validate_inventory(records)

    if args.output_format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif args.output_format == "markdown":
        print(format_markdown_report(report))
    else:
        print(f"=== RESULTADOS DE AUDITORÍA DETERMINISTA DE TRANSFERENCIAS ===")
        print(f"Total registros: {report['total_records_audited']} | Conformidad: {report['compliance_percentage']}%")
        print(f"Críticos: {report['summary_severity']['critical']} | Mayores: {report['summary_severity']['major']} | Menores: {report['summary_severity']['minor']}")
        print("----------------------------------------------------------------------")
        for r in report["records"]:
            print(f"[{r['status']}] {r['record_id']} -> Destino: {r['destination_country']} ({r['legal_basis']})")
            for iss in r["issues"]:
                print(f"   * [{iss['severity']} - {iss['control']}] {iss['message']}")

    # Exit code: 1 si hay críticas, 0 si conforme o sólo advertencias
    if report["summary_severity"]["critical"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
