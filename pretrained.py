# -*- coding: utf-8 -*-
"""Pretrained.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Rdda9QJ28NAjXc5SGiBALRo8qONsiMCT
"""

# !pip install transformers
#  Image media display
# from IPython.display import display
# !pip install summa
# !pip install gtts
# !pip install playsound
# !pip install pyttsx3

import audioop
import cv2
import os
import summa
import playsound
import pyttsx3
import gtts
import requests

# Backend
import torch
import transformers
import PIL

from IPython.display import HTML,Audio
from base64 import b64encode
# Image Processing
from PIL import Image
from googletrans import Translator
# from transformers import pipeline
import urllib.parse as parse
import os
from deep_translator import GoogleTranslator
def clearframes():
    folder_path = "Frames/"  # Replace with the actual path to your folder

# List all files in the folder
    files = os.listdir(folder_path)
    if files:
    # Iterate through the files and delete images (you can modify the condition based on your file types)
        for file in files:
            file_path = os.path.join(folder_path, file)

            # Check if the file is an image (you may need to adjust the condition based on your file types)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file}")
                except Exception as e:
                    print(f"Error deleting {file}: {e}")

    print("Deletion process completed.")
def videoToFrame(video):
  clearframes()
  vs = cv2.VideoCapture(video)
  prop = cv2.CAP_PROP_FRAME_COUNT
  total = int(vs.get(prop))
  print("[INFO] {} total frame in video".format(total))


  ret, img = vs.read()

  print(ret)

  count = 1
  while ret:
      cv2.imwrite("Frames//frame%d.jpg" %count, img)
      ret, img = vs.read()
      # print("Read a new frame: ", ret)
      count += 1
  return total

# Web links Handler


# Transformer and pre-trained Model
#VisionEncoderDecoderModel  --vision-to-text tasks-- image encoder & text decoder
#ViTImageProcessor --preprocessing images before feeding them into the VisionEncoderDecoderModel.
#GPT2TokenizerFast  --pre-trained language model-- convert text data into a format that can be processed by language models
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, GPT2TokenizerFast

# Managing loading processing
# displaying progress bars during lengthy operations,like loading large models or processing data.
from tqdm import tqdm

# Assign available GPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# Loading a fine-tuned image captioning Transformer Model

# ViT Encoder-Decoder Model
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning").to(device)

# Corresponding ViT Tokenizer
tokenizer = GPT2TokenizerFast.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Image processor
image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Accesssing images from the web

# # Verify url
def check_url(string):
    try:
        result = parse.urlparse(string)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

# # Load an image
def load_image(image_path):
    if check_url(image_path):
        return Image.open(requests.get(image_path, stream=True).raw)
    elif os.path.exists(image_path):  #local file path
        return Image.open(image_path)

# Image inference

def get_caption(model, image_processor, tokenizer, image_path):
    image = load_image(image_path)  #it returns the image as an object

    # Preprocessing the Image
    img = image_processor(image, return_tensors="pt").to(device)   #The return_tensors="pt" argument specifies that the output should be in PyTorch tensor format

    # Generating captions
    output = model.generate(**img)

    #The generated captions are typically in tokenized form.
    caption = tokenizer.batch_decode(output, skip_special_tokens=True)[0]

    return caption

def generate_caption(total_frames):
  caption_list = []
  curr_frame = 15
  while curr_frame < total_frames:
    url = "Frames/frame{}.jpg".format(curr_frame)
    caption_list.append(get_caption(model, image_processor, tokenizer, url))
    print(caption_list)
    curr_frame += 30
  return caption_list

# from transformers import pipeline
# # from summarizer import Summarizer
# def summarize(text):
#     summarizer = pipeline("summarization")
#     summary = summarizer(text, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
#     return summary[0]['summary']
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords

def summarize_text(text):
    return summarize(text,ratio=0.5).replace("\n","")

# def translate_text(text, target_language='en'):
#     translator = Translator()
#     translation = translator.translate(text, dest=target_language)
#     return translation.text

def translate_text(text, target_language='en'):
    text = GoogleTranslator(source='auto', target=target_language).translate(text) 
    return text


def textToSpeach(caption,i,language="en"):

  tts = gtts.gTTS(caption,lang=language) #Provide the string to convert to speech
  tts.save('static/{}.wav'.format(i)) #save the string converted to speech as a .wav file
  sound_file = '{}.wav'.format(i)
  #return Audio(sound_file, autoplay=True)



# Function to display video with playback controls
def display_video(video_path):
    video_content = open(video_path, "rb").read()
    video_encoded = "data:video/mp4;base64," + b64encode(video_content).decode("utf-8")
    return HTML(f"""
    <video width="440" height="400" controls>
        <source src="{video_encoded}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    """)



def get_video_path(video_name):
    # Specify the directory where your video is located
    directory = 'static/'

    # Use os.path.join to create the full path to the video file
    video_path = os.path.join(directory, video_name)

    return video_path

def videovoiceover_path(video):
    name = video
    video = get_video_path(name)
    total_frames = videoToFrame(video)
    caption_list = generate_caption(total_frames)
    print(caption_list)
    caption_string = ""
    for caption in caption_list:
        caption_string += caption[0].upper() + caption[1:-1] +". "
    print(caption_string)
    caption_string = summarize_text(caption_string)
    print("Hi this is capstring: ",caption_string)
    caption_list1 = [caption_string]

    languages = ['ta', 'hi', 'fr', 'de', 'zh-CN',"ja"]  # Language codes: Tamil, Hindi, French, German, Chinese

    for lang in languages:
        translated_text = translate_text(caption_string, lang)
        caption_list1.append(translated_text)
    
    print("\nCaption:", caption_list1)
    lang_list = ["en","ta","hi","fr","de","zh","ja"]
    for i in range(len(lang_list)):
        textToSpeach(caption_list1[i],i,language=lang_list[i])
    return [caption_list1,"static/1.wav",name]

# Example usage: Replace 'your_video_path.mp4' with the path to your video file
def videovoiceover(video):
    name = video
    video = get_video_path(video)
    total_frames = videoToFrame(video)
    caption_list = generate_caption(total_frames)
    print(caption_list)
    caption_string = ""
    for caption in caption_list:
        caption_string += caption[0].upper() + caption[1:-1] +". "
    print(caption_string)
    caption_string = summarize_text(caption_string)
    print("\n Hi this is capstring: ",caption_string)
    caption_list1 = [caption_string]

    languages = ['ta', 'hi', 'fr', 'de', 'zh-CN',"ja"]  # Language codes: Tamil, Hindi, French, German, Chinese

    for lang in languages:
        translated_text = translate_text(caption_string, lang)
        caption_list1.append(translated_text)
    
    print("\nCaption:", caption_list1)
    lang_list = ["en","ta","hi","fr","de","zh","ja"]
    for i in range(len(lang_list)):
        textToSpeach(caption_list1[i],i,language=lang_list[i])
    return [caption_list1,"static/1.wav",name]
