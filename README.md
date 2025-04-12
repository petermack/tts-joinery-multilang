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
pip install tts-joinery-utf
```

  
or use `pipx` to install as a standalone tool.  

### Additional Dependencies:

This fork requires the following additional packages:  

```bash
pip install spacy tiktoken
python -m spacy download xx_sent_ud_sm
```

  
**Requires ffmpeg** for audio file processing.  
Installation may vary depending on your system:  
* *   **Linux:** Use your system package manager (e.g., `apt install ffmpeg`).
* *   **Mac:** `brew install ffmpeg`.
* *   **Windows:** [Download ffmpeg](https://ffmpeg.org/download.html#build-windows) and add it to your PATH.  

* * *

## Usage

### Command-Line Interface (CLI)

The CLI expects to find an OpenAI API Key in an `OPENAI_API_KEY` environment variable, or in a `.env` file.  

#### Syntax

```css
ttsjoin [OPTIONS] [COMMAND]
```

  

#### Options

```vim
Options:
--input-file FILENAME   Plaintext file to process into speech, otherwise stdin
--output-file FILENAME  MP3 result, otherwise stdout
--model TEXT            Slug of the text-to-speech model to be used (tts-1, tts-1-hd or gpt-4o-mini-tts)
--service TEXT          API service (currently only supports openai)
--voice TEXT            Slug of the voice to be used
--instructions TEXT     Voice instructions (only for gpt-4o-mini-tts model)
--no-cache BOOLEAN      Disable caching
--help                  Show this message and exit.

Commands:
  cache [clear, show]
```

  

#### Examples

1. 1.  Using an input file and specifying an output file:  

```bash
# Basic usage with tts-1 model
ttsjoin --input-file input.txt --output-file output.mp3 --model tts-1 --service openai --voice onyx

# Using the new gpt-4o-mini-tts model with instructions
ttsjoin --input-file input.txt --output-file output.mp3 --model gpt-4o-mini-tts --voice ballad --instructions "Speak in a calm, soothing voice"
```

  
1. 2.  Using stdin and stdout with default options:  

```bash
echo "Your text to be processed" | ttsjoin > output.mp3
```

  
1. 3.  Disable caching (each chunk of text is cached by default for performance):  

```bash
ttsjoin --input-file input.txt --output-file output.mp3 --no-cache
```

  
1. 4.  Clear cache directory:  

```bash
ttsjoin cache clear
```

  

* * *

### Python Library

You can also use `tts-joinery-utf` as part of your Python project:  

```python
from joinery.op import JoinOp
from joinery.api.openai import OpenAIApi

tts = JoinOp(
    text='This is only a test!',
    api=OpenAIApi(
        model='tts-1-hd',  # or 'gpt-4o-mini-tts'
        voice='onyx',
        api_key='your-openai-api-key',
        instructions='Speak in a calm, soothing voice',  # Optional, only for gpt-4o-mini-tts
    ),
)

tts.process_to_file('output.mp3')
```

  

* * *

## Changelog

#### v1.0.6-multilang (2025-04-12)

* *   ✅ Forked original project to support multilingual and punctuation-light texts.
* *   ✅ Replaced NLTK Punkt tokenizer with spaCy multilingual tokenizer (`xx_sent_ud_sm`).
* *   ✅ Added robust token-aware chunking logic using `tiktoken`.  

#### v1.0.5 (2025-03-20, original project)

* *   Added support for OpenAI's gpt-4o-mini-tts model and `instructions` parameter.  

#### v1.0.4 (2024-10-11, original project)

* *   Fixed issue with nltk dependency [#4](https://github.com/drien/tts-joinery/issues/5).
* *   Model, voice, and service CLI params are now case-insensitive.  
(See original [tts-joinery changelog](https://github.com/drien/tts-joinery) for earlier versions.)  

* * *

## Contributing

Contributions are welcome, particularly for other TTS APIs or further multilingual improvements. Check existing issues beforehand and feel free to open a PR. Code is formatted with [Black](https://github.com/psf/black).  
Tests can be run manually. The suite includes end-to-end tests with live API calls; ensure you have an `OPENAI_API_KEY`set in `.env.test`, and run `pytest`. Install development dependencies with:  

```bash
pip install -e .[test]
```

  

* * *

## Contributors

Special thanks to the original author and contributors:  
* *   Adrien Delessert ([@drien](https://github.com/drien))
* *   [Mayank Vishwakarma](mailto:mayank@mynk.me) (@mayankwebbing)  

* * *

## License

This project is licensed under the MIT License, same as the original project.  
Copyright © 2024 Adrien Delessert

Forked and modified © 2025 Peter Mack
