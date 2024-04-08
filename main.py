from flask import Flask, render_template, request, jsonify
from llama_index.core import StorageContext, load_index_from_storage

import os

os.environ["OPENAI_API_KEY"] = "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"

app = Flask(__name__)

# Load the index
def load_index():
    storage_context = StorageContext.from_defaults(persist_dir="index.json")
    return load_index_from_storage(storage_context)

# Home route
@app.route('/')
def home():
    prompt_message = "Hello! My name is Jarvis, Welcome to CodeCaste! How can I help you today?"
    return render_template('index5.html', prompt_message=prompt_message)

# Ask route
@app.route('/ask', methods=['POST'])
def ask():
    if request.method == 'POST':
        user_query = request.form['user_query']
        if user_query.lower() == 'bye':
            return jsonify({'response': 'Goodbye!'})
        else:
            response = query_engine.query(user_query)

            # Check if the response indicates that the chatbot does not know the answer
            if "I'm sorry" in response.response:
                return jsonify({'response': "Oops! It seems like you've asked a question outside the scope of our current conversation. If you have any specific inquiries related to website design or development, feel free to ask, and I'll do my best to help you!"})
            else:
                return jsonify({'response': response.response})

if __name__ == '__main__':
    query_engine = load_index().as_query_engine()
    app.run(debug=True)
