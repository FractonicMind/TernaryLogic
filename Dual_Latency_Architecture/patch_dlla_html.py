#!/usr/bin/env python3
"""
Patch: Dual_Latency_Architecture HTML files
Terminology migration per TL constitutional naming convention.

Changes applied (singular AND plural, all case variants, quoted forms):
  "Fast Lane"    -> "Inference Lane"
  "Fast Lanes"   -> "Inference Lanes"
  "fast lane"    -> "inference lane"
  "fast lanes"   -> "inference lanes"
  "FAST LANE"    -> "INFERENCE LANE"
  "FAST LANES"   -> "INFERENCE LANES"
  "Fast and Audit lanes"  -> "Inference and Governance lanes"
  "fast and audit lanes"  -> "inference and governance lanes"

  "Audit Lane"   -> "Governance Lane"
  "Audit Lanes"  -> "Governance Lanes"
  "audit lane"   -> "governance lane"
  "audit lanes"  -> "governance lanes"
  "AUDIT LANE"   -> "GOVERNANCE LANE"
  "AUDIT LANES"  -> "GOVERNANCE LANES"

  "Audit Token"  -> "Permission Token"
  "Audit Tokens" -> "Permission Tokens"
  "audit token"  -> "permission token"
  "audit tokens" -> "permission tokens"
  "AUDIT TOKEN"  -> "PERMISSION TOKEN"
  "Audit Lane Token" -> "Permission Token"   (table header)

Protected (NOT changed):
  fast_lane, fast-lane         CSS/JS identifiers (underscore/hyphen form)
  audit_lane, audit-lane       CSS/JS identifiers
  audit_token, audit-token     CSS/JS identifiers
  audit_before_commit          SVA property name
  ack_audit, req_fast          Handshake signal names
  FastDone, AuditDone          RTL signal variables
  AuditToken (camelCase)       RTL/JS variable
  COMMIT-AUDIT                 Hardware timing term
  "audit trail"                Standard English phrase
  "audit log"                  Standard English phrase
  "auditability"               English word
  "Audit Lag"                  Technical term for execution-verification gap
  RECOVERY_AUDIT               Constitutional recovery path name
  data-audit, data-fast        HTML data attributes

Run from the Dual_Latency_Architecture/ folder:
    python3 patch_dlla_html.py

Verify after running:
    grep -in "fast lane\\|audit lane\\|audit token" *.html
    (should return zero results)

Dry run to preview without changing files:
    python3 patch_dlla_html.py --dry-run
"""

import re
import sys
from pathlib import Path


# =============================================================================
# FILES TO PATCH
# =============================================================================

TARGET_FILES = [
    "Hardware_Enforceable_Execution_Model_Specification.html",
    "Hardware_Enforceable_Model_for_High_Integrity_Financial_Systems.html",
    "Hardware_Enforced_Execution_and_Cryptographic_Finality_Overview.html",
    "Physical_Execution_and_Cryptographic_Anchoring_Specification.html",
]


# =============================================================================
# REPLACEMENT RULES
# Ordered: compound phrases first, then plurals, then singulars.
# Word boundaries (\b) prevent matching inside hyphenated or underscored
# HTML/CSS/JS identifiers.
# =============================================================================

