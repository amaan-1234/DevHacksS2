import json
from transformers import pipeline

# Load the JSON file
with open("grouped_discord_messages.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Combine all messages into one article-like string
all_messages = []
for user, messages in data.items():
    for msg in messages:
        content = msg["content"].strip()
        if content:  # Skip empty messages
            all_messages.append(content)

ARTICLE = " ".join(all_messages)

# Load summarization pipeline (SLM version)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")

# Generate summary
summary = summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False)
summary_text = summary[0]['summary_text']

# Save summary to JSON
output_data = {"summary": summary_text}
with open("discord_summary_bart.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=4)

print("Summary saved to 'discord_summary_bart.json'")
