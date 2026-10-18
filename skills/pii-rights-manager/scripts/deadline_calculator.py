#!/usr/bin/env python3
"""
deadline_calculator.py - Deterministic DSAR / ARCO Deadline and Expiration Tracker
Compliant with ISO/IEC 27701:2025 (A.1.3, A.1.3.7, A.1.3.10) and multi-jurisdictional privacy laws.

Calculates:
- Statutory response deadlines based on jurisdiction, request date, and exercised right.
- Extension limits for complex requests.
- Business days vs calendar days adjustment (including weekend rollover).
- Expiration alerts (CRITICAL, WARNING, ON_TRACK, EXPIRED) relative to an audit/current date.
"""

import sys
import os
import json
import csv
import argparse
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional, Tuple


# Jurisdiction Rules Configuration
# counting: 'calendar' | 'business' | 'month'
JURISDICTION_RULES: Dict[str, Dict[str, Any]] = {
    "GDPR": {
        "name": "General Data Protection Regulation (EU 2016/679)",
        "default": {"days": 1, "counting": "month", "extension_days": 2, "extension_counting": "month"},
    },
    "RGPD": {
        "name": "Reglamento General de Protección de Datos (UE)",
        "default": {"days": 1, "counting": "month", "extension_days": 2, "extension_counting": "month"},
    },
    "CCPA": {
        "name": "California Consumer Privacy Act / CPRA",
        "default": {"days": 45, "counting": "calendar", "extension_days": 45, "extension_counting": "calendar"},
    },
    "LGPD": {
        "name": "Lei Geral de Proteção de Dados (Brazil)",
        "access_simplified": {"days": 0, "counting": "calendar", "extension_days": 0, "extension_counting": "calendar"},
        "default": {"days": 15, "counting": "calendar", "extension_days": 0, "extension_counting": "calendar"},
    },
    "MX_LFPDPPP": {
        "name": "Ley Federal de Protección de Datos Personales (México)",
        "default": {"days": 20, "counting": "business", "extension_days": 20, "extension_counting": "business"},
    },
    "CO_LEY1581": {
        "name": "Ley 1581 de 2012 (Colombia)",
        "access": {"days": 10, "counting": "business", "extension_days": 5, "extension_counting": "business"},
        "rectification": {"days": 15, "counting": "business", "extension_days": 8, "extension_counting": "business"},
        "erasure": {"days": 15, "counting": "business", "extension_days": 8, "extension_counting": "business"},
        "default": {"days": 15, "counting": "business", "extension_days": 8, "extension_counting": "business"},
    },
    "PE_LEY29733": {
        "name": "Ley 29733 de Protección de Datos Personales (Perú)",
        "access": {"days": 20, "counting": "business", "extension_days": 20, "extension_counting": "business"},
        "rectification": {"days": 10, "counting": "business", "extension_days": 10, "extension_counting": "business"},
        "erasure": {"days": 10, "counting": "business", "extension_days": 10, "extension_counting": "business"},
        "objection": {"days": 10, "counting": "business", "extension_days": 10, "extension_counting": "business"},
        "default": {"days": 10, "counting": "business", "extension_days": 10, "extension_counting": "business"},
    },
    "AR_LEY25326": {
        "name": "Ley 25.326 de Protección de los Datos Personales (Argentina)",
        "access": {"days": 10, "counting": "calendar", "extension_days": 0, "extension_counting": "calendar"},
        "rectification": {"days": 5, "counting": "business", "extension_days": 0, "extension_counting": "business"},
        "erasure": {"days": 5, "counting": "business", "extension_days": 0, "extension_counting": "business"},
        "default": {"days": 10, "counting": "calendar", "extension_days": 0, "extension_counting": "calendar"},
    },
    "CL_LEY19628": {
        "name": "Ley 19.628 Sobre Protección de la Vida Privada (Chile)",
        "default": {"days": 2, "counting": "business", "extension_days": 0, "extension_counting": "business"},
    },
}


