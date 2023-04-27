# Executive Summary Generator

This script takes a text file as input and generates an executive summary using OpenAI's GPT-3 language model.

# Installation
Clone this repository.  
Install the required packages: `pip install -r requirements.txt`  
Create a free OpenAI account and get an API key.  
Set the OPENAI_KEY environment variable to your API key. 

# Usage
Run the script with the filename of the input text file as an argument. For example:

`python summary_generator.py input_file.txt`

The script will generate an executive summary and save it to a new file with the name input_file_summary.


# Options
You can customize the behavior of the script by modifying the following parameters in the gpt3_completion function:

engine: the ID of the GPT-3 engine to use (default: text-davinci-003)  
temp: the temperature parameter of the GPT-3 model (default: 0.5)  
top_p: the top-p parameter of the GPT-3 model (default: 1.0)  
tokens: the maximum number of tokens to generate (default: 2500)  
freq_pen: the frequency penalty parameter of the GPT-3 model (default: 0.2)  
pres_pen: the presence penalty parameter of the GPT-3 model (default: 0)  

You can also change the summary_prompt.txt and exec_summary_prompt.txt files to modify the prompt templates.

# To Do

I plan to add the ability to change the length of the final summary as well as how the summaries are constructed
as the length of the total remaining text changes. I have some ideas!

# License
This project is licensed under the MIT License. See the LICENSE file for details.