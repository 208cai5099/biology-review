import streamlit as st

if "chat_log" not in st.session_state.keys():
    st.session_state["chat_log"] = [{
        "role" : "assistant",
        "content" : '''
        Interested in reviewing biology? \n To get started, go to the sidebar to select a topic and specify the number of practice questions. 
        Use the chat feature to answer the questions. Once you've finished a question, click Next to move onto the next question.
        ''',
        "avatar" : "🧬"
    }]

if "user_input_disabled" not in st.session_state.keys():
    st.session_state["user_input_disabled"] = True

if "user_input_placeholder" not in st.session_state.keys():
    st.session_state["user_input_placeholder"] = "Press Start in the sidebar to begin"

if "next_question_disabled" not in st.session_state.keys():
    st.session_state["next_question_disabled"] = True

st.title("BioChat Review Tool :dna:")

with st.sidebar:

    instructions = st.text('''
    Please fill out the form below and press Start.
    ''')


    with st.form("Request Questions Form"):

        topic_selection = st.selectbox(
            "Select a topic:",
            ("Biochemistry", "Cells", "Genetics", "Evolution", "Human Body Systems", "Reproduction", "Ecology")
        )

        question_count_selection = st.slider(label="Select number of questions:", min_value=5, max_value=15, 
                                                    value=5, step=1)

        submit_status = st.form_submit_button("Start")

with st.container():

    # print out the messages from the chat log
    for message in st.session_state["chat_log"]:
        role = message["role"]
        content = message["content"]
        avatar = message["avatar"]
        with st.chat_message(name=role, avatar=avatar):
            st.write(content)

    # create a message box to type in user response
    user_input = st.chat_input(placeholder=st.session_state["user_input_placeholder"], max_chars=200, disabled=st.session_state["user_input_disabled"])

    # add the user's response to the chat log
    if user_input is not None:
        st.session_state["chat_log"].append({"role" : "user", "content" : user_input, "avatar" : "💭"})
        with st.chat_message(name="user", avatar="💭"):
            st.write(user_input)

# button for requesting next question
next_question_button = st.button(label="Next", disabled=st.session_state["next_question_disabled"])