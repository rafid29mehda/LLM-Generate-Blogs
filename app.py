import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from huggingface_hub import hf_hub_download

# Function to get response from LLama 3.1 model (Meta-Llama-3.1-8B-Instruct)
def getLLamaResponse(input_text, no_words, blog_style):
    # Downloading the model from Hugging Face Hub
    model_path = hf_hub_download(repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct", filename="ggmlv3.q8_0.bin")

    # Initialize the LLama 3.1 model using CTransformers
    llm = CTransformers(model=model_path, 
                        model_type='llama',
                        config={'max_new_tokens': int(no_words),
                                'temperature': 0.01})
    
    # Prompt Template with Conditional Logic
    template = """
        {%- if blog_style == 'Researchers' -%}
        Write a formal blog post for researchers on the topic '{input_text}' within {no_words} words. 
        Include detailed analysis and references to relevant studies.
        {%- elif blog_style == 'Data Scientist' -%} 
        Write a technical blog post for data scientists on the topic '{input_text}' within {no_words} words. 
        Explain key concepts and include code snippets where appropriate.
        {%- elif blog_style == 'Common People' -%}
        Write a casual, engaging blog post for common people on the topic '{input_text}' within {no_words} words. 
        Use simple language and relatable examples to explain the topic.
        {%- endif -%}
    """
    
    prompt = PromptTemplate(input_variables=["blog_style", "input_text", "no_words"],
                            template=template)
    
    # Generate response from the LLama 3.1 model
    response = llm(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
    
    return response

# Streamlit Page Configuration
st.set_page_config(page_title="Generate Blogs", 
                   page_icon='🤖', 
                   layout='centered', 
                   initial_sidebar_state='collapsed')

# App Header
st.header("Generate Blogs 🤖")

# Input Fields
input_text = st.text_input("Enter the Blog Topic")

# Creating two more columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')
with col2:
    blog_style = st.selectbox('Writing the blog for',
                              ('Researchers', 'Data Scientist', 'Common People'),
                              index=0)

# Generate Button
submit = st.button("Generate")

# Final Response
if submit:
    if input_text and no_words and blog_style:
        try:
            response = getLLamaResponse(input_text, no_words, blog_style)
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please fill out all fields!")
