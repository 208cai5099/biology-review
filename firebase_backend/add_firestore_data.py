from firebase import db
from process_questions import questions_and_answers_list

"""
Input: Firestore Cloud database and a dictionary containing question and answer info
Adds the question and answer info to the corresponding collection in the Firestore Cloud database
"""
def add_data(firestore_db, question_dict):

    unit = question_dict["unit"]
    question_num = question_dict["question_num"]

    firestore_db.collection(unit.lower()).document(f"{unit}-{question_num}").set(question_dict)

# iterate through each question and answer info and add it to the database
for question_dict in questions_and_answers_list:
    #add_data(db, question_dict)    # comment out to avoid accidental adding