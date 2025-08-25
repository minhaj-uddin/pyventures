from flask import Flask, request, jsonify
from tasks import send_email_notification

app = Flask(__name__)


@app.route("/signup", methods=["POST"])
def signup():
    user_data = request.json
    email = user_data.get("email")
    name = user_data.get("name")

    # Queue the email sending task (non-blocking)
    send_email_notification.delay(email, f"Welcome {name}!")

    return jsonify({"message": "User signed up successfully. Confirmation email will be sent shortly."})


@app.route("/purchase", methods=["POST"])
def purchase():
    user_data = request.json
    email = user_data.get("email")
    item = user_data.get("item")

    send_email_notification.delay(email, f"Thanks for purchasing {item}!")

    return jsonify({"message": "Purchase completed. Receipt email will be sent shortly."})


if __name__ == "__main__":
    app.run(debug=True)
