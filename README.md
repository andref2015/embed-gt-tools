## Overview
Generates pre-computed text embeddings for Cleaerer Thinking tools using gemini-embedding-001. The output is JS code you can import in a GuidedTrack custom service.

## Files
- `tools.csv`: Input with headers `name,description,url` (this is the file you want to update with new tools)
- `main.py`: Reads `tools.csv` CSV, calls gemini-embedding-001, normalizes vectors, writes `toolEmbeddings.js` as output
- `toolEmbeddings.js`: Output array with embeddings for each tool
 - `customService.js`: Example GuidedTrack custom service. Expects a POST body, embeds it with Gemini, computes cosine similarity against `toolEmbeddings`, and returns `{ similarPrograms: [ { name, description, icon, url, similarity }, ... ] }`. Requires `GEMINI_API_KEY` as environment variable.

## Setup
1. Install dependencies for `main.py`. In your terminal, run:
```
pip3 install google-genai numpy python-dotenv
```
2. Then create `.env` file with your API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage
1. Add tools you want to embed as rows to `tools.csv` (must include `name,description,icon,url`).

2. Run:
```
python main.py
```
This outputs a t
3. Copy-paste your `toolEmbeddings.js` code in your GuidedTrack custom service.

## Using customService.js
- Use it as a template for your GuidedTrack custom service. Ensure `toolEmbeddings` is in scope (e.g., paste the generated array from toolEmbeddings.js into your custom service).
- Deploy with `GEMINI_API_KEY` environment variable.

## Questions
Contact [André](https://andreferretti.com/)