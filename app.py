from flask import Flask, request, jsonify
from flask_cors import CORS
from src.timecraft.generate import generate_timetable

app = Flask(__name__)
# CORS(app)


@app.route("/create_timetable", methods=["POST"])
def create_timetable():
    data = request.json
    try:
        return jsonify(generate_timetable(data, verbose=True)), 200
    except Exception as e:
        return ({"message": str(e)}, 400)


if __name__ == "__main__":
    app.run(debug=True)
