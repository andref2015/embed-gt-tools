from google import genai
from google.genai import types
import json
import numpy as np
import csv
import sys
import os
from dotenv import load_dotenv
from generate_js_from_csv import write_tool_embeddings_js

# Load environment variables from .env file
load_dotenv()

# Write your Gemini API key here
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Load csv of tools
tools = []
with open('tools.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tools.append({
            "name": row["name"],
            "description": row["description"],
            "icon": row["icon"],
            "url": row["url"]
        })

# Generate embeddings for each tool
embedded_tools = []

for tool in tools:
    # Combine name and description for richer embedding
    content = f"{tool['name']}: {tool['description']}"
    
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=content,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=768
        )
    )
    
    # Get the embedding and normalize it
    embedding = np.array(result.embeddings[0].values)
    normalized = (embedding / np.linalg.norm(embedding)).tolist()
    
    embedded_tools.append({
        "name": tool["name"],
        "description": tool["description"],
        "icon": tool["icon"],
        "url": tool["url"],
        "embedding": normalized
    })
    
    print(f"Embedded: {tool['name']}")

# Save embedded tools to CSV
with open('toolEmbeddings.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'description', 'icon', 'url', 'embedding'])
    for tool in embedded_tools:
        writer.writerow([
            tool['name'],
            tool['description'],
            tool['icon'],
            tool['url'],
            json.dumps(tool['embedding'])
        ])

print(f"Created toolEmbeddings.csv with {len(embedded_tools)} tools")

# Also write a JS module with the embeddings for frontend usage
write_tool_embeddings_js(embedded_tools)
print(f"Created toolEmbeddings.js with {len(embedded_tools)} tools")