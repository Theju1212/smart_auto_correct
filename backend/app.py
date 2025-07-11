from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# Secure API key from environment
API_KEY = os.environ.get("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/correct', methods=['POST'])
def correct_text():
    data = request.json
    user_text = data.get('text', '')
    mode = data.get('mode', 'grammar')  # default mode

    # Mode instructions
    instructions = {
        "grammar": (
            "You are a helpful assistant that fixes grammar, spelling, and sentence structure. "
            "If words are misspelled or unclear, try to interpret them intelligently. "
            "For example, fix 'ma od less ou' to 'May God bless you'. "
            "Treat unknown words like names (e.g., 'theju')."
        ),
        "polite": "Rewrite the sentence in a more polite and respectful tone.",
        "expand": "Expand the sentence with more detail and emotion.",
        "shorten": "Make the sentence more concise while keeping the meaning.",
        "confident": "Rewrite the sentence to sound more assertive and confident."
    }

    prompt = instructions.get(mode, instructions["grammar"])

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "anthropic/claude-3-haiku",  # Change if needed
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.4,
            "max_tokens": 300
        }

        response = requests.post(BASE_URL, headers=headers, json=body)
        data = response.json()

        if "choices" in data:
            corrected = data["choices"][0]["message"]["content"].strip()
            return jsonify({"corrected": corrected})
        else:
            return jsonify({"error": data.get("error", "Unknown error occurred")}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
