import streamlit as st
from gtts import gTTS
from io import BytesIO
from PIL import Image
import base64
import google.generativeai as genai

# Load the image from your local system
image_path = "angel.jpeg"  # Ensure the image is located at this path
image = Image.open(image_path)

# Function to convert the image to base64 for embedding into CSS
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Convert the image to base64
image_base64 = image_to_base64(image)

# Set the moving background using CSS and change text color to black
st.markdown(
    f"""
    <style>
    /* Create a moving background using CSS animation */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_base64}");
        background-size: cover;
        background-attachment: fixed;
        animation: moveBackground 10s linear infinite;
    }}

    /* Keyframe animation to move the background */
    @keyframes moveBackground {{
        0% {{ background-position: 0 0; }}
        100% {{ background-position: -200px -200px; }}
    }}

    /* Change text color to black */
    body, .stMarkdown, h1, h2, h3, h4, h5, h6, p {{
        color: black !important;
        font-size: 20px !important;  /* Increase font size */
        font-weight: bold !important; /* Make text bold */
    }}
    /* Customize the button */
    .stButton > button {{
        background-color: red !important;  /* Change button color to red */
        color: white !important;  /* Button text color to white */
        font-size: 18px !important;  /* Increase button text font size */
        font-weight: bold !important;  /* Make button text bold */
        border-radius: 12px;  /* Make button edges rounded */
        padding: 0.5em 1.5em;  /* Add padding to the button */
        border: none;  /* Remove button border */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);  /* Add shadow to the button */
    }}
    .stButton > button:hover {{
        background-color: darkred !important;  /* Change button color on hover */
        cursor: pointer;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);  /* Add shadow on hover */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Configure the Google Generative AI (Gemini) API
api_key = "AIzaSyAMiWy1F1dafR2lENKoyVh0nIF75kerdaw"  # Replace with your actual Google Generative AI API key
genai.configure(api_key=api_key)

# Create the generative model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Streamlit App Layout
st.markdown("<h1>✨ AI Story Generator 🧚‍♀️📚</h1>", unsafe_allow_html=True)
st.markdown("<h2>Story Settings 📝</h2>", unsafe_allow_html=True)

story_type = st.selectbox("Choose the type of story 🏰", ["Fantasy 🧙‍♂️", "Sci-Fi 🚀", "Mystery 🕵️‍♀️", "Romance 💖"])
prompt = st.text_area("Enter your prompt for the story ✍️:", "A brave knight sets out on a quest 🏇.")
language = st.selectbox("Select the language 🌍", ["English 🇬🇧", "Spanish 🇪🇸", "French 🇫🇷", "German 🇩🇪", "Chinese 🇨🇳", "Malayalam 🇮🇳"])

# Generate Story Button
if st.button("Generate Story 🎉"):
    user_input = f"A {story_type} story. Prompt: {prompt}"
    
    try:
        # Start a chat session and generate a story
        chat_session = model.start_chat(
            history=[
                {"role": "user", "parts": [user_input]},
            ]
        )
        response = chat_session.send_message("Please generate the story.")
        story_text = response.text

        # Display the generated story
        st.markdown("<h2>Generated Story 📖:</h2>", unsafe_allow_html=True)
        st.write(story_text)

        # Generate voice-over using gTTS
        st.markdown("<h2>Voice Over 🎤:</h2>", unsafe_allow_html=True)
        lang_code = 'ml' if language == 'Malayalam' else 'en'  # Add more language codes if necessary
        tts = gTTS(text=story_text, lang=lang_code)
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)

        # Play the generated voice-over
        st.audio(audio_file, format='audio/mp3')

    except Exception as e:
        st.error(f"An error occurred: {e}")
