# tts-joinery-multilang

**tts-joinery-multilang** is a multilingual-friendly fork of [tts-joinery](https://github.com/drien/tts-joinery), optimized specifically for UTF-8 texts, multilingual content, and texts lacking clear punctuation.

The original project uses NLTK Punkt tokenizer, which works well for English and similar languages. This fork replaces it with a robust, token-aware chunking method using **spaCy** and **tiktoken**, ensuring reliable processing of multilingual and punctuation-light texts.

## Key Differences from Original:

- ✅ Uses **spaCy multilingual tokenizer** (`xx_sent_ud_sm`) instead of NLTK Punkt.
- ✅ Implements robust, token-aware chunking to handle texts without clear punctuation.
- ✅ Explicitly supports multilingual and UTF-8 encoded texts.

## How it Works:

Since currently-popular TTS APIs (like OpenAI's) are limited to 4096 characters or 2000 tokens per request, this library will:

- Chunk the input text into manageable segments using spaCy and tiktoken.
- Run each chunk through the TTS API.
- Join together the resulting audio chunks to produce a single MP3 file.

Currently, only the OpenAI API is supported, with the intent to add more in the future.

---

## Installation

Install via pip:

```bash
pip install tts-joinery-multilang
