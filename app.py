from tokenize import Number
import streamlit as st
import urllib.request
import re
from pytube import YouTube
import os
from pydub import AudioSegment
import email, smtplib, ssl
from urllib import request
from urllib.request import Request, urlopen
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def mail(receiver_email):
    subject = "Your mp3 mashup"
    body = "Your mp3 mashup sent by Sukhmanjit Singh 102003484"
    sender_email = "sukhmanjat@gmail.com"
    password = "ivcjwytzqlaqoxsv"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "final.mp4"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
def  mashup(name,num_video,audio_duration,email_id):
    search_keyword = name.replace(" ","+")
    request_site=Request("https://www.youtube.com/results?search_query=" + search_keyword,headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(request_site)
    video_ids = re.findall(r"watch\?v=(\S{11})",html.read().decode())

    #where to save
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'Videos')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    for i in range(0,num_video):
        YouTube("https://www.youtube.com/watch?v="+video_ids[i]).streams.filter(file_extension="mp4").last().download(final_directory)

    
    # loading video dsa gfg intro video
    list_dir = os.listdir("./Videos")
    print(list_dir)
    audio = AudioSegment.empty()
    for i in list_dir:
        file_name="Videos/"+i
        path = os.path.join(current_directory,file_name)
        sound = AudioSegment.from_file(path,format="mp4")
        # getting subclip as video is large
        audio+=sound[30*1000:30*1000+audio_duration*1000]
    audio.export("final.mp4", format="mp4")
    mail(email_id)
def main():
    st.title("Mashup Creator")
    html_temp="""
    <div style = "background-color:tomato;padding:10px">
    <h2 style ="color:white;text-align:center;">Mp3 Mashup Creator</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    SingerName = st.text_input("Name of Singer","Type Here")
    NumberOfVideos = st.text_input("Number of videos","Type Here")
    AudioDuration = st.text_input("Duration of mashup","Type Here")
    EmailId = st.text_input("Enter your email id","Type Here")
    result=""
    if st.button("Submit"):
        result = mashup(SingerName,int(NumberOfVideos),int(AudioDuration),EmailId)

if __name__=='__main__':
    main()