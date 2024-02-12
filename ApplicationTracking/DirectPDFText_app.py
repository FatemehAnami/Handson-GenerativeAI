import streamlit as st 
import os
import io
from pypdf import PdfReader
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv
# load all environment variables
load_dotenv()


genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# function to load Gmini model
def get_gemini_response(prompt):
    """ 
    Function for analysing resume and return the similarity of the role with
    applicant resume 

    Args:
        input_text (string): the detail description of the Role

    Returns:
        text: the response of gemeni
    """
    response = model.generate_content(prompt)
    return response.text

def convert_pdf_to_text(uploaded_file):
    """Function for uploading resume and return text within it

    Args:
        uploaded_file (pdf): resume of the applicant
    Returns:
        text: the coverted content to text
    """
    contents = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            contents += page.extract_text()
    return contents



# initialize streamlit
st.set_page_config(page_title="Application Tracker System")

st.header("Evaluate The Appication form based on Job Description")
jd = st.text_input("Enter Job Description: ", key = "input")
uploaded_file = st.file_uploader("Select an image of Bill", type = ["pdf"])
submit = st.button("Analysis")

if uploaded_file is not None :
    resume_contents = convert_pdf_to_text(uploaded_file)


input_prompt = """
You are like an experienced ATS (Application Tracking System) with a deep understanding of tech field, data science, software engineer,
Web development, Big Data Egineering, Devops, Data Analysys, your task is to review
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile which is given in resume_contents 
aligns with the job description explains in jd and give your best assistance for improving the resume.
Give the percentage of match based on jd, aslo give the strength of condidate based on resume_contents and missing keywords in it with high accuracy. 
resume: {resume_contents}
description: {jd}

I want the response having the structure
{{"JD Match" : "%", 
"Strength Keywords : []", 
"Missing KeyWords : []", 
"Profile Summary" : ""}}
"""    

# If submit botten clicked
if submit :
    response = get_gemini_response(input_prompt)
    st.subheader("The Response is: ")
    st.write(response)

