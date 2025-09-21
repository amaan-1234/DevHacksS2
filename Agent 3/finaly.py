import json
from transformers import pipeline
import os

def summarize_tasks(employee_name, tasks_file, output_file, model_name="sshleifer/distilbart-cnn-12-6"):
    with open(tasks_file, "r") as f:
        tasks = json.load(f)

    # Load summarization model
    summarizer = pipeline("summarization", model=model_name)

    # Prepare summary categories
    completed = []
    not_completed = []
    missed_deadlines = []
    completed_on_time = []

    for task in tasks:
        # Handle string-only tasks
        if isinstance(task, str):
            description = task
            status = "not completed"
            deadline = ""
            completed_date = ""
        elif isinstance(task, dict):
            description = task.get("description", "")
            status = task.get("status", "").lower()
            deadline = task.get("deadline", "")
            completed_date = task.get("completed_date", "")
        else:
            continue  # skip unknown types

        # Summarize if text is long
        text = f"Task: {description} Status: {status} Deadline: {deadline} Completed: {completed_date}"
        summary = summarizer(text, max_length=60, min_length=10, do_sample=False)[0]['summary_text']

        # Sort into buckets
        if status == "completed":
            completed.append(summary)
            if completed_date and deadline and completed_date <= deadline:
                completed_on_time.append(summary)
            elif completed_date and deadline and completed_date > deadline:
                missed_deadlines.append(summary)
        else:
            not_completed.append(summary)

    summary_output = {
        "Work completed": completed,
        "Work not completed": not_completed,
        "Missed deadlines": missed_deadlines,
        "Tasks completed on time": completed_on_time
    }

    with open(output_file, "w") as f:
        json.dump(summary_output, f, indent=2)

    print(f"Summary saved to {output_file}")

# Example usage
if __name__ == "__main__":
    summarize_tasks(
        employee_name="Shreyas Srinivasan",
        tasks_file="Agent 1/summary.json",
        output_file="Agent 2/summary.json"
    )
