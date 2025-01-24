import os
import time
from transformers import GPT2Tokenizer
import requests

# Function to count tokens
def count_tokens(text):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokens = tokenizer.encode(text, add_special_tokens=False)
    return len(tokens)

# Function to read files from a folder and combine content
def read_files_from_folder(directory):
    combined_content = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    combined_content.append(f.read())
            except Exception as e:
                print(f"Could not read file {file_path}: {e}")
    return combined_content

# Function to batch content based on token limits
def batch_content(contents, max_tokens):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    batches = []
    current_batch = ""
    current_tokens = 0

    for content in contents:
        tokens = tokenizer.encode(content, add_special_tokens=False)
        if current_tokens + len(tokens) > max_tokens:
            # Save the current batch and reset
            batches.append(current_batch.strip())
            current_batch = ""
            current_tokens = 0
        # Add content to the current batch
        current_batch += content + "\n"
        current_tokens += len(tokens)

    # Add the last batch if it has any content
    if current_batch.strip():
        batches.append(current_batch.strip())

    return batches

# Function to send a batch to an API
def send_to_api(batch, api_url):
    response = requests.post(api_url, data={"content": batch})
    return response

def run(folder_path, api_url):
    api_key = input("Enter your API key: ")
    

    # Read files from the folder
    all_contents = read_files_from_folder(folder_path)

    # Token constraint: 10,000 tokens per minute
    max_tokens_per_batch = 10_000
    batches = batch_content(all_contents, max_tokens_per_batch)

    print(f"Total batches to send: {len(batches)}")

    # Send each batch to the API with a delay
    for i, batch in enumerate(batches):
        print(f"Sending batch {i + 1}/{len(batches)}...")
        response = send_to_api(batch, api_url)
        
        if response.status_code == 200:
            print(f"Batch {i + 1} sent successfully!")
        else:
            print(f"Batch {i + 1} failed with status code: {response.status_code}")
        
        # If this isn't the last batch, wait to respect the token limit
        if i < len(batches) - 1:
            print("Waiting 60 seconds to respect token limit...")
            time.sleep(60)
