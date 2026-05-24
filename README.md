# AI-Powered Autonomous Loan Negotiation System

An offline AI-to-AI loan negotiation prototype where a Personal AI agent negotiates directly with a Bank AI agent using local LLaMA 3 through Ollama. The system demonstrates how future financial interactions could be handled by autonomous agents that reason over user financial data, institutional lending rules, and natural language negotiation strategies without direct human involvement.

## Project Description

This project was developed as an AI-powered autonomous loan negotiation system where a Personal AI agent, aware of user-specific financial data such as salary, expenses, credit score, education, income, and expected loan amount, communicates with a Bank AI agent that enforces institutional lending policies.

Using local LLaMA 3 via Ollama, both agents negotiate in natural language and attempt to reach mutually acceptable loan terms without human input. The application is built with Python Flask and a live browser-based chat interface. It runs fully offline once Ollama and the LLaMA 3 model are available locally.

The project demonstrates the future of AI-to-AI financial interactions through structured reasoning, prompt engineering, agent coordination logic, and autonomous decision-making.

## Demo and Article

## YouTube Demo

[![Watch the demo](https://img.youtube.com/vi/756sYJhqdgo/maxresdefault.jpg)](https://www.youtube.com/watch?v=756sYJhqdgo)


## Medium Article

- Medium Article: https://medium.com/@sudamgd/the-future-of-banking-when-your-personal-ai-negotiates-loans-for-you-f2da6605718b

## Key Features

- Autonomous negotiation between two AI agents
- Personal AI agent uses customer financial profile data
- Bank AI agent follows bank-side risk and lending objectives
- Natural language negotiation powered by local LLaMA 3
- Fully offline execution using Ollama
- Flask backend with simple REST endpoints
- Live browser-based chat UI
- Start, stop, restart, and save negotiation controls
- Structured loan offer extraction using an XML-like offer format
- Automatic negotiation completion when both agents reach similar monthly payment terms
- Chat history saving to JSON

## Technology Stack

- Python
- Flask
- HTML
- JavaScript
- LLaMA 3
- Ollama
- Prompt engineering
- Agent coordination logic

## System Architecture

```text
User Browser
    |
    | Live Chat UI
    v
Flask Web Application
    |
    | Builds prompts for each AI role
    v
Personal AI Agent <---- Negotiation History ----> Bank AI Agent
    |
    | Local API call
    v
Ollama running LLaMA 3
    |
    | Generated negotiation response
    v
Offer Extraction and Agreement Check
```

## How It Works

1. The user starts the negotiation from the web interface.
2. The Flask backend launches a negotiation loop in a separate thread.
3. The Personal AI agent receives the customer financial profile and negotiates for better loan terms.
4. The Bank AI agent responds based on bank-side objectives such as profit, risk control, and lending limits.
5. Each agent includes a structured loan offer at the end of its response.
6. The backend extracts loan terms such as amount, interest rate, term, and monthly payment.
7. The negotiation continues until both agents reach similar monthly payment terms or the user stops the process.
8. The conversation can be saved as a JSON file for review.

## Agent Roles

### Personal AI Agent

The Personal AI agent acts on behalf of the customer. It uses the customer's salary, other income, monthly expenses, credit score, education, and expected loan amount to negotiate better terms.

Its main objectives are to:

- Reduce the interest rate
- Reduce monthly payments
- Reduce the total loan cost
- Negotiate terms that are affordable for the customer

### Bank AI Agent

The Bank AI agent acts on behalf of the lending institution. It evaluates the negotiation from a bank perspective.

Its main objectives are to:

- Maximize bank profitability
- Reduce lending risk
- Avoid increasing the requested loan amount
- Provide loan terms that remain acceptable from an institutional lending perspective

## Loan Offer Format

Each AI response is expected to include a structured loan offer in the following format:

```text
<offer>
amount: [total loan amount in LKR]
interest_rate: [annual interest percentage]
term_months: [loan term in months]
monthly_payment: [estimated monthly payment]
</offer>
```

This format allows the Flask backend to extract and compare negotiation terms programmatically.

## Project Structure

```text
.
├── app.py
├── templates/
│   └── chat.html
├── chat_history.json
└── README.md
```

Note: Flask expects the HTML file to be inside a `templates` directory. If `chat.html` is currently in the project root, move it into a folder named `templates`.

## Prerequisites

Make sure the following are installed before running the project:

- Python 3.10 or higher
- pip
- Ollama
- LLaMA 3 model pulled locally through Ollama

## Installation

Clone the repository or download the project files.

```bash
git clone <repository-url>
cd <project-folder>
```

Create and activate a virtual environment.

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

Install the required Python packages.

```bash
pip install flask requests
```

Install and run Ollama, then pull the LLaMA 3 model.

```bash
ollama pull llama3
```

Start Ollama if it is not already running.

```bash
ollama serve
```

## Running the Application

Run the Flask application.

```bash
python app.py
```

Open the application in your browser.

```text
http://127.0.0.1:5000
```

Use the interface controls to start, stop, restart, or save the negotiation.

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Loads the chat interface |
| `/start` | POST | Starts the autonomous negotiation loop |
| `/stop` | POST | Stops the negotiation |
| `/restart` | POST | Clears the conversation and resets the negotiation state |
| `/save` | POST | Saves the conversation and offers to `chat_history.json` |
| `/chat` | GET | Returns the current conversation and extracted offers |

## Example Customer Profile

The current prototype includes a sample customer profile:

```python
USER_PROFILE = {
    "name": "Sudam",
    "salary": 250000,
    "other_income": 50000,
    "education": "Bachelor's in IT",
    "monthly_expenses": 100000,
    "credit_score": 720,
    "expected_loan_amount": 4000000
}
```

This profile can be changed in `app.py` to test different loan negotiation scenarios.

## Example Use Cases

- Demonstrating autonomous AI-to-AI financial negotiation
- Exploring prompt engineering for multi-agent systems
- Testing local LLM capabilities in financial decision workflows
- Building proof-of-concept banking automation systems
- Simulating customer-bank loan negotiations without exposing data to cloud APIs

## Offline and Privacy-Focused Design

The project uses Ollama and a locally running LLaMA 3 model, meaning the negotiation can run without sending prompts or financial data to an external cloud AI service. This makes it suitable for exploring privacy-focused AI workflows where sensitive customer information remains on the local machine.

## Limitations

This project is a prototype and should not be used as a real financial decision-making system.

Current limitations include:

- No real credit bureau integration
- No formal loan affordability calculation engine
- No authentication or user management
- No database persistence beyond JSON export
- No regulatory compliance checks
- No production-ready risk model
- No validation that generated loan terms are financially accurate

## Future Improvements

Potential improvements include:

- Add a proper loan repayment calculation module
- Store negotiation history in a database
- Add user authentication and profile management
- Introduce configurable bank lending policies
- Add a formal affordability and risk assessment engine
- Improve agreement detection beyond monthly payment similarity
- Add support for multiple customer profiles
- Add PDF export for final negotiated loan terms
- Build a dashboard for comparing agent offers
- Add audit logs for explainability and compliance review

## Important Note

This project is created for educational and demonstration purposes only. It does not provide financial advice, lending approval, or real banking decisions. Any real-world loan decision should involve licensed financial professionals, regulatory checks, and verified financial data.

## Author

Developed as a demonstration of autonomous AI agents, local LLM usage, and AI-to-AI financial negotiation workflows.
