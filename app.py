import os
from google.cloud import texttospeech

import io
import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret.json'


def synthesize_speech(text, lang='English', gender='Neutral'):
  gender_type = {
      'Male':texttospeech.SsmlVoiceGender.MALE,
      'Female':texttospeech.SsmlVoiceGender.FEMALE,
      'Neutral':texttospeech.SsmlVoiceGender.NEUTRAL
  }
  
  lang_code = {
      'English': 'en-US',
      '日本語': 'ja-JP',
      'Español': 'es-PE',
      '中文' :'zh-TW'
  }
  
  #lang = 'English'
  #gender = 'Neutral'
  #text = "Hello I'm John Thirdfield junior from Jacksonville Florida. Oh That' my super hero"
  
  client = texttospeech.TextToSpeechClient()
  
  
  synthesis_input = texttospeech.SynthesisInput(text=text)
      
  
  voice = texttospeech.VoiceSelectionParams(
      language_code=lang_code[lang], ssml_gender=gender_type[gender]
  )
  
  audio_config = texttospeech.AudioConfig(
      audio_encoding=texttospeech.AudioEncoding.MP3
  )
  
  response = client.synthesize_speech(
      input=synthesis_input, voice=voice, audio_config=audio_config
  )
  return response

st.title('Audio Output App🎨')

st.markdown('### データ準備')

input_option = st.selectbox(
    'Please select input data',
    ('Input directly', 'Text file')
)
input_data = None

if input_option == 'Input directly':
    input_data = st.text_area('Please input text here.', '1 2 3')
else:
    uploaded_file = st.file_uploader('Please upload a text file.', ['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data = content.decode() 
        
if input_data is not None:
    st.write('↓入力されたデータ')
    st.write(input_data)
    st.markdown('### パラーメータ設定🖼')
    st.subheader('Language & Speaker settings')

    lang = st.selectbox(
        'Please select the language (日本語,English,Español or 中文)',
        ('日本語','English','Español','中文')
    )
    gender = st.selectbox(
        'Please select the speaker',
        ('Neutral', 'Male', 'Female')
    )
    st.markdown('### 音声合成')
    st.write('Okay to proceed?')
    if st.button('Play♪'):
        comment = st.empty()
        comment.write('Start Playing')
        response = synthesize_speech(input_data, lang=lang, gender=gender)
        ##音声再生↓
        st.audio(response.audio_content)
        comment.write('Completed!! Please click the button below.')
       
##背景設定
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/free-photo/white-baby-breath-s-flower-border-blue-background-with-copy-space-writing-text_23-2148048520.jpg?w=740&t=st=1667745546~exp=1667746146~hmac=a0dd46402ef393ed68de872779ba11f943aae3c87990ec60f4a868dd9e8cc4ab");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 
