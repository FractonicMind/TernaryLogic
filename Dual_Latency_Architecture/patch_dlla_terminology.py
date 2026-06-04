#!/usr/bin/env python3
"""
Patch: Dual_Latency_Architecture markdown files
Terminology migration per TL constitutional naming convention.

Changes applied:
  "Fast Lane"   -> "Inference Lane"   (prose and headings only)
  "Audit Lane"  -> "Governance Lane"  (prose and headings only)
  "Audit Token" -> "Permission Token" (prose only)

Protected (NOT changed):
  fast_lane_pos, fast_lane_neg          RTL port names (underscore form)
  fast_lane_data, fast_lane_*           Any underscore RTL identifier
  audit_valid_pos, audit_valid_neg      RTL port names
  audit_before_commit                   SVA property name
  forbidden_null_to_commit_without_audit SVA sequence name
  ack_audit                             Handshake signal name
  req_fast                              Handshake signal name
  AuditDone, FastDone                   RTL signal variables in prose
  AuditToken (camelCase)                Internal RTL token variable
  A_tok                                 Signal abbreviation
  COMMIT-AUDIT GAP                      Hardware timing term (hyphen form)
  "audit trail"                         Standard English phrase
  "audit log"                           Standard English phrase
  "audit record"                        Standard English phrase
  "audit chain"                         Standard English phrase
  "auditability"                        English word
  RECOVERY_AUDIT                        Constitutional recovery path name
  GAS_LIMIT_AUDIT                       Smart contract parameter
  AUDIT_HOLD                            Smart contract state
  AUDIT_FLAG                            Log entry flag

Run from the Dual_Latency_Architecture/ folder:
    python3 patch_dlla_terminology.py

Verify after running:
    grep -in "fast lane\\|audit lane\\|audit token" *.md
    (should return zero results)

    grep -n "fast_lane\\|audit_before_commit\\|COMMIT-AUDIT\\|AuditDone\\|FastDone" *.md
    (should return results, confirming protected terms were preserved)
"""

import re
import sys
from pathlib import Path


# =============================================================================
# FILES TO PATCH
# =============================================================================

TARGET_FILES = [
    "README.md",
    "Hardware_Enforceable_Execution_Model_Specification.md",
    "Hardware_Enforceable_Model_for_High_Integrity_Financial_Systems.md",
    "Hardware_Enforced_Execution_and_Cryptographic_Finality_Overview.md",
    "Physical_Execution_and_Cryptographic_Anchoring_Specification.md",
]


# =============================================================================
# REPLACEMENT RULES
# Each rule: (pattern, replacement, description, use_regex)
#
# ORDERING MATTERS: more specific patterns before more general ones.
# Rules that protect underscore-form identifiers are applied BEFORE
# rules that replace space-form phrases. We achieve this by checking
# that replacements only occur when surrounded by word-boundary or
# space contexts, never inside identifiers.
# =============================================================================

def build_replacements():
    """
    Build ordered list of (pattern, replacement, description) tuples.
    All replacements are case-sensitive.
    Protected forms use underscores or camelCase and are never matched
    by the space-form patterns below.
    """
    rules = []

    # ------------------------------------------------------------------
    # RULE GROUP 1: "Fast Lane" prose variants -> "Inference Lane"
    # The pattern word-boundary ensures we never match fast_lane (underscore).
    # ------------------------------------------------------------------

    # "Fast Lane" (title case, standalone)
    rules.append((
        r'\bFast Lane\b',
        "Inference Lane",
        "Fast Lane -> Inference Lane (title case)"
    ))

    # "fast lane" (lowercase prose)
    rules.append((
        r'\bfast lane\b',
        "inference lane",
        "fast lane -> inference lane (lowercase)"
    ))

    # "FAST LANE" (uppercase, ASCII diagrams)
    rules.append((
        r'\bFAST LANE\b',
        "INFERENCE LANE",
        "FAST LANE -> INFERENCE LANE (uppercase)"
    ))

    # ------------------------------------------------------------------
    # RULE GROUP 2: "Audit Lane" prose variants -> "Governance Lane"
    # The word-boundary ensures we never match "audit_lane" (underscore).
    # ------------------------------------------------------------------

    # "Audit Lane" (title case)
    rules.append((
        r'\bAudit Lane\b',
        "Governance Lane",
        "Audit Lane -> Governance Lane (title case)"
    ))

    # "audit lane" (lowercase)
    rules.append((
        r'\baudit lane\b',
        "governance lane",
        "audit lane -> governance lane (lowercase)"
    ))

    # "AUDIT LANE" (uppercase, ASCII diagrams)
    rules.append((
        r'\bAUDIT LANE\b',
        "GOVERNANCE LANE",
        "AUDIT LANE -> GOVERNANCE LANE (uppercase)"
    ))

    # ------------------------------------------------------------------
    # RULE GROUP 3: "Audit Token" -> "Permission Token"
    # Specifically "Audit Token" (two words, space-separated, title case).
    # Protected: AuditToken (camelCase, RTL), A_tok (abbreviation).
    # ------------------------------------------------------------------

    # "Audit Token" (title case, two words)
    rules.append((
        r'\bAudit Token\b',
        "Permission Token",
        "Audit Token -> Permission Token (title case)"
    ))

    # "audit token" (lowercase)
    rules.append((
        r'\baudit token\b',
        "permission token",
        "audit token -> permission token (lowercase)"
    ))

    # "AUDIT TOKEN" (uppercase)
    rules.append((
        r'\bAUDIT TOKEN\b',
        "PERMISSION TOKEN",
        "AUDIT TOKEN -> PERMISSION TOKEN (uppercase)"
    ))

    # ------------------------------------------------------------------
    # RULE GROUP 4: Specific compound phrases that contain lane names
    # and need coordinated replacement in table headers and section titles.
    # These are already handled by Rules 1-3 above since they contain
    # "Fast Lane" and "Audit Lane" as substrings. No extra rules needed.
    # ------------------------------------------------------------------

    # "Audit Lane Token" (table header) -> "Permission Token"
    # Handled by: "Audit Lane" -> "Governance Lane" makes it
    # "Governance Lane Token", but the correct term is "Permission Token".
    # So we need a targeted rule BEFORE Rule 2:
    # Insert this BEFORE the Audit Lane rule.

    return rules


