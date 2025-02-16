import re
import json

question = ""
questions_list = []
answers_list = []
topics_list = []

question_filenames = ["OpenStax Concepts of Biology Chapter Review Questions.txt"]

# iterate through each file with questions
for filename in question_filenames:

    # store the questions in a list, organized by topics
    with open(f"/Users/zhuobiaocai/Desktop/biology-review/questions_and_answers/{filename}", "r") as question_source:
        all_questions = "".join(question_source.readlines())
        questions_by_topic = re.split(r"Topic: [\w\s]+\n", all_questions.strip())[1:]
        topic_names = re.findall(r"Topic: [\w\s]+\n", all_questions.strip())

    # iterate through each topic's questions and store each individual question separately
    for topic_questions in questions_by_topic:

        current_topic = topic_names.pop(0).strip().replace("Topic: ", "")

        question_regex = r"Multiple-Choice Question\n"

        for q in re.split(question_regex, topic_questions):
            if len(q.strip()) > 0:
                questions_list.append(q.strip())
                topics_list.append(current_topic)

answer_filenames = ["OpenStax Concepts of Biology Chapter Review Answers.txt"]

# iterate through each file with answers and save the answers in a list in the same order 
# as written in the file
for filename in answer_filenames:
    with open(f"/Users/zhuobiaocai/Desktop/biology-review/questions_and_answers/{filename}", "r") as answer_source:
        all_answers = "".join(answer_source.readlines())
        answers_by_topic = re.split(r"Topic: [\w\s]+\n", all_answers.strip())[1:]

        answer_num_regex = r"[\d]+\. [ABCD]{1}[\n]*"
        for answer in re.findall(answer_num_regex, all_answers):
            answers_list.append(answer.strip()[-1].lower())

# format each question and its answer as a dictionary structure
# {"topic" : topic, "question_num" : num, "question": question, "answer_choices": list of choices, "correct_answer" : correct answer}
# store all the dictionaries inside a list
questions_and_answers_list = []

for i in range(len(questions_list)):
    question = questions_list[i]
    answer = answers_list[i]
    topic = topics_list[i].lower()

    # extract only the question
    choice_a_matcher = re.search(r"a\. [\s\w\-,:;’]+[\.]*\n", question)
    question_only = question[ : choice_a_matcher.start() ].strip()

    question_num_matcher = re.search(r"[\d]+\. ", question_only)
    question_num = int(question_only[ : question_num_matcher.end()].strip().strip("."))
    question_only = question_only[ question_num_matcher.end() : ]

    # use regex to parse for the answer choices
    answer_choices = [ 
        re.findall(r"a\. [\s\w\-,:;’]+[\.]*\n", question)[0].strip(),
        re.findall(r"b\. [\s\w\-,:;’]+[\.]*\n", question)[0].strip(),
        re.findall(r"c\. [\s\w\-,:;’]+[\.]*\n", question)[0].strip(),
        re.findall(r"d\. [\s\w\-,:;’]+[\.]*[\n]*", question)[0].strip()
    ]

    correct_answer = answers_list[i]

    questions_and_answers_list.append({
        "topic" : topic,
        "question_num" : question_num,
        "question" : question_only,
        "answer_choices" : answer_choices,
        "correct_answer" : correct_answer,
    })

output_filename = "/Users/zhuobiaocai/Desktop/biology-review/questions_and_answers/processed_questions.json"
with open(output_filename, "w") as file:
    json.dump(questions_and_answers_list, file)