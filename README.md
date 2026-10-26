# 🧠 ETIKU AI

### Intelligence. Knowledge. Action.

**ETIKU AI** is an intelligent, conversational AI assistant built with Python, Streamlit, and Google's Gemini models. It provides a modern, interactive environment for learning, research, coding, creative thinking, and everyday problem-solving.

The project is developed by **Kefas Etiku Francis** and named in honor of the founder's grandfather.

## Overview

ETIKU AI combines the conversational capabilities of Google's Gemini models with a custom-designed Streamlit interface to deliver a responsive, user-friendly AI experience.

The application features a midnight-navy interface, teal accents, organized chat history, configurable AI responses, and real-time response streaming.

## Features

- **AI-powered conversations:** Ask questions, explore ideas, generate content, and receive assistance with programming and technical topics.
- **Streaming responses:** View AI-generated answers as they are produced.
- **Conversation history:** Create, search, rename, and delete conversations.
- **Date-grouped chats:** Organize conversations under Today, Yesterday, Previous 7 Days, Previous 30 Days, and Older.
- **Response settings:** Adjust response style and creativity.
- **Session isolation:** Keep each visitor's conversations separate in the public demo.
- **Custom interface:** Responsive Streamlit design with ETIKU AI branding.
- **Secure API configuration:** Supports environment variables and Streamlit Cloud Secrets.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application interface |
| Google Gemini API | AI response generation |
| Google Gen AI SDK | Gemini model integration |
| Streamlit Session State | Temporary, session-specific chat storage |
| SQLite | Local development conversation storage |
| CSS | Custom user interface styling |
| GitHub | Version control and source hosting |

## Project Structure

```text
ETIKU-AI/
├── assets/
│   └── style.css
├── src/
│   └── etiku_ai/
│       ├── assistant.py
│       ├── config.py
│       ├── session_storage.py
│       └── settings.py
├── etiku_app.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/kefras/etiku-ai.git
cd etiku-ai
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure your Gemini API key**

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit your real API key to GitHub.

**5. Start ETIKU AI**

```bash
streamlit run etiku_app.py
```

Open the local URL displayed in your terminal.

## Deployment

ETIKU AI is designed for deployment using Streamlit Community Cloud.

The application uses Streamlit Secrets to securely load the Gemini API key in the hosted environment.

The public-demo version stores conversations in individual Streamlit sessions. Conversation history is temporary and may be lost when a session ends or the application restarts.

## Roadmap

- User registration and authentication
- Secure cloud database for persistent conversations
- Document upload and conversational PDF analysis
- Retrieval-Augmented Generation (RAG)
- Voice interaction
- Expanded AI model integrations
- Improved mobile experience
- Usage monitoring and reliability improvements

## Developer

**Kefas Etiku Francis**

Computer Science Student | Cloud & DevOps Enthusiast | AI Developer

- **Portfolio:** https://kefas.live
- **GitHub:** https://github.com/kefras

## License

This project is distributed under the terms of the MIT License. See `LICENSE` for details.

---

**ETIKU AI — Intelligence. Knowledge. Action.**

*Built to make knowledge and intelligent assistance more accessible.*