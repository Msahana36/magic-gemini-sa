import google.generativeai as genai
import os
import utility


def parse_triple_quotes(in_str, parse_str):
# Parse out the string after ```sql and before ```
  # Using Python's string manipulation methods to extract the SQL query
  #start = in_str.find("```python") + len("```python\n")  # Start after ```sql and the newline
  start = in_str.find(parse_str) + len(parse_str+"\n")
  end = in_str.rfind("```")  # Find the last occurrence of ```
  out_str = in_str[start:end].strip()  # Extract the SQL query and strip leading/trailing whitespace
  print(f'OUTPUT STRING\n{out_str}')
  return out_str





def nl_python_gemini(user_prompt, seed):
 
 
    api_key=os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)  # Configure the API key for all subsequent calls.
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
            Wrap the generated code in a function named  generated_code(), create a file  named gemini_generated_code.py and put the function along with code in that file. Do not call the function.
            Call the generated_code function. do not use if __name__ == "__main__"
            
    """
   
    #  For any question that asks for summary , use textblob python library but convert series using str.cat to string before using it.
    #Wrap the generated code in a function named  generated_code(), create a file  named gemini_generated_code.py and put the function along with code in that file
    # Convert series using str.cat to string before using it.    
          
#gemini-pro is not working in v1beta version(deprecated)
    models = genai.GenerativeModel('gemini-1.5-pro')
    response = models.generate_content(   prompt + "\n\n Generate python code for : " + user_prompt,
                                          generation_config=genai.types.GenerationConfig(temperature=0.0)
                                      )
    generated_code = response.text
  ####
    #print(f'GENERATED CODE >>>\n {generated_code}')
    if ( generated_code.find("```python") != -1   ) :
        generated_code=parse_triple_quotes(generated_code,"```python")
    else:
        if ( generated_code.find("```") != -1   ) :
            generated_code=parse_triple_quotes(generated_code,"```")
    
    #print(f'Cleaned up code >>>>>>>>>>>>>>>>>>> \n{generated_code}')
    
    #utility.write_code_to_file(generated_code)
    #print(f'WRITTEN CODE TO FILE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    return generated_code

  

    
