"""computes metrics: coverage/traceability/ambiguity/testability"""

import json

#AUTO METRICS FILE
#LOAD ALL FILES:
#Review groups
with open("../data/review_groups_auto.json", "r") as f:
    reviewGroups = json.load(f)["groups"]

#Personas
with open("../personas/personas_auto.json", "r") as f:
    personas = json.load(f)["personas"]

#Tests
with open("../tests/tests_auto.json", "r") as f:
    tests = json.load(f)["tests"]

#Requirements
with open("../spec/spec_auto.md", "r") as f:
    specs = f.read()

#count num of requirements by making list of ids
requirementIDs = []
lines = specs.split("\n")

for line in lines:
    if line.startswith("# Requirement ID:"):
        reqId = line.replace("# Requirement ID:", "").strip()
        requirementIDs.append(reqId)

#accumulating results:
#1
pipeline = "automated"

#2
datasetSize = 600 #limit to pass to LLM for tokens

#3 - persona_count
personaCount = len(personas)

#4 - requirements_count
requirementsCount = len(requirementIDs)

#5 - tests_count
testsCount = len(tests)

#6 - traceability_links
traceabilityLinks = 0

#links from personas to group
traceabilityLinks += sum(1 for w in personas if w.get("derived_from_group"))

#links from requirements to persona
for line in lines:
    if line.startswith("- Source Persona:"):
        traceabilityLinks += 1

#links from test to requirements
traceabilityLinks += sum(1 for w in tests if w.get("requirement_id"))

#7 - review_coverage
allReviewIDs = set()
for group in reviewGroups:
    for revId in group.get("review_ids", []):
        allReviewIDs.add(revId)

reviewCoverage = len(allReviewIDs) / datasetSize

#8 - traceability_ratio
possibleLinks = personaCount + requirementsCount + testsCount
traceabilityRatio = traceabilityLinks / possibleLinks

#9 - testability_rate (1 test per requirement)
reqsWithTests = set()
for test in tests:
    if test.get("requirement_id"):
        reqsWithTests.add(test["requirement_id"])

testabilityRate = len(reqsWithTests) / requirementsCount

#10 - ambiguity_ratio
#list of ambiguous words to check against
vagueWords = ["may", "might", "could", "should", "possibly", "quickly", "rapidly", "instantaneous", "timely",
              "efficient", "significantly better", "usually", "normally", "frequently", "occasionally", "typically", 
              "periodically", "generally", "some", "many", "various", "approximately", "several", "roughly"]

ambiguousCount = 0
for line in lines:
    if line.startswith("- Description:"):
        desc = line.lower()
        if any(word in desc for word in vagueWords):
            ambiguousCount += 1

ambiguityRatio = ambiguousCount / requirementsCount


#put metrics in metrics_auto
metrics = {
    "pipeline": pipeline,
    "dataset_size": datasetSize,
    "persona_count": personaCount,
    "requirements_count": requirementsCount,
    "tests_count": testsCount,
    "traceability_links": traceabilityLinks,
    "review_coverage": round(reviewCoverage, 2),
    "traceability_ratio": round(traceabilityRatio, 2),
    "testability_rate": round(testabilityRate, 2),
    "ambiguity_ratio": round(ambiguityRatio, 2)
}

with open("../metrics/metrics_auto.json", "w") as f:
    json.dump(metrics, f, indent=4)

#---------------------------------------------------------------
#MANUAL METRICS FILE
#LOAD ALL FILES:
#Review groups
with open("../data/review_groups_manual.json", "r") as f:
    reviewGroups = json.load(f)["groups"]

#Personas
with open("../personas/personas_manual.json", "r") as f:
    personas = json.load(f)["personas"]

#Tests
with open("../tests/tests_manual.json", "r") as f:
    tests = json.load(f)["tests"]

#Requirements
with open("../spec/spec_manual.md", "r") as f:
    specs = f.read()

#count num of requirements by making list of ids
requirementIDs = []
lines = specs.split("\n")

for line in lines:
    if line.startswith("# Requirement ID:"):
        reqId = line.replace("# Requirement ID:", "").strip()
        requirementIDs.append(reqId)

#accumulating results:
#1
pipeline = "manual"

#2
datasetSize = 2506

#3 - persona_count
personaCount = len(personas)

#4 - requirements_count
requirementsCount = len(requirementIDs)

#5 - tests_count
testsCount = len(tests)

#6 - traceability_links
traceabilityLinks = 0

#links from personas to group
traceabilityLinks += sum(1 for w in personas if w.get("derived_from_group"))

#links from requirements to persona
for line in lines:
    if line.startswith("- Source Persona:"):
        traceabilityLinks += 1

#links from test to requirements
traceabilityLinks += sum(1 for w in tests if w.get("requirement_id"))

#7 - review_coverage
allReviewIDs = set()
for group in reviewGroups:
    for revId in group.get("review_ids", []):
        allReviewIDs.add(revId)

reviewCoverage = len(allReviewIDs) / datasetSize

