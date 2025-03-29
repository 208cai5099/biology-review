import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import streamlit as st
from streamlit_helper import *
import json
import os
import replicate

os.environ["REPLICATE_API_TOKEN"] = st.secrets["replicate_key"]

# initialize Firebase app
firebase_key = json.loads(st.secrets["firebase_key"])
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key)
    app = firebase_admin.initialize_app(cred)

# establish connection to Firestore
firestore_db = firestore.client()

# establish initial session states
if "chat_log" not in st.session_state.keys():

    content = '''
    Hi there, I'm a chatbot that can help you review biology topics. Go to the sidebar to get started. On mobile, press the top-left arrow to access the sidebar.
    '''
    st.session_state["chat_log"] = [{
        "role" : "assistant",
        "content" : content,
        "avatar" : "🧬"
    }]

if "user_input_placeholder" not in st.session_state.keys():
    st.session_state["user_input_placeholder"] = "Enter your response"

if "question_list" not in st.session_state.keys():
    st.session_state["question_list"] = []

if "current_question" not in st.session_state.keys():
    st.session_state["current_question"] = None

if "next_question_disabled" not in st.session_state.keys():
    st.session_state["next_question_disabled"] = True 

if "chat_input_disabled" not in st.session_state.keys():
    st.session_state["chat_input_disabled"] = True

# format the title and next question button
title, next_question = st.columns(spec=[0.7, 0.3], vertical_alignment="bottom")

with title:
    st.title("Biology Chatbot Review")

# button for requesting next question
with next_question:
    st.button(label="Next Question", disabled=st.session_state["next_question_disabled"], on_click=get_next_question, kwargs={"session_state" : st.session_state}, use_container_width=True)

# sidebar contains instructions and input widgets to request questions from Firestore
with st.sidebar:

    instructions = st.markdown('''
    **Instructions**: 
    
    Select a topic and specify the number of questions.
    ''')

    topic_selection = st.selectbox(
        "Select a topic:",
        ("Biochemistry", "Cells", "Genetics", "Evolution", "Human Physiology", "Reproduction and Development", "Ecology")
    )

    question_count_selection = st.slider(label="Select number of questions:", min_value=1, max_value=5, 
                                         value=1, step=1)
    
    submit_status = st.button(label="Start", help="Click to get questions", on_click=get_questions_by_topic,
                              kwargs={"firestore_db" : firestore_db, "topic" : topic_selection, "num_of_questions" : question_count_selection, "session_state" : st.session_state})

    llama_note = st.markdown('''
    \n
    Built with Meta Llama 3

    The questions in this app were generated using Meta's Llama 3 model. The chatbot responses in this app are generated using the same model. The questions were checked in advance for correctness. See [GitHub](https://github.com/208cai5099/biology-review) repository for details.
    
    Please keep in mind that the model can make mistakes. It is possible for the chatbot to display incorrect information about a biological concept or topic.
    ''')

# print out the messages from the chat log
for message in st.session_state["chat_log"]:
    role = message["role"]
    content = message["content"]
    avatar = message["avatar"]
    with st.chat_message(name=role, avatar=avatar):
        st.text(content)
    
# create a message box to type in user response
user_input = st.chat_input(placeholder=st.session_state["user_input_placeholder"], max_chars=200, disabled=st.session_state["chat_input_disabled"])

if user_input is not None:

    llm_response = None

    # append the user's response to the chat log
    with st.chat_message(name="user", avatar="💭"):
        st.text(user_input)

        st.session_state["chat_log"].append({
            "role" : "user",
            "content" : f"{user_input}",
            "avatar" : "💭"
        }
        )

    # stream the LLM's response to the user's response
    with st.chat_message(name="assistant", avatar="🧬"):
        piece = send_chat_to_llm(session_state=st.session_state, replicate_connection=replicate)
        llm_response = st.write_stream(piece)

        # append the LLM's response to the chat log
        st.session_state["chat_log"].append({
            "role" : "assistant",
            "content" : f"{llm_response}",
            "avatar" : "🧬"
        })