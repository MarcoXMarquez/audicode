#!/usr/bin/env python3
"""
schema_minimization_checker.py - Deterministic PII Schema and Data Minimization Auditor

Audits SQL DDL (CREATE TABLE) and JSON schema/payload files against ISO/IEC 27701:2025
controls (A.1.4.2 Limit collection, A.1.4.5 Minimization objectives, A.1.4.6 De-identification)
and ISO/IEC 20889:2018 de-identification techniques.

Usage:
    python schema_minimization_checker.py <file_or_directory_path> [--purpose <purpose>] [--min-risk <LOW|MEDIUM|HIGH|CRITICAL>] [--json]

Examples:
    python schema_minimization_checker.py schema.sql --purpose "e-commerce checkout"
    python schema_minimization_checker.py api_payload.json --min-risk HIGH --json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Classification of PII patterns by risk severity and category
PII_PATTERNS = {
    "CRITICAL": {
        "special_category_health": {
            "patterns": [
                r"\b(health|diagnos|medical|disease|disabilit|blood_type|treatment|prescription|hospital|clinic)\b",
                r"\b(salud|diagnostico|medico|enfermedad|discapacidad|grupo_sanguineo|tratamiento|receta)\b"
            ],
            "category": "Special Category (Health/Medical)",
            "iso_20889_remedy": "Supresión inmediata si no es indispensable; en su defecto, pseudonimización con segregación física estricta o tokenización no determinista con HSM."
        },
        "special_category_biometric_genetic": {
            "patterns": [
                r"\b(biometric|fingerprint|face_print|facial_template|retina|iris_scan|voice_print|genetic|dna)\b",
                r"\b(biometrico|huella_dactilar|patron_facial|iris|voz_template|genetico|adn)\b"
            ],
            "category": "Special Category (Biometric / Genetic)",
            "iso_20889_remedy": "Almacenamiento exclusivo en dispositivo del usuario (on-device match-on-card) o plantillas irreversibles con hashing salteado y ruido de cuantización."
        },
        "special_category_beliefs_orientation": {
            "patterns": [
                r"\b(religio|political|trade_union|philosoph|ethnic|race|sexual_orientation|gender_identity)\b",
                r"\b(religion|politica|sindicato|filosofia|etnia|raza|orientacion_sexual|identidad_genero)\b"
            ],
            "category": "Special Category (Beliefs / Political / Ethnicity / Sexual)",
            "iso_20889_remedy": "Exclusión total por defecto (A.1.4.2). Si es legalmente exigido, agregación categórica amplia y anonimización estadística irreversible."
        },
        "national_identifiers_raw": {
            "patterns": [
                r"\b(ssn|social_security|dni|curp|cpf|nie|nif|cuit|rut|national_id|passport_num|driver_licen[cs]e)\b",
                r"\b(cedula|pasaporte|documento_identidad|tarjeta_militar)\b"
            ],
            "category": "National Government Identifier (Direct High-Risk)",
            "iso_20889_remedy": "Sustitución por UUID sintético seudónimo (A.1.4.5). Si se requiere para deduplicación, almacenar únicamente hash criptográfico con sal y pimienta (HMAC-SHA256)."
        },
        "raw_credentials_or_pan": {
            "patterns": [
                r"\b(password|passwd|pin_code|cvv|cvc|card_number|pan|credit_card_full|private_key|secret_key)\b",
                r"\b(clave|contrasena|tarjeta_completa|codigo_seguridad)\b"
            ],
            "category": "Raw Credentials / Financial PAN",
            "iso_20889_remedy": "Prohibición absoluta en texto plano. Usar KDF seguro (Argon2id/bcrypt) para claves y tokenización PCI-DSS validada para tarjetas."
        }
    },
    "HIGH": {
        "direct_contact_identifiers": {
            "patterns": [
                r"\b(email|e_mail|correo|correo_electronico|personal_mail)\b",
                r"\b(phone|telephone|mobile|cellphone|fax|telefono|celular|movil)\b"
            ],
            "category": "Direct Contact PII",
            "iso_20889_remedy": "Enmascaramiento dinámico en interfaces (e.g., m***@domain.com, +34 *** 456) y segregación lógica del repositorio transaccional."
        },
        "direct_name_address": {
            "patterns": [
                r"\b(first[_\s]+name|last[_\s]+name|full[_\s]+name|surname|mother[_\s]+name|father[_\s]+name|maiden[_\s]+name|mother[_\s]+maiden|cardholder[_\s]+name|nombre|apellido|apellidos)\b",
                r"\b(street[_\s]+address|home[_\s]+address|residence[_\s]+address|apartment[_\s]+num|billing[_\s]+address|direccion_domicilio|calle_numero)\b"
            ],
            "category": "Direct Personal Identity & Exact Address",
            "iso_20889_remedy": "Separación de perfil en tabla de identidad con ID seudónimo interno. Truncamiento de dirección a nivel de distrito/ciudad cuando no hay entrega física directa."
        },
        "exact_birthdate_age": {
            "patterns": [
                r"\b(birth_?date|dob|date[_\s]+of[_\s]+birth|fecha[_\s]+nacimiento|f_nacimiento)\b"
            ],
            "category": "Exact Date of Birth",
            "iso_20889_remedy": "Generalización (ISO 20889 §7): transformar a rango etario (ej. '18-24', '25-34') o almacenar únicamente el año de nacimiento si el propósito es verificar mayoría de edad."
        },
        "precise_geolocation": {
            "patterns": [
                r"\b(latitude|longitude|gps_coord|exact_location|lat_long|coordenadas_gps|ubicacion_precisa)\b"
            ],
            "category": "Precise Geolocation",
            "iso_20889_remedy": "Reducción de granularidad espacial (truncar decimales a 1-2 dígitos, precisión de barrio/municipio) o generalización a código de país/región."
        }
    },
    "MEDIUM": {
        "indirect_device_network": {
            "patterns": [
                r"\b(ip[_\s]+address|client[_\s]+ip|remote[_\s]+addr|mac[_\s]+address|device[_\s]+id|imei|advertising[_\s]+id|idfa|gaid|sim[_\s]+serial(?:[_\s]+number)?|sim[_\s]+card|bssid|ssid|wifi[_\s]+bssid|device[_\s]+serial)\b",
                r"\b(canvas_fingerprint|browser_fingerprint|user_agent_full|huella_dispositivo)\b"
            ],
            "category": "Network / Device Indirect Identifiers",
            "iso_20889_remedy": "Truncamiento de último octeto en IPv4 (/24) o prefijo /48 en IPv6; anonimización de User-Agent extrayendo solo navegador/SO principal; expiración TTL < 30 días."
        },
        "financial_metadata": {
            "patterns": [
                r"\b(salary|income|revenue|wage|bank_account|iban|sueldo|salario|ingresos|cuenta_bancaria)\b"
            ],
            "category": "Financial / Socioeconomic Metadata",
            "iso_20889_remedy": "Enmascaramiento de IBAN (mostrar solo últimos 4 dígitos) y generalización en bandas o deciles salariales para fines estadísticos."
        },
        "postal_code_granular": {
            "patterns": [
                r"\b(zip[_\s]?code|postal[_\s]?code|codigo[_\s]?postal|cp)\b"
            ],
            "category": "Granular Postal Code",
            "iso_20889_remedy": "Truncar código postal a 2-3 dígitos principales si se cruza con otros datos demográficos (prevención de reidentificación de Sweeney)."
        }
    },
    "LOW": {
        "interaction_telemetry": {
            "patterns": [
                r"\b(click_stream|mouse_movement|keystroke_log|session_replay|heat_map|telemetry_detail)\b"
            ],
            "category": "Excessive Interaction Telemetry",
            "iso_20889_remedy": "Muestreo estadístico agregado, descarte inmediato de datos en bruto y sanitización de campos de texto antes de la captura."
        },
        "temporary_and_debug_artifacts": {
            "patterns": [
                r"\b(debug[_\s]+log|raw[_\s]+dump|temp[_\s]+payload|scratch[_\s]+buffer|stack[_\s]+trace|payload[_\s]+dump)\b"
            ],
            "category": "Temporary Processing Logs / Debug Dumps",
            "iso_20889_remedy": "Aplicación estricta de control A.1.4.7: TTL automatizado <= 24 horas y filtros regex en middlewares para evitar la persistencia de PII en logs."
        }
    }
}


def compile_pii_rules():
    """Compiles regex patterns into a structured lookup structure."""
    compiled = []
    for severity, categories in PII_PATTERNS.items():
        for cat_key, cat_data in categories.items():
            for p_str in cat_data["patterns"]:
                regex = re.compile(p_str, re.IGNORECASE)
                compiled.append({
                    "severity": severity,
                    "category_key": cat_key,
                    "category_name": cat_data["category"],
                    "remedy": cat_data["iso_20889_remedy"],
                    "regex": regex
                })
    return compiled


COMPILED_RULES = compile_pii_rules()


class SchemaAuditFinding:
    def __init__(
        self,
        target_name: str,
        field_name: str,
        data_type: str,
        severity: str,
        category: str,
        is_required: bool,
        remedy: str,
        excess_factor: str
    ):
        self.target_name = target_name
        self.field_name = field_name
        self.data_type = data_type
        self.severity = severity
        self.category = category
        self.is_required = is_required
        self.remedy = remedy
        self.excess_factor = excess_factor

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target": self.target_name,
            "field": self.field_name,
            "data_type": self.data_type,
            "severity": self.severity,
            "category": self.category,
            "is_required": self.is_required,
            "excess_factor": self.excess_factor,
            "recommended_technique": self.remedy,
            "iso_controls": ["A.1.4.2", "A.1.4.5"] if self.severity in ["CRITICAL", "HIGH"] else ["A.1.4.2"]
        }


def match_field(field_name: str) -> Optional[Dict[str, Any]]:
    """Check if a field name matches known PII patterns."""
    clean_name = field_name.strip("`'\" []")
    for rule in COMPILED_RULES:
        if rule["regex"].search(clean_name):
            return rule
    # Test spaced version replacing underscores, dots, and hyphens
    spaced_name = re.sub(r'[_.\-]+', ' ', clean_name)
    for rule in COMPILED_RULES:
        if rule["regex"].search(spaced_name):
            return rule
    return None


def parse_sql_ddl(sql_text: str, filename: str) -> List[SchemaAuditFinding]:
    """Parse CREATE TABLE SQL statements and evaluate columns for PII minimization issues."""
    findings: List[SchemaAuditFinding] = []

    # Clean SQL comments
    clean_sql = re.sub(r'--[^\n]*', '', sql_text)
    clean_sql = re.sub(r'/\*.*?\*/', '', clean_sql, flags=re.DOTALL)

    # Robust balanced-parentheses SQL table extraction
    create_pattern = re.compile(
        r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([`"\'\w\.]+)\s*\(',
        re.IGNORECASE
    )

    pos = 0
    while True:
        match = create_pattern.search(clean_sql, pos)
        if not match:
            break
        raw_table_name = match.group(1).strip("`'\" ")
        start_paren = match.end() - 1
        paren_depth = 0
        end_paren = -1
        for i in range(start_paren, len(clean_sql)):
            if clean_sql[i] == '(':
                paren_depth += 1
            elif clean_sql[i] == ')':
                paren_depth -= 1
                if paren_depth == 0:
                    end_paren = i
                    break

        if end_paren == -1:
            pos = match.end()
            continue

        table_body = clean_sql[start_paren + 1:end_paren]
        pos = end_paren + 1

        # Split columns by comma (ignoring commas inside parentheses)
        col_definitions = []
        paren_depth = 0
        current_chunk = []
        for char in table_body:
            if char == '(':
                paren_depth += 1
                current_chunk.append(char)
            elif char == ')':
                paren_depth -= 1
                current_chunk.append(char)
            elif char == ',' and paren_depth == 0:
                col_definitions.append(''.join(current_chunk).strip())
                current_chunk = []
            else:
                current_chunk.append(char)
        if current_chunk:
            col_definitions.append(''.join(current_chunk).strip())

        for col_def in col_definitions:
            if not col_def:
                continue

            # Skip table-level constraints (PRIMARY KEY, CONSTRAINT, UNIQUE, FOREIGN KEY, CHECK, INDEX)
            if re.match(r'^(PRIMARY\s+KEY|CONSTRAINT|FOREIGN\s+KEY|UNIQUE|CHECK|KEY|INDEX)\b', col_def, re.IGNORECASE):
                continue

            # Extract column name, type, and constraints
            col_parts = col_def.split()
            if len(col_parts) < 2:
                continue

            raw_col_name = col_parts[0].strip("`'\" ")
            data_type = col_parts[1].upper()
            is_not_null = bool(re.search(r'\bNOT\s+NULL\b', col_def, re.IGNORECASE))

            rule = match_field(raw_col_name)
            if rule:
                excess_reasons = []
                if is_not_null and rule["severity"] in ["CRITICAL", "HIGH"]:
                    excess_reasons.append("Marcado como NOT NULL obligatorio (posible violación de privacidad por defecto A.1.4.2)")

                if "birth" in raw_col_name.lower() and ("DATE" in data_type or "TIMESTAMP" in data_type):
                    excess_reasons.append("Fecha exacta con granularidad de día/hora en lugar de rango etario (A.1.4.5)")
                elif "ip" in raw_col_name.lower() and not ("trunc" in raw_col_name.lower() or "mask" in raw_col_name.lower()):
                    excess_reasons.append("Dirección IP almacenada en texto plano sin truncamiento de subred")
                elif "gps" in raw_col_name.lower() or "lat" in raw_col_name.lower():
                    excess_reasons.append("Coordenadas geográficas de alta precisión sin generalización zonal")

                excess_factor = "; ".join(excess_reasons) if excess_reasons else "Identificador directo/indirecto persistido sin técnica de de-identificación declarada"

                findings.append(SchemaAuditFinding(
                    target_name=f"{filename} -> Table: {raw_table_name}",
                    field_name=raw_col_name,
                    data_type=data_type,
                    severity=rule["severity"],
                    category=rule["category_name"],
                    is_required=is_not_null,
                    remedy=rule["remedy"],
                    excess_factor=excess_factor
                ))

    return findings


def parse_json_schema_or_payload(json_data: Any, target_name: str, path: str = "") -> List[SchemaAuditFinding]:
    """Parse JSON schema or JSON payload structure recursively to detect PII attributes."""
    findings: List[SchemaAuditFinding] = []

    if isinstance(json_data, dict):
        # Case 1: Standard JSON Schema with 'properties' and 'required'
        if "properties" in json_data and isinstance(json_data["properties"], dict):
            required_fields = json_data.get("required", [])
            for prop_name, prop_attrs in json_data["properties"].items():
                current_path = f"{path}.{prop_name}" if path else prop_name
                is_req = prop_name in required_fields
                prop_type = prop_attrs.get("type", "unknown") if isinstance(prop_attrs, dict) else "unknown"

                rule = match_field(prop_name)
                if rule:
                    excess_reasons = []
                    if is_req and rule["severity"] in ["CRITICAL", "HIGH"]:
                        excess_reasons.append("Definido como 'required: true' (recolección mandatoria sin justificación de necesidad demostrada)")
                    excess_factor = "; ".join(excess_reasons) if excess_reasons else "Atributo PII expuesto en payload/esquema sin política de minimización explícita"

                    findings.append(SchemaAuditFinding(
                        target_name=target_name,
                        field_name=current_path,
                        data_type=str(prop_type),
                        severity=rule["severity"],
                        category=rule["category_name"],
                        is_required=is_req,
                        remedy=rule["remedy"],
                        excess_factor=excess_factor
                    ))

                # Recurse if nested object
                if isinstance(prop_attrs, dict) and prop_attrs.get("type") == "object":
                    findings.extend(parse_json_schema_or_payload(prop_attrs, target_name, current_path))
                elif isinstance(prop_attrs, dict) and prop_attrs.get("type") == "array" and "items" in prop_attrs:
                    findings.extend(parse_json_schema_or_payload(prop_attrs["items"], target_name, f"{current_path}[]"))

        # Case 2: Regular JSON API payload / dictionary
        else:
            for key, val in json_data.items():
                current_path = f"{path}.{key}" if path else key
                val_type = type(val).__name__

                rule = match_field(key)
                if rule:
                    excess_factor = "Campo PII en carga útil REST/JSON susceptible de sobre-recolección (over-fetching)"
                    findings.append(SchemaAuditFinding(
                        target_name=target_name,
                        field_name=current_path,
                        data_type=val_type,
                        severity=rule["severity"],
                        category=rule["category_name"],
                        is_required=False,
                        remedy=rule["remedy"],
                        excess_factor=excess_factor
                    ))

                # Recurse into nested dictionaries or lists
                if isinstance(val, dict):
                    findings.extend(parse_json_schema_or_payload(val, target_name, current_path))
                elif isinstance(val, list) and val and isinstance(val[0], dict):
                    findings.extend(parse_json_schema_or_payload(val[0], target_name, f"{current_path}[0]"))

    elif isinstance(json_data, list) and json_data and isinstance(json_data[0], dict):
        findings.extend(parse_json_schema_or_payload(json_data[0], target_name, f"{path}[0]"))

    return findings


def audit_file(file_path: Path) -> List[SchemaAuditFinding]:
    """Audit an individual file based on its extension."""
    suffix = file_path.suffix.lower()
    findings: List[SchemaAuditFinding] = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        sys.stderr.write(f"Error reading {file_path}: {e}\n")
        return []

    if suffix in [".sql", ".ddl"]:
        findings = parse_sql_ddl(content, file_path.name)
    elif suffix in [".json", ".jsonld"]:
        try:
            parsed = json.loads(content)
            findings = parse_json_schema_or_payload(parsed, file_path.name)
        except json.JSONDecodeError as err:
            sys.stderr.write(f"JSON parsing error in {file_path.name}: {err}\n")
    else:
        # Fallback: test if it's SQL or JSON by content inspection
        if "CREATE TABLE" in content.upper():
            findings = parse_sql_ddl(content, file_path.name)
        elif content.strip().startswith("{") or content.strip().startswith("["):
            try:
                parsed = json.loads(content)
                findings = parse_json_schema_or_payload(parsed, file_path.name)
            except Exception:
                pass

    return findings


def filter_by_risk(findings: List[SchemaAuditFinding], min_risk: str) -> List[SchemaAuditFinding]:
    """Filter findings by minimum severity level."""
    order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    threshold = order.get(min_risk.upper(), 1)
    return [f for f in findings if order.get(f.severity, 0) >= threshold]


def format_text_report(findings: List[SchemaAuditFinding], purpose: Optional[str] = None) -> str:
    """Generate a clean markdown report of minimization findings."""
    lines = []
    lines.append("# Reporte Determinista de Minimización de Datos y Esquemas PII")
    lines.append(f"**Referencia Normativa**: ISO/IEC 27701:2025 (A.1.4.2, A.1.4.5) & ISO/IEC 20889:2018")
    if purpose:
        lines.append(f"**Propósito del Tratamiento Declarado**: `{purpose}`")
    lines.append(f"**Total de Campos PII Identificados**: {len(findings)}\n")

    if not findings:
        lines.append("> [!NOTE]")
        lines.append("> No se detectaron atributos PII ni violaciones directas de minimización en los artefactos auditados.\n")
        return "\n".join(lines)

    # Summary table by severity
    critical_count = sum(1 for f in findings if f.severity == "CRITICAL")
    high_count = sum(1 for f in findings if f.severity == "HIGH")
    medium_count = sum(1 for f in findings if f.severity == "MEDIUM")
    low_count = sum(1 for f in findings if f.severity == "LOW")

    lines.append("## Resumen de Severidad")
    lines.append("| Nivel de Riesgo | Cantidad | Impacto en Privacidad |")
    lines.append("|---|---|---|")
    lines.append(f"| **CRITICAL** | {critical_count} | Datos sensibles / Identificadores nacionales / Credenciales expuestas |")
    lines.append(f"| **HIGH** | {high_count} | Identificadores directos, contacto o localización precisa obligatoria |")
    lines.append(f"| **MEDIUM** | {medium_count} | Identificadores indirectos, IPs o metadatos de contexto sin enmascarar |")
    lines.append(f"| **LOW** | {low_count} | Telemetría excesiva o logs transitorios sin TTL explícito |")
    lines.append("")

    lines.append("## Detalle de Hallazgos y Recomendaciones de De-identificación")
    lines.append("| Origen / Artefacto | Campo PII | Tipo / Req | Severidad | Categoría | Recomendación Técnica (ISO 20889) |")
    lines.append("|---|---|---|---|---|---|")

    for f in findings:
        req_str = "REQ" if f.is_required else "OPT"
        lines.append(
            f"| `{f.target_name}` | `{f.field_name}` | {f.data_type} ({req_str}) | **{f.severity}** | {f.category} | {f.remedy} |"
        )

    lines.append("")
    lines.append("## Factores Específicos de Sobre-Recolección")
    for f in findings:
        lines.append(f"- **`{f.field_name}`** ({f.severity}): {f.excess_factor}")

    lines.append("")
    lines.append("---")
    lines.append("*Análisis determinista ejecutado con schema_minimization_checker.py v1.0*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic PII Schema and Data Minimization Auditor (ISO/IEC 27701:2025 & ISO/IEC 20889)"
    )
    parser.add_argument("path", help="Path to SQL DDL file, JSON file, or directory containing schemas")
    parser.add_argument("--purpose", help="Declared business purpose for the data (used for context evaluation)", default=None)
    parser.add_argument("--min-risk", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"], default="LOW", help="Minimum severity level to report")
    parser.add_argument("--json", action="store_true", help="Output findings in machine-readable JSON format")

    args = parser.parse_args()
    target_path = Path(args.path)

    if not target_path.exists():
        sys.stderr.write(f"Error: Target path does not exist: {target_path}\n")
        sys.exit(2)

    findings: List[SchemaAuditFinding] = []

    if target_path.is_file():
        findings = audit_file(target_path)
    elif target_path.is_dir():
        for ext in ["*.sql", "*.ddl", "*.json"]:
            for f in target_path.rglob(ext):
                findings.extend(audit_file(f))

    filtered_findings = filter_by_risk(findings, args.min_risk)

    if args.json:
        output_data = {
            "standards": ["ISO/IEC 27701:2025", "ISO/IEC 20889:2018"],
            "target": str(target_path),
            "declared_purpose": args.purpose,
            "min_risk_filter": args.min_risk,
            "total_findings": len(filtered_findings),
            "findings": [f.to_dict() for f in filtered_findings]
        }
        print(json.dumps(output_data, indent=2, ensure_ascii=False))
    else:
        print(format_text_report(filtered_findings, args.purpose))

    # Exit with code 1 if critical issues were detected, else 0
    if any(f.severity == "CRITICAL" for f in filtered_findings):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
