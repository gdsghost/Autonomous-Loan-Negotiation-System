from flask import Flask, render_template, request, jsonify
import requests
import json
import threading
import time
import re

app = Flask(__name__)
conversation = []
offers = {"you": {}, "bank": {}}
is_running = False

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

USER_PROFILE = {
    "name": "Sudam",
    "salary": 250000,
    "other_income": 50000,
    "education": "Bachelor's in IT",
    "monthly_expenses": 100000,
    "credit_score": 720,
    "expected_loan_amount" : 4000000
}

def query_llama(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"].strip()

def build_prompt(role, history):
    persona = {
        "you": """You are an personal AI assistant negotiating a loan with the bank on behalf of the person. You want to reduce interest rate, monthly payments, and total cost. You must include your current loan offer in the following format at the end of each message:

<offer>
amount: [total loan amount in LKR]
interest_rate: [annual interest %]
term_months: [loan term in months]
monthly_payment: [estimated monthly payment]
</offer>""",
        "bank": """You are an AI loan officer negotiating on behalf of the bank. Maximize interest and profits to the bank while reducing risk and not increasing the expected loan amount. Negotiate while explaining pros and cons. Include your current offer at the end of your message in this format:

<offer>
amount: [total loan amount in LKR]
interest_rate: [annual interest %]
term_months: [loan term in months]
monthly_payment: [estimated monthly payment]
</offer>"""
    }

    profile_info = ""
    if role == "you":
        profile_info = (
            f"Customer details:\n"
            f"- Name: {USER_PROFILE['name']}\n"
            f"- Salary: {USER_PROFILE['salary']} LKR/month\n"
            f"- Other income: {USER_PROFILE['other_income']} LKR/month\n"
            f"- Expenses: {USER_PROFILE['monthly_expenses']} LKR/month\n"
            f"- Education: {USER_PROFILE['education']}\n"
            f"- Expected Loan Amount: {USER_PROFILE['expected_loan_amount']}\n"
            f"- Credit score: {USER_PROFILE['credit_score']}\n\n"
        )

    chat = "\n".join([f"{h['sender'].capitalize()}: {h['message']}" for h in history])
    return profile_info + persona[role] + "\n\nConversation:\n" + chat + f"\n{role.capitalize()}:"

def extract_offer(text):
    try:
        block = re.search(r"<offer>(.*?)</offer>", text, re.DOTALL)
        if not block:
            return {}
        lines = block.group(1).strip().splitlines()
        result = {}
        for line in lines:
            k, v = line.split(":")
            result[k.strip()] = float(v.strip())
        return result
    except:
        return {}

def negotiation_loop():
    global conversation, offers, is_running

    speaker = "you" if not conversation else ("bank" if conversation[-1]["sender"] == "you" else "you")

    while is_running:
        prompt = build_prompt(speaker, conversation)
        reply = query_llama(prompt)

        conversation.append({"sender": speaker, "message": reply})
        offers[speaker] = extract_offer(reply)

        # ✅ Auto-end if offers are similar
        if offers.get("you") and offers.get("bank"):
            y = offers["you"].get("monthly_payment")
            b = offers["bank"].get("monthly_payment")
            if y and b and abs(y - b) <= 500:
                conversation.append({
                    "sender": "system",
                    "message": "✅ Negotiation complete. Both parties have agreed on similar terms."
                })
                is_running = False
                break

        speaker = "bank" if speaker == "you" else "you"
        time.sleep(3)

@app.route('/')
def chat():
    return render_template("chat.html")

@app.route('/start', methods=['POST'])
def start():
    global is_running
    if not is_running:
        is_running = True
        thread = threading.Thread(target=negotiation_loop)
        thread.start()
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop():
    global is_running
    is_running = False
    return jsonify({"status": "stopped"})

@app.route('/restart', methods=['POST'])
def restart():
    global conversation, offers, is_running
    conversation = []
    offers = {"you": {}, "bank": {}}
    is_running = False
    return jsonify({"status": "restarted"})

@app.route('/save', methods=['POST'])
def save():
    with open("chat_history.json", "w") as f:
        json.dump({"conversation": conversation, "offers": offers}, f, indent=2)
    return jsonify({"status": "saved"})

@app.route('/chat', methods=['GET'])
def get_chat():
    return jsonify({"conversation": conversation, "offers": offers})

if __name__ == "__main__":
    app.run(debug=True)