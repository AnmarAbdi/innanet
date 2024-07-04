import os
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BertModel
import torch
import json

# Load up BERT tokenizer and model (pre-trained, so we don't have to train from scratch)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_embedding(text, max_length=512):
    # Tokenize the text and split it into chunks of max_length
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=max_length)
    with torch.no_grad():  # No need to calculate gradients (we're not training)
        outputs = model(**inputs)
    # Get the embeddings for the [CLS] token, which summarizes the input
    cls_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    return cls_embeddings.mean(axis=0)  # Average the embeddings of all tokens

def parse_html_files(directory, class_name):
    documents = {}
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".html"):  # Only process HTML files
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                soup = BeautifulSoup(file, 'html.parser')
                # Get the title from the <title> tag
                title = soup.title.string if soup.title else filename
                # Find all paragraphs with the specified class
                paragraphs = soup.find_all('p', class_=class_name)
                # Combine the text from all these paragraphs
                content = ' '.join([p.get_text() for p in paragraphs])
                # Store title and content in a dictionary
                documents[filename] = {'title': title, 'content': content}
    return documents

def encode_documents(documents):
    embeddings = {}
    # Loop through each document and get its embedding
    for filename, doc in documents.items():
        embedding = get_embedding(doc['content'])
        embeddings[filename] = embedding.tolist()  # Convert numpy array to list for JSON
    return embeddings

def save_embeddings(embeddings, output_file):
    # Save the embeddings to a JSON file
    with open(output_file, 'w') as file:
        json.dump(embeddings, file)

if __name__ == "__main__":
    document_dir = "projects"  # Directory where the HTML files are
    output_file = "embeddings.json"  # Output file for embeddings
    class_name = "input-content"  # Class name to filter paragraphs
    
    # Parse HTML files and get their content
    documents = parse_html_files(document_dir, class_name)
    # Encode the documents to get embeddings
    embeddings = encode_documents(documents)
    # Save the embeddings to a file
    save_embeddings(embeddings, output_file)
    
    print(f"Embeddings saved to {output_file}")
