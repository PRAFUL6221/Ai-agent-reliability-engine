# 🚀 Deployment Guide

## GitHub
1. Create a repository named `oosc-ai-agent-reliability-engine`.
2. Upload the project files.
3. Confirm `app.py` and `requirements.txt` are in the repository root.
4. Do **not** upload an API key.

## Streamlit Community Cloud
1. Sign in to Streamlit Community Cloud with GitHub.
2. Choose **Create app**.
3. Select your repository and `main` branch.
4. Set the main file to `app.py`.
5. Deploy.
6. Open **Advanced settings → Secrets**.
7. Add:
```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```
8. Save/redeploy.
9. Test the live URL.

## Final checks
- Single Evaluation works
- Groq/Llama generation works
- LLM-as-a-Judge works
- Test Suite works
- Red Team works
- Dashboard works
- CSV/JSON downloads work
- README has live URL/GitHub/demo links
- No API key is visible in GitHub
