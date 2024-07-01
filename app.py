import json
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import pytesseract as tess
from PIL import Image
from streamlit_lottie import st_lottie 
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import os
os.environ['GOOGLE_API_KEY'] = "AIzaSyCihuiYQK_yBKxHtduqrMIM8_BtaBOxYKo"

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

## Yeh Rha Hamara Gpt Model
model = genai.GenerativeModel('gemini-pro')
print(model)

# Navigation Bar
# Define the navigation options
nav_options = {
    "Home": "Home",
    "Text Summary": "Text Summary",
    "Video Summary": "Video Summary",
    "Documentation": "Documentation", 
    "About": "About"
}

#For Lootie Aimation
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)
    
# Create a sidebar with a selectbox for navigation
selected_page = st.sidebar.selectbox("Navigation", list(nav_options.keys()))

# Display content based on the selected page
if selected_page == "Home":
    # Title Of The Website
    st.markdown("""
        <style>
            .title {
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 class='title'>Summary Master</h1>", unsafe_allow_html=True)
    #Lottie
    lottie_scanner = load_lottiefile("Lottie/home page.json")
    st_lottie(
        lottie_scanner,
        key = "None",
    )

    st.markdown("""
## Welcome to Summary Master!

### Overview

Summary Master helps you quickly get summaries of YouTube videos and text images.

### Features

1. **YouTube Video Summarizer**
    - Paste the URL of a YouTube video to get a summary.

2. **Image Text Summarizer**
    - Upload or capture an image of text to receive a summary.

Explore the specific pages for detailed instructions on how to use each feature.
""")
    # Add content for home page
elif selected_page == "About":
    #Lottie
    lottie_scanner = load_lottiefile("Lottie/hello.json")
    st_lottie(
        lottie_scanner,
        key = "None",
    )

    st.markdown("""
## About This Project

Hello, I'm Aditya Sarkar, the creator of Summary Master. 

### Why I Created This Project

In today's fast-paced world, time is a precious commodity. We are constantly bombarded with information, whether it's through lengthy YouTube videos, dense articles, or pages of text. I realized there was a need for a tool that could help people quickly and efficiently extract the key points from this vast amount of content. That's why I created Summary Master.

### Our Mission

The mission of Summary Master is simple: to save you time and make your life easier. Whether you're a student needing to quickly understand a lecture video, a professional summarizing reports, or anyone who wants to get the gist of a document without reading through it all, Summary Master is here to help.

### How It Works

Summary Master offers two main features:
1. **YouTube Video Summarizer:** Paste a YouTube video URL, and get a concise summary of its content.
2. **Image Text Summarizer:** Upload or capture an image of text, and receive a detailed summary of the extracted text.

## Contact Information

Feel free to reach out to me on social media or via email. I'd love to hear your feedback and suggestions!

- **Email**: adi.sarkar2004@gmail.com
- **Email**: +91 8989028700

                """)
    # Add content for about page
elif selected_page == "Video Summary":
    # Display instructions for YouTube summary page
   #Lottie
    lottie_scanner = load_lottiefile("Lottie/youtube.json")
    st_lottie(
        lottie_scanner,
        key = "None",
    )
    st.markdown("""
    ### Instructions:
    1. Paste the URL of a YouTube video into the text box below.
    2. Click the 'Summarize' button to generate a summary of the video's content.

    **Note:** Ensure the video URL is valid and publicly accessible.

    ---

    ### Example Video URLs:
    - https://www.youtube.com/watch?v=dQw4w9WgXcQ
    - https://www.youtube.com/watch?v=3mD2KykyuV0

    """)
    # Add content for video summary page
    # Now we have To get Youtube Link from the user
    youtube_video = st.text_input("Enter Your Youtube Link")
    if st.button("Summarize"):
        if youtube_video:
           try:
                # Ensure the URL is in the correct format
              if "youtube.com/watch?v=" in youtube_video:
                  video_id = youtube_video.split("v=")[1]
                  video_id = video_id.split("&")[0]  # To handle cases where there are additional parameters after the video ID
                  print(video_id)
                  # To diplay the thumbnail 
                  st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
                  # Fetch the transcript
                  transcript = YouTubeTranscriptApi.get_transcript(video_id)
                  # Combine transcript text
                  Sex = "Higher Studies"
                  result = ""
                  for i in transcript:
                    result += ' ' + i['text']
                    
                  
                  response = model.generate_content("""Give the detail overview or summary of the transcript in 1000-1500 words in detail in points and paragraphs 
                                                    with proper headings and subheading kindly diplay t also so write it required in a proper markdown  
                                                    format so I can diplay it on my website. This transcript is appended here: """+result)
                  text = response._result.candidates[0].content.parts[0].text
                  st.markdown(text)

                  
              else:
                st.error("Invalid YouTube URL. Please enter a valid URL in the format: https://www.youtube.com/watch?v=VIDEO_ID")
           
           except Exception as e:
             st.error(f"An error occurred: {e}")

elif selected_page == "Text Summary":
    #Lottie
    lottie_scanner = load_lottiefile("Lottie/textScanner.json")
    st_lottie(
        lottie_scanner,
        key = "None",
    )
    st.markdown("""
    ### Instructions:
    1. Click the 'Upload Image' button to select an image file from your device or click 'Capture Image' to use your camera and take a picture of the text.
    2. After the image is uploaded or captured, you can view the image to ensure the correct document is uploaded.
    3. After the text is extracted, click the 'Summarize' button to create a detailed summary of the text.
    
    **Note:** Ensure the image contains clear and legible text for accurate extraction and summarization.
    
    ---

    ### Example Images:
    - An image of a book page with a paragraph.
    - A photo of a printed document with text.
    """)
    # New Commit
    def extract_text_from_image(image):
        text = tess.image_to_string(image)
        return text
        
    # Camera Input
    test_image_camera = st.camera_input("Take a Picture")
    # File Input
    test_image_upload = st.file_uploader("Choose File", type=["jpg", "jpeg", "png"])
    # This button will show the image
    if st.button("Show Image"):
        if test_image_camera:
            st.image(test_image_camera, caption='Selected Image.', use_column_width=True)
        elif test_image_upload:
            st.image(test_image_upload, caption='Selected Image.', use_column_width=True)
        else:
            st.write("Please capture an image or upload a file first.")

    if st.button("Summarize"):
    
       if test_image_camera:
         image = Image.open(test_image_camera)
         image_text = extract_text_from_image(image)
         response = model.generate_content("""Please provide a detailed overview or summary of the given paragraph in 500-600 words. 
                                           Ensure the summary is comprehensive, organized into points and paragraphs, and includes 
                                           proper headings and subheadings. Format the response in markdown so it can be displayed 
                                           on my website. The paragraph is appended here: """+image_text)
         text = response._result.candidates[0].content.parts[0].text
         st.markdown(text)
    
        
       elif test_image_upload:
         image = Image.open(test_image_upload)
         image_text = extract_text_from_image(image)
         response = model.generate_content("""Please provide a detailed overview or summary of the given paragraph in 500-600 words. 
                                           Ensure the summary is comprehensive, organized into points and paragraphs, and includes 
                                           proper headings and subheadings. Format the response in markdown so it can be displayed 
                                           on my website. The paragraph is appended here: """+image_text)
         text = response._result.candidates[0].content.parts[0].text
         st.markdown(text)
         
 # Footer Jisme Insta, Github and Linkdin hai        

elif selected_page == "Documentation":
    #Lottie
    lottie_scanner = load_lottiefile("Lottie/documentation.json")
    st_lottie(
        lottie_scanner,
        key = "None",
    )
    st.markdown("""
## Documentation

Welcome to the documentation for Summary Master. This guide provides information on the libraries and technologies used in our web application.

### Technologies and Libraries Used

1. **Streamlit**
    - **Description:** Streamlit is an open-source app framework for Machine Learning and Data Science teams. It allows you to create beautiful, custom web apps for machine learning and data science.
    - **Usage:** Used to create the web app interface and manage the navigation between different pages.

2. **YouTube Transcript API**
    - **Description:** The YouTube Transcript API is a Python library for retrieving the transcript of a YouTube video.
    - **Usage:** Used to fetch the transcript of YouTube videos for summarization.

3. **Pytesseract**
    - **Description:** Pytesseract is an Optical Character Recognition (OCR) tool for Python. It is a wrapper for Google's Tesseract-OCR Engine.
    - **Usage:** Used to extract text from images.

4. **Pillow**
    - **Description:** Pillow is a Python Imaging Library (PIL) that adds image processing capabilities to your Python interpreter.
    - **Usage:** Used to open and manipulate image files.

5. **Google Generative AI (GenAI)**
    - **Description:** Google Generative AI provides advanced AI models and tools to generate high-quality content.
    - **Usage:** Used to generate detailed summaries from the extracted text and video transcripts.

6. **Lottie Animations**
    - **Description:** Lottie is a library for rendering animations and vector graphics natively in web and mobile applications.
    - **Usage:** Used to add interactive and visually appealing animations to enhance user experience throughout the web application.

### How It Works

1. **YouTube Video Summarizer:**
    - The user inputs a YouTube video URL.
    - The YouTube Transcript API retrieves the video's transcript.
    - The transcript is processed and sent to Google Generative AI for summarization.
    - The generated summary is displayed to the user.

2. **Image Text Summarizer:**
    - The user uploads or captures an image containing text.
    - Pytesseract extracts the text from the image.
    - The extracted text is processed and sent to Google Generative AI for summarization.
    - The generated summary is displayed to the user.
""")



st.markdown("""
    <style>
        .social-icons {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px; /* Adjust the gap between icons if needed */
        }
        .social-icons .icon {
            margin: 0 10px;
        }
    </style>
    <div class="social-icons">
        <a href="https://www.linkedin.com/in/aditya-sarkar-a7a321206/" target="_blank" class="icon">
            <img src="https://img.icons8.com/color/48/000000/linkedin.png"/>
        </a>
        <a href="https://www.instagram.com/adi_jong_un/" target="_blank" class="icon">
            <img src="https://img.icons8.com/color/48/000000/instagram-new.png"/>
        </a>
        <a href="https://github.com/SarkariKill" target="_blank" class="icon">
            <img src="https://img.icons8.com/material-rounded/48/000000/github.png"/>
        </a>
    </div>
    """, unsafe_allow_html=True)         
st.markdown("""           
---



Thank you for choosing Summary Master.
Together, we can make extracting key insights faster and easier!


                """)



