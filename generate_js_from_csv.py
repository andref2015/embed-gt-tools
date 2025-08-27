import csv
import json

def read_embedded_tools_csv(csv_path: str):
    tools = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            embedding = json.loads(row['embedding']) if row.get('embedding') else []
            tools.append({
                'name': row['name'],
                'description': row['description'],
                'icon': row['icon'],
                'url': row['url'],
                'embedding': embedding,
            })
    return tools


def write_tool_embeddings_js(tools, output_js_path: str):
    with open(output_js_path, 'w') as f:
        f.write('// Auto-generated tool embeddings\n')
        f.write('export const toolEmbeddings = ')
        f.write('[\n')
        for i, tool in enumerate(tools):
            f.write('  {\n')
            f.write(f'    name: {json.dumps(tool["name"])},\n')
            f.write(f'    description: {json.dumps(tool["description"])},\n')
            f.write(f'    icon: {json.dumps(tool["icon"])},\n')
            f.write(f'    url: {json.dumps(tool["url"])},\n')
            f.write('    embedding: [')
            f.write(','.join(str(x) for x in tool['embedding']))
            f.write(']\n')
            f.write('  }')
            if i < len(tools) - 1:
                f.write(',')
            f.write('\n')
        f.write('];\n')

tools = read_embedded_tools_csv('embedded_tools.csv')
write_tool_embeddings_js(tools, 'toolEmbeddings.js')
print(f"Created toolEmbeddings.js with {len(tools)} tools from embedded_tools.csv")