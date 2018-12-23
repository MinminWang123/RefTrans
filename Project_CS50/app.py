from flask import Flask, jsonify, render_template, request
from Parser import transfer

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    return render_template("demo.html")


@app.route('/transfer')
def transfer():
    if not request.args.get("o"):
        raise RuntimeError("missing original reference")
    if not request.args.get("j"):
        raise RuntimeError("missing journal format")

    return jsonify({"tag": True,
                    "text": request.args.get("o") + request.args.get("j")})


if __name__ == '__main__':
    app.run()
