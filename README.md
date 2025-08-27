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
2. Then create an `.env` file with your API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage
1. Add the Clearer Thinking tools you want to embed as rows to `tools.csv` (must include `name,description,icon,url`).

2. Run:
```
python main.py
```
The script above outputs the tool embeddings both in csv. format and as .js code. Here's an example of the .js code, you will see the last line of each tool has the embeddings:
```customService.js
// Auto-generated tool embeddings
export const toolEmbeddings = [
  {
    name: "40 Winks: Better Sleep Made Easy",
    description: "Achieve your optimal sleep experience with personalized recommendations based on your specific situation.",
    icon: "fas fa-bed",
    url: "https://programs.clearerthinking.org/40_winks.html",
    embedding: [-0.018600957328794663,-0.022704962296625733,0.0017865335355843953,-0.1320592178539956,-0.004145144440923949,...]
 },
  {
    name: "Achieve Your Goals",
    description: "Build a step-by-step plan for your chosen goal and set milestone reminders to track your progress.",
    icon: "fas fa-bullseye",
    url: "https://programs.clearerthinking.org/achieve_your_goals.html",
    embedding: [-0.00788683872817934,0.027745177755655968,-0.00026693852563894257, [...]
  },
  etc.
```


1. That's it! Copy-paste your `toolEmbeddings.js` output code at the end of your GuidedTrack custom service. See [`customService.js`](customService.js) for an example implementation (you will see it has the embeddings pasted at the end).

## Using customService.js
- Use it as a template for your GuidedTrack custom service. Ensure `toolEmbeddings` is in scope (e.g., paste the generated array from toolEmbeddings.js into your custom service).
- Deploy with `GEMINI_API_KEY` environment variable.

## Questions
Contact [André](https://andreferretti.com/)