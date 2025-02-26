import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import time

# initialize Firebase application
cred = credentials.Certificate('/Users/zhuobiaocai/Desktop/biology-review/firebase_key.json')
app = firebase_admin.initialize_app(cred)

# establish Firestore connection
db = firestore.client()

"""
Input: Firestore Cloud database and a dictionary containing question and answer info
Adds the question and answer info to the corresponding collection in the Firestore Cloud database
"""
def add_question(firestore_db, question_dict):

    topic = question_dict["topic"]
    question_num = question_dict["question_num"]

    firestore_db.collection(topic.lower()).document(f"{topic}-{question_num}").set(question_dict)

"""
Input: Firestore Cloud database and a dictionary containing the count of questions for each topic
Updates the number of available questions for each topic
"""

def update_question_counts(firestore_db, question_counts_by_topic):

    for topic in question_counts_by_topic.keys():

        firestore_db.collection("question_counts").document(f"{topic}").set({"count" : question_counts_by_topic[topic]})

# load all the processed questions as a list
processed_questions_filename = "/Users/zhuobiaocai/Desktop/biology-review/question_generation/processed_questions.json"
with open(processed_questions_filename, "r") as file:
    questions_and_answers_list = json.load(file)

# iterate through each question and answer info and add it to the database
index = 0
for question_dict in questions_and_answers_list:
    add_question(db, question_dict)    # comment out to avoid accidental addition

    # add a sleep block to avoid hitting request limit
    if index % 50 == 0:
        time.sleep(5)
    
    index += 1

question_counts_by_topic = {}
for question_dict in questions_and_answers_list:
    topic = question_dict["topic"]

    if question_counts_by_topic.get(topic) is None:
        question_counts_by_topic[topic] = 1
    else:
        question_counts_by_topic[topic] += 1

update_question_counts(db, question_counts_by_topic)  # comment out to avoid accidental update