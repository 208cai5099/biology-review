from firebase import db
import json

"""
Input: Firestore Cloud database and a dictionary containing question and answer info
Adds the question and answer info to the corresponding collection in the Firestore Cloud database
"""
def add_data(firestore_db, question_dict):

    topic = question_dict["topic"]
    question_num = question_dict["question_num"]

    firestore_db.collection(topic.lower()).document(f"{topic}-{question_num}").set(question_dict)

# load all the processed questions as a list
processed_questions_filename = "/Users/zhuobiaocai/Desktop/biology-review/questions_and_answers/processed_questions.json"
with open(processed_questions_filename, "r") as file:
    questions_and_answers_list = json.load(file)

# iterate through each question and answer info and add it to the database
for question_dict in questions_and_answers_list:
    #add_data(db, question_dict)    # comment out to avoid accidental adding