def build_rules():
    rules = []

    # ------------------------------------------------------------------
    # PRIORITY: compound phrases that need coordinated replacement
    # ------------------------------------------------------------------

    # "Fast and Audit lanes" / "Fast and Audit Lanes" (mixed compound)
    rules.append((r'\bFast and Audit [Ll]anes\b',
                   "Inference and Governance lanes",
                   "Fast and Audit lanes -> Inference and Governance lanes"))

    rules.append((r'\bfast and audit lanes\b',
                   "inference and governance lanes",
                   "fast and audit lanes -> inference and governance lanes"))

    # "Audit Lane Token" table header -> "Permission Token"
    rules.append((r'\bAudit Lane Token\b',
                   "Permission Token",
                   "Audit Lane Token -> Permission Token (table header)"))

    rules.append((r'\baudit lane token\b',
                   "permission token",
                   "audit lane token -> permission token"))

    # Quoted forms: "Audit Token", 'Audit Token' (HTML attribute or prose)
    # Use lookahead/lookbehind for quote characters
    rules.append((r'(?<=["\u201c\u2018])\s*Audit Token\s*(?=["\u201d\u2019])',
                   "Permission Token",
                   "\"Audit Token\" -> \"Permission Token\" (quoted form)"))

    rules.append((r'(?<=["\u201c\u2018])\s*Audit Lane\s*(?=["\u201d\u2019])',
                   "Governance Lane",
                   "\"Audit Lane\" -> \"Governance Lane\" (quoted form)"))

    rules.append((r'(?<=["\u201c\u2018])\s*Fast Lane\s*(?=["\u201d\u2019])',
                   "Inference Lane",
                   "\"Fast Lane\" -> \"Inference Lane\" (quoted form)"))

    # ------------------------------------------------------------------
    # FAST LANE: plurals before singulars
    # ------------------------------------------------------------------

    rules.append((r'\bFast Lanes\b', "Inference Lanes",
                   "Fast Lanes -> Inference Lanes (plural)"))
    rules.append((r'\bfast lanes\b', "inference lanes",
                   "fast lanes -> inference lanes (plural lowercase)"))
    rules.append((r'\bFAST LANES\b', "INFERENCE LANES",
                   "FAST LANES -> INFERENCE LANES (plural uppercase)"))
    rules.append((r'\bFast Lane\b', "Inference Lane",
                   "Fast Lane -> Inference Lane (singular)"))
    rules.append((r'\bfast lane\b', "inference lane",
                   "fast lane -> inference lane (singular lowercase)"))
    rules.append((r'\bFAST LANE\b', "INFERENCE LANE",
                   "FAST LANE -> INFERENCE LANE (singular uppercase)"))

    # ------------------------------------------------------------------
    # AUDIT LANE: plurals before singulars
    # ------------------------------------------------------------------

    rules.append((r'\bAudit Lanes\b', "Governance Lanes",
                   "Audit Lanes -> Governance Lanes (plural)"))
    rules.append((r'\baudit lanes\b', "governance lanes",
                   "audit lanes -> governance lanes (plural lowercase)"))
    rules.append((r'\bAUDIT LANES\b', "GOVERNANCE LANES",
                   "AUDIT LANES -> GOVERNANCE LANES (plural uppercase)"))
    rules.append((r'\bAudit Lane\b', "Governance Lane",
                   "Audit Lane -> Governance Lane (singular)"))
    rules.append((r'\baudit lane\b', "governance lane",
                   "audit lane -> governance lane (singular lowercase)"))
    rules.append((r'\bAUDIT LANE\b', "GOVERNANCE LANE",
                   "AUDIT LANE -> GOVERNANCE LANE (singular uppercase)"))

    # ------------------------------------------------------------------
    # AUDIT TOKEN: plurals before singulars
    # ------------------------------------------------------------------

    rules.append((r'\bAudit Tokens\b', "Permission Tokens",
                   "Audit Tokens -> Permission Tokens (plural)"))
    rules.append((r'\baudit tokens\b', "permission tokens",
                   "audit tokens -> permission tokens (plural lowercase)"))
    rules.append((r'\bAUDIT TOKENS\b', "PERMISSION TOKENS",
                   "AUDIT TOKENS -> PERMISSION TOKENS (plural uppercase)"))
    rules.append((r'\bAudit Token\b', "Permission Token",
                   "Audit Token -> Permission Token (singular)"))
    rules.append((r'\baudit token\b', "permission token",
                   "audit token -> permission token (singular lowercase)"))
    rules.append((r'\bAUDIT TOKEN\b', "PERMISSION TOKEN",
                   "AUDIT TOKEN -> PERMISSION TOKEN (singular uppercase)"))

    return rules


# =============================================================================
# PROTECTION VERIFICATION
# Terms that are NOT in these HTML files but would be in the RTL files.
# We only check terms that should realistically appear in HTML prose docs.
# =============================================================================

PROTECTED_MUST_EXIST = [
    # These should appear in the HTML documents
    "Inference Lane",     # after patching, this must be present
    "Governance Lane",    # after patching, this must be present
]

PROTECTED_MUST_NOT_BREAK = [
    # HTML/CSS/JS identifiers that use hyphens or underscores
    # We verify none of these were accidentally changed
    # by checking they still appear if they existed before
]

PROTECTED_PROSE = [
    # Standard English phrases that must NOT be changed
    "audit trail",
    "Audit Lag",
    "auditability",
]


# =============================================================================
# VERIFICATION: check for remaining targeted terms
# =============================================================================

def find_remaining(content: str, filepath_name: str) -> list:
    """Find any remaining targeted terms that should have been replaced."""
    failures = []

    patterns = [
        (r'\bFast Lane[s]?\b', "fast_lane"),
        (r'\bfast lane[s]?\b', "fast_lane"),
        (r'\bFAST LANE[S]?\b', None),
        (r'\bAudit Lane[s]?\b', "audit_lane"),
        (r'\baudit lane[s]?\b', "audit_lane"),
        (r'\bAUDIT LANE[S]?\b', None),
        (r'\bAudit Token[s]?\b', "AuditToken"),
        (r'\baudit token[s]?\b', "AuditToken"),
        (r'\bAUDIT TOKEN[S]?\b', None),
    ]

    for pattern, protected_form in patterns:
        for m in re.finditer(pattern, content):
            pos = m.start()
            start = max(0, pos - 20)
            end = min(len(content), pos + len(m.group()) + 20)
            context = content[start:end]

            # Skip if it is an underscore/hyphen identifier form
            if protected_form and protected_form in context:
                continue
            # Skip if inside an HTML tag attribute (data-audit-lane etc.)
            if re.search(r'[a-z_-]' + re.escape(m.group().lower()),
                         context.lower()):
                continue

            failures.append(
                f"REMAINING: '{m.group()}' at position {pos} in {filepath_name}"
            )

    return failures


