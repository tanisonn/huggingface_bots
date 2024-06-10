from flask import Flask, render_template, request, jsonify
from transformers import T5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)

# Load the T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')

def answer_question(question, paragraph):
    # Prepare the input by combining the question and paragraph
    input_text = f"question: {question} context: {paragraph}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    # Generate an answer
    answer_ids = model.generate(input_ids, num_return_sequences=1, max_length=50)

    # Decode the answer
    answer = tokenizer.decode(answer_ids[0], skip_special_tokens=True)

    return answer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_user_input', methods=['POST'])
def process_user_input():
    # Get the user input (recognized text) from the JSON request
    data = request.get_json()
    user_input = data.get('user_input', '')

    # Example paragraph (you can replace this with any paragraph you want)
    paragraph = '''Your example paragraph here'''

    # Get the T5 model's answer to the user's question
    bot_reply = answer_question(user_input, paragraph)

    # Return the bot's reply as a JSON response
    response_data = {'processed_text': bot_reply}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
