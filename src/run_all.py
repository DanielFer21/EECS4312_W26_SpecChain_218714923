"""runs the full pipeline end-to-end"""

import subprocess

#step 1: scrape data from google play store, populates reviews_raw.jsonl
collectData = "01_collect_or_import.py"
subprocess.run(["python", collectData], check=True)

#step 2: clean the dataset, populates reviews_clean.jsonl
cleanData = "02_clean.py"
subprocess.run(["python", cleanData], check=True)

#step 3: create groups then personas from the cleaned dataset using an LLM, populates review_groups_auto.josn and personas_auto.json
GandPGeneration = "05_personas_auto.py"
subprocess.run(["python", GandPGeneration], check=True)

#step 4: spec generation using the personas from the previous step, populates spec_auto.md
specGeneration = "06_spec_generate.py"
subprocess.run(["python", specGeneration], check=True)

#step 5: test generation using the requirements from previous step, populates tests_auto.json
testGeneration = "07_tests_generate.py"
subprocess.run(["python", testGeneration], check=True)

#step 6: metrics calculations, the following file automatically calculates metrics across all three piplines and also compiles all three into a summary file.
#the files are: metrics_auto.json, metrics_hybrid.json, metrics_manual.json and metrics_summary.json
metricsCalc = "08_metrics.py"
subprocess.run(["python", metricsCalc], check=True)

print("All auto processes complete.")

