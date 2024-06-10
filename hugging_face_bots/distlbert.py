from flask import Flask, render_template, request, jsonify
import torch
from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer

app = Flask(__name__)

# Load the DistilBERT model and tokenizer
model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-cased-distilled-squad', return_dict=False)
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')

def answer_question(question, paragraph, confidence_threshold=0.2):
    # Tokenize the question and paragraph
    encoding = tokenizer.encode_plus(text=question, text_pair=paragraph)
    inputs = encoding['input_ids']
    tokens = tokenizer.convert_ids_to_tokens(inputs)

    # Wrap the input tensor in an extra dimension to simulate a batch
    inputs = torch.tensor([inputs])

    # Get the start and end indices for the answer
    start_scores, end_scores = model(input_ids=inputs)
    start_index = torch.argmax(start_scores).item()
    end_index = torch.argmax(end_scores).item()

    # Extract the answer from tokens
    answer = ' '.join(tokens[start_index:end_index + 1])

    corrected_answer = ''
    for word in answer.split():
        if word[0:2] == '##':
            corrected_answer += word[2:]
        else:
            corrected_answer += ' ' + word

    # Check if the confidence in the answer is below the threshold or if the answer is empty
    if corrected_answer.strip() == "[CLS]":
        return "Unknown answer"
    else:
        return corrected_answer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_user_input', methods=['POST'])
def process_user_input():
    # Get the user input (recognized text) from the JSON request
    data = request.get_json()
    user_input = data.get('user_input', '')

    # Example paragraph (you can replace this with any paragraph you want)
    paragraph = '''The Bermuda Triangle, also known as the Devil's Triangle, is an urban legend focused on a loosely defined region in the western part of the North Atlantic Ocean where a number of aircraft and ships are said to have disappeared under mysterious circumstances. The idea of the area as uniquely prone to disappearances arose in the mid-20th century, but most reputable sources dismiss the idea that there is any mystery.[1][2][3]'''

    # Get the DistilBERT model's answer to the user's question
    bot_reply = answer_question(user_input, paragraph)

    # Return the bot's reply as a JSON response
    response_data = {'processed_text': bot_reply}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
