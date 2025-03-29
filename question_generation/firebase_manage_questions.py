import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import time

"""
Input: Firestore Cloud database and a topic
Output: Returns the number of questions in the database for the topic
"""
def get_question_count(firestore_db, topic):

    document_dict = firestore_db.collection("question_counts").document(topic).get().to_dict()

    return document_dict["count"]

"""
Input: Firestore Cloud database and a topic
Updates the count of available questions for the topic
"""
def update_question_count(firestore_db, topic, new_count):

    firestore_db.collection("question_counts").document(topic).set({"count" : new_count})

"""
Input: Firestore Cloud database and a dictionary containing question and answer choices
Adds the question and answer choices to the corresponding collection in the Firestore Cloud database
Updates the count of available questions for the question's topic
"""
def add_question(firestore_db, question_dict):

    topic = question_dict["topic"]

    count = get_question_count(firestore_db, topic)

    question_num = count + 1
    question_dict["question_num"] = question_num

    firestore_db.collection(topic).document(f"{topic}-{question_num}").set(question_dict)

    update_question_count(firestore_db, topic, question_num)

"""
Input: Firestore database and the topic and question number of the question to be deleted
Deletes the question of the specified topic and question number from the database
"""
def delete_question(firestore_db, topic, question_num):

    firestore_db.collection(topic).document(f"{topic}-{question_num}").delete()

    new_count = question_num - 1
    update_question_count(firestore_db, topic, new_count)

# initialize Firebase application
cred = credentials.Certificate('/Users/zhuobiaocai/Desktop/biology-review/firebase_key.json')
app = firebase_admin.initialize_app(cred)

# establish Firestore connection
db = firestore.client()

# load all the processed questions as a list
processed_questions_filename = "processed_questions.json"
with open(processed_questions_filename, "r") as file:
    questions_and_answers_list = json.load(file)

# iterate through each question and answer info and add it to the database
index = 0
for question_dict in questions_and_answers_list:
    # add_question(db, question_dict)    # comment out to avoid accidental addition

    # add a sleep block to avoid hitting request limit
    if index % 50 == 0:
        time.sleep(5)
    
    index += 1