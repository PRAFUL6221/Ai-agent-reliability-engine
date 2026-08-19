# 🤖 AI Agent Evaluation & Reliability Engine

## Problem
AI agents can sound convincing while producing inaccurate, unsupported, inconsistent or unsafe responses.

## Solution
A quality-control layer that evaluates AI-agent outputs before deployment.

### Core workflow
`Test Prompt → AI Agent → Evaluation Engine → Reliability Score → Dashboard`

### Metrics
| Metric | Weight |
|---|---:|
| Accuracy | 35% |
| Grounding | 25% |
| Consistency | 20% |
| Safety | 20% |

`Reliability = .35 Accuracy + .25 Grounding + .20 Consistency + .20 Safety`

### Features
- Groq + Llama response generation
- LLM-as-a-Judge
- Deterministic fallback evaluator
- Single-response evaluation
- Automated JSON test suites
- Red-team testing
- Dashboard and charts
- CSV and JSON reports
- Pytest unit tests
- Streamlit deployment ready

## Run locally
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Project structure
```text
app.py
agent.py
evaluator.py
requirements.txt
README.md
DEPLOYMENT.md
DEMO_SCRIPT.md
data/
  sample_test_suite.json
  red_team_suite.json
tests/
  test_evaluator.py
.streamlit/
  config.toml
```

## Why it is innovative
This is not another chatbot. It is an **evaluation layer for AI agents**, combining repeatable scoring, LLM-based semantic judging, benchmark tests and adversarial tests.

## Future scope
RAG citation verification, persistent history, model comparison, human review, CI/CD reliability gates, API access and domain-specific benchmarks.

## Team
**Team Name:** Ssbitians

**Members:**
- Praful Patil
- Shubham Surwade
- Mohit Mahajan

**College:**
Shram Sadhana Bombay Trust, College of Engineering & Technology, Jalgaon

