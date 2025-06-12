from flask import Flask, render_template
import yaml

app = Flask(__name__)

# Load the YAML data
def load_yaml():
    with open('../catalog_entry.yml', 'r') as file:
        return yaml.safe_load(file)['sources']

@app.route('/')
def index():
    data = load_yaml()
    sources = []
    for key, value in data.items():
        source_name = key
        source_url = value['metadata']['source_url']
        sources.append({'name': source_name, 'url': source_url})
    return render_template('index.html', sources=sources)


if __name__ == '__main__':
    app.run(debug=False)
