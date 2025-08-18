## Overview
Generate `toolEmbeddings.js` from `tools.csv` using Google Gemini embeddings. The output is JS code you can import in your GuidedTrack custom service.

## Files
- `tools.csv`: Input with headers `name,description,url`
- `main.py`: Reads CSV, calls `gemini-embedding-001`, normalizes vectors, writes `toolEmbeddings.js`
- `toolEmbeddings.js`: Output array `export const toolEmbeddings = [...]`
 - `customService.js`: Example GuidedTrack custom service. Expects a POST body `{ userQuery }`, embeds it with Gemini, computes cosine similarity against `toolEmbeddings`, and returns `{ similarPrograms: [ { name, description, url, similarity }, ... ] }`. Requires `GEMINI_API_KEY` in the environment.

## Setup
1. Install dependencies
```
pip3 install google-genai numpy python-dotenv
```
2. Create `.env` file with your key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage
1. Add tools as rows to `tools.csv` (must include `name,description,url`).

2. Run:
```
python3 main.py
```
3. Copy-paste your `toolEmbeddings.js` code in your GuidedTrack custom service.

## Using `customService.js`
- Use it as a template for your GuidedTrack custom service. Ensure `toolEmbeddings` is in scope (either paste the generated array into the file or import it if your runtime supports ESM).
- Deploy with `GEMINI_API_KEY` set. Send a POST with `{ "userQuery": "..." }` and it returns the top 7 similar tools in `similarPrograms`.