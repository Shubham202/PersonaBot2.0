# Hitesh & Piyush AI Chatbot

A fun and educational chatbot simulating conversations between [Hitesh Choudhary](https://www.youtube.com/@HiteshChoudhary), [Piyush Garg](https://www.youtube.com/@PiyushGarg) and User, powered by OpenAI (for Hitesh) and Gemini (for Piyush), using video transcripts from YouTube to mimic their real speaking style.

## 🧠 Features

- Chat with AI personas of Hitesh and Piyush together.
- Uses real YouTube transcripts to learn their tone and language.
- Hitesh replies using OpenAI ChatGPT.
- Piyush replies using Google Gemini.
- Built with `Streamlit` for a simple web UI.
- Caches YouTube transcripts to avoid refetching.

## 🛠️ Setup Instructions

1. **Clone the repository**
```
   git clone https://github.com/your-username/hitesh-piyush-chatbot.git
   cd hitesh-piyush-chatbot
```

2. **Create a .env file**

Inside your project directory, create a .env file and add:
``` 

    OPENAI_API_KEY=your_openai_key_here
    GEMINI_API_KEY=your_gemini_key_here
```

3. **Install dependencies**
```
    pip install -r requirements.txt
``` 

4. **Run the app**
```
    streamlit run app.py
```