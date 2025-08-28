import os
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, session, url_for

from app.components.retriever import create_qa_chain


load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    # Init session:
    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        user_input = request.form.get("prompt")

        if user_input:
            messages = session["messages"]
            messages.append({"role": "user", "content": user_input})
            session["messages"] = messages

            try:
                # Retrieve and append retrieved response:
                qa_chain = create_qa_chain()
                response = qa_chain.invoke({"query": user_input})
                result = response.get("result", "No response")

                messages.append({"role": "assistant", "content": result})

                session["messages"] = messages

            except Exception as e:
                error_message = f"Error: {str(e)}"
                return render_template(
                    "index.html", messages=session["messages"], error=error_message
                )

        return redirect(url_for("index"))

    return render_template("index.html", messages=session.get("messages", []))


@app.route("/clear")
def clear():
    session.pop("messages", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=False, use_reloader=False)