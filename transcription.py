from youtube_transcript_api import YouTubeTranscriptApi
import re

class YouTubeTranscriber:
    def __init__(self, url):
        self.url = url
        self.video_id = None
        self.transcript = None

    def get_video_id(self):
        """Extract the video ID from a YouTube URL."""
        video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', self.url)
        if video_id_match:
            self.video_id = video_id_match.group(1)
        else:
            raise ValueError("Invalid YouTube URL")

    def fetch_transcript(self):
        """Fetch the transcript for the given video ID."""
        if self.video_id is None:
            raise ValueError("Video ID is not set. Call get_video_id() first.")

        try:
            self.transcript = YouTubeTranscriptApi.get_transcript(self.video_id)
        except Exception as e:
            print(f"An error occurred while fetching the transcript: {str(e)}")
            self.transcript = None

    def extract_text(self):
        """Extract the text from the transcript."""
        if self.transcript is None:
            raise ValueError("Transcript is not available. Call fetch_transcript() first.")

        text = ' '.join([entry['text'] for entry in self.transcript])
        return text

    def get_transcription(self):
        """Get the transcription text."""
        self.get_video_id()
        self.fetch_transcript()
        return self.extract_text()


def main(url):
    # Get YouTube URL from the user
    video_url = url
    try:
        # Create an instance of YouTubeTranscriber
        transcriber = YouTubeTranscriber(video_url)

        # Get and print the transcription
        transcription = transcriber.get_transcription()
        return transcription
    except ValueError as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    print(main())
