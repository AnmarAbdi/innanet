import os
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BertModel
import torch
import json

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)
    cls_embedding = outputs.last_hidden_state[:, 0, :].numpy()
    return cls_embedding

def parse_html_files(directory):
    documents = {}
    for filename in os.listdir(directory, class_name):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                soup = BeautifulSoup(file, 'html.parser')
                title = soup.title.string if soup.title else filename
                paragraphs = soup.find_all('p', class_=class_name)
                content = ' '.join([p.get_text() for p in paragraphs])
                documents[filename] = {'title': title, 'content': content}
    return documents

def encode_documents(documents):
    embeddings = {}
    for filename, doc in documents.items():
        embedding = get_embedding(doc['content'])
        embeddings[filename] = embedding.tolist()  # Convert numpy array to list for JSON serialization
    return embeddings

def save_embeddings(embeddings, output_file):
    with open(output_file, 'w') as file:
        json.dump(embeddings, file)

if __name__ == "__main__":
    document_dir = "projects"
    output_file = "embeddings.json"
    class_name = "input-content"
    
    documents = parse_html_files(document_dir)
    embeddings = encode_documents(documents)
    save_embeddings(embeddings, output_file)
    
    print(f"Embeddings saved to {output_file}")