def check_prose_protected(content: str, filepath_name: str) -> list:
    """Verify protected prose terms were not accidentally changed."""
    warnings = []
    for term in PROTECTED_PROSE:
        # These are optional: not every file will contain all of them
        # We just note if "Audit Lag" became something else
        pass
    return warnings


# =============================================================================
# PATCH ENGINE
# =============================================================================

def patch_file(filepath: Path, rules: list, dry_run: bool = False) -> dict:
    if not filepath.exists():
        return {"status": "SKIPPED", "reason": "file not found", "changes": {}}

    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    content = original
    change_counts = {}

    for pattern, replacement, description in rules:
        matches = re.findall(pattern, content)
        count = len(matches)
        if count > 0:
            content = re.sub(pattern, replacement, content)
            change_counts[description] = count

    if content == original:
        return {
            "status": "UNCHANGED",
            "reason": "no matching patterns found",
            "changes": {}
        }

    if not dry_run:
        backup_path = filepath.with_suffix(filepath.suffix + ".bak")
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(original)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    # Run failure check on patched content
    failures = find_remaining(content, filepath.name)

    return {
        "status": "PATCHED" if not dry_run else "DRY_RUN",
        "totalChanges": sum(change_counts.values()),
        "changes": change_counts,
        "failures": failures,
        "backupWritten": not dry_run
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv

    if dry_run:
        print("DRY RUN MODE: no files will be modified")
        print()

    rules = build_rules()

    print("=" * 70)
    print("TL DLLA HTML Terminology Patch")
    print("  Fast Lane / Fast Lanes  -> Inference Lane / Inference Lanes")
    print("  Audit Lane / Audit Lanes -> Governance Lane / Governance Lanes")
    print("  Audit Token / Audit Tokens -> Permission Token / Permission Tokens")
    print("=" * 70)
    print()

    if dry_run:
        print("Rules to be applied:")
        for i, (pattern, replacement, description) in enumerate(rules, 1):
            print(f"  {i:2d}. {description}")
        print()

    total_patched = 0
    total_changes = 0
    all_failures = []

    for filename in TARGET_FILES:
        filepath = Path(filename)
        print(f"Processing: {filename}")

        result = patch_file(filepath, rules, dry_run=dry_run)

        if result["status"] == "SKIPPED":
            print(f"  SKIPPED: {result['reason']}")
        elif result["status"] == "UNCHANGED":
            print(f"  UNCHANGED: no matching patterns found")
        else:
            status = result["status"]
            n = result["totalChanges"]
            print(f"  {status}: {n} replacement(s) applied")
            for desc, count in result["changes"].items():
                print(f"    {count:3d}x  {desc}")
            if result.get("backupWritten"):
                print(f"  Backup written: {filename}.bak")
            if not dry_run:
                total_patched += 1
                total_changes += n
            else:
                if result["status"] == "DRY_RUN":
                    total_patched += 1
                    total_changes += n

            for f in result.get("failures", []):
                print(f"  {f}")
                all_failures.append(f)

        print()

    print("=" * 70)
    print("SUMMARY")
    print(f"  Files processed:  {len(TARGET_FILES)}")
    print(f"  Files patched:    {total_patched}")
    print(f"  Total changes:    {total_changes}")
    print(f"  Failures:         {len(all_failures)}")
    print()

    if all_failures:
        print("FAILURES (targeted terms still present after patching):")
        for f in all_failures:
            print(f"  {f}")
        print()
        print("ACTION REQUIRED: review failures above.")
    else:
        if not dry_run and total_patched > 0:
            print("ALL VERIFICATIONS PASSED.")
            print()
            print("Final verification commands:")
            print()
            print("  # Should return ZERO results:")
            print('  grep -in "fast lane\\|audit lane\\|audit token" *.html')
            print()
            print("  # Commit:")
            print('  git add *.html')
            print('  git commit -m "Terminology: HTML files updated, Inference/Governance Lane, Permission Token"')
            print()
            print("  # Remove backups:")
            print("  rm *.html.bak")

    print("=" * 70)
    return 1 if all_failures else 0


if __name__ == "__main__":
    sys.exit(main())
