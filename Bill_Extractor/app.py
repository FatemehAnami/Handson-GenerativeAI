import streamlit as st 
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
# load all environment variables
load_dotenv()


genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")

# function to load Gmini model
def get_gemini_response(request, image, prompt):
    response = model.generate_content([prompt, image[0], request])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None :
        # read the file into bytes
        bytes_of_image = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data": bytes_of_image
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file Uploaded")
    
# initialize streamlit
st.set_page_config(page_title="MultiLanguage Bill Extractor")

st.header("Multi Language Bill Extractor powered by Gimini")

upload_file = st.file_uploader("Select an image of Bill", type = ["jpg", "jpeg", "png"])
image = ""
if upload_file is not None :
    image = Image.open(upload_file)
    st.image(image, caption = "Uploaded Bill Image.", use_column_width = True)

input_text = st.text_input("Enter your question about bill: ", key = "input")
submit = st.button("Send")

input_prompt = """
You are an expert in understanding Bills. We will upload an image and you will have to answer any questions based on the uploaded Bill image
"""

# If submit botten clicked
if submit :
    image_data = input_image_details(upload_file)
    response = get_gemini_response(input_text, image_data, input_prompt)
    st.subheader("The Response is: ")
    st.write(response)

