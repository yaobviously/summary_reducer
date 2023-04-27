# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 14:38:56 2023

@author: yaobv
"""

import os
import sys
import openai
import re
import textwrap

from time import time, sleep
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get('OPENAI_KEY')

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
    
def gpt3_completion(prompt, engine='text-davinci-003', temp=0.5, top_p=1.0, 
                    tokens=2500, freq_pen=0.2, pres_pen=0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            with open('summary_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            print("some sort of error")
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)
 

def process_paragraphs(paragraphs=None):

    paragraphs = paragraphs

    while len(paragraphs) > 1:

        new_paragraphs = []

        for i in range(0, len(paragraphs) - 1, 3):
            print(i)
            if i + 3 < len(paragraphs):
                prompt_text = '\n'.join(paragraphs[i:i+3])
                prompt = open_file('summary_prompt.txt').replace(
                    '<<SUMMARY>>', prompt_text)
                prompt = prompt.encode(
                    encoding='ASCII', errors='ignore').decode()
                summary_ = gpt3_completion(prompt)
                new_paragraphs.append(summary_)
            else:
                prompt_text = '\n'.join(paragraphs[i:])
                prompt = open_file('exec_summary_prompt.txt').replace(
                    '<<SUMMARY>>', prompt_text)
                prompt = prompt.encode(
                    encoding='ASCII', errors='ignore').decode()
                summary_ = gpt3_completion(prompt)
                new_paragraphs.append(summary_)

        paragraphs = new_paragraphs

    return paragraphs[0]


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Please provide the filename as an argument")
        sys.exit()

    filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            print(text)
    except FileNotFoundError:
        print(f"File '{filename}' not found")

    
    paragraphs = text.split('\n')
    
    if len(paragraphs) < 10 or len(paragraphs) > 50:
        paragraphs = textwrap.wrap(text, 2500)

    final_summary = process_paragraphs(paragraphs=paragraphs)
    save_file(final_summary, f'{filename}_summary')