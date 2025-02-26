import re
import json

question = ""
questions_list = []
answers_list = []
topics_list = []

question_filenames = ["original_generated_questions.txt"]

# iterate through each file with questions
for filename in question_filenames:

    # store the questions in a list, organized by topics
    with open(f"question_generation/{filename}", "r") as question_source:
        all_questions = "".join(question_source.readlines())

        # append each question's topic to the list
        for topic in re.findall(r"Topic: [\w\s]+\n", all_questions.strip()):
            topics_list.append(topic.strip().replace("Topic: ", ""))
        
        # append each question's answer to the list
        for answer in re.findall(r"Correct Answer: [abcd]{1}\n", all_questions.strip()):
            answers_list.append(answer.strip().replace("Correct Answer: ", ""))

        all_questions_split = re.split(r"Topic: [\w\s]+\n", all_questions.strip())[1:]
    
        # iterate through each question and append it
        for question in all_questions_split:
            questions_list.append(question.strip())

# map each sub-topic to a major topic
cells = ["Ribosome", "Nucleus", "Cell Membrane", "Mitochondria", "Chloroplast", "Cell Wall", "Lysosome", "Rough Endoplasmic Reticulum",
        "Smooth Endoplasmic Reticulum", "Golgi Body", "Vacuole", "Cytoplasm"]
biochemistry = ["Photosynthesis", "Aerobic Respiration", "Anaerobic Respiration or Fermentation", "Glycolysis", "Enzyme", "Transcription",
                "Translation", "Protein Synthesis", "Protein Structure"]
genetics = ["Nucleotides", "Gene", "DNA Replication", "DNA Structure", "Chromosome Structure", "Gene Expression",
            "Genotype", "Phenotype", "Genetic Engineering", "Bacterial Transformation", "CRISPR-Cas9"]
human_physiology = ["Human Circulatory System", "Human Respiratory System", "Human Digestive System", "Human Nervous System", 
                    "Human Endocrine System", "Human Immune System", "Human Male Reproductive System", "Human Female Reproductive System",
                    "Hormone Functions"]
reproduction_and_development = ["Sexual Reproduction", "Asexual Reproduction", "Mitosis", "Meiosis", "Gametes", "Menstrual Cycle",
                                "Zygote", "Germ Cell Layers", "Stem Cells"]
evolution = ["Natural Selection", "Resource Competition", "Genetic Drift", "Convergent Evolution", "Divergent Evolution", 
             "Common Ancestor", "Adaptive Radiation"]
ecology = ["Heterotroph vs Autotroph", "Predator-Prey Relationship", "Ecological Succession", "Invasive Species", "Food Chain",
           "Carrying Capacity", "Niche", "Symbiosis"]


def add_subtopic(topic_mapping, sub_topic_list, major_topic):
    for sub_topic in sub_topic_list:
        topic_mapping[sub_topic] = major_topic

    return topic_mapping

topic_mapping = {}
for major_topic in ["cells", "biochemistry", "genetics", "human_physiology", "reproduction_and_development", "evolution", "ecology"]:

    if major_topic == "cells":
        topic_mapping = add_subtopic(topic_mapping, cells, "cells")
    elif major_topic == "biochemistry":
        topic_mapping = add_subtopic(topic_mapping, biochemistry, "biochemistry")
    elif major_topic == "genetics":
        topic_mapping = add_subtopic(topic_mapping, genetics, "genetics")
    elif major_topic == "human_physiology":
        topic_mapping = add_subtopic(topic_mapping, human_physiology, "human_physiology")
    elif major_topic == "reproduction_and_development":
        topic_mapping = add_subtopic(topic_mapping, reproduction_and_development, "reproduction_and_development")
    elif major_topic == "evolution":
        topic_mapping = add_subtopic(topic_mapping, evolution, "evolution")
    elif major_topic == "ecology":
        topic_mapping = add_subtopic(topic_mapping, ecology, "ecology")
    
# format each question and its answer as a dictionary structure
# {"topic" : major topic, "question_num" : num, "question": question, "answer_choices": list of choices, "correct_answer" : correct answer}
# store all the dictionaries inside a list
questions_and_answers_list = []

# keep track of the number of questions for each major topic
# use this to assign a number to each question
question_num_by_major_topic = {}
for major_topic in ["cells", "biochemistry", "genetics", "human_physiology", "reproduction_and_development", "evolution", "ecology"]:
    question_num_by_major_topic[major_topic] = 1

for i in range(len(questions_list)):
    question = questions_list[i]
    answer = answers_list[i]
    major_topic = topic_mapping[topics_list[i]]

    # use regex to where answer choice a begins and use indexing to extract just the question
    choice_a_matcher = re.search(r"a\. [\s\w\-,:;’°\(\)]+[\.]*\n", question)
    question_only = question[ : choice_a_matcher.start() ].strip()

    # use regex to parse for the answer choices
    answer_choices = [ 
        re.findall(r"a\. [\s\w\-,:;’°\(\)]+[\.]*\n", question)[0].strip(),
        re.findall(r"b\. [\s\w\-,:;’°\(\)]+[\.]*\n", question)[0].strip(),
        re.findall(r"c\. [\s\w\-,:;’°\(\)]+[\.]*\n", question)[0].strip(),
        re.findall(r"d\. [\s\w\-,:;’°\(\)]+[\.]*\n", question)[0].strip()
    ]

    correct_answer = answers_list[i]

    questions_and_answers_list.append({
        "topic" : major_topic,
        "question_num" : question_num_by_major_topic[major_topic],
        "question" : question_only,
        "answer_choices" : answer_choices,
        "correct_answer" : correct_answer,
    })

    # increment the question number for the topic that just got appended
    question_num_by_major_topic[major_topic] += 1


output_filename = "question_generation/processed_questions.json"
with open(output_filename, "w") as file:
    json.dump(questions_and_answers_list, file)