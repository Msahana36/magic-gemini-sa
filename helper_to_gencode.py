import os
import anthropic
import pandas as pd

def call_gemini(text_input):
    """ Calls Claude AI to generate a concise summary. """
    
    os.makedirs('logs', exist_ok=True)
    
    api_key = os.getenv("CLAUDE_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    if isinstance(text_input, pd.Series):
        text_input = ' '.join([str(item) for item in text_input if pd.notna(item)])
    elif isinstance(text_input, list):
        text_input = ' '.join([str(item) for item in text_input if item is not None])
    
    text_input = str(text_input)

    prompt = f"""
    Summarize the following text into a concise, meaningful response, without listing step-by-step processing details. 
    Do NOT include individual sentiment scores or debugging messages. Only return a well-structured summary:

    "{text_input}"
    """

    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    if isinstance(response.content, list) and len(response.content) > 0:
        summary = response.content[0].text
    else:
        summary = str(response.content)
        
    return summary