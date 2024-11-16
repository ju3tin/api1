from flask import Flask, request, jsonify
   # from app import app
from flask import Flask, request, redirect, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
from groq import Groq
import os
os.environ["GROQ_API_KEY"]= "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"
# Initialize Flask app


# Initialize Groq client
client = Groq()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Extract user input from the request
        data = request.json
        messages = data.get("messages", [])
        temperature = data.get("temperature", 1)
        max_tokens = data.get("max_tokens", 1024)
        top_p = data.get("top_p", 1)

        # Validate the input
        if not messages:
            return jsonify({"error": "Messages are required"}), 400

        # Create completion using Groq
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,  # Disable streaming for API response
            stop=None,
        )

        # Extract relevant data from the completion object
        response_data = {
            "id": completion.id,
            "model": completion.model,
            "choices": [
                {
                    "message": choice.message.dict(),
                    "finish_reason": choice.finish_reason,
                    "index": choice.index
                }
                for choice in completion.choices
            ],
            "usage": {
                "prompt_tokens": completion.usage.prompt_tokens,
                "completion_tokens": completion.usage.completion_tokens,
                "total_tokens": completion.usage.total_tokens,
            }
        }

        # Return the serialized response
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
