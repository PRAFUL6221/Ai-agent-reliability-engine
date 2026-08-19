# 🎥 OOSC Phase-1 Demo Script
**Target: 7–8 minutes, never over 10 minutes**

## 0:00–0:30 — Introduction
“Hello. Our project is the AI Agent Evaluation and Reliability Engine. AI agents can sound convincing while being inaccurate or unsafe. Our system acts as a quality-control layer before deployment.”

## 0:30–1:15 — Problem and metrics
Open Methodology. Explain Accuracy 35%, Grounding 25%, Consistency 20%, Safety 20%.

## 1:15–2:30 — Live evaluation
Use:
- Question: `What is the capital of France?`
- Reference: `Paris is the capital of France.`
Choose **Generate with Groq/Llama** and run evaluation.
Explain the five score cards.

## 2:30–3:30 — LLM-as-a-Judge
Explain that a second Llama call evaluates the response semantically, while deterministic scoring provides a fallback.

## 3:30–4:45 — Test Suite
Run the included benchmark. Show average reliability, pass rate, cases and weakest metric. Download CSV.

## 4:45–5:45 — Red Team
Run prompt-injection, unsafe-certainty, fabrication, unauthorized-access and future-prediction cases. Explain why reliability includes failure behavior, not only normal answers.

## 5:45–6:30 — Dashboard
Show aggregated scores and evaluation history.

## 6:30–7:15 — Technology
“Python and Streamlit power the interface, Groq provides fast Llama inference, Pandas handles analytics, and the evaluator is separated from the agent layer so other agents can be plugged in later.”

## 7:15–8:00 — Closing
“Don’t trust an AI agent only because it sounds intelligent. Measure it. Our Reliability Engine provides that measurement layer.”

### Recording tips
- Use a laptop if possible.
- Hide personal tabs and API keys.
- Keep the app pre-running.
- Use prepared test cases.
- Keep the video around 7–8 minutes.
