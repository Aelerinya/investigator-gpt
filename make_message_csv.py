import json
import csv
import sys

def extract_messages_to_csv(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract messages
    messages = data['messages']

    # Define CSV file path
    csv_file_path = json_file_path.replace('.json', '_messages.csv')

    # Create CSV and write the data
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Timestamp', 'Author ID', 'Author Name', 'Message Content', 'Is Pinned'])
        
        # Write message data
        for message in messages:
            timestamp = message['timestamp']
            author_id = message['author']['id']
            author_name = message['author']['name']
            content = message['content']
            is_pinned = message['isPinned']
            writer.writerow([timestamp, author_id, author_name, content, is_pinned])
    
    print(f"CSV file created: {csv_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
    else:
        json_file_path = sys.argv[1]
        extract_messages_to_csv(json_file_path)
