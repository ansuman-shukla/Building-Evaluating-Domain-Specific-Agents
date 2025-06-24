"""
Few-shot prompting implementation for domain-specific agents.
This module provides utilities for few-shot learning approaches.
"""
import sys
import os

# Add the parent directory to the Python path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import *
from src.model import *

def few_shot_prompt(task_description, examples, context=""):
    """
    Generate a few-shot prompt with examples for the given task.
    
    Args:
        task_description (str): Description of the task to be performed
        examples (list): List of example input-output pairs
        context (str): Additional context for the task
    
    Returns:
        str: Formatted few-shot prompt
    """
    prompt = f"Task: {task_description}\n\nContext: {context}\n\nExamples:\n"
    
    for i, example in enumerate(examples, 1):
        prompt += f"\nExample {i}:\n"
        prompt += f"Input: {example.get('input', '')}\n"
        prompt += f"Output: {example.get('output', '')}\n"
    
    prompt += "\nNow, please solve the following:\nInput: "
    return prompt

def create_example(input_text, output_text):
    """
    Create an example dictionary for few-shot prompting.
    
    Args:
        input_text (str): Example input
        output_text (str): Example output
    
    Returns:
        dict: Example dictionary
    """
    return {"input": input_text, "output": output_text}

def evaluate_few_shot_response(response, examples, expected_output=None):
    """
    Evaluate the quality of a few-shot response.
    
    Args:
        response (str): The agent's response
        examples (list): Examples used in the prompt
        expected_output (str): Expected output for comparison
    
    Returns:
        dict: Evaluation metrics
    """
    metrics = {
        "length": len(response),
        "has_solution": bool(response.strip()),
        "num_examples_used": len(examples),
        "matches_expected": response == expected_output if expected_output else None
    }
    return metrics
