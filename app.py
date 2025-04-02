import streamlit as st
from PIL import Image
import joblib
import numpy as np
import pandas as pd
from features_extraction import extract_features

# Set custom page config
st.set_page_config(
    page_title="Phishing Detector",
    page_icon="🔐",
    layout="wide"
)

# Load logo
logo = Image.open("logo.png")
st.sidebar.image(logo, width=150)

# Sidebar - Help & Info
st.sidebar.title("🔹 Help & Info")
st.sidebar.markdown("""
**How to Use**
- Paste a URL in the input field
- Choose a detection model
- Click **Check This URL** to run prediction

**What is Phishing?**
Phishing sites are fake websites used to steal personal info. They may:
- Look nearly identical to trusted sites
- Use strange symbols or misspellings
- Trick users into clicking unsafe links

**Examples:**
- `https://login-facebook.security-alert.com`
- `https://apple-id-reset-login.info`

:warning: *This tool makes predictions using machine learning. It may not always be correct.*
""")

# Custom CSS for theme
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Open Sans', sans-serif;
        background-color: #f4f6f9;
    }
    .main h1 {color: #003366; font-size: 3em;}
    .stButton > button {
        background-color: #003366;
        color: white;
        border-radius: 8px;
    }
    footer {visibility: hidden;}
    .footer-text {
        text-align: center;
        font-size: 0.8em;
        color: #888;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🔐 Phishing URL Detector")
st.markdown("""
This tool helps you detect whether a URL is **phishing** or **legitimate** using machine learning.
Paste a link, choose a model, and get a result instantly.
""")

# Input URL
url_input = st.text_input("Paste a website URL (e.g. https://login-bank-example.com)", "https://google.com")

# Model selection
model_option = st.selectbox("Choose a model:", ["Random Forest", "Support Vector Machine", "Naive Bayes"])
model_map = {
    "Random Forest": joblib.load("model_rf.pkl"),
    "Support Vector Machine": joblib.load("model_svm.pkl"),
    "Naive Bayes": joblib.load("model_nb.pkl")
}
model = model_map[model_option]

# Predict
if st.button("Check This URL"):
    with st.spinner("Analyzing the URL, please wait..."):
        try:
            features = extract_features(url_input)
            X = pd.DataFrame([features.values()], columns=features.keys())
            prediction = model.predict(X)[0]

            if hasattr(model, "predict_proba"):
                confidence = round(np.max(model.predict_proba(X)) * 100, 2)
            else:
                confidence = "-"

            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric(
                    label="\n\nResult",
                    value="\n\n🟢 Legitimate" if prediction == 0 else "🔴 Phishing",
                    delta=f"Confidence: {confidence}%" if confidence != "-" else ""
                )
            with col2:
                st.info("""
                    **Why this result?**  
                    Based on the URL's length, digits, dashes, symbols, and structure — the model flagged it accordingly.
                """)
        except Exception as e:
            st.error("Something went wrong during prediction.")
            st.exception(e)

# Expandable: About the Model
with st.expander("ℹ️ About the Model"):
    st.markdown(f"This page uses a **{model_option}** classifier trained on real-world phishing URLs. It analyzes lexical URL patterns.")

# Expandable: Feedback form
with st.expander("📩 Submit Suspicious URL (Mock-up)"):
    suspicious_url = st.text_input("Suspicious URL:")
    if st.button("Submit for review"):
        st.success("Thanks! This mock form does not store data.")

# Footer
st.markdown("""
<div class="footer-text">
Developed by Tobias, 2025 | <a href="https://github.com/Tobias9901/phishing-detector-app" target="_blank">GitHub</a>  
This tool is for educational use only. It may make mistakes.
</div>
""", unsafe_allow_html=True)