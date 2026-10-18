#!/usr/bin/env python3
"""
consent_flow_checker.py - Deterministic Consent Flow & Ledger Auditor
Aligned with ISO/IEC 27701:2025 (Controls A.1.2.4, A.1.2.5, A.1.3.5, A.2.2.4).

Evaluates consent collection configurations (forms, UI components, CMP banners)
and consent ledger audit records against normative data protection requirements.

Checks performed:
1. Pre-ticked checkboxes / default affirmative selection (CRITICAL - A.1.2.5).
2. Purpose granularity and bundling detection (HIGH - A.1.2.4).
3. Prior information & Privacy Notice linkage (MEDIUM/HIGH - A.1.2.4, A.1.3.3).
4. Revocation and opt-out mechanism symmetry (HIGH/CRITICAL - A.1.3.5).
5. Consent ledger audit trail integrity (timestamps, subject ID, policy version/hash).
6. Processor marketing restrictions (HIGH - A.2.2.4).

Usage:
    python consent_flow_checker.py --input form_config.json
    python consent_flow_checker.py --input consent_ledger.json --strict
    python consent_flow_checker.py --input sample.json --format json
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


def is_valid_iso8601(timestamp_str: str) -> bool:
    """Validate ISO 8601 UTC timestamp format."""
    if not isinstance(timestamp_str, str):
        return False
    # Common ISO 8601 regex with Z or timezone offset
    iso_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$'
    return bool(re.match(iso_regex, timestamp_str))


def audit_form_configuration(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Audit form UI or CMP consent configuration."""
    findings: List[Dict[str, Any]] = []

    # Check for checkboxes/selectors
    elements = data.get("checkboxes") or data.get("fields") or data.get("consent_elements") or []
    if not elements and "checkboxes" not in data:
        # Check if root itself defines a consent element
        if any(k in data for k in ["pre_ticked", "default_value", "purpose", "label"]):
            elements = [data]

    has_privacy_link = data.get("has_privacy_notice_link", False) or data.get("privacy_notice_url") is not None
    revocation_mechanism = data.get("revocation_mechanism") or data.get("opt_out_link") or data.get("preference_center")
    is_processor = data.get("role", "").lower() == "processor"

    # Rule 1: Checkboxes must not be pre-ticked
    for idx, elem in enumerate(elements):
        label = elem.get("label", f"Element #{idx + 1}")
        pre_ticked = elem.get("pre_ticked", False) or elem.get("default_checked", False) or elem.get("default_value") is True
        required = elem.get("required", False)
        purpose = elem.get("purpose", "").lower()

        if pre_ticked:
            findings.append({
                "rule_id": "CV-R01-PRE-TICKED",
                "control": "ISO/IEC 27701:2025 A.1.2.5",
                "severity": "CRÍTICA",
                "element": label,
                "evidence": f"Element '{label}' has pre_ticked/default_checked = True.",
                "recommendation": "Configure all consent checkboxes to default to unchecked (opt-in explicit action)."
            })

        # Rule 2: Bundling non-essential purposes with required status
        non_essential_keywords = ["marketing", "publicidad", "terceros", "third_party", "newsletter", "tracking", "cookies_analytics"]
        is_commercial = any(kw in purpose for kw in non_essential_keywords) or any(kw in label.lower() for kw in non_essential_keywords)

        if required and is_commercial:
            findings.append({
                "rule_id": "CV-R02-FORCED-CONSENT",
                "control": "ISO/IEC 27701:2025 A.1.2.4",
                "severity": "CRÍTICA",
                "element": label,
                "evidence": f"Commercial/secondary purpose '{label}' is marked as 'required=True', conditioning basic service.",
                "recommendation": "Decouple commercial consent from mandatory service terms; consent must be freely given."
            })

    # Rule 3: Single checkbox bundling multiple purposes
    purposes_list = data.get("purposes") or []
    if len(elements) == 1 and len(purposes_list) > 1:
        findings.append({
            "rule_id": "CV-R03-BUNDLED-PURPOSES",
            "control": "ISO/IEC 27701:2025 A.1.2.4",
            "severity": "MAYOR",
            "element": "Form Structure",
            "evidence": f"Form bundles {len(purposes_list)} separate purposes under a single generic selection element.",
            "recommendation": "Implement granular checkboxes allowing data subjects to consent individually to each specific purpose."
        })

    # Rule 4: Verification of prior information link
    if not has_privacy_link:
        findings.append({
            "rule_id": "CV-R04-NO-PRIVACY-LINK",
            "control": "ISO/IEC 27701:2025 A.1.2.4 / A.1.3.3",
            "severity": "MAYOR",
            "element": "Transparency Link",
            "evidence": "No clear hyperlink or reference to the complete Privacy Notice was detected in the consent form.",
            "recommendation": "Embed an explicit, visible hyperlink to the full Privacy Notice directly adjacent to the consent mechanism."
        })

    # Rule 5: Revocation / Opt-out mechanism presence & symmetry
    if not revocation_mechanism:
        findings.append({
            "rule_id": "CV-R05-NO-REVOCATION-METHOD",
            "control": "ISO/IEC 27701:2025 A.1.3.5",
            "severity": "MAYOR",
            "element": "Revocation Mechanism",
            "evidence": "No self-service revocation mechanism, opt-out link, or preference center configuration defined in flow.",
            "recommendation": "Provide an accessible mechanism (preference center or 1-click opt-out) to withdraw consent as easily as giving it."
        })

    # Rule 6: Processor marketing restrictions
    if is_processor:
        processor_marketing = data.get("processor_marketing_enabled", False)
        customer_consent_verified = data.get("customer_consent_verified", False)
        if processor_marketing and not customer_consent_verified:
            findings.append({
                "rule_id": "CV-R06-PROCESSOR-MARKETING",
                "control": "ISO/IEC 27701:2025 A.2.2.4",
                "severity": "CRÍTICA",
                "element": "Processor Role Restrictions",
                "evidence": "Processor entity is configured to use customer PII for secondary marketing without verified prior consent.",
                "recommendation": "Disable secondary marketing exploitation on customer PII or secure explicit documented authorization."
            })

    return findings


