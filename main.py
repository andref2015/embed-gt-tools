from google import genai
from google.genai import types
import json
import numpy as np
import csv
import sys
import os
from dotenv import load_dotenv

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
        "url": tool["url"],
        "embedding": normalized
    })
    
    print(f"Embedded: {tool['name']}")

# Create JavaScript file
with open('toolEmbeddings.js', 'w') as f:
    f.write('// Auto-generated tool embeddings\n')
    f.write('export const toolEmbeddings = ')
    
    # Write the array more compactly
    f.write('[\n')
    for i, tool in enumerate(embedded_tools):
        f.write('  {\n')
        f.write(f'    name: {json.dumps(tool["name"])},\n')
        f.write(f'    description: {json.dumps(tool["description"])},\n')
        f.write(f'    url: {json.dumps(tool["url"])},\n')
        
        # Write embedding as a compact array
        f.write('    embedding: [')
        # Join numbers without spaces to save size
        f.write(','.join(str(x) for x in tool["embedding"]))
        f.write(']\n')
        
        f.write('  }')
        if i < len(embedded_tools) - 1:
            f.write(',')
        f.write('\n')
    f.write('];\n')

print(f"Created toolEmbeddings.js with {len(embedded_tools)} tools")