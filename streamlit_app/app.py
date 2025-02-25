from firebase import db
import streamlit as st
from streamlit_helper import *

if "chat_log" not in st.session_state.keys():
    st.session_state["chat_log"] = [{
        "role" : "assistant",
        "content" : '''
        Interested in reviewing biology? 

        To get started, go to the sidebar to select a topic and specify the number of practice questions. 
        Use the chat feature to answer the questions. Once you've finished a question, click Next to move onto the next question.
        ''',
        "avatar" : "🧬"
    }]

if "user_input_placeholder" not in st.session_state.keys():
    st.session_state["user_input_placeholder"] = "Enter your response"

if "question_list" not in st.session_state.keys():
    st.session_state["question_list"] = []

if "current_question" not in st.session_state.keys():
    st.session_state["current_question"] = None

title, next_question = st.columns(spec=[0.7, 0.3], vertical_alignment="bottom")

# set the title
with title:
    st.title("BioChat Review Tool :dna:")

# button for requesting next question
with next_question:
    st.button(label="Next Question", on_click=get_next_question, kwargs={"session_state" : st.session_state}, use_container_width=True)

with st.sidebar:

    instructions = st.text('''
    Please fill out the form below and press Start.
    ''')

    topic_selection = st.selectbox(
        "Select a topic:",
        ("Biochemistry", "Cells", "Genetics", "Evolution", "Human Body Systems", "Reproduction", "Ecology")
    )

    question_count_selection = st.slider(label="Select number of questions:", min_value=1, max_value=10, 
                                         value=2, step=1)
    
    submit_status = st.button(label="Start", help="Click to get questions", on_click=get_questions_by_topic,
                              kwargs={"firestore_db" : db, "topic" : topic_selection, "num_of_questions" : question_count_selection, "session_state" : st.session_state})

# print out the messages from the chat log
for message in st.session_state["chat_log"]:
    role = message["role"]
    content = message["content"]
    avatar = message["avatar"]
    with st.chat_message(name=role, avatar=avatar):
        st.text(content)

# create a message box to type in user response
user_input = st.chat_input(placeholder=st.session_state["user_input_placeholder"], max_chars=200)

# add the user's response to the chat log
if user_input is not None:
    st.session_state["chat_log"].append({"role" : "user", "content" : user_input, "avatar" : "💭"})
    with st.chat_message(name="user", avatar="💭"):
        st.text(user_input)
