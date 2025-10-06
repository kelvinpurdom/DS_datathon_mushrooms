import streamlit as st
import pandas as pd
from src.pd_functions import *

# Path to results
RESULTS_PATH = 'data/true_y.csv'

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="🍄 Poisonous Mushroom Classifier",
    page_icon="🍄",
    layout="centered"
    st.markdown('Welcome to the housing classification app. Please enter your first name below, then upload your results file to check your accuracy and see the leaderboard.')
    st.markdown('🤖 Good Luck and remember it is just for fun!! 🤖')
    st.markdown('🏋🏻‍♂️ Remember to fit your model on (X, y) before you predict. 🏋🏻‍♂️'),
)

# --- DARK MODE STYLING ---
st.markdown(
    """
    <style>
        /* Set global background & text colors */
        body {
            background-color: #0e1117;
            color: #fafafa;
        }

        /* Style Streamlit elements */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }

        /* Title */
        .title-text {
            font-size: 2em;
            font-weight: 700;
            text-align: center;
            color: #ff4b4b;
            margin-top: -20px;
        }

        /* File uploader styling */
        .stFileUploader label {
            color: #fafafa !important;
            font-weight: bold;
        }

        /* Info, success, error boxes */
        .stAlert {
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- TITLE HEADER ---
st.markdown("## 🧫🍄 **Poisonous Mushroom Classification Competition** 🍄🧪")

def main():
    # Get participant name
    participant_name = get_participant_name()

    # Handle file upload
    if participant_name:
        uploaded_file = st.file_uploader("📤 Upload your prediction file (CSV):", type="csv")
        process_file_upload(uploaded_file, participant_name)

    # Show leaderboard
    try:
        show_leaderboard()
    except:
        st.info("⚠️ There are no submissions yet. Be the first one!")

def get_participant_name():
    text_input_container = st.empty()
    text_input_container.text_input("👤 Enter your participant name:", key="text_input")

    if st.session_state.text_input != "":
        text_input_container.empty()
        st.success(f'✅ Welcome, **{st.session_state.text_input}**!')
        return st.session_state.text_input

    return None

def process_file_upload(uploaded_file, participant_name):
    if uploaded_file is not None:
        try:
            test = get_ready_test(RESULTS_PATH, uploaded_file)
            
            if isinstance(test, pd.DataFrame):
                participant_results = get_metrics(RESULTS_PATH, test)    
                st.success('📊 Dataframe uploaded successfully!')
                display_participant_results(participant_results)
                update_submissions(participant_results)
                plot_submissions()

        except Exception as e:
            st.error(f"❌ The file format seems wrong. Please review and reload it.\n\n**Error:** {str(e)}")

def display_participant_results(participant_results):
    st.subheader('🏅 Participant Results')
    st.dataframe(participant_results, use_container_width=True)

if __name__ == "__main__":
    main()
