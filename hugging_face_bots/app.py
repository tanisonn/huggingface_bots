from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_user_input', methods=['POST'])
def process_user_input():
    data = request.get_json()
    user_input = data.get('user_input', '')

    # Your BERT model logic here to process the user_input
    processed_text = "Processed text will appear here."  # Replace this with the actual processed text
    
    response_data = {'processed_text': processed_text}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
