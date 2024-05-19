from flask import Flask, jsonify
from ai import ai
from editor import editor
from info import info
from library import library
from ran import ran

app = Flask(__name__)
app.register_blueprint(ai)
app.register_blueprint(editor)
app.register_blueprint(info)
app.register_blueprint(library)
app.register_blueprint(ran)


@app.route("/api/data", methods=["GET"])
def get_data():
    data = {"message": "Hello, Vue.js!"}
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
