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
    
    return f"Here is the question:\n{question}\n{"\n".join(answer_choices)}"

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
