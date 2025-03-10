import os
import time
import anthropic

def parse_triple_quotes(in_str, parse_str="```python"):
    """Extracts code from triple backticks"""
    
    parts = in_str.split(parse_str)
    if len(parts) < 2:
        print(f"Error: '{parse_str}' not found in input string.")
        return ""

    code_part = parts[1]

    code_part = code_part.split("```")[0]

    return code_part.strip()

def nl_python_gemini(user_prompt, seed):
    api_key = os.getenv("CLAUDE_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    print(f'SEED SENT TO PROMPT ==============={seed}')
    prompt =  f"""
        
             First you rephrase the user input so that a Python code generator can understand it.
            
            Generate python code to answer the user input based on service_contracts_survey_data.csv file which has the columns: 
            
                ID
                Name
                Contact Number
                Email
                Year
                Make
                Model
                City
                State
                Zip Code
                Feedback
                How did you hear about our vehicle extended service contracts?
                How easy was it to purchase your extended service contract?
                How satisfied are you with the coverage options provided?
                Rate the clarity of information provided regarding what is and isnt covered under your service contract.
                Have you had to use your extended service contract for vehicle repairs?
                How easy was it to file a claim under your extended service contract?
                How satisfied were you with the speed of claim processing?
                Rate the quality of repair service received.
                How would you rate the customer service you received?
                How likely are you to renew your extended service contract?
                How likely are you to recommend our extended service contracts to others?
                How would you rate your experience with our self-care web and mobile app in managing your extended service contract?
                What features or functionalities would you like to see improved or added to our self-care web and mobile app?
                What aspects of our service and contract options can be improved?
            
            Include the question mark if present in the column name while generating dataframe.
            Do not use underscore to separate words in datframe column name. Keep original name with spaces
            use pandas read_csv and pass file to read the file content.
            If the user asks you to plot a graph or "plot" is there in the user_prompt, then only generate graph, use matplotlib,   get the data you need for it, do not use figure function,generate and save the image as graph_{seed}.png.
            Adjust graph so that all values are seen. The image size should be adjusted so that every metrics is visible to the user. 

            Use plt.close() at the end to close.
            Put print debug statements after each line to show the progress of the code.
            Do not use print statement but write the output to a new file gencode_{seed}.log instead. 
            If there is graphical output , do not write to the gencode_{seed}.log
            Do not use dropna
            For any question that asks for statistics on positive or negative,happy or unhappy, use the textblob python library to compute sentiment polarity and do not filter on exact word. Do not use sklearn.
            For any question that asks for summary, import helper_to_gencode.py and call the function helper_to_gencode.call_gemini passing the text to summarize as input. The function returns the summarized text.
        
            Only use the output of your code to answer the question.
            You might know the answer without running any code, but you should still run the code to get the answer.Use this to chat with the user regarding customer survey data.
            Saves logs inside a 'logs/' directory (create it if it doesn't exist).
            Before reading the log file, add a 0.5-second delay to ensure the file is available.
            Do not print debug statements.
            Only log the final summary to `logs/gencode_{seed}.log`, not intermediate steps.
            Output Rules:  
          - If a summary is requested, write only the final summarized insights to `logs/gencode_{seed}.log`, rather than graphs.  
          - Avoid step-by-step process logs.  
          - For an overall view, return a complete summary rather than the steps taken to generate it. 
          If the user asks for a summary, DO NOT generate any graphs, visualizations, or matplotlib code.  
Summarization requests must **ONLY** call `helper_to_gencode.call_gemini` and store the final summarized insights in `logs/gencode_{seed}.log`.  

      For summarization requests:  
      - **NEVER** include `matplotlib.pyplot`, `plt.savefig()`, or any visualization libraries.  
      - **ONLY** extract relevant text from the dataset, call `helper_to_gencode.call_gemini()`, and log the final summary.  
      - **DO NOT** generate, save, or reference any `.png` file.  

      Any request containing "summarize", "summary", "give an overview", or similar **must follow this rule strictly**.
 
            
            Summarization requests should **not** contain debugging logs or intermediate steps, only the final insights and the final summary should be saved under logs/directory mandatorily, from there summary should be read.

            Your generated code MUST follow this template structure:

        def generated_code():
            # 1. First create logs directory
            os.makedirs('logs', exist_ok=True)
            
            # 2. Read the CSV data
            df = pd.read_csv('service_contracts_survey_data.csv')
            
            # 3. Process the data based on user request
            # [Your processing code here]
            
            # 4. Save results to logs directory
            log_file = f'logs/gencode_{seed}.log'
            with open(log_file, 'w') as f:
                f.write(results)
 

            Wrap the generated code in a function named  generated_code(), create a file  named gemini_generated_code.py and put the function along with code in that file. Do not call the function.
            Call the generated_code function. do not use if __name__ == "__main__"

            IMPORTANT DECISION RULES - READ THESE CAREFULLY:

1. IF AND ONLY IF the user asks to "plot" or "generate" something or mentions "graph" or "visualize":
   - Generate matplotlib code
   - Save the output as graph_{seed}.png
   - DO NOT write to logs in this case

2. FOR ALL OTHER QUERIES, INCLUDING SUMMARIES:
   - DO NOT generate any matplotlib code or plots
   - ALWAYS create the logs directory with: os.makedirs('logs', exist_ok=True)
   - ALWAYS save output ONLY to logs/gencode_{seed}.log

These rules are mutually exclusive - never mix graphing and logging to files in the same response.

For summary requests or any non-visualization query:
- import os
- os.makedirs('logs', exist_ok=True)  # This line is mandatory
- process data as needed
- write results ONLY to logs/gencode_{seed}.log
- NEVER include plt, matplotlib, or any visualization code

Your code must follow this exact structure:

def generated_code():
    import os
    import pandas as pd
    from textblob import TextBlob
    
    # Always create logs directory first
    os.makedirs('logs', exist_ok=True)
    
    # Read the data
    df = pd.read_csv('service_contracts_survey_data.csv')
    
    # Determine if this is a plotting request or a summary/analysis request
    if "plot" in user_prompt or "graph" in user_prompt or "visualize" in user_prompt:
        # PLOTTING CODE PATH
        import matplotlib.pyplot as plt
        # [Your plotting code here]
        plt.savefig(f'graph_{seed}.png')
        plt.close()
    else:
        # NON-PLOTTING CODE PATH - ALWAYS WRITE TO LOG FILE
        # [Your analysis code here]
        result = "Your analysis results here"
        
        # Write to log file - THIS IS MANDATORY FOR NON-PLOTTING REQUESTS
        log_file = f'logs/gencode_{seed}.log'
        with open(log_file, 'w') as f:
            f.write(result)
            
    """

    response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    generated_code = "".join([msg.text for msg in response.content])

    if "```python" in generated_code:
        generated_code = generated_code.split("```python")[1].split("```")[0].strip()
    elif "```" in generated_code:
        generated_code = generated_code.split("```")[1].split("```")[0].strip()

    output_dir = "claude_code"
    os.makedirs(output_dir, exist_ok=True)

    # 🔹 Save the extracted code to a file
    file_path = os.path.join(output_dir, f'claude_generated_code_{seed}.py')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(generated_code)

    print(f"Generated code saved to {file_path}")

    try:
        exec(generated_code, globals())
    except Exception as e:
        print(f"Error executing generated code: {e}")

    return generated_code