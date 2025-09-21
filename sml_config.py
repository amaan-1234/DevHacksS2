"""
SLM (Small Language Model) Configuration
========================================

This file contains all SLM model configurations for the multi-agent system.
Easily switch between different small language models for different use cases.
"""

# Available SLM Models for Different Tasks
SLM_MODELS = {
    # Summarization Models (Best for text summarization)
    "summarization": {
        "distilbart": "sshleifer/distilbart-cnn-12-6",  # 60MB, fast, good quality
        "distilbart_large": "facebook/bart-large-cnn-distilled",  # 160MB, better quality
        "pegasus": "google/pegasus-xsum",  # 570MB, excellent for summarization
        "tiny_bart": "facebook/bart-large-cnn",  # Original (not SLM but included for comparison)
    },
    
    # Text Generation Models (For chat/completion tasks)
    "text_generation": {
        "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # 1.1B params, very fast
        "phi3_mini": "microsoft/Phi-3-mini-4k-instruct",  # 3.8B params, good quality
        "dialogpt_small": "microsoft/DialoGPT-small",  # 117M params, ultra-fast
        "distilgpt2": "distilbert/distilgpt2",  # 82M params, very lightweight
    },
    
    # Classification Models (For task categorization)
    "classification": {
        "distilbert": "distilbert-base-uncased",  # 67M params, good for classification
        "tiny_bert": "prajjwal1/bert-tiny",  # 4.4M params, ultra-lightweight
        "mobile_bert": "google/mobilebert-uncased",  # 25M params, mobile-optimized
    }
}

# Default Model Selection
DEFAULT_MODELS = {
    "summarization": "distilbart",  # sshleifer/distilbart-cnn-12-6
    "text_generation": "tinyllama",  # TinyLlama/TinyLlama-1.1B-Chat-v1.0
    "classification": "distilbert",  # distilbert-base-uncased
}

# Model Performance Characteristics
MODEL_SPECS = {
    "sshleifer/distilbart-cnn-12-6": {
        "size": "60MB",
        "parameters": "39M",
        "speed": "Fast",
        "quality": "Good",
        "use_case": "Text summarization",
        "memory_usage": "Low"
    },
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0": {
        "size": "2.2GB",
        "parameters": "1.1B",
        "speed": "Very Fast",
        "quality": "Good",
        "use_case": "Chat and text generation",
        "memory_usage": "Medium"
    },
    "microsoft/Phi-3-mini-4k-instruct": {
        "size": "7.4GB",
        "parameters": "3.8B",
        "speed": "Fast",
        "quality": "Excellent",
        "use_case": "Instruction following, chat",
        "memory_usage": "High"
    },
    "distilbert-base-uncased": {
        "size": "67MB",
        "parameters": "66M",
        "speed": "Very Fast",
        "quality": "Good",
        "use_case": "Classification, feature extraction",
        "memory_usage": "Low"
    }
}

def get_model_name(task_type, model_key=None):
    """
    Get the model name for a specific task type.
    
    Args:
        task_type (str): Type of task ('summarization', 'text_generation', 'classification')
        model_key (str, optional): Specific model key. If None, uses default.
    
    Returns:
        str: Model name for use with transformers pipeline
    """
    if model_key is None:
        model_key = DEFAULT_MODELS.get(task_type, "distilbart")
    
    return SLM_MODELS[task_type][model_key]

def get_model_specs(model_name):
    """
    Get specifications for a model.
    
    Args:
        model_name (str): Full model name
    
    Returns:
        dict: Model specifications
    """
    return MODEL_SPECS.get(model_name, {
        "size": "Unknown",
        "parameters": "Unknown",
        "speed": "Unknown",
        "quality": "Unknown",
        "use_case": "Unknown",
        "memory_usage": "Unknown"
    })

def list_available_models():
    """List all available models by category."""
    print("🤖 Available SLM Models:")
    print("=" * 50)
    
    for category, models in SLM_MODELS.items():
        print(f"\n📋 {category.upper()}:")
        for key, model_name in models.items():
            specs = get_model_specs(model_name)
            print(f"  {key}: {model_name}")
            print(f"    Size: {specs['size']} | Params: {specs['parameters']} | Speed: {specs['speed']}")

if __name__ == "__main__":
    list_available_models()
    
    print(f"\n🔧 Current Default Models:")
    for task, model_key in DEFAULT_MODELS.items():
        model_name = get_model_name(task)
        print(f"  {task}: {model_name}")