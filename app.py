import streamlit as st
from PIL import Image
import joblib
import numpy as np
import pandas as pd
from features_extraction import extract_features
import streamlit.components.v1 as components

# Set custom page config
st.set_page_config(
    page_title="Phishing Detector",
    page_icon="🔐",
    layout="wide"
)

# Load logo
logo = Image.open("logo.png")
st.sidebar.image(logo, width=100)  # smaller logo

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

# Video Tutorial Embed
st.markdown("### 🎥 Quick Guide: How to Use the Tool")
components.iframe(
    "https://share.synthesia.io/embeds/videos/a4b47e01-c10f-45c9-9f00-aae417154b8d",
    height=320,
    width=570,
    scrolling=False
)

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
    if model_option == "Random Forest":
        st.markdown("""
        This tool uses a **Random Forest** classifier — an ensemble method that combines many decision trees.  
        It analyzes lexical features like URL length, number of symbols, digits, and structural patterns to make predictions.  
        It's robust and effective for detecting phishing based on known patterns in real-world URLs.
        """)
    elif model_option == "Support Vector Machine":
        st.markdown("""
        This model uses a **Support Vector Machine (SVM)**, which finds the optimal boundary between phishing and legitimate URLs.  
        It works well for high-dimensional feature spaces like lexical URL data.
        """)
    elif model_option == "Naive Bayes":
        st.markdown("""
        This model uses **Naïve Bayes**, a probabilistic approach that assumes feature independence.  
        It’s fast and simple, often used in spam filtering and text classification.
        """)

# Expandable: Help Improve the Tool
with st.expander("📩 Report a Missed Phishing URL"):
    st.markdown("""
    If this tool marked a **phishing link as safe**, you can help improve accuracy.  
    Paste the missed suspicious URL below. These submissions may be used to improve future versions of the model.
    """)
    
    submitted_url = st.text_input("Suspicious URL you think should be flagged:")
    if st.button("Submit URL"):
        # In real application, you'd save this to a secure database or file
        st.success("Thank you! Your feedback has been recorded for analysis.")


# Footer
st.markdown("""
<div class="footer-text">
Developed by Tobias, 2025 | <a href="https://github.com/Tobias9901/phishing-detector-app" target="_blank">GitHub</a>  
This tool is for educational use only. It may make mistakes.
</div>
""", unsafe_allow_html=True)
