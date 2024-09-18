# VidSummarize

VidSummarize is an AI-powered Flask Python Web app that generates summaries and enables interactive Q&A for YouTube videos. The goal of this project is to make video content more accessible and interactive.

## 🛠️ Tech Stack

- **Backend**: Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **AI**: Google Gemini AI

## 🔐 User Authentication

1. Traditional signup with credentials
2. Google OAuth integration for seamless sign-in and log-in

## ⚙️ Core Features

1. **Video Transcription**: Paste any YouTube URL, and the app will transcribe the video using the youtube_transcript_api.
2. **AI-Powered Summarization**: Leverages Google Gemini AI (via the Google Gemini API and google.generativeai module) to provide concise summaries of the transcribed content.
3. **Interactive Q&A**: Users can ask questions about the video, and the AI will provide relevant answers.
4. **Secure Logout**: Ensures user privacy and security with a robust logout functionality.

## 💡 Additional Features

1. Dark mode and light mode options for comfortable viewing
2. User profile customization, including profile picture updates

## 🔜 Future Plans

1. Implement a new chat option similar to ChatGPT and Gemini
2. Integrate MongoDB for efficient chat history storage
3. Host the application on the Google Cloud platform
4. Explore integration of Meta's Llama 3.1 AI model with the application

## 🙏 Acknowledgements

- YouTube Transcript API
- Google Gemini AI
- Flask community