def add_months(source_date: date, months: int) -> date:
    """Add integer months to a date, pinning to the last day of the target month if needed."""
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    # Handle end of month boundary
    days_in_month = [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
                     31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    max_day = days_in_month[month - 1]
    day = min(source_date.day, max_day)
    return date(year, month, day)


def add_business_days(start_date: date, num_days: int) -> date:
    """Add business days (excluding Saturdays and Sundays)."""
    current = start_date
    added = 0
    while added < num_days:
        current += timedelta(days=1)
        # 0 = Monday, ..., 5 = Saturday, 6 = Sunday
        if current.weekday() < 5:
            added += 1
    return current


def adjust_to_next_business_day(target_date: date) -> date:
    """If target_date falls on a weekend, roll over to the following Monday."""
    if target_date.weekday() == 5:  # Saturday
        return target_date + timedelta(days=2)
    elif target_date.weekday() == 6:  # Sunday
        return target_date + timedelta(days=1)
    return target_date


def calculate_deadline(
    received_date: date,
    jurisdiction: str,
    right_type: str = "access",
    with_extension: bool = False
) -> Dict[str, Any]:
    """Calculate statutory deadline and extension deadline for a specific request."""
    jurisdiction_key = jurisdiction.upper()
    if jurisdiction_key not in JURISDICTION_RULES:
        # Fallback to standard 30 calendar days
        rule_set = {"days": 30, "counting": "calendar", "extension_days": 30, "extension_counting": "calendar"}
        jurisdiction_name = f"Custom / Fallback ({jurisdiction})"
    else:
        config = JURISDICTION_RULES[jurisdiction_key]
        jurisdiction_name = config.get("name", jurisdiction_key)
        normalized_right = right_type.lower().strip()
        rule_set = config.get(normalized_right, config.get("default", {"days": 30, "counting": "calendar", "extension_days": 0, "extension_counting": "calendar"}))

    # Base deadline calculation
    counting_type = rule_set.get("counting", "calendar")
    base_days = rule_set.get("days", 30)

    if counting_type == "month":
        raw_deadline = add_months(received_date, base_days)
    elif counting_type == "business":
        raw_deadline = add_business_days(received_date, base_days)
    else:  # calendar
        raw_deadline = received_date + timedelta(days=base_days)

    final_statutory_deadline = adjust_to_next_business_day(raw_deadline)

    # Extension calculation
    ext_days = rule_set.get("extension_days", 0)
    ext_counting = rule_set.get("extension_counting", counting_type)

    if ext_days > 0:
        if ext_counting == "month":
            raw_ext = add_months(final_statutory_deadline, ext_days)
        elif ext_counting == "business":
            raw_ext = add_business_days(final_statutory_deadline, ext_days)
        else:
            raw_ext = final_statutory_deadline + timedelta(days=ext_days)
        final_extension_deadline = adjust_to_next_business_day(raw_ext)
    else:
        final_extension_deadline = final_statutory_deadline

    effective_deadline = final_extension_deadline if with_extension else final_statutory_deadline

    return {
        "jurisdiction": jurisdiction_key,
        "jurisdiction_name": jurisdiction_name,
        "right_type": right_type,
        "received_date": received_date.isoformat(),
        "statutory_days_allowed": base_days,
        "counting_mode": counting_type,
        "statutory_deadline": final_statutory_deadline.isoformat(),
        "extension_available": ext_days > 0,
        "extension_days_allowed": ext_days,
        "extended_deadline": final_extension_deadline.isoformat() if ext_days > 0 else None,
        "with_extension_applied": with_extension,
        "effective_deadline": effective_deadline.isoformat()
    }


def evaluate_status(effective_deadline_str: str, as_of_date: date) -> Dict[str, Any]:
    """Evaluate days remaining and urgency status relative to an evaluation date."""
    target = date.fromisoformat(effective_deadline_str)
    delta_days = (target - as_of_date).days

    if delta_days < 0:
        status = "EXPIRED"
        severity = "Crítica"
        message = f"Vencido hace {abs(delta_days)} días. Posible infracción de A.1.3.10 / A.1.3.7."
    elif delta_days <= 3:
        status = "CRITICAL"
        severity = "Alta"
        message = f"Plazo crítico: restan {delta_days} días naturales para respuesta obligatoria."
    elif delta_days <= 7:
        status = "WARNING"
        severity = "Media"
        message = f"Alerta preventiva: restan {delta_days} días para vencimiento."
    else:
        status = "ON_TRACK"
        severity = "Baja"
        message = f"En plazo regular: restan {delta_days} días."

    return {
        "as_of_date": as_of_date.isoformat(),
        "days_remaining": delta_days,
        "status": status,
        "severity": severity,
        "alert_message": message
    }


def process_record(item: Dict[str, Any], as_of_date: date) -> Dict[str, Any]:
    """Process a single DSAR request record."""
    req_id = item.get("id") or item.get("request_id") or "DSAR-UNKNOWN"
    date_str = item.get("date") or item.get("received_date") or as_of_date.isoformat()
    jurisdiction = item.get("jurisdiction") or "GDPR"
    right_type = item.get("right") or item.get("right_type") or "access"
    extended = bool(item.get("extended") or item.get("with_extension") or False)

    try:
        rec_date = date.fromisoformat(str(date_str).strip())
    except ValueError:
        rec_date = as_of_date

    deadline_info = calculate_deadline(rec_date, jurisdiction, right_type, extended)
    status_info = evaluate_status(deadline_info["effective_deadline"], as_of_date)

    result = {
        "request_id": req_id,
        **deadline_info,
        **status_info
    }
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Calculadora determinista de plazos de atención y vencimiento DSAR / ARCO (ISO 27701:2025)."
    )
    parser.add_argument("--date", type=str, help="Fecha de recepción (YYYY-MM-DD). Por defecto: hoy.")
    parser.add_argument("--jurisdiction", type=str, default="GDPR", help="Jurisdicción (GDPR, CCPA, LGPD, MX_LFPDPPP, CO_LEY1581, PE_LEY29733, AR_LEY25326, CL_LEY19628).")
    parser.add_argument("--right", type=str, default="access", help="Tipo de derecho (access, rectification, erasure, objection, portability).")
    parser.add_argument("--extended", action="store_true", help="Aplica la prórroga legal justificada.")
    parser.add_argument("--as-of", type=str, help="Fecha de auditoría/cálculo relativo (YYYY-MM-DD). Por defecto: hoy.")
    parser.add_argument("--input", type=str, help="Ruta a archivo JSON o CSV con lote de solicitudes a evaluar.")
    parser.add_argument("--output", type=str, help="Ruta para guardar resultados en formato JSON.")
    parser.add_argument("--format", choices=["json", "table"], default="table", help="Formato de salida en consola.")

    args = parser.parse_args()

    as_of_date = date.fromisoformat(args.as_of) if args.as_of else date.today()

    if args.input:
        if not os.path.exists(args.input):
            print(f"Error: El archivo de entrada '{args.input}' no existe.", file=sys.stderr)
            sys.exit(1)

        records = []
        if args.input.endswith(".json"):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                records = raw_data if isinstance(raw_data, list) else [raw_data]
        elif args.input.endswith(".csv"):
            with open(args.input, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                records = [row for row in reader]

        results = [process_record(r, as_of_date) for r in records]
    else:
        rec_date = date.fromisoformat(args.date) if args.date else date.today()
        single_item = {
            "id": "REQ-001",
            "date": rec_date.isoformat(),
            "jurisdiction": args.jurisdiction,
            "right": args.right,
            "extended": args.extended
        }
        results = [process_record(single_item, as_of_date)]

    # Format output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({"as_of_date": as_of_date.isoformat(), "total_evaluated": len(results), "requests": results}, f, indent=2, ensure_ascii=False)
        print(f"[OK] Reporte exportado a: {args.output}")

    if args.format == "json":
        print(json.dumps({"requests": results}, indent=2, ensure_ascii=False))
    else:
        print("\n=== REPORTE DE PLAZOS Y ESTADO DE SOLICITUDES DSAR / ARCO ===")
        print(f"Fecha de corte de auditoría: {as_of_date.isoformat()}\n")
        header = f"{'ID Solicitud':<14} | {'Jurisd.':<10} | {'Derecho':<12} | {'Recepción':<10} | {'Fecha Límite':<12} | {'Días':<5} | {'Estado':<10} | {'Severidad':<10}"
        print(header)
        print("-" * len(header))
        for r in results:
            print(f"{r['request_id']:<14} | {r['jurisdiction']:<10} | {r['right_type']:<12} | {r['received_date']:<10} | {r['effective_deadline']:<12} | {r['days_remaining']:<5} | {r['status']:<10} | {r['severity']:<10}")
        print("\n" + "=" * len(header) + "\n")

    # Exit code: 0 if no expired, 2 if expired requests found
    has_expired = any(r["status"] == "EXPIRED" for r in results)
    sys.exit(2 if has_expired else 0)


if __name__ == "__main__":
    main()
