"""
Chain-of-Thought (CoT) prompting implementation for domain-specific agents.
This module provides utilities for CoT reasoning approaches.
"""
import sys
import os

# Add the parent directory to the Python path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import *
from src.model import *


def cot_prompt(task_description, context="", include_reasoning=True):
    """
    Generate a Chain-of-Thought prompt for the given task.
    
    Args:
        task_description (str): Description of the task to be performed
        context (str): Additional context for the task
        include_reasoning (bool): Whether to include reasoning steps
    
    Returns:
        str: Formatted CoT prompt
    """
    prompt = f"""
    Task: {task_description}
    
    Context: {context}
    """
    
    if include_reasoning:
        prompt += """
    
    Please solve this step by step:
    1. First, analyze the problem
    2. Break it down into smaller components
    3. Solve each component
    4. Combine the solutions
    5. Provide the final answer
    
    Let's work through this step by step:
    """
    
    return prompt.strip()


def evaluate_cot_response(response, expected_output=None):
    """
    Evaluate the quality of a Chain-of-Thought response.
    
    Args:
        response (str): The agent's CoT response
        expected_output (str): Expected output for comparison
    
    Returns:
        dict: Evaluation metrics
    """
    
    metrics = {
        "length": len(response),
        "has_final_answer": bool(response.strip()),
        "matches_expected": check_final_answer(response, expected_output) if expected_output else None,
    }
    return metrics


def use_cot_prompt():
    file_path = "evaluation/input_queries.json"
    queries = load_json(file_path)
    model = get_model()
    responses = []
    
    for query in queries:
        task_description = query.get("input", "")
        context = query.get("context", "") 
        expected_output = query.get("expected_output", None)
        
        # Generate CoT prompt
        prompt = cot_prompt(task_description, context)
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


    evaluation_results = []
    for item in responses:
        response = item["response"]
        expected_output = item["expected_output"]
        task_description = item["task_description"]
        metrics = evaluate_cot_response(response, expected_output)
        evaluation_results.append({
            'task_description': task_description,
            "response": response,  
            "expected_output": expected_output,
            "metrics": metrics
        })    # Save evaluation results
    output_file = "evaluation/cot_evaluation_results.json"
    save_json(evaluation_results, output_file)
    
    print(f"Evaluation completed. Results saved to {output_file}")
    return evaluation_results
        



if __name__ == "__main__":
    use_cot_prompt()