import os
try:
    from groq import Groq
except ImportError:
    Groq = None

def api_key():
    key = os.getenv("GROQ_API_KEY")
    if key: 
        return key
    try:
        import streamlit as st
        return st.secrets.get("GROQ_API_KEY")
    except Exception: 
        return None

def get_groq_status():
    key = api_key()
    return {"available": bool(key and Groq), "key_present": bool(key)}

def generate_agent_response(question, model="llama-3.3-70b-versatile", temperature=0.2):
    key = api_key()
    if not key: 
        return {"ok": False, "text": "", "error": "GROQ_API_KEY is not configured in Streamlit Secrets or environment variables."}
    if Groq is None: 
        return {"ok": False, "text": "", "error": "groq package is missing. Run pip install -r requirements.txt."}
    try:
        client = Groq(api_key=key)
        out = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI agent undergoing reliability evaluation. Provide accurate, grounded, and secure responses."},
                {"role": "user", "content": question}
            ],
            temperature=float(temperature),
            max_tokens=700
        )
        return {"ok": True, "text": out.choices[0].message.content.strip(), "error": ""}
    except Exception as e:
        return {"ok": False, "text": "", "error": f"Groq API error: {e}"}
