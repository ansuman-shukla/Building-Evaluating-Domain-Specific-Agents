"""
Zero-shot prompting implementation for domain-specific agents.
This module provides utilities for zero-shot learning approaches.
"""

import sys
import os

# Add the parent directory to the Python path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import *
from src.model import *

def zero_shot_prompt(task_description, context=""):
    """
    Generate a zero-shot prompt for the given task.
    
    Args:
        task_description (str): Description of the task to be performed
        context (str): Additional context for the task
    
    Returns:
        str: Formatted zero-shot prompt
    """
    prompt = f"""
    Task: {task_description}
    
    Context: {context}
    
    Please provide a solution based on your understanding without any examples. In the end just return the final answer in integers.

    """
    return prompt.strip()

def evaluate_zero_shot_response(response, expected_output):
    """
    Evaluate the quality of a zero-shot response.
    
    Args:
        response (str): The agent's response
        expected_output (str): Expected output for comparison
    
    Returns:
        dict: Evaluation metrics
    """
    metrics = {
        "length": len(response),
        "matches_expected": check_final_answer(response, expected_output) if expected_output else None,
    }
    return metrics


def evaluate_zero_shot():
    """
    Evaluate the quality of a zero-shot prompt and response.
    
    Returns:
        dict: Evaluation metrics
    """
    file_path = "evaluation/input_queries.json"
    queries = load_json(file_path)
    model = get_model()
    responses = []
    
    for query in queries:
        task_description = query.get("input", "")
        context = query.get("context", "") 
        expected_output = query.get("expected_output", None)
        
        # Generate zero-shot prompt
        prompt = zero_shot_prompt(task_description, context)

        if is_query_harmful(prompt, model):
            print(f"Query is harmful, skipping: {task_description}")
            continue
        else:
            print(f"Query is safe, processing: {task_description} ")
            
            try:
                response = model.invoke(prompt)
                responses.append({
                    "task_description": task_description,
                    "response": response.content,  # Extract content from AIMessage
                    "expected_output": expected_output
                })
            except Exception as e:
                print(f"Error generating response for task: {task_description}, Error: {e}")
                continue

    # Evaluate responses
    evaluation_results = []
    for item in responses:
        response = item["response"]
        expected_output = item["expected_output"]
        task_description = item["task_description"]
        metrics = evaluate_zero_shot_response(response, expected_output)
        evaluation_results.append({
            'task_description': task_description,
            "response": response,  
            "expected_output": expected_output,
            "metrics": metrics
        })    # Save evaluation results
    output_file = "evaluation/zero_shot_evaluation_results.json"
    save_json(evaluation_results, output_file)
    
    print(f"Evaluation completed. Results saved to {output_file}")
    return evaluation_results


if __name__ == "__main__":
    evaluate_zero_shot()