def build_replacements_ordered():
    """
    Final ordered replacement list with targeted compound phrases first.
    """
    rules = []

    # ------------------------------------------------------------------
    # PRIORITY RULES: compound phrases that need specific handling
    # ------------------------------------------------------------------

    # "Audit Lane Token" (table column header) -> "Permission Token"
    rules.append((
        r'\bAudit Lane Token\b',
        "Permission Token",
        "Audit Lane Token -> Permission Token (table header)"
    ))

    rules.append((
        r'\baudit lane token\b',
        "permission token",
        "audit lane token -> permission token (lowercase)"
    ))

    # until both Fast Lane (req_fast) and Audit Lane (ack_audit) agree
    # -> until both Inference Lane (req_fast) and Governance Lane (ack_audit) agree
    # (req_fast and ack_audit signal names preserved as they are inside parentheses)
    rules.append((
        r'\bFast Lane \(req_fast\)',
        "Inference Lane (req_fast)",
        "Fast Lane (req_fast) -> Inference Lane (req_fast) preserving signal name"
    ))

    rules.append((
        r'\bAudit Lane \(ack_audit\)',
        "Governance Lane (ack_audit)",
        "Audit Lane (ack_audit) -> Governance Lane (ack_audit) preserving signal name"
    ))

    # ------------------------------------------------------------------
    # MAIN RULES: space-form lane names
    # ------------------------------------------------------------------

    # "Fast Lane" variants
    rules.append((r'\bFast Lane\b', "Inference Lane", "Fast Lane -> Inference Lane"))
    rules.append((r'\bfast lane\b', "inference lane", "fast lane -> inference lane"))
    rules.append((r'\bFAST LANE\b', "INFERENCE LANE", "FAST LANE -> INFERENCE LANE"))

    # "The Fast Lane" -> "The Inference Lane" (already handled above)
    # ASCII diagram: "FAST LANE [EXEC]" -> "INFERENCE LANE [EXEC]" (handled above)

    # "Audit Lane" variants
    rules.append((r'\bAudit Lane\b', "Governance Lane", "Audit Lane -> Governance Lane"))
    rules.append((r'\baudit lane\b', "governance lane", "audit lane -> governance lane"))
    rules.append((r'\bAUDIT LANE\b', "GOVERNANCE LANE", "AUDIT LANE -> GOVERNANCE LANE"))

    # "Audit Token" variants (two-word, space form)
    rules.append((r'\bAudit Token\b', "Permission Token", "Audit Token -> Permission Token"))
    rules.append((r'\baudit token\b', "permission token", "audit token -> permission token"))
    rules.append((r'\bAUDIT TOKEN\b', "PERMISSION TOKEN", "AUDIT TOKEN -> PERMISSION TOKEN"))

    return rules


# =============================================================================
# PROTECTION VERIFICATION
# After patching, verify that protected terms are still present (not broken).
# =============================================================================

PROTECTED_TERMS = [
    # RTL signal names
    "fast_lane",        # fast_lane_pos, fast_lane_neg, fast_lane_data etc.
    "audit_valid",      # audit_valid_pos, audit_valid_neg
    # SVA property names
    "audit_before_commit",
    "forbidden_null_to_commit_without_audit",
    # Handshake signals
    "ack_audit",
    "req_fast",
    # RTL variables
    "FastDone",
    "AuditDone",
    "AuditToken",       # camelCase RTL variable
    # Hardware timing terms
    "COMMIT-AUDIT",     # COMMIT-AUDIT GAP
    # Standard English (check a representative sample)
    "audit trail",
    "auditability",
]

