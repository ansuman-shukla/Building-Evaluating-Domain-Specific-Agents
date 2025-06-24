"""
Utility functions for the domain-specific agent evaluation system.
This module provides helper functions for data processing and analysis.
"""

import json
import os
from typing import Dict, List, Any, Union
from statistics import mean
from langchain_google_genai import ChatGoogleGenerativeAI

def load_json(file_path: str) -> Union[Dict, List]:
    """
    Load JSON data from a file.
    
    Args:
        file_path (str): Path to the JSON file
    
    Returns:
        Union[Dict, List]: Loaded JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return []

def save_json(data: Union[Dict, List], file_path: str, indent: int = 2):
    """
    Save data to a JSON file.
    
    Args:
        data (Union[Dict, List]): Data to save
        file_path (str): Path to save the JSON file
        indent (int): JSON indentation level
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent, ensure_ascii=False)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving JSON to {file_path}: {e}")

def check_final_answer(genrated_response: str , actual_respons: str) -> bool:
    """
    Check if the response contains a final answer.
    
    Args:
        response (str): The agent's response
    
    Returns:
        bool: True if a final answer is present, False otherwise
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        temperature=0.0,
        max_output_tokens=56,
        top_p=0.95,
        top_k=40
    )

    query = f"""
    You are a final answer classifier. Your task is to determine if a genrated response matches Actual answer.
    A response is considered correct if it contains the Actual answer. Please respond with "correct" if the response contains a final answer,
    and "wrong" if it does not contain the Actual answer.
    
    genrated response:
    {genrated_response} 

    Actual answer:
    {actual_respons}
    """

    print(f"Final answer check query: {query}")
    response = llm.invoke(query)

    if not response:
        print("No response received from the model.")
        return False
    print(f"Final answer check response: {response.content}")

    
    if response.content == "correct":
        return True
    
    
    return False