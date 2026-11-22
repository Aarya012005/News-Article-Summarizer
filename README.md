📰 News Article Summarizer 

Problem Statement: Readers lack time to read full articles. This tool takes a news URL or pasted text and returns a 5-line summary + 3 key points, along with the headline, topic, tone, and time saved.

Built by:Aarya Patil  
GitHub: https://github.com/Aarya012005

---

Features

Two inputs: a URL box (auto-extracts article text) and a paste-text box.

Structured JSON output from the LLM: 5-line summary, 3 key points, headline, topic, and tone.

Works with Gemini (free), Groq (free), or Ollama (local, offline); switch in .env.

Long-article handling: text is capped at 40,000 characters and condensed in chunks (map-reduce).

Statistics: original words, summary words, compression %, and reading time saved.

Download the summary as Markdown, plus session history in the sidebar.

Reliable API calls: automatic retries on timeouts, rate limits (429), and busy servers, with a 120-second timeout.

Error handling for bad URLs, blocked sites, short text, missing API keys, and invalid JSON.

16 offline unit tests and an evaluation script over 5 sample articles.


Architecture

text
URL ──► extractor.py (requests + BeautifulSoup) ─┐
                                                 ├─► pipeline.py
Pasted text ─────────────────────────────────────┘
     ─► prompts.py ─► llm.py ─► JSON ─► app.py (Streamlit)
          (chunking, validation)
```

Tech Stack

- Python 3.9+
- Streamlit
- Requests
- BeautifulSoup4
- python-dotenv
- unittest

LLM Providers:
- Gemini 3.8 Flash via API (default)
- Llama 3.3 via Groq
- Llama 3.2 via Ollama

 Setup

Clone the repository:

```bash
git clone https://github.com/Aarya012005/News-Article-Summarizer.git
cd News-Article-Summarizer
```

Create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

For Mac/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
copy .env.example .env
```

For Mac/Linux:

```bash
cp .env.example .env
```

Open `.env` and set your API key:

Free API key: https://aistudio.google.com/apikey

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Run the application:

```bash
streamlit run app.py
```

The app opens at:

```text
http://localhost:8098
```

Other Providers:

Set `LLM_PROVIDER=groq` with `GROQ_API_KEY`, or `LLM_PROVIDER=ollama` after running:

```bash
ollama pull llama3.2
```

 Run Tests

Run offline unit tests (no API key needed):

```bash
python -m unittest discover -s tests -t . -v
```

Run the evaluation script:

```bash
python evaluate.py
```

The evaluation script runs 5 sample articles and generates `test_results.md`.


Project Structure

```text
app.py                  Streamlit UI
evaluate.py             Batch test on samples/, writes test_results.md

summarizer/
    extractor.py        URL -> clean article text
    prompts.py          Prompt v1 (draft) and v2 (final)
    llm.py               Gemini / Groq / Ollama client with retries
    pipeline.py          Chunking, JSON parsing, validation, stats

samples/                5 sample articles
tests/                  Unit tests (LLM mocked)
screenshots/            Output screenshots
```

Troubleshooting

| Problem | Solution |
|---|---|
| `GEMINI_API_KEY missing` | Check that `.env` exists in the project root with the key, without quotes or spaces. |
| `404 model is no longer available` | Set `GEMINI_MODEL` in `.env` to the model name shown in the error message. |
| `429` or timeout | Wait a minute and retry. The app already retries automatically. |
| Could not find enough article text | The website may block scrapers or require JavaScript. Use the **Paste Text** tab instead. |

 Limitations & Future Work

- Paywalled or JavaScript-rendered websites cannot be scraped; the paste-text tab is the fallback.
- Summaries can miss nuance in very long or opinion-heavy articles.
- Future improvements:
  - Multilingual summaries.
  - Summary-length slider.
  - ROUGE scoring.
  - RSS batch mode.

---

Developed by Aarya Patil  
https://github.com/Aarya012005
