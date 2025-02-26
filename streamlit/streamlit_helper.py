import random

"""
Retrieve the number of available questions for the specified topic
"""
def get_question_count(firestore_db, topic):

    document_reference = firestore_db.collection("question_counts").document(topic)

    document = document_reference.get()

    if document.exists is True:
        return document.to_dict()["count"]
    else:
        return None

"""
Extract the question and answer choices and format them for display in the chat
"""
def format_question_for_chat(question_dict):

    question = question_dict["question"]
    answer_choices = question_dict["answer_choices"]
    
    return f"Here is the question:\n{question}\n{"\n".join(answer_choices)}\nWhat is the answer?"

"""
Select a question from the list of retrieved questions to ask the user
Clear the chat log and let the selected question be the initial entry
"""
def get_next_question(session_state):
    
    session_state["current_question"] = session_state["question_list"].pop()

    reformatted_question = format_question_for_chat(session_state["current_question"])

    session_state["chat_log"] = [{
        "role" : "assistant",
        "content" : f"{reformatted_question}",
        "avatar" : "🧬"
    }
    ]

    if len(session_state["question_list"]) == 0:
        session_state["next_question_disabled"] = True

"""
Retrieves a list of random questions from a specific topic
"""
def get_questions_by_topic(firestore_db, topic, num_of_questions, session_state):

    # format the topic name
    reformatted_topic = "_".join(topic.lower().split(" "))

    question_count = get_question_count(firestore_db, reformatted_topic)

    # randomly generate question numbers for querying
    question_numbers = random.sample(population=[i for i in range(1, question_count + 1)], k=num_of_questions)

    questions = []

    for num in question_numbers:

        document_name = f"{reformatted_topic}-{num}"
        document_reference = firestore_db.collection(reformatted_topic).document(document_name)

        document = document_reference.get()

        if document.exists is True:
            questions.append(document.to_dict())
        else:
            return None
    
    session_state["question_list"] = questions
    get_next_question(session_state)

    # control the functionality of the next question button
    if len(session_state["question_list"]) > 0:
        session_state["next_question_disabled"] = False

    session_state["chat_input_disabled"] = False

'''
Takes a chat log and formats it as a linear chat history for the LLM to process and generate a response
'''
def format_prompt(chat_log):

    prompt = '''You are a computer assistant for tutoring BIOLOGY. A student is responding to a biology question from you. Read through the following messages between you two. Explain the correct answer BRIEFLY. If a student ask questions, answer them with your understanding of biology.'''

    for message in chat_log:

        role = message["role"]
        content = message["content"]

        if role == "assistant":
            prompt += "\n\nAssistant:\n"
        
        elif role == "user":
            prompt += "\nStudent:\n"

        prompt += f"{content}"
        prompt += "\n"

    return prompt

"""
Sends the chat log to the LLM and receive a response
Append the chat log with the response
"""
def send_chat_to_llm(session_state, replicate_connection):

    chat_log = session_state["chat_log"]

    prompt = format_prompt(chat_log)
    correct_answer = session_state["current_question"]["correct_answer"]

    system_prompt = f'''You are a high school biology tutor. 
    You just gave a question to a student. Even if the student answers correctly, explain the answer.
    IMPORTANT: The correct answer is {correct_answer}.
    IMPORTANT: Respond as BRIEFLY as possible.
    IMPORTANT: Your explanation must demonstrate understanding of biological concepts.
    IMPORTANT: DO NOT give a new question. If the student asks for a new question, tell them to use the app's sidebar to get new questions.
    '''

    max_output_tokens = 150

    llm_input = {
        "prompt" : prompt,
        "system_prompt" : system_prompt,
        "max_tokens" : max_output_tokens
    }

    model_name = "meta/meta-llama-3-70b-instruct"

    for piece in replicate_connection.stream(model_name, input=llm_input):
        yield str(piece)
