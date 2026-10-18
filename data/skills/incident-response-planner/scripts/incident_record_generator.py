#!/usr/bin/env python3
"""
incident_record_generator.py - Generador Determinista de Registros de Brechas PII
Conforme a ISO/IEC 27701:2025 Controles A.3.11, A.3.12, A.3.14, A.3.25 y Guías B.3.11, B.3.12.

Este script procesa, valida y genera registros formales de incidentes de seguridad
con afectación de PII en formatos JSON y Markdown estructurado, verificando el
cumplimiento exhaustivo de todos los campos mandatorios de evidencia probatoria
exigidos por la norma y calculando la ventana de cumplimiento de notificación (72h).
"""

import sys
import os
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

# Definición de campos mandatorios bajo ISO/IEC 27701:2025 B.3.12
MANDATORY_B312_FIELDS = {
    "incident_id": "Identificador único del expediente de incidente",
    "description": "Descripción detallada de la naturaleza del incidente",
    "time_period": "Cronología completa (detección, ocurrencia, confirmación)",
    "reporter": "Nombre y datos del informante inicial",
    "reported_to": "Personas / Órganos a quienes se reportó el incidente (CSIRT/DPO)",
    "impact_classification": "Afectación expresa a Confidencialidad, Integridad y/o Disponibilidad",
    "pii_compromised": "Categorías y volumen estimado de PII comprometida",
    "consequences": "Consecuencias e impactos observados o potenciales",
    "resolution_steps": "Medidas de contención, erradicación y resolución con responsable",
    "notifications": "Registro formal de notificaciones (Autoridades, Titulares, Clientes)"
}


def parse_iso_datetime(dt_str: str) -> Optional[datetime]:
    """Parsea una cadena de fecha/hora en formato ISO 8601 a un objeto datetime con zona horaria."""
    if not dt_str:
        return None
    try:
        # Reemplazar sufijo Z por +00:00 para compatibilidad estándar
        clean_str = dt_str.strip().replace("Z", "+00:00")
        return datetime.fromisoformat(clean_str)
    except Exception:
        # Fallback a formatos comunes
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(dt_str.strip(), fmt)
                return dt.replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        return None


def calculate_72h_compliance(confirmation_dt_str: str, notification_dt_str: Optional[str]) -> Dict[str, Any]:
    """Calcula las horas transcurridas y verifica el cumplimiento del plazo de 72 horas."""
    conf_dt = parse_iso_datetime(confirmation_dt_str)
    if not conf_dt:
        return {
            "status": "ERROR",
            "hours_elapsed": None,
            "message": "Fecha de confirmación inválida o ausente."
        }

    if not notification_dt_str:
        now_dt = datetime.now(timezone.utc)
        diff = (now_dt - conf_dt).total_seconds() / 3600.0
        remaining = 72.0 - diff
        return {
            "status": "PENDING",
            "hours_elapsed": round(diff, 2),
            "hours_remaining": round(remaining, 2),
            "is_breached": diff > 72.0,
            "message": f"Notificación aún no efectuada. Horas transcurridas: {diff:.1f}h. "
                       f"{'PLAZO DE 72H SUPERADO' if diff > 72 else f'Quedan {remaining:.1f}h'}"
        }

    notif_dt = parse_iso_datetime(notification_dt_str)
    if not notif_dt:
        return {
            "status": "ERROR",
            "hours_elapsed": None,
            "message": "Fecha de notificación provista inválida."
        }

    diff = (notif_dt - conf_dt).total_seconds() / 3600.0
    compliant = diff <= 72.0
    return {
        "status": "COMPLIANT" if compliant else "NON_COMPLIANT",
        "hours_elapsed": round(diff, 2),
        "is_compliant": compliant,
        "message": f"Notificado en {diff:.1f} horas. "
                   f"{'CONFORME con el límite de 72h' if compliant else 'NO CONFORME: Excedió el plazo de 72h'}"
    }


