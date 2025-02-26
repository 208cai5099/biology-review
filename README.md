# Biology Chatbot Review

https://biology-chatbot-review.streamlit.app/

## Introduction

Biology Chatbot Review is a web application that enables users to reinforce their understanding of biology topics by answering review questions. A LLM verifies the inputted answers and explains the correct answers through a chatbot interface. This tool is designed to help students learning general biology topics at a high school-level.

Tools used: Streamlit, Firebase, Replicate, Meta's Llama 3 model

This project was inspired by Chanin Nantasenamat's chatbot built using Streamlit and Meta's Llama 2 model. Check out his [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/) for details.

## How Does this App Work?

You first select a topic and the number of questions to answer in the sidebar. Once you have made your selections, the chatbot will in the application will give you questions to answer one at a time. You can respond using the chat feature and ask clarifying questions as needed.

## How Does the Chatbot Feature Work?

In case you do not know, a language model is a model or program that predicts text based on some input. If you use the autocomplete function on your phone or computer, you are using a language model to help predict what words follow the text that you typed. A Large Language Model (LLM) essentially does the same thing. A LLM is a prediction program that is trained to produce human-like responses based on some input ("How are you?", "What's the weather?", "I like ...", etc.). A LLM has the term "Large" in its name, because a LLM is trained on large amounts of text data to recognize patterns and trends in sentence structure, grammar, and other linguistic characteristics. Due to the size of the dataset and the design of the program, a LLM can perform text completion that resemble human-like responses.

The LLM used for the chatbot in this application is Meta's open-source [Llama 3 70b instruct model](https://replicate.com/meta/meta-llama-3-70b-instruct). Due to the large computations, Replicate is used to run the model. The messages from the chat are sent to Replicate. Replicate then runs the model to produce a response based on the chat history. The response is sent back to the application for display.

Please keep in mind that LLMs can make mistakes. It is possible for the model to generate a message with incorrect information about a biological concept or topic. If you suspect there is a mistake, please use a resource to verify it.

## Where do the Review Questions Come From?

The review questions were generated in advance using Meta's Llama 3 70b instruct model. Prompts were given to the model to generate multiple-choice questions about particular biology concepts. Because LLMs can make mistakes, the questions were edited as needed to ensure accuracy and correctness. All the questions are stored inside a Firebase project.

## Additional Information

[Llama Website](https://www.llama.com/)

[Llama 3 Community License Agreement](https://github.com/meta-llama/llama3/blob/main/LICENSE)

[Streamlit Website](https://streamlit.io/)

[Firebase Website](https://firebase.google.com/)

[Replicate Website](https://replicate.com/home)
