import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import requests
from src.LLM import generate, loadMessagesToMemory
from conf.Models import llm_url


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/ask", methods=["POST", "HEAD"])
    def generate_response():
        if request.method == "POST":
            query = request.json["query"]

            if not any(char.isalpha() for char in query):
                # Query doesn't have any alpha characters
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Question must contain alpha characters",
                        }
                    ),
                    400,
                )

            response, passage, summary = generate(query, db)
            # print(f"request host: {request.host}")
            data = {"Response": response, "Context": passage, "Summary": summary}

            try:
                url = f"{llm_url}/getlawyers"
                print(f"Getting lawyers from {url}")
                # Make an internal request to the /api/data route
                response = requests.post(url, json={"query": query})
                response.raise_for_status()
                if response.status_code == 200:
                    laywersData = response.json()
                    if "lawyersData" in laywersData:
                        lawyers = laywersData["lawyersData"]
                        data["lawyers"] = lawyers
                        print(f"Finished getting lawyers")
                    else:
                        data["lawyers"] = []
                        print(laywersData)

            except requests.exceptions.RequestException as e:
                print(e)
                data["lawyers"] = []
                data["lawyerError"] = str(e)

            print(f"Sending back data")
            return jsonify(data)

        else:
            return jsonify({"success": True, "message": "Message recieved"})

    
    @app.route("/loadcontext", methods=["POST"])
    def load_context():
        if request.method == "POST":
            messages = request.json["messages"]
            loadMessagesToMemory(messages)
            return jsonify({"success": True})
        else:
            abort(502, "Unsupported request method")

    @app.route("/wake", methods=["GET", "HEAD"])
    def wake():
        return jsonify({"success": True})

    return app


app = create_app()