def validate_incident_record(data: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    """Valida la completitud de la estructura del registro contra ISO/IEC 27701:2025 B.3.12."""
    missing_fields = []
    audit_notes = {}

    for field, desc in MANDATORY_B312_FIELDS.items():
        if field not in data or data[field] is None or data[field] == "" or data[field] == {}:
            missing_fields.append(f"{field} ({desc})")

    # Validación detallada de subcampos críticos
    time_p = data.get("time_period", {})
    conf_dt = time_p.get("confirmed_at")
    if not conf_dt:
        missing_fields.append("time_period.confirmed_at (Fecha/hora de confirmación formal)")

    impact = data.get("impact_classification", {})
    if not any(k in impact for k in ("confidentiality", "integrity", "availability")):
        missing_fields.append("impact_classification (Debe indicar afectación a confidencialidad, integridad o disponibilidad)")

    # Evaluación de 72h de la autoridad
    notifs = data.get("notifications", {})
    auth_notif = notifs.get("supervisory_authority", {})
    auth_dt = auth_notif.get("notified_at")
    calc_res = calculate_72h_compliance(conf_dt or "", auth_dt)
    audit_notes["regulatory_72h_compliance"] = calc_res

    # Validación de cadena de custodia (A.3.14)
    forensic = data.get("forensic_evidence_preservation", {})
    audit_notes["forensic_custody_compliant"] = bool(forensic.get("chain_of_custody_logged", False))

    # Validación de resiliencia y respaldos (A.3.25)
    backup_info = data.get("backup_restoration_verification", {})
    audit_notes["backup_verification_logged"] = bool(backup_info.get("backup_integrity_verified", False))

    is_valid = len(missing_fields) == 0
    return is_valid, missing_fields, audit_notes


def generate_sample_incident_data() -> Dict[str, Any]:
    """Genera un caso de uso realista de incidente de ransomware y exfiltración de PII."""
    return {
        "incident_id": "INC-20261001-0842",
        "title": "Ataque de Ransomware con Exfiltración de Base de Datos de Clientes y Nómina",
        "organization": {
            "name": "Financiera Global S.A.",
            "role": "PII Controller",
            "dpo_contact": "dpo@financieraglobal.example.com"
        },
        "time_period": {
            "occurred_at": "2026-09-30T18:20:00Z",
            "detected_at": "2026-10-01T02:15:00Z",
            "confirmed_at": "2026-10-01T04:30:00Z",
            "contained_at": "2026-10-01T07:45:00Z",
            "resolved_at": None,
            "status": "CONTENIDO - EN PROCESO DE RESTAURACIÓN Y FORENSE"
        },
        "reporter": {
            "name": "Carlos Mendoza",
            "role": "Analista Senior SOC Nivel 2",
            "reporting_channel": "Alerta SIEM automatizada + Escalamiento telefónico de emergencia"
        },
        "reported_to": {
            "body": "Equipo de Respuesta a Incidentes de Privacidad (CSIRT / CIRT)",
            "primary_lead": "Elena Valenzuela (CISO) y Roberto Arismendi (DPO)"
        },
        "description": "Se detectó movimiento lateral y ejecución de ransomware tipo BlackByte sobre dos servidores "
                       "de bases de datos. Los atacantes comprometieron credenciales privilegiadas de VPN y lograron "
                       "exfiltrar fragmentos de tablas antes de cifrar los volúmenes de almacenamiento.",
        "root_cause_and_vulnerabilities": "Explotación de credencial de acceso remoto sin segundo factor (MFA) "
                                          "en cuenta de servicio huérfana y falta de segmentación estricta de red interna.",
        "impact_classification": {
            "confidentiality": {
                "impacted": True,
                "detail": "Exfiltración confirmada de 1.8 GB de tablas con datos de clientes."
            },
            "integrity": {
                "impacted": False,
                "detail": "No se evidenció alteración ni corrupción de transacciones previas al cifrado."
            },
            "availability": {
                "impacted": True,
                "detail": "Indisponibilidad temporal del sistema de gestión durante 5 horas tras el cifrado."
            }
        },
        "pii_compromised": {
            "estimated_principals_affected": 12500,
            "estimated_records_affected": 45000,
            "categories": [
                "Nombres y apellidos completos",
                "Números de documento de identidad (DNI / RFC)",
                "Correos electrónicos y números de teléfono",
                "Datos bancarios (números de cuenta CLABE / IBAN sin CVV)",
                "Datos de salarios de empleados"
            ],
            "sensitive_data_involved": True,
            "sensitive_data_description": "Datos económicos y salarios de 350 empleados internos."
        },
        "consequences": {
            "impact_on_principals": "Riesgo alto de phishing dirigido, intentos de extorsión y fraude financiero.",
            "impact_on_organization": "Afectación reputacional temporal, suspensión preventiva de servicios en línea y costos forenses.",
            "overall_risk_level": "Alto"
        },
        "forensic_evidence_preservation": {
            "chain_of_custody_logged": True,
            "custodian_name": "Ing. Fernando Morales (Perito Forense Digital)",
            "actions_taken": [
                "Volcado de memoria RAM previo al aislamiento lógico.",
                "Clonación forense bit a bit de los discos virtuales en formato raw/dd.",
                "Cálculo y depósito de hashes criptográficos SHA-256 de todas las imágenes.",
                "Extracción y congelamiento inmutable de registros de syslog y firewall (Control A.3.14)."
            ]
        },
        "backup_restoration_verification": {
            "backup_integrity_verified": True,
            "backup_technology": "Repositorio inmutable fuera de línea (Air-gapped) con snapshots WORM",
            "data_recovered": "100% de la base de datos operativa restaurada a las 06:30Z (Control A.3.25)",
            "rto_achieved_hours": 4.25
        },
        "resolution_steps": [
            {
                "step": "Aislamiento inmediato de los servidores afectados del resto de la LAN/WAN",
                "responsible": "Carlos Mendoza (SOC)",
                "timestamp": "2026-10-01T02:40:00Z"
            },
            {
                "step": "Revocación masiva de credenciales de acceso remoto y tokens de sesión activos",
                "responsible": "Marcos Silva (Administrador de Directorio Activo)",
                "timestamp": "2026-10-01T03:00:00Z"
            },
            {
                "step": "Verificación y escaneo de integridad de copias de seguridad inmutables",
                "responsible": "Laura Gómez (Infraestructura y Backup)",
                "timestamp": "2026-10-01T05:00:00Z"
            },
            {
                "step": "Reinstalación limpia del sistema operativo y restauración desde copia saneada",
                "responsible": "Laura Gómez (Infraestructura)",
                "timestamp": "2026-10-01T06:30:00Z"
            }
        ],
        "notifications": {
            "supervisory_authority": {
                "required": True,
                "authority_name": "Agencia de Protección de Datos Competente",
                "notified_at": "2026-10-01T11:00:00Z",
                "status": "NOTIFICACIÓN INICIAL ENVIADA (FASE 1)",
                "official_ticket_reference": "EXP-APD-2026-98124",
                "delay_justification": None
            },
            "data_subjects": {
                "required": True,
                "reason": "Riesgo alto para derechos y libertades debido a datos bancarios y salarios expuestos",
                "notified_at": None,
                "status": "EN PREPARACIÓN - ENVÍO PROGRAMADO PARA HOY 16:00Z",
                "communication_channel": "Correo electrónico directo individual y portal de ayuda al cliente"
            },
            "corporate_customers_processors": {
                "required": False,
                "detail": "No aplica; la entidad actúa como Responsable Directo."
            }
        },
        "post_mortem_and_lessons_learned": {
            "review_meeting_date": "2026-10-01T14:00:00Z",
            "action_items": [
                {
                    "action": "Obligatoriedad incondicional de MFA en el 100% de accesos VPN y cuentas de servicio",
                    "owner": "CISO",
                    "deadline": "2026-10-03"
                },
                {
                    "action": "Segmentación micro-granular de VLANs de base de datos con reglas Zero-Trust",
                    "owner": "Jefe de Redes",
                    "deadline": "2026-10-15"
                },
                {
                    "action": "Actualización del análisis de riesgos del SGIP (Cláusulas 6.1.2 y 8.2)",
                    "owner": "DPO",
                    "deadline": "2026-10-20"
                }
            ]
        }
    }


def format_incident_markdown(data: Dict[str, Any], audit_notes: Dict[str, Any]) -> str:
    """Genera el informe formal en formato Markdown con estructura aprobada para auditorías ISO 27701."""
    time_p = data.get("time_period", {})
    impact = data.get("impact_classification", {})
    pii = data.get("pii_compromised", {})
    notifs = data.get("notifications", {})
    auth_notif = notifs.get("supervisory_authority", {})
    subjects_notif = notifs.get("data_subjects", {})
    compliance_72h = audit_notes.get("regulatory_72h_compliance", {})

    lines = [
        f"# Expediente Formal de Brecha de Datos Personales (PII Breach Record)",
        f"",
        f"- **ID del Incidente**: `{data.get('incident_id', 'N/A')}`",
        f"- **Título**: {data.get('title', 'Sin título')}",
        f"- **Norma de Referencia**: ISO/IEC 27701:2025 Controles A.3.11, A.3.12 y Guía B.3.12",
        f"- **Entidad**: {data.get('organization', {}).get('name', 'N/A')} (Rol: {data.get('organization', {}).get('role', 'N/A')})",
        f"- **DPO / Contacto**: {data.get('organization', {}).get('dpo_contact', 'N/A')}",
        f"- **Fecha de Emisión del Expediente**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"",
        f"---",
        f"",
        f"## 1. Cronología Oficial del Incidente (B.3.12)",
        f"",
        f"| Hito Temporal | Marca de Tiempo (UTC) | Notas de Auditoría |",
        f"|---|---|---|",
        f"| **Ocurrencia Estimada** | `{time_p.get('occurred_at', 'Desconocido')}` | Inicio presunto del vector de ataque |",
        f"| **Detección Inicial** | `{time_p.get('detected_at', 'N/A')}` | Detección por monitorización / reporte |",
        f"| **Confirmación Formal de Brecha PII** | `{time_p.get('confirmed_at', 'N/A')}` | **Punto de inicio para el cómputo de 72 horas** |",
        f"| **Contención Técnica** | `{time_p.get('contained_at', 'Pendiente')}` | Aislamiento y neutralización de la amenaza |",
        f"| **Resolución y Cierre** | `{time_p.get('resolved_at', 'En curso')}` | Estado: {time_p.get('status', 'N/A')} |",
        f"",
        f"### Verificación de Plazo Legal de Notificación (Regla de 72 Horas)",
        f"- **Horas transcurridas hasta notificación**: `{compliance_72h.get('hours_elapsed', 'N/A')}` horas.",
        f"- **Dictamen de Cumplimiento**: **{compliance_72h.get('status', 'N/A')}** ({compliance_72h.get('message', '')})",
        f"",
        f"---",
        f"",
        f"## 2. Identificación del Informante y Receptores (B.3.12)",
        f"",
        f"- **Informante**: {data.get('reporter', {}).get('name', 'N/A')} ({data.get('reporter', {}).get('role', 'N/A')})",
        f"- **Canal de Reporte**: {data.get('reporter', {}).get('reporting_channel', 'N/A')}",
        f"- **Órgano Receptor Interno**: {data.get('reported_to', {}).get('body', 'N/A')}",
        f"- **Líderes de Respuesta**: {data.get('reported_to', {}).get('primary_lead', 'N/A')}",
        f"",
        f"---",
        f"",
        f"## 3. Naturaleza, Causa Raíz y Afectación de Seguridad de la Información (B.3.12)",
        f"",
        f"### 3.1 Descripción de los Hechos y Causa Raíz",
        f"{data.get('description', 'Sin descripción')}",
        f"",
        f"**Causa Raíz / Vulnerabilidad Explotada**: {data.get('root_cause_and_vulnerabilities', 'En investigación')}",
        f"",
        f"### 3.2 Clasificación de la Afectación a la PII (Tríada CIA)",
        f"",
        f"| Dimensión de Seguridad | ¿Afectada? | Detalle de la Evidencia |",
        f"|---|---|---|",
        f"| **Confidencialidad** (Divulgación / Acceso No Autorizado) | `{'SÍ' if impact.get('confidentiality', {}).get('impacted') else 'NO'}` | {impact.get('confidentiality', {}).get('detail', 'N/A')} |",
        f"| **Integridad** (Alteración / Falsificación) | `{'SÍ' if impact.get('integrity', {}).get('impacted') else 'NO'}` | {impact.get('integrity', {}).get('detail', 'N/A')} |",
        f"| **Disponibilidad** (Pérdida / Destrucción / Cifrado) | `{'SÍ' if impact.get('availability', {}).get('impacted') else 'NO'}` | {impact.get('availability', {}).get('detail', 'N/A')} |",
        f"",
        f"---",
        f"",
        f"## 4. Alcance y Categorías de PII Comprometidas (B.3.12)",
        f"",
        f"- **Número Estimado de Titulares Afectados**: `{pii.get('estimated_principals_affected', 'N/A'):,}` personas",
        f"- **Número Estimado de Registros Involucrados**: `{pii.get('estimated_records_affected', 'N/A'):,}` registros",
        f"- **¿Involucra Datos Sensibles / Especiales?**: `{'SÍ' if pii.get('sensitive_data_involved') else 'NO'}`",
        f"- **Detalle de Datos Sensibles**: {pii.get('sensitive_data_description', 'Ninguno')}",
        f"",
        f"**Categorías Específicas de PII Identificadas**:",
    ]

    for cat in pii.get("categories", []):
        lines.append(f"- {cat}")

    conseq = data.get("consequences", {})
    lines.extend([
        f"",
        f"---",
        f"",
        f"## 5. Evaluación de Consecuencias y Nivel de Riesgo (B.3.11 / B.3.12)",
        f"",
        f"- **Nivel Global de Riesgo para los Titulares**: **{conseq.get('overall_risk_level', 'N/A')}**",
        f"- **Consecuencias para los Titulares**: {conseq.get('impact_on_principals', 'N/A')}",
        f"- **Consecuencias para la Organización**: {conseq.get('impact_on_organization', 'N/A')}",
        f"",
        f"---",
        f"",
        f"## 6. Preservación Forense y Resiliencia de Respaldos (A.3.14 y A.3.25)",
        f"",
        f"### 6.1 Cadena de Custodia y Evidencias Digitales (A.3.14)",
        f"- **Registro de Cadena de Custodia**: `{'ACTIVO Y CONFORME' if audit_notes.get('forensic_custody_compliant') else 'DEFICIENTE / PENDIENTE'}`",
        f"- **Custodio Asignado**: {data.get('forensic_evidence_preservation', {}).get('custodian_name', 'N/A')}",
        f"- **Acciones de Preservación Ejecutadas**:"
    ])

    for act in data.get("forensic_evidence_preservation", {}).get("actions_taken", []):
        lines.append(f"  * {act}")

    lines.extend([
        f"",
        f"### 6.2 Resiliencia y Restauración desde Backups (A.3.25)",
        f"- **Verificación de Integridad de Respaldos**: `{'VERIFICADO' if audit_notes.get('backup_verification_logged') else 'NO VERIFICADO'}`",
        f"- **Tecnología de Respaldo**: {data.get('backup_restoration_verification', {}).get('backup_technology', 'N/A')}",
        f"- **Datos Recuperados**: {data.get('backup_restoration_verification', {}).get('data_recovered', 'N/A')}",
        f"- **RTO Logrado**: {data.get('backup_restoration_verification', {}).get('rto_achieved_hours', 'N/A')} horas",
        f"",
        f"---",
        f"",
        f"## 7. Pasos de Resolución y Mitigación Adoptados (B.3.12)",
        f"",
        f"| Paso / Acción Ejecutada | Responsable Asignado | Marca de Tiempo (UTC) |",
        f"|---|---|---|",
    ])

    for step in data.get("resolution_steps", []):
        lines.append(f"| {step.get('step', 'N/A')} | {step.get('responsible', 'N/A')} | `{step.get('timestamp', 'N/A')}` |")

    lines.extend([
        f"",
        f"---",
        f"",
        f"## 8. Registro de Notificaciones Realizadas (B.3.11 / B.3.12)",
        f"",
        f"### 8.1 Notificación a la Autoridad de Supervisión",
        f"- **Exigibilidad**: `{'OBLIGATORIA' if auth_notif.get('required') else 'NO EXIGIBLE'}`",
        f"- **Autoridad**: {auth_notif.get('authority_name', 'N/A')}",
        f"- **Fecha/Hora de Envío**: `{auth_notif.get('notified_at', 'Pendiente')}`",
        f"- **Estado / Expediente**: {auth_notif.get('status', 'N/A')} (Ref: `{auth_notif.get('official_ticket_reference', 'N/A')}`)",
        f"",
        f"### 8.2 Notificación a los Titulares de PII",
        f"- **Exigibilidad**: `{'OBLIGATORIA (Alto Riesgo)' if subjects_notif.get('required') else 'NO REQUERIDA (Riesgo Bajo)'}`",
        f"- **Fundamento**: {subjects_notif.get('reason', 'N/A')}",
        f"- **Estado y Canal**: {subjects_notif.get('status', 'N/A')} | Canal: {subjects_notif.get('communication_channel', 'N/A')}",
        f"",
        f"---",
        f"",
        f"## 9. Lecciones Aprendidas y Acciones Preventivas Post-Mortem (A.3.12)",
        f"",
        f"- **Fecha de Sesión de Revisión**: `{data.get('post_mortem_and_lessons_learned', {}).get('review_meeting_date', 'Pendiente')}`",
        f"",
        f"| Acción Preventiva / Correctiva | Responsable | Fecha Límite |",
        f"|---|---|---|",
    ])

    for item in data.get("post_mortem_and_lessons_learned", {}).get("action_items", []):
        lines.append(f"| {item.get('action', 'N/A')} | {item.get('owner', 'N/A')} | `{item.get('deadline', 'N/A')}` |")

    lines.extend([
        f"",
        f"---",
        f"*Expediente archivado conforme al Control A.3.14 (Protección de Registros del SGIP) con retención mínima reglamentaria.*"
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generador determinista del registro formal de incidentes PII bajo ISO/IEC 27701:2025 B.3.12"
    )
    parser.add_argument("--input", "-i", type=str, help="Ruta al archivo JSON con datos del incidente")
    parser.add_argument("--sample", "-s", action="store_true", help="Generar un caso de uso de muestra realista")
    parser.add_argument("--output-json", "-oj", type=str, help="Ruta para guardar el expediente formal en JSON")
    parser.add_argument("--output-md", "-om", type=str, help="Ruta para guardar el informe de auditoría en Markdown")
    parser.add_argument("--validate", "-v", action="store_true", help="Validar completitud contra requisitos ISO 27701 B.3.12")

    args = parser.parse_args()

    if not args.input and not args.sample:
        parser.print_help()
        print("\n[ERROR] Debe especificar un archivo de entrada (--input) o utilizar la opción de muestra (--sample).")
        sys.exit(1)

    # Carga de datos
    if args.sample:
        data = generate_sample_incident_data()
        print("[INFO] Generando expediente a partir del caso de muestra de alta fidelidad.")
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"[ERROR] El archivo de entrada no existe: {input_path}")
            sys.exit(1)
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    # Validación
    is_valid, missing, audit_notes = validate_incident_record(data)

    print("================================================================================")
    print(" EVALUACIÓN DE CONFORMIDAD DE EXPEDIENTE - ISO/IEC 27701:2025 B.3.12")
    print("================================================================================")
    print(f"ID Incidente: {data.get('incident_id', 'N/A')}")
    print(f"Título:       {data.get('title', 'N/A')}")
    print(f"Estado B.3.12: {'CONFORME (100% de campos mandatorios)' if is_valid else 'NO CONFORME'}")

    if not is_valid:
        print("\n[ALERTA] Campos mandatorios ausentes o incompletos:")
        for m in missing:
            print(f"  - [FALTANTE] {m}")
    else:
        print("[OK] Todos los campos de evidencia requeridos por B.3.12 están presentes.")

    # Estado de la ventana de 72 horas
    calc = audit_notes.get("regulatory_72h_compliance", {})
    print(f"\n[CONTROL REGULATORIO 72H]: Status: {calc.get('status')} | {calc.get('message')}")
    print(f"[CONTROL A.3.14 - FORENSE]: Cadena de custodia registrada: {'SÍ' if audit_notes.get('forensic_custody_compliant') else 'NO'}")
    print(f"[CONTROL A.3.25 - BACKUP]:  Integridad de copias de seguridad: {'SÍ' if audit_notes.get('backup_verification_logged') else 'NO'}")
    print("================================================================================\n")

    # Guardar salidas
    if args.output_json:
        out_json_path = Path(args.output_json)
        out_json_path.parent.mkdir(parents=True, exist_ok=True)
        export_payload = {
            "metadata": {
                "standard": "ISO/IEC 27701:2025",
                "controls": ["A.3.11", "A.3.12", "A.3.14", "A.3.25", "B.3.11", "B.3.12"],
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "is_audit_compliant": is_valid
            },
            "audit_evaluation": audit_notes,
            "incident_record": data
        }
        with open(out_json_path, "w", encoding="utf-8") as f:
            json.dump(export_payload, f, indent=2, ensure_ascii=False)
        print(f"[OK] Expediente JSON guardado en: {out_json_path.resolve()}")

    if args.output_md:
        out_md_path = Path(args.output_md)
        out_md_path.parent.mkdir(parents=True, exist_ok=True)
        md_content = format_incident_markdown(data, audit_notes)
        with open(out_md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"[OK] Reporte Markdown guardado en: {out_md_path.resolve()}")

    if not is_valid and args.validate:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
