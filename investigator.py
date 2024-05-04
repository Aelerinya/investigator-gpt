import csv
from openai import OpenAI
import os
import sys

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fetch the OpenAI API key from the environment variable


def process_batch(messages):
    """
    Function to check if the text contains personal information using OpenAI's Chat API with the GPT-3.5 Turbo model.
    """

    system_prompt = """
You are a helpful assistant trained to identify and extract specific types of personal information from text, 
focusing exclusively on the sender of each message. Review the following messages and list any occurrences 
of the following types of personal information related solely to the sender: 
full names, phone numbers, addresses, email addresses, dates of birth, nationalities, 
and any other personally identifiable information pertaining directly to the sender.
"""


    user_messages = [{"role": "user", "content": msg} for msg in messages]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}] + user_messages,
        )
        # Extracting the response text
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print("An error occurred:", e)
        return "Error"


# Path to your CSV file
csv_file_path = sys.argv[1]

# Batch size for processing messages
batch_size = 5


def summarize_personal_information(info_items):
    """
    Summarize all extracted personal information into a concise report.
    """
    prompt = "Summarize the following personal information details into a concise report. Use bullets points like this: '- Email: bob@example.com'."
    detailed_info = "\n".join(info_items)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": detailed_info},
            ],
        )
        # Extracting the summary text
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print("An error occurred while summarizing:", e)
        return "Error in summarization"


# Read the CSV file and process in batches
with open(csv_file_path, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    batch = []
    personal_info_summary = []

    # Go through each message and collect batches
    for i, row in enumerate(reader):
        # if i >= 50:
        #     break
        batch.append(row["Message Content"])
        if len(batch) >= batch_size:
            results = process_batch(batch)
            personal_info_summary.append(results)
            print(f"Batch Processed:\n{results}\n")
            batch = []

    # Process any remaining messages in the final batch
    if batch:
        results = process_batch(batch)
        personal_info_summary.append(results)
        print(f"Final Batch Processed:\n{results}\n")

    # Summarize or list all extracted personal information
    if personal_info_summary:
        # Join all information into a single string (customize as needed)
        full_summary = " ".join(personal_info_summary)
        print(
            "Summary of Personal Information Extracted from All Messages:\n",
            full_summary,
        )

    # Generate a summarized report of all personal information
    if personal_info_summary:
        summary = summarize_personal_information(personal_info_summary)
        print("Summarized Report of Personal Information:\n", summary)
