"""checks required files/folders exist"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

requiredStructure = [
    "data/dataset_metadata.json",
    "data/review_groups_auto.json",
    "data/review_groups_hybrid.json",
    "data/review_groups_manual.json",
    "data/reviews_clean.jsonl",
    "data/reviews_raw.jsonl",

    "metrics/metrics_auto.json",
    "metrics/metrics_hybrid.json",
    "metrics/metrics_manual.json",
    "metrics/metrics_summary.json",

    "personas/personas_auto.json",
    "personas/personas_hybrid.json",
    "personas/personas_auto.json",

    "prompts/prompt_auto.json",

    "reflection/reflection.md",

    "spec/spec_auto.md",
    "spec/spec_hybrid.md",
    "spec/spec_manual.md",

    "src/00_validate_repo.py",
    "src/01_collect_or_import.py",
    "src/02_clean.py",
    "src/03_manual_coding_template.py",
    "src/04_personas_manual.py",
    "src/05_personas_auto.py",
    "src/06_spec_generate.py",
    "src/07_tests_generate.py",
    "src/08_metrics.py",
    "src/run_all.py",

    "tests/tests_auto.json",
    "tests/tests_hybrid.json",
    "tests/tests_manual.json",

    "README.md"
]

print("Checking repository structure...")

all_found = True
for path in requiredStructure:
    full_path = os.path.join(ROOT, path)
    if os.path.exists(full_path):
        print(f"  {path} found")
    else:
        print(f"  {path} missing")
        all_found = False

if all_found:
    print("Repository validation complete")
else:
    print("Repository validation failed — missing files above")