import re
import json

question = ""
questions_list = []
answers_list = []
topics_list = []

question_filenames = ["generated_questions_3_28_2025.txt"]

# iterate through each file with questions
for filename in question_filenames:

    # store the questions in a list, organized by topics
    with open(f"{filename}", "r") as question_source:
        all_questions = "".join(question_source.readlines()).strip()

        # append each question's topic to the list
        for topic in re.findall(r"Major Topic: [\w\s-]+\n", all_questions):
            topics_list.append(topic.strip().replace("Major Topic: ", ""))
        
        # append each question's correct answer to the list
        for answer in re.findall(r"Correct Answer: [abcd]{1}", all_questions):
            answers_list.append(answer.strip().replace("Correct Answer: ", ""))

        all_questions_split = re.split(r"Major Topic: [\w\s-]+\n", all_questions)[1:]
    
        # iterate through each question and append it
        for question in all_questions_split:
            questions_list.append(question.strip())
            
    
# format each question and its answer as a dictionary structure
# {"topic" : topic, "question": question, "answer_choices": list of choices, "correct_answer" : correct answer}
# store all the dictionaries inside a list
questions_and_answers_list = []

for i in range(len(questions_list)):
    question = questions_list[i]
    correct_answer = answers_list[i]
    topic = topics_list[i]

    # use regex to find where answer choice a begins and use indexing to extract just the question
    choice_a_matcher = re.search(r"a\. [\s\w\-,:;’°\(\)]+[\.]*\n", question)
    question_only = question[ : choice_a_matcher.start() ].strip()

    # use regex to parse for the answer choices
    answer_choices = [ 
        re.findall(r"a\. [\s\w\-,:;’°\(\)]+[\.]*\n", question)[0].strip(),
        re.findall(r"b\. [\s\w\-,:;’°\(\)]+[\.]*\n", question)[0].strip(),
        re.findall(r"c\. [\s\w\-,:;’°\(\)]+[\.]*\n", question)[0].strip(),
        re.findall(r"d\. [\s\w\-,:;’°\(\)]+[\.]*\n", question)[0].strip()
    ]

    # make the topic be snake case
    formatted_topic = "_".join(topic.lower().split(" "))

    questions_and_answers_list.append({
        "topic" : formatted_topic,
        "question" : question_only,
        "answer_choices" : answer_choices,
        "correct_answer" : correct_answer,
    })

output_filename = "processed_questions.json"
with open(output_filename, "w") as file:
    json.dump(questions_and_answers_list, file)