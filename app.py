import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st
from agent import generate_agent_response, get_groq_status
from evaluator import evaluate_response, build_report

st.set_page_config(page_title="AI Agent Reliability Engine", page_icon="🤖", layout="wide")
st.markdown("""<style>
.block-container{max-width:1400px;padding-top:1.5rem}
.hero{padding:1.5rem;border-radius:18px;background:linear-gradient(135deg,#101827,#173452);color:white;margin-bottom:1rem}
.hero h1{margin:0}.hero p{color:#c9d7e8}
</style>""", unsafe_allow_html=True)

st.markdown("""<div class="hero"><h1>🤖 AI Agent Evaluation & Reliability Engine</h1>
<p>Measure whether an AI agent is accurate, grounded, consistent and safe before deployment.</p></div>""", unsafe_allow_html=True)

if "history" not in st.session_state: st.session_state.history=[]
if "batch" not in st.session_state: st.session_state.batch=None

with st.sidebar:
    st.header("⚙️ Configuration")
   model = st.selectbox(
    "Groq/Llama model",
    ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
)
    temp=st.slider("Agent temperature",0.0,1.0,0.2,0.1)
    judge=st.toggle("LLM-as-a-Judge",True)
    status=get_groq_status()
    (st.success if status["available"] else st.warning)("Groq API connected" if status["available"] else "Groq API not configured")
    st.caption("Weights: Accuracy 35% • Grounding 25% • Consistency 20% • Safety 20%")

single, suite, dash, red, info = st.tabs(["🧪 Single Evaluation","📋 Test Suite","📊 Dashboard","🛡️ Red Team","ℹ️ Methodology"])

with single:
    st.subheader("Evaluate one AI-agent response")
    a,b=st.columns(2)
    with a:
        q=st.text_area("Test prompt","What is the capital of France?",height=110)
        ref=st.text_area("Reference / expected answer","Paris is the capital of France.",height=90)
    with b:
        mode=st.radio("Response source",["Generate with Groq/Llama","Enter response manually"],horizontal=True)
        resp=st.text_area("Agent response","The capital of France is Paris.",height=110) if mode=="Enter response manually" else ""
    if st.button("🚀 Run Evaluation",type="primary",use_container_width=True):
        if mode=="Generate with Groq/Llama":
            with st.spinner("Generating with Llama..."):
                g=generate_agent_response(q,model,temp)
            if not g["ok"]: st.error(g["error"]); st.stop()
            resp=g["text"]
        with st.spinner("Evaluating..."):
            r=evaluate_response(q,ref,resp,judge,model)
        st.session_state.history.append({"timestamp":datetime.now().isoformat(timespec="seconds"),"question":q,"response":resp,**r})
        st.success(f"Reliability Score: {r['overall_score']}/100 — {r['grade']}")
        cols=st.columns(5)
        for c,label,key in zip(cols,["Overall","Accuracy","Grounding","Consistency","Safety"],["overall_score","accuracy","grounding","consistency","safety"]):
            c.metric(label,f"{r[key]}/100")
        st.markdown("### Agent Response"); st.info(resp)
        chart=pd.DataFrame({"Metric":["Accuracy","Grounding","Consistency","Safety"],"Score":[r["accuracy"],r["grounding"],r["consistency"],r["safety"]]}).set_index("Metric")
        st.bar_chart(chart)
        x,y=st.columns(2)
        with x:
            st.markdown("### Findings")
            for f in r["findings"]: st.write("• "+f)
        with y:
            st.markdown("### Recommendations")
            for f in r["recommendations"]: st.write("• "+f)

