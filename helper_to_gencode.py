import os
import google.generativeai as genai
import pandas as pd
safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    }
]

def call_gemini(text_input):
    api_key=os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)  # Configure the API key for all subsequent calls.

    #Convert series or list to string
    if isinstance(text_input, pd.Series) or isinstance(text_input, list) :
        text_input = ''.join(text_input)
   

    models = genai.GenerativeModel('gemini-1.5-pro')
    response = models.generate_content(   "Summarize the text :  "  + text_input,
                                          generation_config=genai.types.GenerationConfig(temperature=0.0)
                                     , safety_settings = safety_settings )
    return(response.text)