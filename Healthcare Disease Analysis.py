import streamlit as st
from openai import OpenAI
import json
import pandas as pd
import plotly.express as px

# Setup API Key
client = OpenAI(api_key=st.secrets["OPEN_API_KEY"])


def safe_float(value):
    """Βοηθητική συνάρτηση για μετατροπή σε νούμερο"""
    try:
        clean_value = str(value).replace('%', '').strip()
        return float(clean_value)
    except ValueError:
        return 0.0


def get_disease_info(disease_name):
    system_prompt = f"""
    You are a medical assistant. Provide information for {disease_name}. 
    Return STRICTLY in JSON format with these keys: 'name', 'statistics', 'recovery_options', 'medication'.
    'statistics' must contain: 'recovery_rate' (number only, 0-100), 'mortality_rate' (number only, 0-100).
    'recovery_options' should be a dictionary.
    'medication' should be a dictionary.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_prompt}]
    )
    return response.choices[0].message.content


def display_disease_info(disease_info):
    try:
        info = json.loads(disease_info)

        rec_rate = safe_float(info['statistics'].get('recovery_rate', 0))
        mort_rate = safe_float(info['statistics'].get('mortality_rate', 0))

        st.write(f"## Ανάλυση για: {info['name']}")

        tab1, tab2, tab3 = st.tabs(["📊 Στατιστικά", "🚑 Επιλογές Ανάρρωσης", "💊 Φάρμακα"])

        with tab1:
            st.metric("Recovery Rate", f"{rec_rate}%")

            # Δημιουργία στηλών για να μπουν τα γραφήματα δίπλα-δίπλα
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Pie Chart")
                fig_pie = px.pie(values=[rec_rate, mort_rate], names=['Ανάρρωση', 'Θνησιμότητα'],
                                 color_discrete_sequence=['#00CC96', '#EF553B'])
                st.plotly_chart(fig_pie, use_container_width=True)

            with col2:
                st.subheader("Bar Chart")
                df_bar = pd.DataFrame({'Κατηγορία': ['Ανάρρωση', 'Θνησιμότητα'], 'Ποσοστό': [rec_rate, mort_rate]})
                fig_bar = px.bar(df_bar, x='Κατηγορία', y='Ποσοστό', color='Κατηγορία',
                                 color_discrete_sequence=['#00CC96', '#EF553B'])
                st.plotly_chart(fig_bar, use_container_width=True)

        with tab2:
            for option, desc in info.get('recovery_options', {}).items():
                st.subheader(option)
                st.write(desc)

        with tab3:
            for med, desc in info.get('medication', {}).items():
                st.subheader(med)
                st.write(desc)

    except json.JSONDecodeError:
        st.error("Σφάλμα στην ανάγνωση των δεδομένων. Παρακαλώ δοκιμάστε ξανά.")


# UI
st.title("🏥 Disease Information Dashboard")
disease_name = st.text_input("Εισάγετε όνομα ασθένειας:")

if disease_name:
    with st.spinner('Αναζήτηση πληροφοριών...'):
        info_json = get_disease_info(disease_name)
        display_disease_info(info_json)