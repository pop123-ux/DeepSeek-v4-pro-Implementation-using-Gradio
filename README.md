# DeepSeek Chat — Gradio UI 💬

A streaming chat interface over **DeepSeek**'s OpenAI-compatible API, built with **Gradio**. Ships in two flavors so you can pick whichever fits your workflow:

- **[`app.py`](./app.py)** — standalone Python app you run locally.
- **[`notebook.ipynb`](./notebook.ipynb)** — one-cell-at-a-time Colab notebook (badge below).

<a href="https://colab.research.google.com/github/pop123-ux/DeepSeek-v4-pro-Implementation-using-Gradio/blob/main/notebook.ipynb" target="_parent">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Features

- 🔁 **Token streaming** — replies render as the model generates them, no waiting for the full response.
- 🧠 **Full conversation memory** — chat history is threaded back into every request in OpenAI messages format.
- ⚙️ **Runtime controls** (in `app.py`) — editable system prompt, temperature slider, max-tokens slider, example prompts.
- 🔐 **No hard-coded keys** — reads `DEEPSEEK_API_KEY` from your environment (or Colab's Secrets panel).
- 🎯 **Model-agnostic within DeepSeek's catalog** — swap the target model via one env var (`DEEPSEEK_MODEL`).
- 🛡️ **Graceful failures** — API errors surface as inline chat messages instead of crashing the UI.

## Screenshot

<!-- Add a screenshot of the running Gradio UI here, e.g.:
![DeepSeek Chat UI](./docs/screenshot.png)
-->

## Getting your API key

Grab one from **[platform.deepseek.com](https://platform.deepseek.com/)** → *API Keys*. DeepSeek's endpoint is OpenAI-compatible, so the [`openai` Python SDK](https://github.com/openai/openai-python) works directly against it.

## Run it locally

```bash
git clone https://github.com/pop123-ux/DeepSeek-v4-pro-Implementation-using-Gradio.git
cd DeepSeek-v4-pro-Implementation-using-Gradio

pip install -r requirements.txt

cp .env.example .env      # then edit .env and paste your key
export $(grep -v '^#' .env | xargs)   # load DEEPSEEK_API_KEY into this shell

python app.py
```

Then open the printed local URL (usually http://127.0.0.1:7860). To expose a temporary public URL, change `share=False` to `share=True` at the bottom of `app.py`.

## Run it in Colab

1. Click the **Open In Colab** badge above.
2. In Colab's left sidebar open the 🔑 **Secrets** panel and add `DEEPSEEK_API_KEY`.
3. Run the cells top-to-bottom — Gradio prints a public share link at the end.

## Configuration

Everything is controlled by environment variables (or by editing the constants at the top of `app.py`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DEEPSEEK_API_KEY`  | *(required)* | Your DeepSeek API key. |
| `DEEPSEEK_MODEL`    | `deepseek-v4-pro` | Model ID sent in the `model` field. See DeepSeek's docs for currently available IDs. |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com` | OpenAI-compatible base URL. Override to point at a proxy or a different endpoint. |

## Project layout

```
DeepSeek-v4-pro-Implementation-using-Gradio/
├── app.py               # standalone Gradio app (recommended for local use)
├── notebook.ipynb       # Colab-first notebook version
├── requirements.txt     # gradio + openai
├── .env.example         # template for local API-key config
└── .gitignore
```

## Tech stack

Python · [Gradio](https://gradio.app/) · [OpenAI Python SDK](https://github.com/openai/openai-python) · [DeepSeek API](https://platform.deepseek.com/)

## License

MIT — feel free to fork and adapt.

## 🔗 More

- Author: [@pop123-ux](https://github.com/pop123-ux)
- Medium write-ups: [medium.com/@Pop123](https://medium.com/@Pop123)
