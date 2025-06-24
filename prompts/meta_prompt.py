"""
Meta-prompting implementation for domain-specific agents.
This module provides utilities for meta-prompting and prompt optimization.
"""

def meta_prompt(task_description, agent_capabilities, context=""):
    """
    Generate a meta-prompt that instructs the agent on how to approach the task.
    
    Args:
        task_description (str): Description of the task to be performed
        agent_capabilities (list): List of agent's known capabilities
        context (str): Additional context for the task
    
    Returns:
        str: Formatted meta-prompt
    """
    capabilities_str = ", ".join(agent_capabilities)
    
    prompt = f"""
    You are an AI agent with the following capabilities: {capabilities_str}
    
    Task: {task_description}
    Context: {context}
    
    Before solving this task, please:
    1. Analyze which of your capabilities are most relevant
    2. Determine the best approach strategy
    3. Identify potential challenges and how to address them
    4. Plan your response structure
    
    Then proceed with solving the task using your planned approach.
    """
    
    return prompt.strip()

def optimize_prompt(base_prompt, performance_feedback):
    """
    Optimize a prompt based on performance feedback.
    
    Args:
        base_prompt (str): Original prompt
        performance_feedback (dict): Feedback on prompt performance
    
    Returns:
        str: Optimized prompt
    """
    optimizations = []
    
    if performance_feedback.get("clarity_score", 0) < 0.7:
        optimizations.append("Make instructions more explicit and clear")
    
    if performance_feedback.get("completeness_score", 0) < 0.7:
        optimizations.append("Add more context and examples")
    
    if performance_feedback.get("accuracy_score", 0) < 0.7:
        optimizations.append("Include more specific constraints and guidelines")
    
    if optimizations:
        optimization_instructions = "; ".join(optimizations)
        optimized_prompt = f"""
        {base_prompt}
        
        Additional Instructions: {optimization_instructions}
        """
        return optimized_prompt.strip()
    
    return base_prompt

def generate_prompt_variants(base_prompt, num_variants=3):
    """
    Generate multiple variants of a prompt for A/B testing.
    
    Args:
        base_prompt (str): Original prompt
        num_variants (int): Number of variants to generate
    
    Returns:
        list: List of prompt variants
    """
    variants = [base_prompt]  # Include original
    
    # Variant 1: More structured
    structured_variant = f"""
    TASK ANALYSIS:
    {base_prompt}
    
    APPROACH:
    Please follow these steps:
    1. Read and understand the task
    2. Plan your solution
    3. Execute the plan
    4. Verify your answer
    """
    variants.append(structured_variant)
    
    # Variant 2: More conversational
    conversational_variant = f"""
    Let's work on this together:
    
    {base_prompt}
    
    Take your time and think through this carefully. I'm here to help if you need clarification.
    """
    variants.append(conversational_variant)
    
    # Variant 3: More direct
    if num_variants > 3:
        direct_variant = f"TASK: {base_prompt}\n\nSOLUTION:"
        variants.append(direct_variant)
    
    return variants[:num_variants + 1]