PROTECTED_TERMS_OPTIONAL = [
    # These may not appear in every file, so absence is not an error
    "A_tok",
    "RECOVERY_AUDIT",
]


# =============================================================================
# PATCH ENGINE
# =============================================================================

def patch_file(filepath: Path, rules: list, dry_run: bool = False) -> dict:
    """
    Apply all rules to a file. Returns a summary dict.
    """
    if not filepath.exists():
        return {"status": "SKIPPED", "reason": "file not found", "changes": {}}

    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    content = original
    change_counts = {}

    for pattern, replacement, description in rules:
        count = len(re.findall(pattern, content))
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
        # Write backup
        backup_path = filepath.with_suffix(filepath.suffix + ".bak")
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(original)

        # Write patched file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return {
        "status": "PATCHED" if not dry_run else "DRY_RUN",
        "totalChanges": sum(change_counts.values()),
        "changes": change_counts,
        "backupWritten": not dry_run
    }


def verify_protection(filepath: Path) -> list:
    """
    Verify that protected terms are still present in the patched file.
    Returns list of warnings for terms that are absent.
    """
    if not filepath.exists():
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    warnings = []
    for term in PROTECTED_TERMS:
        if term not in content:
            warnings.append(f"WARNING: protected term '{term}' not found in {filepath.name}")

    return warnings


def verify_replacements(filepath: Path) -> list:
    """
    Verify that targeted terms are no longer present.
    Returns list of failures for terms that are still present.
    """
    if not filepath.exists():
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    failures = []
    check_terms = [
        ("Fast Lane", "fast_lane"),   # (target, allowed underscore form)
        ("fast lane", "fast_lane"),
        ("Audit Lane", "audit_lane"),
        ("audit lane", "audit_lane"),
        ("Audit Token", "AuditToken"),
        ("audit token", "AuditToken"),
    ]

    for target, protected_form in check_terms:
        # Find all occurrences of target
        matches = [(m.start(), m.group()) for m in re.finditer(re.escape(target), content, re.IGNORECASE)]
        for pos, match in matches:
            # Check if it is the protected underscore form
            # Get surrounding context
            start = max(0, pos - 5)
            end = min(len(content), pos + len(match) + 5)
            context = content[start:end]
            if "_" not in context:  # Not an underscore identifier
                failures.append(
                    f"REMAINING: '{match}' still present in {filepath.name} "
                    f"at position {pos}"
                )

    return failures


# =============================================================================
# MAIN
# =============================================================================

def main():
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv

    if dry_run:
        print("DRY RUN MODE: no files will be modified")
        print()

    rules = build_replacements_ordered()

    print("=" * 70)
    print("TL DLLA Terminology Patch: Audit Lane -> Governance Lane")
    print("                           Fast Lane  -> Inference Lane")
    print("                           Audit Token -> Permission Token")
    print("=" * 70)
    print()

    if dry_run:
        print("Rules to be applied:")
        for i, (pattern, replacement, description) in enumerate(rules, 1):
            print(f"  {i:2d}. {description}")
        print()

    total_files_patched = 0
    total_changes = 0
    all_warnings = []
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
            total_files_patched += 1
            total_changes += n

        if not dry_run and result["status"] == "PATCHED":
            # Protection verification
            warnings = verify_protection(filepath)
            for w in warnings:
                print(f"  {w}")
            all_warnings.extend(warnings)

            # Replacement verification
            failures = verify_replacements(filepath)
            for f in failures:
                print(f"  {f}")
            all_failures.extend(failures)

        print()

    # Summary
    print("=" * 70)
    print(f"SUMMARY")
    print(f"  Files processed:  {len(TARGET_FILES)}")
    print(f"  Files patched:    {total_files_patched}")
    print(f"  Total changes:    {total_changes}")
    print(f"  Warnings:         {len(all_warnings)}")
    print(f"  Failures:         {len(all_failures)}")
    print()

    if all_warnings:
        print("WARNINGS (protected terms may be absent from some files):")
        for w in all_warnings:
            print(f"  {w}")
        print()

    if all_failures:
        print("FAILURES (targeted terms still present after patching):")
        for f in all_failures:
            print(f"  {f}")
        print()
        print("ACTION REQUIRED: review failures above before committing.")
    else:
        if not dry_run and total_files_patched > 0:
            print("ALL VERIFICATIONS PASSED.")
            print()
            print("Final verification commands:")
            print()
            print("  # Should return ZERO results:")
            print('  grep -in "fast lane\\|audit lane\\|audit token" *.md')
            print()
            print("  # Should return results (protected terms preserved):")
            print('  grep -n "fast_lane\\|audit_before_commit\\|COMMIT-AUDIT\\|AuditDone\\|FastDone" *.md')
            print()
            print("  # Remove backups after verification:")
            print("  rm *.md.bak")

    print("=" * 70)

    return 1 if all_failures else 0


if __name__ == "__main__":
    sys.exit(main())
