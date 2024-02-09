from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(text,pdf_content,prompt):
    '''
    Function to crete an instance of Gemini vision model
    the model will get the input question, resume content and a prompt 
    to talk with Gemini and return the response of Gemini 
    '''
    response = model.generate_content([prompt,pdf_content[0],text])
    return response.text


def input_pdf_setup(uploaded_file):
    """
    Function for converting the resume in pdf formet to image format
    then it can be read by Gemini model and interpret
    """
    if uploaded_file is not None:
        
        images = pdf2image.convert_from_bytes(uploaded_file.read(),
                                              poppler_path = os.getenv("POPPLER_PATH"))
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        #first_page = images[0]
        total_width = max(img.width for img in images)
        total_hight = sum(img.height for img in images)
        all_pages = Image.new("RGB", (total_width, total_hight))
        offset = 0
        for image in images :
            all_pages.paste(image, (0,offset))
            offset+= image.height
          
        all_pages.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type" :  "image/jpeg",
                "data": img_byte_arr
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# initialize user interface
st.set_page_config(page_title = "ATS Resume Expert")
st.header('Application Tracker System')
input_text = st.text_area("Enter Jop Description:", key = "input")
uploaded_file = st.file_uploader("Upload your resume in PDF format", type = ["pdf"])



if uploaded_file is not None and uploaded_file.type == "application/pdf":
    st.write("Your Resume Uploaded Successfuly.")
    print(uploaded_file)
else:
    st.write("Please upload a PDF file")
    

submit_summary = st.button("Tell me about the resume")

input_prompt_summary = '''
You are an experienced Technical HR with Expreience in the field of data science, Full stack 
Web development, Big Data Egineering, Devops, Data Analysys, your task is to review
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with role. give me the percentage of match if 
the resume matches job description. 
First the output should come as percentge, Second output should be the strengths of the 
relation to the specific job profiles, Third output should be the weaknesses as compare to related job profile and 
final output should be your final tought..
'''

if submit_summary:
    if uploaded_file is not None:
        # convert pdf file to image then it will be nterpritable by Gemini pro vision 
        pdf_content=input_pdf_setup(uploaded_file)

        response=get_gemini_response(input_text, pdf_content, input_prompt_summary)
        st.subheader("The repsonse is:")
        #st.image(pdf_content, caption = "Page1", use_column_width= True)
        st.write(response)
    else:
        st.write("Please uplaod the resume")
