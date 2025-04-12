from typing import Optional
from pydub import AudioSegment
import spacy
import tiktoken

from joinery.api.base import BaseTtsApi

class JoinOp:
    MAX_TOKENS = 1800  # safely below 2000 token limit

    def __init__(self, text: str, api: BaseTtsApi):
        self.text = text
        self.api = api
        self.nlp = spacy.load("xx_sent_ud_sm")
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")

    def process_to_file(self, file_path):
        chunks = self.chunk_all()
        audio = None
        for chunk in chunks:
            result = self.run_tts(chunk)
            audio = self.join_audio(result, append_to=audio)
        audio.export(file_path)

    def chunk_all(self):
        paragraphs = [p.strip() for p in self.text.split("\n") if p.strip()]

        chunks = []
        current_chunk = ""
        current_chunk_tokens = 0

        for paragraph in paragraphs:
            paragraph_tokens = len(self.tokenizer.encode(paragraph))

            if paragraph_tokens > self.MAX_TOKENS:
                words = paragraph.split()
                sub_chunk = ""
                sub_chunk_tokens = 0

                for word in words:
                    word_tokens = len(self.tokenizer.encode(word + " "))
                    if sub_chunk_tokens + word_tokens <= self.MAX_TOKENS:
                        sub_chunk += word + " "
                        sub_chunk_tokens += word_tokens
                    else:
                        chunks.append(sub_chunk.strip())
                        sub_chunk = word + " "
                        sub_chunk_tokens = word_tokens

                if sub_chunk.strip():
                    chunks.append(sub_chunk.strip())

                current_chunk = ""
                current_chunk_tokens = 0
            else:
                if current_chunk_tokens + paragraph_tokens <= self.MAX_TOKENS:
                    current_chunk += ("\n" if current_chunk else "") + paragraph
                    current_chunk_tokens += paragraph_tokens
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = paragraph
                    current_chunk_tokens = paragraph_tokens

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def run_tts(self, chunk):
        return self.api.process_to_file(chunk)

    def join_audio(
        self, file_path, append_to: Optional[AudioSegment] = None
    ) -> AudioSegment:
        segment = AudioSegment.from_mp3(file_path)
        if append_to is None:
            append_to = segment
        else:
            append_to += segment

        return append_to
