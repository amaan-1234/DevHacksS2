import json
from transformers import pipeline
import os
from sml_config import get_model_name, get_model_specs

def summarize_tasks(employee_name, tasks_file, output_file, model_key="distilbart"):
    """
    Summarize tasks using SLM models.
    
    Args:
        employee_name (str): Name of the employee
        tasks_file (str): Path to tasks JSON file
        output_file (str): Path to output JSON file
        model_key (str): SLM model key from sml_config.py
    """
    with open(tasks_file, "r") as f:
        tasks = json.load(f)

    # Get SLM model name
    model_name = get_model_name("summarization", model_key)
    print(f"🤖 Using SLM Model: {model_name}")
    print(f"📊 Model Specs: {get_model_specs(model_name)}")

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
        "Tasks completed on time": completed_on_time,
        "model_used": model_name,
        "model_specs": get_model_specs(model_name)
    }

    with open(output_file, "w") as f:
        json.dump(summary_output, f, indent=2)

    print(f"✅ Summary saved to {output_file}")
    print(f"📊 Summary Stats:")
    print(f"  - Completed: {len(completed)}")
    print(f"  - Not Completed: {len(not_completed)}")
    print(f"  - On Time: {len(completed_on_time)}")
    print(f"  - Missed Deadlines: {len(missed_deadlines)}")

# Example usage with different SLM models
if __name__ == "__main__":
    print("🚀 Testing different SLM models for task summarization...")
    
    # Test with different models
    models_to_test = ["distilbart", "distilbart_large", "pegasus"]
    
    for model_key in models_to_test:
        print(f"\n{'='*50}")
        print(f"Testing with {model_key}...")
        try:
            summarize_tasks(
                employee_name="Shreyas Srinivasan",
                tasks_file="Agent 1/summary.json",
                output_file=f"Agent 3/summary_{model_key}.json",
                model_key=model_key
            )
        except Exception as e:
            print(f"❌ Error with {model_key}: {str(e)}")
    
    print(f"\n🎉 SLM model testing completed!")
