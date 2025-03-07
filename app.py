
import pandas as pd
import gencode
import readfile
from datetime import datetime

from flask import Flask, request, send_file
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')
from execute_gen_code import execute_code
from utility import read_code_from_file

app = Flask(__name__)
CORS(app)

MAX_GEN_RETRY=3



@app.route('/gencode/', methods=['GET', 'POST'])
def prompt_process():
   

    sql_prompt = request.args.get('prompt')
    reponse_type = 'text'
    success_run=False

    seed=datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    print (f'seed generated================ {seed}')
    #seed=100
    if (not reponse_type): reponse_type='text'
    if (  sql_prompt ):
        for x in range(MAX_GEN_RETRY):

            try:
                generated_code=gencode.nl_python_gemini (sql_prompt,seed)
                if "plt.savefig" in generated_code:
                    print("plt.savefig found")
                    reponse_type='image'
                else:
                     reponse_type='text'
                #generated_code= read_code_from_file()
                execute_code(generated_code)
                success_run=True
                break

            except Exception as e:
                print(f"An error occurred: {e}" ) 
                continue
                
        if success_run :
            if reponse_type.lower() =='image':
                image_path = f'graph_{seed}.png'  # Replace with the path to your PNG file
                try:
                    print(f'Sending back contents of file {image_path}')
                    return send_file(image_path, mimetype='image/png')
                     #return image_path
                     #return image_path
                except Exception as e:
                    return str(e), 404  # Return a 404 not found if there's any error

            else:
                #Read from gencode.log and return
                file_path=f'gencode_{seed}.log'
                print(f'Sending back contents of file {file_path}')
                return readfile.read_file_content(file_path)
        else:
            return ("Could not generate code to run your query")
      
    else:
       return("No prompt given. Please provide prompt as argument")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
