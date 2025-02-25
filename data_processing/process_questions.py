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
    with open(f"/Users/zhuobiaocai/Desktop/biology-review/data_processing/{filename}", "r") as question_source:
        all_questions = "".join(question_source.readlines())

        # append each question's topic to the running list
        for topic in re.findall(r"Topic: [\w\s]+\n", all_questions.strip()):
            topics_list.append(topic.strip().replace("Topic: ", ""))

        all_questions_split = re.split(r"Topic: [\w\s]+\n", all_questions.strip())[1:]
    
        # iterate through each question and append it
        for question in all_questions_split:
            questions_list.append(question.strip())
    
answer_filenames = ["OpenStax Concepts of Biology Chapter Review Answers.txt"]

# iterate through each file with answers and save the answers in a list in the same order 
# as written in the file
for filename in answer_filenames:
    with open(f"/Users/zhuobiaocai/Desktop/biology-review/data_processing/{filename}", "r") as answer_source:
        all_answers = "".join(answer_source.readlines())

        answer_num_regex = r"[\d]+\. [ABCD]{1}[\n]*"
        for answer in re.findall(answer_num_regex, all_answers):
            answers_list.append(answer.strip()[-1].lower())

# format each question and its answer as a dictionary structure
# {"topic" : topic, "question_num" : num, "question": question, "answer_choices": list of choices, "correct_answer" : correct answer}
# store all the dictionaries inside a list
questions_and_answers_list = []

# keep track of the number of questions for each topic
# use this to assign a number to each question
question_num_by_topic = {}
for topic in set(topics_list):
    formatted_topic = "_".join(topic.lower().split(" "))
    question_num_by_topic[formatted_topic] = 1

for i in range(len(questions_list)):
    question = questions_list[i]
    answer = answers_list[i]
    topic = "_".join(topics_list[i].lower().split(" "))

    # use regex to where answer choice a begins and use indexing to extract just the question
    choice_a_matcher = re.search(r"a\. [\s\w\-,:;’]+[\.]*\n", question)
    question_only = question[ : choice_a_matcher.start() ].strip()

    # use regex to extract the question's number and remove the question number from the question
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
        "question_num" : question_num_by_topic[topic],
        "question" : question_only,
        "answer_choices" : answer_choices,
        "correct_answer" : correct_answer,
    })

    # increment the question number for the topic that just got appended
    question_num_by_topic[topic] += 1

output_filename = "/Users/zhuobiaocai/Desktop/biology-review/processed_questions.json"
with open(output_filename, "w") as file:
    json.dump(questions_and_answers_list, file)