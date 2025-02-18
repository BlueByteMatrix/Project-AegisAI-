from flask import Flask, request, jsonify
from bcrypt import hashpw, gensalt, checkpw

app = Flask(__name__)

# Simulated user database with hashed passwords
users = {}

# Route to register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    users[username] = hashed_password
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        stored_password_hash = users[username]
        if checkpw(password.encode('utf-8'), stored_password_hash):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
        return jsonify({'message': 'Invalid username'}), 401

if __name__ == '__main__':
    app.run(debug=True)


class Subscription:
    def __init__(self, subscription_id, user_id, plan_type, start_date, end_date, status="Active"):
        self.subscription_id = subscription_id
        self.user_id = user_id
        self.plan_type = plan_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def activate_subscription(self):
        self.status = "Active"
        print(f"Subscription {self.subscription_id} activated.")

    def cancel_subscription(self):
        self.status = "Cancelled"
        print(f"Subscription {self.subscription_id} cancelled.")


class Feedback:
    def __init__(self, feedback_id, user_id, content, rating):
        self.feedback_id = feedback_id
        self.user_id = user_id
        self.content = content
        self.rating = rating

    def add_feedback(self):
        print(f"Feedback from user {self.user_id} added successfully.")



class FileUpload:
    def __init__(self, file_id, user_id, upload_date, status="Pending"):
        self.file_id = file_id
        self.user_id = user_id
        self.upload_date = upload_date
        self.status = status

    def upload_file(self, file_name):
        print(f"File {file_name} uploaded successfully.")



class Payment:
    def __init__(self, payment_id, user_id, amount, status="Pending"):
        self.payment_id = payment_id
        self.user_id = user_id
        self.amount = amount
        self.status = status

    def process_payment(self):
        self.status = "Completed"
        print(f"Payment of ${self.amount} processed successfully.")