#8 - traceability_ratio
possibleLinks = personaCount + requirementsCount + testsCount
traceabilityRatio = traceabilityLinks / possibleLinks

#9 - testability_rate (1 test per requirement)
reqsWithTests = set()
for test in tests:
    if test.get("requirement_id"):
        reqsWithTests.add(test["requirement_id"])

testabilityRate = len(reqsWithTests) / requirementsCount

#10 - ambiguity_ratio
#list of ambiguous words to check against
vagueWords = ["may", "might", "could", "should", "possibly", "quickly", "rapidly", "instantaneous", "timely",
              "efficient", "significantly better", "usually", "normally", "frequently", "occasionally", "typically", 
              "periodically", "generally", "some", "many", "various", "approximately", "several", "roughly"]

ambiguousCount = 0
for line in lines:
    if line.startswith("- Description:"):
        desc = line.lower()
        if any(word in desc for word in vagueWords):
            ambiguousCount += 1

ambiguityRatio = ambiguousCount / requirementsCount

#put metrics in metrics_manual
metrics = {
    "pipeline": pipeline,
    "dataset_size": datasetSize,
    "persona_count": personaCount,
    "requirements_count": requirementsCount,
    "tests_count": testsCount,
    "traceability_links": traceabilityLinks,
    "review_coverage": round(reviewCoverage, 2),
    "traceability_ratio": round(traceabilityRatio, 2),
    "testability_rate": round(testabilityRate, 2),
    "ambiguity_ratio": round(ambiguityRatio, 2)
}

with open("../metrics/metrics_manual.json", "w") as f:
    json.dump(metrics, f, indent=4)


#---------------------------------------------------------------
#HYBRID METRICS FILE
#LOAD ALL FILES:
#Review groups
with open("../data/review_groups_hybrid.json", "r") as f:
    reviewGroups = json.load(f)["groups"]

#Personas
with open("../personas/personas_hybrid.json", "r") as f:
    personas = json.load(f)["personas"]

#Tests
with open("../tests/tests_hybrid.json", "r") as f:
    tests = json.load(f)["tests"]

#Requirements
with open("../spec/spec_hybrid.md", "r") as f:
    specs = f.read()

#count num of requirements by making list of ids
requirementIDs = []
lines = specs.split("\n")

for line in lines:
    if line.startswith("# Requirement ID:"):
        reqId = line.replace("# Requirement ID:", "").strip()
        requirementIDs.append(reqId)

#accumulating results:
#1
pipeline = "hybrid"

#2
datasetSize = 600 #limit to pass to LLM for tokens

#3 - persona_count
personaCount = len(personas)

#4 - requirements_count
requirementsCount = len(requirementIDs)

#5 - tests_count
testsCount = len(tests)

#6 - traceability_links
traceabilityLinks = 0

#links from personas to group
traceabilityLinks += sum(1 for w in personas if w.get("derived_from_group"))

#links from requirements to persona
for line in lines:
    if line.startswith("- Source Persona:"):
        traceabilityLinks += 1

#links from test to requirements
traceabilityLinks += sum(1 for w in tests if w.get("requirement_id"))

#7 - review_coverage
allReviewIDs = set()
for group in reviewGroups:
    for revId in group.get("review_ids", []):
        allReviewIDs.add(revId)

reviewCoverage = len(allReviewIDs) / datasetSize

#8 - traceability_ratio
possibleLinks = personaCount + requirementsCount + testsCount
traceabilityRatio = traceabilityLinks / possibleLinks

#9 - testability_rate (1 test per requirement)
reqsWithTests = set()
for test in tests:
    if test.get("requirement_id"):
        reqsWithTests.add(test["requirement_id"])

testabilityRate = len(reqsWithTests) / requirementsCount

#10 - ambiguity_ratio
#list of ambiguous words to check against
vagueWords = ["may", "might", "could", "should", "possibly", "quickly", "rapidly", "instantaneous", "timely",
              "efficient", "significantly better", "usually", "normally", "frequently", "occasionally", "typically", 
              "periodically", "generally", "some", "many", "various", "approximately", "several", "roughly"]

ambiguousCount = 0
for line in lines:
    if line.startswith("- Description:"):
        desc = line.lower()
        if any(word in desc for word in vagueWords):
            ambiguousCount += 1

ambiguityRatio = ambiguousCount / requirementsCount

#put metrics in metrics_hybrid
metrics = {
    "pipeline": pipeline,
    "dataset_size": datasetSize,
    "persona_count": personaCount,
    "requirements_count": requirementsCount,
    "tests_count": testsCount,
    "traceability_links": traceabilityLinks,
    "review_coverage": round(reviewCoverage, 2),
    "traceability_ratio": round(traceabilityRatio, 2),
    "testability_rate": round(testabilityRate, 2),
    "ambiguity_ratio": round(ambiguityRatio, 2)
}

with open("../metrics/metrics_hybrid.json", "w") as f:
    json.dump(metrics, f, indent=4)