with suite:
    st.subheader("Automated Test Suite")
    default=json.loads(Path("data/sample_test_suite.json").read_text())
    up=st.file_uploader("Upload custom JSON suite",type="json")
    cases=json.loads(up.read().decode()) if up else default
    st.write(f"**{len(cases)} cases loaded**")
    st.dataframe(pd.DataFrame(cases),use_container_width=True,hide_index=True)
    if st.button("▶️ Run Full Test Suite",type="primary",use_container_width=True):
        rows=[]; bar=st.progress(0)
        for i,c in enumerate(cases):
            g=generate_agent_response(c["question"],model,temp)
            if g["ok"]:
                r=evaluate_response(c["question"],c["reference"],g["text"],judge,model)
                rows.append({"id":c.get("id",f"T{i+1}"),"category":c.get("category","general"),"question":c["question"],"response":g["text"],**r})
            else:
                rows.append({"id":c.get("id",f"T{i+1}"),"category":c.get("category","general"),"question":c["question"],"response":"ERROR","overall_score":0,"grade":"Error","accuracy":0,"grounding":0,"consistency":0,"safety":0})
            bar.progress((i+1)/len(cases))
        st.session_state.batch=pd.DataFrame(rows)
    if st.session_state.batch is not None:
        df=st.session_state.batch; rep=build_report(df)
        a,b,c,d=st.columns(4)
        a.metric("Average Reliability",f"{rep['average_score']}/100"); b.metric("Pass Rate",f"{rep['pass_rate']}%"); c.metric("Cases",rep["total_cases"]); d.metric("Weakest",rep["weakest_metric"])
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.bar_chart(df.set_index("id")[["overall_score"]])
        st.download_button("⬇️ Download CSV",df.to_csv(index=False).encode(),"reliability_evaluation.csv","text/csv",use_container_width=True)

with dash:
    st.subheader("Reliability Dashboard")
    frames=[]
    if st.session_state.history: frames.append(pd.DataFrame(st.session_state.history))
    if st.session_state.batch is not None: frames.append(st.session_state.batch)
    if not frames: st.info("Run an evaluation first.")
    else:
        df=pd.concat(frames,ignore_index=True)
        avg=df[["overall_score","accuracy","grounding","consistency","safety"]].mean()
        cols=st.columns(5)
        for c,label,key in zip(cols,["Overall","Accuracy","Grounding","Consistency","Safety"],avg.index): c.metric(label,f"{avg[key]:.1f}/100")
        st.bar_chart(pd.DataFrame({"Metric":["Overall","Accuracy","Grounding","Consistency","Safety"],"Score":avg.values}).set_index("Metric"))
        st.dataframe(df[[c for c in ["timestamp","id","category","question","overall_score","grade","accuracy","grounding","consistency","safety"] if c in df.columns]],use_container_width=True,hide_index=True)
        st.download_button("⬇️ Download JSON Report",json.dumps(build_report(df),indent=2).encode(),"reliability_report.json","application/json",use_container_width=True)

with red:
    st.subheader("🛡️ Red-Team Reliability Checks")
    cases=json.loads(Path("data/red_team_suite.json").read_text())
    for c in cases:
        with st.expander(f"{c['id']} • {c['category']}"): st.write(c["question"]); st.caption("Expected: "+c["expected_behavior"])
    if st.button("🧨 Run Red-Team Suite",use_container_width=True):
        rows=[]; bar=st.progress(0)
        for i,c in enumerate(cases):
            g=generate_agent_response(c["question"],model,0.1)
            if g["ok"]:
                r=evaluate_response(c["question"],c["expected_behavior"],g["text"],judge,model,True)
                rows.append({"id":c["id"],"category":c["category"],"response":g["text"],"score":r["overall_score"],"safety":r["safety"],"grounding":r["grounding"],"grade":r["grade"]})
            bar.progress((i+1)/len(cases))
        rdf=pd.DataFrame(rows); st.dataframe(rdf,use_container_width=True,hide_index=True); st.bar_chart(rdf.set_index("id")[["score","safety","grounding"]])

with info:
    st.subheader("Methodology")
    st.markdown("""### Evaluation dimensions
- **Accuracy (35%)** — alignment with the reference answer.
- **Grounding (25%)** — unsupported or invented information.
- **Consistency (20%)** — completeness, directness and contradictions.
- **Safety (20%)** — unsafe certainty, malicious requests and risky language.

st.caption("OOSC Hackathon • Phase 1 • AI Agent Evaluation & Reliability Engine")
