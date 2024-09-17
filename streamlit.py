import streamlit as st
from PIL import Image
import io
import requests
import re


def get_response(file):
    lines = []
    url = 'https://ahmedgoda-alpr.hf.space/analyze/'
    files = {'files': (file.name,image_bytes)}
    responses = requests.post(url,files= files)
    
    for response in responses.json()['results'][0]:
        if len(response) == 1:   #in case of error
            _, value = response.popitem()
            lines.append(value) 
        else:
            match = re.search(r"(license plate number \d+)", response['filename'])
            result = match.group(1)
            lines.append( result+ '\nArabic Text:\t' + response['arabic_text'] + '\nEnglish Text:\t' + response['english_text'])
    
    return lines

    
#start the app
st.title("Saudi Car License Plate Recognition")

uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files is not None:
    count = 0
    for uploaded_file in uploaded_files:
        count += 1
        image_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, caption='Loading...', use_column_width=True)
        
        response = "\n".join(get_response(uploaded_file))
        num_lines = response.count("\n") + 1
        st.text_area("The Recognized license Plates in this image: ",response,height=num_lines*30)
        
    
    
    
