import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from dotenv import load_dotenv
import os
load_dotenv()


def get_llama_response(input_text, number_of_words, blog_style):
    
    """
    Function for loading the model, settg request template
    it will run the llama model with given variables and return the blog related to the template
    """
    # calling the llama 2 model
    llm = CTransformers(model = os.getenv("MODEL_ADDRESS"),
                        model_type = "llama",
                        config = {"max_new_tokens": 256,
                                  "temperature": 0.01}
                        )

    # Prompt Template
    prompt_template = """
        Write a blog for {style} job profile for a topic {text}
        within {no_words}.
        """
    
    # create the prompt templte
    prompt = PromptTemplate(template = prompt_template, 
                            input_variables = ["style", "text", "no_words"]
                            )
    # genetate the response from LLAMA 2 model
    response = llm(prompt.format(style = blog_style, text = input_text, no_words = number_of_words))
    print(response)
    return response



# initialize streamlit
st.set_page_config(page_title = "Generate Blogs",
                   page_icon = "🔥",
                   layout = "centered",
                   initial_sidebar_state = "collapsed")

st.header("Generate Blogs 🔥")
input_text = st.text_input("Enter The Blog Topic")

# creating colums 
col1, col2 = st.columns([5,5])
with col1:
    number_of_words = st.text_input("Number of Words")
    
with col2:
    blog_style = st.selectbox("Writing The Blog For",
                              ("Researchers", "Data Scientists", "Common People"))
    
submit = st.button("Generate") 

## final Response
if submit:
    response = get_llama_response(input_text, number_of_words, blog_style)
    st.write(response)