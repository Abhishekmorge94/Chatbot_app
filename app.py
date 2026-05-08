import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

import streamlit as st
from groq import Groq

st.title("AI CHATBOT USING GROQ")

#stores messages
if "messages" not in st.session_state:
    st.session_state.messages=[]

#display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


#prompt
prompt = st.chat_input("Type your Message")

#when the user sends the message
if prompt:

    #save your message
    st.session_state.messages.append(
        {"role": "user", "content" : prompt}

    )

    #display your message
    with st.chat_message("user"):
        st.markdown("prompt")

    #ai response
    with st.chat_message("assistant"):
        response_txt=""
        response_box = st.empty()

        #streaming response
        stream = client.chat.completions.create(
            model = "openai/gpt-oss-20b",
            messages=st.session_state.messages,
            stream= True
        )

        #response in chunks
        for chunk in stream:

            if chunk.choices[0].delta.content:
                response_txt += chunk.choices[0].delta.content
                response_box.markdown(response_txt)

        #save assistant response
        st.session_state.messages.append(
            {"role" : "assistant" , "content" : response_txt }
        )