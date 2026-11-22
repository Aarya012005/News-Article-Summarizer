"""News Article Summarizer - Streamlit UI.  Run: streamlit run app.py"""
import streamlit as st

from summarizer import summarize, fetch_article, ExtractionError
from summarizer import llm
from summarizer.pipeline import to_markdown

st.set_page_config(page_title="News Article Summarizer", page_icon="📰", layout="wide")

# ---------- sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")
    providers = ["gemini", "groq", "ollama"]
    default = llm.default_provider()
    provider = st.selectbox("LLM provider", providers, index=providers.index(default) if default in providers else 0)
    model = st.text_input("Model", value=llm.default_model(provider))
    st.caption("API keys are read from the `.env` file, never typed into the app.")
    st.divider()
    st.subheader("🕘 History")
    if "history" not in st.session_state:
        st.session_state.history = []
    if not st.session_state.history:
        st.caption("Your summaries will appear here.")
    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"- {item['headline'][:60] or 'Untitled'}")

# ---------- main ----------
st.title("📰 News Article Summarizer")
st.write("Paste a news URL or the article text and get a **5-line summary** plus **3 key points**.")

tab_url, tab_text = st.tabs(["🔗 From URL", "📝 Paste text"])
with tab_url:
    url = st.text_input("News article URL", placeholder="https://www.example.com/news/...")
    go_url = st.button("Summarize URL", type="primary", key="go_url")
with tab_text:
    pasted = st.text_area("Article text", height=260, placeholder="Paste the full article here (min 50 words)...")
    go_text = st.button("Summarize text", type="primary", key="go_text")


def run(text, title="", source=""):
    with st.spinner("Summarizing..."):
        try:
            result = summarize(text, title=title, provider=provider, model=model)
        except (ValueError, llm.LLMError) as e:
            st.error(str(e))
            return
    st.session_state.history.append(result)

    st.subheader(result["headline"] or "Summary")
    c1, c2, c3, c4 = st.columns(4)
    s = result["stats"]
    c1.metric("Original length", f"{s['words_in']} words")
    c2.metric("Summary length", f"{s['words_out']} words")
    c3.metric("Time saved", f"~{s['reading_minutes']} min")
    c4.metric("Compression", f"{s['compression_pct']}%")
    st.caption(f"Topic: **{result['topic']}**  |  Tone: **{result['tone']}**")

    left, right = st.columns(2)
    with left:
        st.markdown("### 5-line summary")
        for i, line in enumerate(result["summary"], 1):
            st.markdown(f"{i}. {line}")
    with right:
        st.markdown("### Key points")
        for k in result["key_points"]:
            st.markdown(f"- {k}")

    st.download_button("⬇️ Download summary (.md)", to_markdown(result, source), file_name="summary.md")
    with st.expander("Show extracted / input text"):
        st.write(text)


if go_url:
    if not url.strip():
        st.warning("Please enter a URL.")
    else:
        try:
            with st.spinner("Downloading article..."):
                art = fetch_article(url)
        except ExtractionError as e:
            st.error(str(e))
        else:
            run(art["text"], art["title"], art["url"])
elif go_text:
    if not pasted.strip():
        st.warning("Please paste some text.")
    else:
        run(pasted.strip())
