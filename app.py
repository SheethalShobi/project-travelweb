from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.llms import Bedrock

app = Flask(__name__)
CORS(app)

# Initialize Bedrock LLM
llm = Bedrock(model_id="anthropic.claude-v2", region_name="us-east-1")

@app.route('/recommendation', methods=['POST'])
def recommendation():
    data = request.json
    user_query = data.get("query", "")
    response = llm.generate(user_query)
    return jsonify({"recommendation": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)