import transcription
import google.generativeai as genai

genai.configure(api_key='GEMINI_API_KEY')

class TranscriptChatbot:
    def __init__(self):
        self.flag = True
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=self.generation_config,
        )
        self.chat_session = self.model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "Analyze the provided YouTube video transcript which i will give following to this message. You need to "
                        "provide me a concise summary. Following the summary, I will ask you questions. Please answer them "
                        "exclusively using information from the transcript. If a question cannot be answered based on the transcript, "
                        "clearly state 'Information not found in transcript. Please remember in this entire chat that you should not answer any other questions apart from the video transcription. You need to say I cannot provide answer for that. Also keep in mind that i will be giving the response to the website. I cannot render markdown output. So don't use any markdown please give it to me in plain text",
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "Please provide the YouTube video transcript. I'm ready to analyze it and answer your questions! 😄 \n",
                    ],
                },
            ]
        )

    def get_summary(self, url):
        response = self.chat_session.send_message(transcription.main(url))
        return response.text

    def start_chat(self, user_input):
        if self.flag:
            self.flag = False
            return self.get_summary(user_input)
        response = self.chat_session.send_message(user_input)
        return response.text