def audit_consent_ledger(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Audit consent record event logs (Consent Ledger) for evidentiary compliance."""
    findings: List[Dict[str, Any]] = []

    records = data.get("records") or data.get("consent_events") or data.get("logs") or []
    if not records and "records" not in data:
        # Root object might be a single consent event record
        if any(k in data for k in ["consent_id", "subject_identifier", "timestamp_utc", "status"]):
            records = [data]

    if not records:
        return findings

    for idx, rec in enumerate(records):
        rec_id = rec.get("consent_id", f"Record #{idx + 1}")

        # Check timestamp
        ts = rec.get("timestamp_utc") or rec.get("timestamp")
        if not ts:
            findings.append({
                "rule_id": "CV-L01-MISSING-TIMESTAMP",
                "control": "ISO/IEC 27701:2025 A.1.2.5",
                "severity": "CRÍTICA",
                "element": f"Record {rec_id}",
                "evidence": "Consent log entry is missing timestamp.",
                "recommendation": "Store accurate ISO 8601 UTC timestamp in all consent capture and withdrawal events."
            })
        elif not is_valid_iso8601(str(ts)):
            findings.append({
                "rule_id": "CV-L02-INVALID-TIMESTAMP-FORMAT",
                "control": "ISO/IEC 27701:2025 A.1.2.5",
                "severity": "MENOR",
                "element": f"Record {rec_id}",
                "evidence": f"Timestamp '{ts}' does not comply with standard ISO 8601 UTC format.",
                "recommendation": "Format timestamps adhering to ISO 8601 UTC (e.g. YYYY-MM-DDTHH:MM:SS.sssZ)."
            })

        # Check subject identifier
        subject_id = rec.get("subject_identifier") or rec.get("user_id") or rec.get("user_identifier")
        if not subject_id:
            findings.append({
                "rule_id": "CV-L03-MISSING-SUBJECT-ID",
                "control": "ISO/IEC 27701:2025 A.1.2.5",
                "severity": "CRÍTICA",
                "element": f"Record {rec_id}",
                "evidence": "Consent entry lacks a verifiable user identifier or pseudonimized subject key.",
                "recommendation": "Associate each consent event with an immutable pseudonimized subject identifier."
            })

        # Check policy version or hash
        policy_ver = rec.get("legal_text_version") or rec.get("policy_version") or (rec.get("legal_context", {}).get("policy_version") if isinstance(rec.get("legal_context"), dict) else None)
        text_hash = rec.get("legal_text_hash") or (rec.get("legal_context", {}).get("text_sha256") if isinstance(rec.get("legal_context"), dict) else None)

        if not policy_ver and not text_hash:
            findings.append({
                "rule_id": "CV-L04-NO-TEXT-VERSION-OR-HASH",
                "control": "ISO/IEC 27701:2025 A.1.2.5",
                "severity": "MAYOR",
                "element": f"Record {rec_id}",
                "evidence": "Log entry does not record the legal text version or cryptographic hash accepted by the subject.",
                "recommendation": "Record policy_version and SHA-256 hash of the exact terms presented at the moment of consent."
            })

        # Check capture channel
        channel = rec.get("capture_channel") or rec.get("collection_channel") or rec.get("channel")
        if not channel:
            findings.append({
                "rule_id": "CV-L05-NO-CAPTURE-CHANNEL",
                "control": "ISO/IEC 27701:2025 A.1.2.5",
                "severity": "MENOR",
                "element": f"Record {rec_id}",
                "evidence": "No capture channel or point of interaction recorded (e.g., WEB, APP, CMP).",
                "recommendation": "Include the capture channel/device context in consent event metadata."
            })

    return findings


def evaluate_consent_json(filepath: Path) -> Dict[str, Any]:
    """Parse JSON and run both form and ledger evaluations."""
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as e:
        return {
            "status": "ERROR",
            "file": str(filepath),
            "error": f"Failed to parse JSON file: {e}",
            "total_findings": 0,
            "critical_findings": 0,
            "major_findings": 0,
            "minor_findings": 0,
            "findings": []
        }

    all_findings: List[Dict[str, Any]] = []

    # If it's a list, analyze items or treat as ledger records
    if isinstance(data, list):
        # Could be list of records or list of form fields
        if data and isinstance(data[0], dict) and ("pre_ticked" in data[0] or "label" in data[0]):
            all_findings.extend(audit_form_configuration({"checkboxes": data}))
        else:
            all_findings.extend(audit_consent_ledger({"records": data}))
    elif isinstance(data, dict):
        all_findings.extend(audit_form_configuration(data))
        all_findings.extend(audit_consent_ledger(data))

    critical_count = sum(1 for f in all_findings if f["severity"] == "CRÍTICA")
    major_count = sum(1 for f in all_findings if f["severity"] == "MAYOR")
    minor_count = sum(1 for f in all_findings if f["severity"] == "MENOR")

    status = "NON_COMPLIANT" if (critical_count > 0 or major_count > 0) else ("OBSERVATIONS" if minor_count > 0 else "COMPLIANT")

    return {
        "status": status,
        "file": str(filepath),
        "total_findings": len(all_findings),
        "critical_findings": critical_count,
        "major_findings": major_count,
        "minor_findings": minor_count,
        "findings": all_findings
    }


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic consent validator for ISO/IEC 27701:2025 controls A.1.2.4, A.1.2.5, A.1.3.5, A.2.2.4"
    )
    parser.add_argument("--input", "-i", required=True, help="Path to JSON file containing form config or consent records")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text", help="Output format (default: text)")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code if any CRITICAL or MAYOR finding exists")

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: Target file not found: {input_path}", file=sys.stderr)
        sys.exit(2)

    result = evaluate_consent_json(input_path)

    if result.get("status") == "ERROR":
        print(f"Error procesando archivo JSON: {result.get('error')}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=" * 72)
        print(" AUDITORÍA DETERMINISTA DE CONSENTIMIENTO (ISO/IEC 27701:2025)")
        print("=" * 72)
        print(f"Archivo analizado : {result['file']}")
        print(f"Estado Dictamen   : {result['status']}")
        print(f"Total Hallazgos   : {result['total_findings']} (Críticas: {result['critical_findings']}, Mayores: {result['major_findings']}, Menores: {result['minor_findings']})")
        print("-" * 72)

        if not result["findings"]:
            print("✓ No se detectaron no conformidades técnicas en la muestra auditada.")
        else:
            for idx, f in enumerate(result["findings"], 1):
                print(f"[{idx}] {f['severity']} | Regla: {f['rule_id']} | Control: {f['control']}")
                print(f"    Elemento       : {f['element']}")
                print(f"    Evidencia      : {f['evidence']}")
                print(f"    Recomendación  : {f['recommendation']}")
                print()
        print("=" * 72)

    if args.strict and (result["critical_findings"] > 0 or result["major_findings"] > 0):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
