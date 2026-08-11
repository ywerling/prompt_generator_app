from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/prompt", methods=["GET", "POST"])
def prompt():
    prompt_text = ""
    submitted = False

    if request.method == "POST":
        prompt_text = request.form.get("prompt", "").strip()
        submitted = bool(prompt_text)

    return render_template(
        "prompt.html",
        prompt_text=prompt_text,
        submitted=submitted,
    )


if __name__ == "__main__":
    app.run(debug=True)
