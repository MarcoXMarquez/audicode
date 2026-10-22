"""Run each deterministic skill script against its eval fixtures."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "skills"


def fx(skill, name):
    return str(S / skill / "evals" / "fixtures" / name)


def sc(skill, name):
    return str(S / skill / "scripts" / name)


# (id, args, output_is_json). Exit codes 1/2 are legitimate "gate failed" results
# (e.g. expired deadline, DPA below threshold); argparse errors are also 2, but
# those would leave empty stdout and fail the output assertions below.
#
# the contract tested is: no crash and usable output.
CASES = [
    ("consent-cookie", [sc("consent-validator", "consent_flow_checker.py"),
                        "-i", fx("consent-validator", "sample_cookie_banner_config.json"), "-f", "json"], True),
    ("minimization-ddl", [sc("data-minimization-checker", "schema_minimization_checker.py"),
                          fx("data-minimization-checker", "sample_ecommerce_ddl.sql"), "--json"], True),
    ("minimization-json", [sc("data-minimization-checker", "schema_minimization_checker.py"),
                           fx("data-minimization-checker", "sample_mobile_analytics_payload.json"), "--json"], True),
    ("incident-ransom", [sc("incident-response-planner", "incident_record_generator.py"),
                         "-i", fx("incident-response-planner", "sample_ransomware_exfiltration_breach.json"),
                         "--validate"], False),
    ("incident-laptop", [sc("incident-response-planner", "incident_record_generator.py"),
                         "-i", fx("incident-response-planner", "sample_lost_encrypted_laptop_incident.json")], False),
    ("incident-sample", [sc("incident-response-planner", "incident_record_generator.py"), "--sample"], False),
    ("pia-high", [sc("pia-reviewer", "pia_risk_scorer.py"),
                  "-f", fx("pia-reviewer", "sample_high_risk_ai_screening.json"), "--format", "json"], True),
    ("pia-low", [sc("pia-reviewer", "pia_risk_scorer.py"),
                 "-f", fx("pia-reviewer", "sample_low_risk_internal_tool.json"), "--format", "json"], True),
    ("rights-batch", [sc("pii-rights-manager", "deadline_calculator.py"),
                      "--input", fx("pii-rights-manager", "sample_batch_dsar_log.json"),
                      "--as-of", "2025-06-01", "--format", "json"], True),
    ("rights-single", [sc("pii-rights-manager", "deadline_calculator.py"),
                       "--date", "2025-01-10", "--jurisdiction", "GDPR", "--right", "erasure",
                       "--format", "json"], True),
    ("transfer-csv", [sc("pii-transfer-auditor", "transfer_record_validator.py"),
                      "-i", fx("pii-transfer-auditor", "sample_international_transfer_inventory.csv"),
                      "-o", "json"], True),
    ("transfer-json", [sc("pii-transfer-auditor", "transfer_record_validator.py"),
                       "-i", fx("pii-transfer-auditor", "sample_cross_border_cloud_flow.json"),
                       "-o", "json"], True),
    ("policy-external", [sc("privacy-policy-reviewer", "policy_structure_scanner.py"),
                         "--file", fx("privacy-policy-reviewer", "sample_external_privacy_notice.md"),
                         "--format", "json"], True),
    ("policy-internal", [sc("privacy-policy-reviewer", "policy_structure_scanner.py"),
                         "--file", fx("privacy-policy-reviewer", "sample_internal_pims_policy.md"),
                         "--type", "internal_policy", "--format", "json"], True),
    ("policy-layered", [sc("privacy-policy-reviewer", "policy_structure_scanner.py"),
                        "--file", fx("privacy-policy-reviewer", "sample_layered_privacy_notice.md"),
                        "--format", "markdown"], False),
    ("dpa-deficient", [sc("processor-contract-validator", "clause_gap_detector.py"),
                       "-f", fx("processor-contract-validator", "sample_vendor_dpa_deficiencies.md"),
                       "--json"], True),
    ("dpa-compliant", [sc("processor-contract-validator", "clause_gap_detector.py"),
                       "-f", fx("processor-contract-validator", "sample_compliant_b2b_dpa.md"),
                       "--json"], True),
    ("dpa-wrapper", [sc("processor-contract-validator", "check_dpa_clauses.py"),
                     "-f", fx("processor-contract-validator", "sample_cloud_provider_standard_terms.md"),
                     "--json"], True),
]


def _run(args):
    return subprocess.run([sys.executable, "-X", "utf8", *args], capture_output=True,
                          text=True, encoding="utf-8", timeout=60, cwd=ROOT)


@pytest.mark.parametrize("args,as_json", [c[1:] for c in CASES], ids=[c[0] for c in CASES])
def test_script_runs_on_fixture(args, as_json):
    p = _run(args)
    assert "Traceback" not in p.stderr, p.stderr
    assert p.returncode in (0, 1, 2), (p.returncode, p.stderr)
    assert p.stdout.strip()
    if as_json:
        json.loads(p.stdout)


@pytest.mark.parametrize("script", sorted(S.glob("*/scripts/*.py")), ids=lambda p: p.name)
def test_script_help(script):
    p = _run([str(script), "--help"])
    assert p.returncode == 0, p.stderr
    assert "usage" in p.stdout.lower()
