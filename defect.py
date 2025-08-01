import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai


from PIL import Image # pillow is used to load,save and manipulate images

st.set_page_config(page_title="Structural Defect Detection", page_icon=":construction_worker:", layout="wide")

st.title('AI assistant for :green[Structural Defect Detection]')


st.subheader(':blue[Prototype for automated structural defect analysis]',divider=True)

with st.expander("About the application", expanded=True):
    st.markdown(''' This prototype is used to detect the structural defects and analyze the 
                defects using AI-powered systems,=.
                - **Defect Deection**: Automatically detects the structural defects in the given images like cracks.
                -**Recommendations**: provides solution and recommendations based on the defect detected.
                -**Report Generative**: Create a detailed report for the documnetation and future reference.
        
                '''
                )
    
key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)


st.subheader(':blue[Upload an image to detect the structural defects]')
input_image=st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], key="image_uploader")


if input_image is not None:
    image = Image.open(input_image)
    st.image(image, caption="Uploaded Image") # Display the uploaded image
    
prompt =f'''
    You are an expert in structural defect detection.    
    Analyze the image and provide a detailed report on the structural defects present in the image.
    Provide recommendations for each defect detected.
    If multiple defects are detected, list them all with their respective recommendations.
    similar cases should be grouped and analyzed together.
    label the defects with appropriate headings IN THE IMAGE ITSELF.
    If no defects are detected, state that no defects were found.
    Provide the report in a structured format with headings and bullet points.
    use the following image for analysis:
    '''
    
if st.button("Analyze Image"):
    if input_image is not None:
        with st.spinner("Analyzing the image..."):
            model = genai.GenerativeModel("gemini-1.5-flash")
            # Prepare the image for Gemini (PIL Image or bytes)
            image = Image.open(input_image)
            #st.write(image)
            # Gemini expects a list of content parts: text and image
            response = model.generate_content([
                prompt,
                image
            ])
            st.subheader("Analysis Report")
            st.markdown(response.text)
    else:
        st.error("Please upload an image to analyze.")