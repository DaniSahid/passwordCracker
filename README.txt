=============================================================
  CSC662 — PASSWORD CRACKING SIMULATOR
  UiTM Faculty of Computer and Mathematical Sciences
=============================================================

FILES IN THIS FOLDER:
─────────────────────
  app.py                  → Streamlit interactive web app
  cracker.ipynb           → Jupyter notebook: dictionary attack simulator
  chart_generator.ipynb   → Jupyter notebook: generates report charts
  wordlist.txt            → Password dictionary (keep in same folder!)
  requirements.txt        → Python dependencies

HOW TO RUN:
─────────────────────

1. INSTALL DEPENDENCIES (run once):
   pip install -r requirements.txt

2. STREAMLIT APP (interactive demo):
   streamlit run app.py
   → Opens in browser at http://localhost:8501

3. JUPYTER NOTEBOOKS (for report):
   jupyter notebook
   → Run cracker.ipynb first  (produces results.csv)
   → Run chart_generator.ipynb (produces charts/ folder)

IMPORTANT:
─────────────────────
  All files must stay in the SAME folder.
  wordlist.txt must be present for the attack to work.

=============================================================
  EDUCATIONAL USE ONLY — CSC662 Cyber Security Awareness
=============================================================
