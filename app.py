import streamlit as st
import joblib
from features_extraction import extract_features

# Load models
rf_model = joblib.load("model_rf.pkl")
svm_model = joblib.load("model_svm.pkl")
nb_model = joblib.load("model_nb.pkl")

# Page config
st.set_page_config(page_title="Phishing URL Checker", layout="wide")
st.title("🔍 Phishing URL Checker")

st.markdown("This simple tool helps you check if a website link might be **phishing** or **safe**, using smart machine learning models.")

# ========== SIDEBAR ==========
with st.sidebar.expander("🎣 What is Phishing?", expanded=False):
    st.markdown("""
    **Phishing** is a type of online scam where attackers trick people into clicking on fake links or entering sensitive information.

    These websites often:
    - Look very real
    - Use long, confusing links
    - Include numbers and symbols to look legitimate

    This tool helps detect phishing attempts by analyzing the link itself.
    """)

with st.sidebar.expander("ℹ️ How This Tool Works", expanded=False):
    st.markdown("""
    **This tool uses machine learning** to analyze website links (URLs) and predict if they are safe or suspicious.

    - You enter a link
    - We extract simple features:
        - Length of the link
        - Number of numbers
        - Number of symbols
    - A trained model checks if the pattern matches known phishing techniques
    - You get a result with explanation and confidence

    No personal data is collected or saved.
    """)

# ========== MAIN APP ==========
st.write("👋 **Paste a website link below and choose a model. Then click 'Check This URL' to get a result.**")

# Input
url_input = st.text_input("🔗 Website URL (e.g. https://login-bank.example.com)")
model_choice = st.selectbox("🧠 Choose a Model", ["Random Forest", "SVM", "Naïve Bayes"])

# Model selector and description
if model_choice == "Random Forest":
    selected_model = rf_model
    with st.expander("🌲 About Random Forest", expanded=True):
        st.markdown("""
        Random Forest is a model made up of many small decision trees.  
        It works well with noisy data and handles real-world phishing patterns effectively.
        """)
elif model_choice == "SVM":
    selected_model = svm_model
    with st.expander("💡 About SVM", expanded=True):
        st.markdown("""
        Support Vector Machine (SVM) finds the best boundary between phishing and safe URLs.  
        It’s highly accurate with clean, text-based data like URLs.
        """)
else:
    selected_model = nb_model
    with st.expander("📊 About Naïve Bayes", expanded=True):
        st.markdown("""
        Naïve Bayes is a fast, lightweight model based on probability.  
        It works well as a baseline for spam and phishing detection.
        """)

# Predict button
if st.button("✅ Check This URL"):
    if url_input:
        features_dict = extract_features(url_input)
        features = list(features_dict.values())

        prediction = selected_model.predict([features])[0]

        try:
            proba = selected_model.predict_proba([features])[0][1]
            confidence = proba if prediction == 1 else 1 - proba
        except:
            confidence = None

        # Display result
        if prediction == 1:
            st.markdown("<h1 style='text-align: center; color: red;'>🔴</h1>", unsafe_allow_html=True)
            st.markdown("## 🚨 This website might be a **phishing site**.")
            st.error("Be cautious. This link looks suspicious.")
        else:
            st.markdown("<h1 style='text-align: center; color: green;'>🟢</h1>", unsafe_allow_html=True)
            st.markdown("## ✅ This website looks **safe**.")
            st.success("No signs of phishing were detected.")

        if confidence is not None:
            st.markdown(f"**Confidence:** {confidence:.2%}")
            st.progress(confidence)

        # 🧠 Why This Result?
        with st.expander("🔍 Why This Result?", expanded=False):
            for name, value in features_dict.items():
                explanation = ""
                if prediction == 1:  # Phishing
                    if name == "url_length":
                        explanation = "Long URLs can be used to disguise dangerous links."
                    elif name == "special_char_count":
                        explanation = "Too many symbols can be used to confuse or trick users."
                    elif name == "digit_count":
                        explanation = "Phishing URLs often use numbers to imitate real sites."
                else:  # Legitimate
                    if name == "url_length":
                        explanation = "This URL is short and easy to read — typical of safe websites."
                    elif name == "special_char_count":
                        explanation = "This URL has few symbols, which is normal for legitimate sites."
                    elif name == "digit_count":
                        explanation = "There are few or no digits — phishing sites often use numbers to deceive."

                st.markdown(f"- **{name.replace('_', ' ').title()}**: {value} → {explanation}")

        # Save history
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append((url_input, model_choice, prediction))

    else:
        st.warning("⚠️ Please paste a URL to check.")

# History
st.markdown("---")
if "history" in st.session_state and st.session_state.history:
    with st.expander("🕓 View Past Checks", expanded=False):
        for url, model, result in st.session_state.history[-5:][::-1]:
            label = "Phishing" if result == 1 else "Legitimate"
            icon = "🚨" if result == 1 else "✅"
            st.markdown(f"- {icon} **{url}** → {label} ({model})")

# Footer
# Disclaimer at the bottom of the page
st.markdown("---")
st.caption("⚠️ This tool may occasionally make incorrect predictions. Always use caution and verify suspicious URLs through trusted sources.")

st.markdown("---")
st.caption("Phishing Detection Web App | Dissertation Project | 2025")








