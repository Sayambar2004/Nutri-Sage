#Import libraries
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import streamlit as st


#Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response_diet(prompt, input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, input])
    return response.text

def get_response_nutrition(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image[0], prompt])
    return response.text

def prep_image(uploaded_file):

    if uploaded_file is not None:
        #Read the file as bytes
        bytes_data = uploaded_file.getvalue()

        #get the image part information
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Is Uploaded!")
    
# Stramlit Configuration

st.set_page_config (
    page_title="Mr Nutritionist",
    layout="wide",
    page_icon="👨‍⚕",
)
st.header("Be Fit")
section_choice1 = st.radio("Enter your choice", ("Food Forensics","Diet Planner"))

# Food Forensics
if section_choice1 == "Food Forensics":
    upload_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png"])
    image = ""
    if upload_file is not None:
        max_width = 200
        max_height = 200
        image = Image.open(upload_file)
        image.thumbnail((max_width, max_height), Image.LANCZOS)
        st.image(image, caption="Image Successfully Uploaded")


# Context
    input_prompt_nutrition = """
    You are an expert packaged food and health drink researcher. As a skilled researcher, you are required to analyze the packaged food in the images and determine the total nutritional value. Additionally, you must provide details of each food component and its chemical compositions and. Food ingredients, Serving size, Calories, Protein (g), Fat, Carbohydrates (g), Fiber (g), Vit B-12, Vit B-6, Iron. Also add if there is any severity in the food. You can give required cautions Please Rate yourself in terms of Accuracy and Precision on the ingridients you pre Show what the Accuracy and Precision are Use the table to show the above information.Highlight the ingredients or chemicals which are harmful for human digestive system and our bodies. Add a red color highlight on those dangerous ingredients. In a new paragraph, provide an overall review of the given product. 
    """
    
    submit = st.button("Start Analyzing Your Product")
    if submit:
        image_data = prep_image(upload_file)
        response = get_response_nutrition(image_data, input_prompt_nutrition)
        st.subheader("Food Analyzer AI: ")
        st.write(response)

# Diet Planner
if section_choice1 == "Diet Planner":

# Context
    input_prompt_diet = """
    You are an Indian Nutritionist. If the input contains a list of ingredients such as fruit, vegetables, or any other ingredients that can be processed by the user, you must provide a diet plan and suggest breakfast, lunch, dinner with the given ingredients. If the input contains numbers, you should suggest an Indian middle class diet plan for breakfast, lunch, dinner in the given number of calories throughout the day.Also make a chart analyzing the quantity of protein, fats and carbohydrates. Assess yourself in terms of Accuracy and Precision of your predicted calories. Return the response using markdown. Also score yourself in terms of accuracy and Precision. Return your answer by giving a score. Also show the Accuracy and Precision.
    """
    
    input_diet = st.text_area("Enter a list of groceries you have at home and get a diet plan or Enter how many calories do you need per day :")
    submit1 = st.button("Plan My Diet")
    if submit1:
        response = get_response_diet(input_prompt_diet, input_diet)
        st.subheader("Diet AI: ")
        st.write(response)
