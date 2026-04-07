"""cleans raw data & make clean dataset"""
import json
from num2words import num2words
import pandas as pd
import spacy
from spacy.cli import download

#spaCy for stopwords and lemmatization
download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

#Load raw reviews and put into dataframe
reviews = []
with open("../data/reviews_raw.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        reviews.append(json.loads(line))

dataFrame = pd.DataFrame(reviews)

#1. Drop duplicate reviews
dataFrame = dataFrame.drop_duplicates(subset="content")

#2. Remove empty reviews
dataFrame = dataFrame[dataFrame["content"].str.strip() != ""]

#3. Remove very short reviews (20 characters or less)
dataFrame = dataFrame[dataFrame["content"].str.len() > 20]

#4. All reviews to lowercase
dataFrame["content"] = dataFrame["content"].str.lower()

#5. Remove emojis
dataFrame["content"] = dataFrame["content"].str.replace(r'[^\x00-\x7F]+', '', regex=True)

#6. Remove special characters (keep letters and numbers for num2words)
dataFrame["content"] = dataFrame["content"].str.replace(r'[^a-z0-9\s]', ' ', regex=True)

#7. Num to words
dataFrame["content"] = dataFrame["content"].apply(
    lambda x: ' '.join([num2words(int(w)) if w.isdigit() else w for w in x.split()])
)

#8. Remove stopwords
dataFrame["content"] = dataFrame["content"].apply(
    lambda x: ' '.join([token.text for token in nlp(x) if not token.is_stop])
)

#9. Lemmatize
dataFrame["content"] = dataFrame["content"].apply(
    lambda x: ' '.join([token.lemma_ for token in nlp(x) if token.is_alpha])
)

#10. Remove extra whitespace
dataFrame["content"] = dataFrame["content"].str.replace(r'\s+', ' ', regex=True).str.strip()

#Save cleaned data
with open("../data/reviews_clean.jsonl", "w", encoding="utf-8") as f:
    for _, row in dataFrame.iterrows():
        f.write(json.dumps(row.to_dict()) + "\n")

print(f"Saved {len(dataFrame)} cleaned reviews.")