from langchain_google_genai import ChatGoogleGenerativeAI
import os



GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def get_model():
    """
    Initialize and return a Google Generative AI model instance.

    Returns:
        ChatGoogleGenerativeAI: Configured model instance
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        temperature=0.7,
        max_output_tokens=1024,
        top_p=0.95,
        top_k=40
    )
    return llm

def is_query_harmful(query, model):
    """
    Check if a query is harmful using the specified model.

    Args:
        query (str): The query to check
        model (ChatGoogleGenerativeAI): The model instance to use for checking

    Returns:
        bool: True if the query is harmful, False otherwise
    """
    query_to_check = f"""
    You are a safety classifier. Your task is to determine if a given query is harmful or
    unsafe. A query is considered harmful if it promotes violence, hate speech, self-harm,
    illegal activities, or any other form of unsafe content. Please respond with "harmful"
    if the query is harmful, and "safe" if it is not.

    Here is the query you need to evaluate:
    {query}
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite-preview-06-17",
        temperature=0.0,
        max_output_tokens=56,
        top_p=0.95,
        top_k=40
    )

    response = model.invoke(query_to_check)
    print(f"Safety check response: {response}")
    if "harmful" in response.content.lower():
        return True
    if "safe" in response.content.lower():
        return False
    
    return False


def check_model_availability():
    """
    Check if the Google Generative AI model is available.

    Returns:
        bool: True if the model is available, False otherwise
    """
    try:
        model = get_model()
        # Perform a simple invocation to check availability
        respone = model.invoke("Test availability")
        print(f"Model is available: {respone}")
        return respone
    except Exception as e:
        print(f"Model availability check failed: {e}")
        return False
    

# if __name__ == "__main__":
    # check_model_availability()