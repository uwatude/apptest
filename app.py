from tkinter import Y
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

subscription_key = '4e909ea77e6d4d2f802b3c602f9cbd45'
endpoint = 'https://2022-yagumai.cognitiveservices.azure.com/'

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def get_tags(filepath):
    local_image = open(filepath, "rb")

    # Call API with remote image
    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
        
    return tags_name
    
def detect_objects(filepath):
    local_image = open(filepath, "rb")

    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects
    return objects

import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

st.title("物体検出App")

uploaded_file = st.file_uploader('Please choose an image...', type={'jpg','png'})
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    #img_path = f'img/{uploaded_file.name}'
    #img.save(img_path)
    #objects = detect_objects(img_path)

    # 描画
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

    

        draw.rectangle([(x,y), (x+w, y+h)], fill=None, outline='orange', width=9)

    
    st.image(img)
    
    tags_name = get_tags(img_path)
    ptags_name = (', '.join(tags_name))
    st.markdown('**Detected content tag(s)**')
    st.markdown(f'> {tags_name}')