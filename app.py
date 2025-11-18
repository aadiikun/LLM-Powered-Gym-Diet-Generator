import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
import streamlit as st
from prompts import diet_prompt

# ---------------------------------------------------------
# BEAUTIFUL METALLIC BLUE THEME (CSS)
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Remove top padding, margin, and white line */
    .css-18e3th9, .css-1d391kg { 
        padding-top: 0 !important;
    }

    /* Remove Streamlit default top padding */
    main.block-container {
        padding-top: 0rem !important;
    }

    /* Remove extra spacing around header */
    header, .stApp > header {
        height: 0 !important;
        background: transparent !important;
    }

    /* Remove any leftover white line */
    .stApp {
        margin-top: -20px !important;
    }

    /* --- Background --- */
    body, .stApp {
        background: linear-gradient(135deg, #0a1a2f, #102f4a);
        color: #e4e4e4 !important;
    }

    /* --- All text labels (inputs, form headers, titles) --- */
    label, .stMarkdown, .stText, .stNumberInput label, 
    .stSelectbox label, .stFormHeader, .stSubheader,
    h1, h2, h3, h4 {
        color: #e4e4e4 !important;
        font-weight: 600;
    }

    /* --- Metallic Black Input Boxes --- */
    input, textarea {
        background: #0d0d0d !important;
        color: #d9d9d9 !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 6px !important;
        padding: 10px !important;
    }

    /* --- SELECTBOX OUTER CONTAINER --- */
    div[data-baseweb="select"] > div {
        background: #0d0d0d !important;
        color: #d9d9d9 !important;
        border-radius: 6px !important;
        border: 1px solid #3a3a3a !important;
    }

    /* --- SELECTBOX selected text --- */
    .css-1dimb5e, .css-1wa3eu0-placeholder {
        color: #d9d9d9 !important;
    }

    /* --- SELECTBOX dropdown list --- */
    div[role="listbox"] {
        background: #0d0d0d !important;
        color: #d9d9d9 !important;
        border-radius: 6px !important;
        border: 1px solid #333 !important;
    }

    /* --- SELECTBOX hover option --- */
    div[role="option"]:hover {
        background: #1b1b1b !important;
    }

    /* --- Regular buttons (NOT the form button) --- */
    .stButton>button {
        background: linear-gradient(135deg, #2b6ca3, #3e8ad1);
        color: black !important;
        border: none;
        padding: 10px 22px;
        border-radius: 6px;
        font-size: 16px;
        font-weight: 600;
        transition: 0.5s;
        cursor: pointer;
    }

    .stButton>button:hover {
        transform: scale(1.02);
    }

    /* --- Code block --- */
    .stCodeBlock {
        background: #0d0d0d !important;
        border: 1px solid #333 !important;
        border-radius: 8px;
    }

    /* -------------------------------------------------
       FIX: STYLE THE "Generate Diet Plan" (FORM BUTTON)
       ------------------------------------------------- */
    div.stForm button[kind="secondary"] {
        background: linear-gradient(135deg, #2b6ca3, #3e8ad1) !important;
        color: black !important;
        border: none !important;
        padding: 10px 22px !important;
        border-radius: 6px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: 0.3s !important;
        cursor: pointer !important;
    }

    div.stForm button[kind="secondary"]:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 10px rgba(70,130,200,0.8) !important;
    }

</style>
""", unsafe_allow_html=True)



# ---------------------------------------------------------
# (Your Logic — UNTOUCHED)
# ---------------------------------------------------------

groq_api_key=os.getenv("GROQ_API_KEY")

groq_api_key = st.text_input(
    "🔑 Enter your GROQ API Key to continue:",
    type="password",
    help="You can get your API key from https://console.groq.com/"
)

if not groq_api_key:
    st.warning("⚠️ Please enter your GROQ API key above to start using the app.")
    st.stop()

llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama-3.1-8b-instant")

st.set_page_config(page_title="Gym Diet Generator", page_icon="🥗")
st.title("🥗 Gym Diet Plan")
st.write("Fill in the details below to generate a personalized diet plan for your clients.")

with st.form("diet_form"):
    st.subheader("Client Details")

    name=st.text_input("Enter your name")
    age=st.number_input("Age",min_value=10,max_value=80)
    weight=st.number_input("Weight(in kg)",min_value=30,max_value=200)
    height=st.number_input("Height(in cm)",min_value=120,max_value=220)

    goal=st.selectbox("Fitness Goal",["Weight Loss","Muscle Gain","Maintainence"])
    diet_type=st.selectbox("Diet Preference",["Veg","Non-Veg","Vegan","Egg + Veg"])
    activity_level=st.selectbox("What is your daily activity level?",[
        "Lazy( In home all day )",
        "Moderate( Goes to work but that is it)",
        "Active (Have a decently hectic schedule that tires you out)",
        "Intensly Active (Spare time for gym even after a hectic schedule)"
    ])

    allergies=st.text_input("Any allergies? (optional)")

    submitted=st.form_submit_button("Generate Diet Plan")

if submitted:
    filled_prompt=diet_prompt.format(
        name=name,
        age=age,
        weight=weight,
        height=height,
        goal=goal,
        diet_type=diet_type,
        activity_level=activity_level,
        allergies=allergies if allergies else "None"
    )

    
    
    with st.spinner("Generating diet plan"):
        response=llm.invoke(filled_prompt)
    
    st.subheader("🍽️ Personalized Diet Plan")
    st.write(response.content)
