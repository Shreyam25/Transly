from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()  # Take environment variables from .env

# Configure Google API key
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Streamlit app
st.set_page_config(page_title="Transly",
                   page_icon="https://i.pinimg.com/564x/78/0c/0a/780c0a065eda7ccfaf90967bd77de846.jpg",
                   initial_sidebar_state="collapsed")

# Add circular styling to the image using CSS

# Custom CSS styling for the background and title
page_element = """
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://i.pinimg.com/564x/c3/82/d1/c382d12cba3ae52de5f25cb0b8af9c3e.jpg");
  color: white;
}
.stMarkdown,.stMarkdown span {
    color: white;
    font-family: Papyrus, fantasy;
}
 .stTextInput label { /* Change input label color */
      color: white !important; /* Set the desired color */
      font-family: cursive;
    }
    .stSelectbox label { /* Change select box label color */
      color: white !important; /* Set the desired color */
      font-family: cursive;}


.stButton>button {
            color: black !important;
            background-color: white !important;
            border-color: black !important;
        }

        /* Add animation for background color transition */
        @keyframes goldenTransition {
            0% { background-color: white; }
            100% { background-color: goldenrod; }
        }

        /* Apply animation to the button */
        .stButton>button:hover {
            animation: goldenTransition 0.5s forwards;
        }

}
</style>
"""
st.markdown(page_element, unsafe_allow_html=True)

# Display the title
st.markdown(
    """
    <h1 style="color:white; font-family: Papyrus, fantasy; line-height: 26.4px; font-weight: bold">Transly </h1>
    """,
    unsafe_allow_html=True
)



# User input fields

to_lang = st.selectbox("To Language:", ["English","Korean" ,"Spanish", "French", "German","Japanese"])  # Add more languages as needed

input_text = st.text_input("Write something here:", key="input")

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

# Translate button
submit_button = st.button("Translate")

# Translation function
def get_gemini_response(question, to_lang):
    model=genai.GenerativeModel("gemini-1.0-pro",generation_config=generation_config) 
    p = f"""
    <sys>You are TongueTalk bot, who helps people translate text. The user provided the following text  {question}.</sys>
    Please translate it to {to_lang}. Additionally, provide an approximation of the pronunciation in English characters (if possible). 
    output should be on differennt lines
     **{to_lang}** : Text in {to_lang} \n\n\\n 
    **script** : {to_lang} 

    Prompt: {question}
    """

    chat = model.start_chat(history=[])
    response = chat.send_message(p, stream=True)
   
    return response

# If the "Translate" button is clicked
if submit_button:
    st.subheader("Translation:")

    response = get_gemini_response(input_text ,to_lang)
    for chunk in response:
        st.write(chunk.text)
