Phishing URL Detector – Backup Version
=====================================

Author: Tobias  
Date: April 2025  
Tool: Machine Learning-based Phishing URL Detection System  
Streamlit Link: https://phishing-detector.streamlit.app (Live Version)

-----

This ZIP contains a backup version of the deployed phishing detection system.

How to Run This App Locally:
----------------------------

1. Install Python 3.10+  
2. Open a terminal and navigate to this project folder  
3. Create a virtual environment (optional, but recommended):
   python -m venv venv
   venv\Scripts\activate    (Windows)
   source venv/bin/activate (Mac/Linux)

4. Install dependencies:
   pip install -r requirements.txt

5. Run the app:
   streamlit run app.py

6. Open your browser to:
   http://localhost:8501/

-----

Files included:
---------------
- app.py                  → Streamlit web interface
- features_extraction.py → URL feature extraction logic
- model_rf.pkl           → Random Forest model
- model_svm.pkl          → Support Vector Machine model
- model_nb.pkl           → Naive Bayes model
- logo.png               → Custom cybersecurity icon
- requirements.txt       → Python packages required

-----

Purpose:
--------
This backup ensures third-party evaluators can still access and test the deliverable
in case GitHub or Streamlit are unavailable at the time of submission.

