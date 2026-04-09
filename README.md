# EECS4312_W26_SpecChain

Application: [Wysa]

Data collection method: google_play_scraper
- reviews_raw.jsonl contains the collected reviews (3000).
- reviews_clean.jsonl contains the cleaned dataset (2506).

# Repository Structure:
- data/ contains datasets and review groups
- personas/ contains persona files
- spec/ contains specifications
- tests/ contains validation tests
- metrics/ contains all metric files
- src/ contains executable Python scripts
- reflection/ contains the final reflection

## instructions:
How to Run:
1. python src/00_validate_repo.py
2. python src/run_all.py
3. Open metrics/metrics_summary.json for comparison results

Please note that it is required to pip install all necessary packages:
- google_play_scraper
- num2words
- pandas
- spacy
- groq

Also to use your own API key from groq, do this command in terminal:
- export GROQ_API_KEY="YOUR_API_KEY_HERE" (MacOS)
- set GROQ_API_KEY=YOUR_API_KEY_HERE (Windows cmd)


