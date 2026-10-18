#!/usr/bin/env python3
"""Check DPA Clauses - Wrapper and CLI Alias for clause_gap_detector.py.

This file provides architectural compatibility with workspace/02-architecture.md
specifications for Skill 7 (processor-contract-validator).

Usage:
  python check_dpa_clauses.py --file path/to/contract.txt [--json] [--report]
"""

import sys
from clause_gap_detector import main

if __name__ == "__main__":
    # Passes sys.argv directly to the clause_gap_detector main CLI engine
    main()
