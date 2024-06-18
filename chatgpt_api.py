import os
from urllib import response
import openai
import pickle
import time
import argparse
import random
import json
import pandas as pd

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
        
parser = argparse.ArgumentParser(description="A simple script.")
parser.add_argument("-p", "--prog_id", type=int, required=True , help="The progress id")
parser.add_argument("-o", "--operation", type=str, required=True , help="Choose the operation")
parser.add_argument("-fs", "--fewshot", type=str2bool, required=True, help="Use fewshot or not")


args = parser.parse_args()

file_type = 'dev'
file_path = 'path_to_grailQ'
file_name = f'{file_path}xx.json'
wq_file_path = 'path_to_wbq/'
wq_file_name = f'{wq_file_path}xx.json'


openai.api_key = 'xxx'
GPT_MODEL = "xxx"


print(f"USING GPT MODEL: {GPT_MODEL}")
print("Progress ID: %d \n" %progress_id)


def davinci_call(message):
    try:

        completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=message[0]['content'],
        max_tokens = 50,
        temperature=0
        )
        res = completion.choices[0].text
        tokens_num = completion["usage"]["total_tokens"]
        return res


    except openai.error.RateLimitError as e:

        retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
        print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return davinci_call(message)

    except openai.error.ServiceUnavailableError as e:
        retry_time = 10  # Adjust the retry time as needed
        print(f"Service is unavailable. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return davinci_call(message)

    except openai.error.APIError as e:
        retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
        print(f"API error occurred. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return davinci_call(message)

    except OSError as e:
            retry_time = 5  # Adjust the retry time as needed
            print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...")      
            time.sleep(retry_time)
            return davinci_call(message)

def gpt4_3party(message):
    try:
        completion = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages = message,
        temperature = 0
        )
        res = completion.choices[0].message['content']
        tokens_num = completion["usage"]["total_tokens"]
        return res


    except openai.error.RateLimitError as e:

        retry_time = e.retry_after if hasattr(e, 'retry_after') else 5
        print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
        print()
        print('-'*20)
        print("May exceed the quota!!")
        print(openai.api_key)
        print('-'*20)
        print()
        time.sleep(retry_time)
        return gpt4_3party(message)

    except openai.error.ServiceUnavailableError as e:
        retry_time = 10  # Adjust the retry time as needed
        print(f"Service is unavailable. Retrying in {retry_time} seconds...")
        print(openai.api_key)
        time.sleep(retry_time)
        return gpt4_3party(message)

    # except openai.error.APIError as e:
    #     retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
    #     print(f"API error occurred. Retrying in {retry_time} seconds...")
    #     print(openai.api_key)
    #     time.sleep(retry_time)
    #     return gpt4_3party(message)

    except OSError as e:
        retry_time = 5  # Adjust the retry time as needed
        print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...") 
        print(openai.api_key)     
        time.sleep(retry_time)
        return gpt4_3party(message)
    
    except openai.error.Timeout as e:
        retry_time = 5
        print(f"Request timed out. Retrying in {retry_time} seconds...")
        print(openai.api_key)
        time.sleep(retry_time)
        return gpt4_3party(message)

    except openai.error.APIConnectionError as e:
        retry_time = 5
        print(f"Remote end closed connection without response. Retry next API ID...")
        print(openai.api_key)
        time.sleep(retry_time)
        return gpt4_3party(message)
    
    ### check API authentication 
    except openai.error.AuthenticationError as e:
        retry_time = 5
        print(f"API ID {openai.api_key} is unavailable now!!!!. Retry next API ID...")
        time.sleep(retry_time)
        return gpt4_3party(message)


def chatgpt_call(message, count):
    global API_id
    idx = count % len(api_key_list)
    openai.api_key = api_key_list[idx]
    print(f"Calling API NO. {idx}")
    try:

        completion = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages = message,
        temperature = 0
        )
        res = completion.choices[0].message['content']
        tokens_num = completion["usage"]["total_tokens"]
        # print(f"API ID {API_id} works. Try next API ID {API_id+1}...")
        # API_id += 1
        # openai.api_key = api_key_list[API_id]
        return res


    except openai.error.RateLimitError as e:

        retry_time = e.retry_after if hasattr(e, 'retry_after') else 10
        print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
        print()
        print('-'*20)
        print("May exceed the quota!!")
        print(openai.api_key)
        print('-'*20)
        print()
        time.sleep(retry_time)
        return chatgpt_call(message, count+1)

    except openai.error.ServiceUnavailableError as e:
        retry_time = 10  # Adjust the retry time as needed
        print(f"Service is unavailable. Retrying in {retry_time} seconds...")
        print(openai.api_key)
        time.sleep(retry_time)
        return chatgpt_call(message, count+1)

    # except openai.error.APIError as e:
    #     retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
    #     print(f"API error occurred. Retrying in {retry_time} seconds...")
    #     print(openai.api_key)
    #     time.sleep(retry_time)
    #     return chatgpt_call(message, count+1)

    except OSError as e:
        retry_time = 5  # Adjust the retry time as needed
        print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...") 
        print(openai.api_key)     
        time.sleep(retry_time)
        return chatgpt_call(message, count+1)
    
    except openai.error.Timeout as e:
        retry_time = 10
        print(f"Request timed out. Retrying in {retry_time} seconds...")
        print(openai.api_key)
        time.sleep(retry_time)
        return chatgpt_call(message, count+1)

    except openai.error.APIConnectionError as e:
        retry_time = 10
        print(f"Remote end closed connection without response. Retry next API ID...")
        print(openai.api_key)
        time.sleep(retry_time)
        return chatgpt_call(message, count+1)
    
    ### check API authentication 
    except openai.error.AuthenticationError as e:
        print(f"API ID {openai.api_key} is unavailable now!!!!. Retry next API ID...")
        return chatgpt_call(message, count+1)


def kg_to_text():

    with open(file_name, 'r') as fi:
        data = json.load(fi)
    
    ## control the size of kg_to_text
    data_split = data[progress_id * split_num:(progress_id+1)*split_num]
    times = len(data_split) // keys_per_min  + 1
    
    ori_graph = [[], [], [], []]
    for item in data_split:
        ori_graph[0].append(item['pos'])
        ori_graph[1].append(item['neg1'])
        ori_graph[2].append(item['neg2'])
        ori_graph[3].append(item['neg3'])
    
    count = 0
    text_all =[[], [], [], []]
    for idx, certain_graph in enumerate(ori_graph):
        if idx != 3:
            continue
        data_idx = 0
        for one_graph in certain_graph:
            intp = str(one_graph)
            print(f"--{count}--")
            print(intp)
            if one_graph == []:
                gpt_feedback = ''
            else:
                message=[
                    {"role": "system", "content": f'''Your task is to transform a knowledge graph to a sentence or multiple sentences. The knowledge graph is: {intp}. The sentence is: '''}
                ]

                gpt_feedback = chatgpt_call(message, count)
            print(gpt_feedback)

            data_idx += 1
            count += 1
            text_all[idx].append(gpt_feedback)

    print(f'total nums:{count}')
    with open(file_path + str((progress_id+1)*split_num)+'_1_' + file_type + '.json', 'w') as fi:
        json.dump(text_all, fi)

def answer_to_text():
    with open(file_name, 'r') as fi:
        data = json.load(fi)
    
    ## control the size of kg_to_text
    data_split = data[progress_id * split_num:(progress_id+1)*split_num]
    
    qa_pair = [[],[]]
    for item in data_split:
        qa_pair[0].append(item['question'])
        qa_pair[1].append(item['answer'])
    
    count = 0
    results =[]
    for idx, example in enumerate(qa_pair[0]):
        data_idx = 0
        
        question = str(example)
        answer = str(qa_pair[1][idx])
        print(f"--{count}--")
        print(question, answer)
        if question == "" or answer == "":
            gpt_feedback = ''
        else:
            message=[
                {"role": "user", "content": f'''Your task is to transform a question and it's answer to a sentence. The question graph is: {question}, the answer is: {answer}, the sentence is: '''}
            ]
            gpt_feedback = chatgpt_call(message, count)

        data_idx += 1
        count += 1

        gpt_feedback = question + '\t\t\t' + gpt_feedback
        results.append(gpt_feedback)

    print(f'total nums:{count}')
    with open(file_path + "statement_" +str((progress_id+1)*split_num)+'_11' + file_type + '.json', 'w') as fi:
        json.dump(results, fi)
    

def evaluate_final_dev(use_template):
    
    file_path = 'dataset/final_dev.csv' 
    data = pd.read_csv(file_path)


    total = {'Support':0, 'Missing':0, 'Contradictory':0, 'Irrelevant':0}
    acc_num = {'Support':0, 'Missing':0, 'Contradictory':0, 'Irrelevant':0}
    acc_rate = {'Support':0, 'Missing':0, 'Contradictory':0, 'Irrelevant':0}
    pre_gold = {'pred':[], 'gold': []}

    for index, row in data.iterrows():
        print(f'---{index}---')
        question = row['query']
        answer = row['answer']
        reference = row['reference']
        g_label = row['label']
        total[g_label] += 1

        if use_template:
            message=[
                {"role": "user", "content": f'''Your task is to evaluate the relationship between a provided reference and the answer to a specific question. There are four possible types of relationships: \n\n1. Support: Choose this if the reference directly confirms or is fully in alignment with the answer, providing all necessary information to substantiate it. \n2. Missing: Choose this when the reference provides only partial backing for the answer, lacking some essential details or evidence needed for full support. \n3. Contradictory: Choose this option if the reference is consistent with the intent of the question but directly opposes or contradicts the answer. \n4. Irrelevant: Select this option if the reference does not match the intent of the question and contains information that is not useful for answering. \n\nPlease read the examples and choose the most appropriate relationship category for the test example. \n\nExample1:\n Question: what places are in the west?\n Answer: midlands Dudley, Wednesfield, and Aldridge are the places in the West Midlands.\n Reference: Dudley is located in the West Midlands. Wednesfield is located in the West Midlands. Aldridge is located in the West Midlands.\n Relationship Category: Support\n\nExample2:\n Question: the lyrics to beauty and the beast were written by who?\n Answer: Alan Menken wrote the lyrics to Beauty and the Beast.\n Reference: Alan Menken is a music songwriter.\n Relationship Category: Missing\n\nExample3:\n Question: what team does colin kaepernick play for\n Answer: Colin Kaepernick plays for the San Francisco 49ers.\n Reference: Colin Kaepernick played for the Knicks de New York.\n Relationship Category: Contradictory\n\nExample4:\n Question: which measurement system's absorbed dose rate unit is gray per second?\n Answer: The absorbed dose rate unit of gray per second belongs to the International System of Units.\n Reference: The absorbed dose rate is measured in Gray per second and is a type of measurement unit dimension.\n Relationship Category: Irrelevant\n\nTest Example:\n Question: {question}\n  Answer: {answer}\n Reference: {reference}\n Relationship Category: '''}
            ]
        else:
            message=[
            {"role": "user", "content": f'''Your task is to evaluate the relationship between a provided reference and the answer to a specific question. There are four possible types of relationships: \n\n1. Support: Choose this if the reference directly confirms or is fully in alignment with the answer, providing all necessary information to substantiate it. \n2. Missing: Choose this when the reference provides only partial backing for the answer, lacking some essential details or evidence needed for full support. \n3. Contradictory: Choose this option if the reference is consistent with the intent of the question but directly opposes or contradicts the answer. \n4. Irrelevant: Select this option if the reference does not match the intent of the question and contains information that is not useful for answering. \n\nFor each of the examples provided: \n\nYou will review the given question and the provided answer. \nYou will compare them to the content of the reference text. \nYou will then select the appropriate relationship category based on whether the reference supports, is missing information, contradicts, or is irrelevant to the answer.\n\nExample:\n\nQuestion: {question}\nAnswer: {answer}\nReference: {reference}\nRelationship Category: '''}
        ]
        gpt_feedback = gpt4_3party(message)

        if g_label.lower() in gpt_feedback.lower():
            acc_num[g_label] += 1
        
        for k,v in acc_num.items():
            if total[k] != 0:
                acc_rate[k] = round(100*v / total[k],2)
        print('A: ', acc_num)
        print('G:', total)
        print('Acc:', acc_rate)


        pre_gold['gold'].append(g_label)
        pre_gold['pred'].append(gpt_feedback)

    with open("results/chatgpt/final" + file_type + GPT_MODEL + "new", 'w') as w_file:
        w_file.write(str(pre_gold))

def evaluate_final2classes_dev(use_template):
    
    file_path = 'dataset/final_dev.csv' 
    data = pd.read_csv(file_path)


    total = {'Supportive':0, 'Unsupported':0}
    acc_num = {'Supportive':0, 'Unsupported':0}
    acc_rate = {'Supportive':0, 'Unsupported':0}
    pre_gold = {'pred':[], 'gold': []}

    for index, row in data.iterrows():
        print(f'---{index}---')
        question = row['query']
        answer = row['answer']
        reference = row['reference']
        g_label = row['label']
        if g_label in ['Missing', 'Contradictory', 'Irrelevant']:
            g_label = 'Unsupported'
        if g_label == 'Support':
            g_label = 'Supportive'
        total[g_label] += 1

        if use_template:
            message=[

            ]
        else:
            message=[
            {"role": "user", "content": f'''Your task is to evaluate the relationship between a provided reference and the answer to a specific question. There are four possible types of relationships: \n\n1. Supportive: Choose this if the reference directly confirms or is fully in alignment with the answer, providing all necessary information to substantiate it. \n2. Unsupported: Choose this when the reference does not confirm or align with the answer, lacking the necessary information or contradicting it.  \n\nFor each of the examples provided: \n\nYou will review the given question and the provided answer. \nYou will compare them to the content of the reference text. \nYou will then select the appropriate relationship category based on whether the reference supportive or unsupported to the answer.\n\nExample:\n\nQuestion: {question}\nAnswer: {answer}\nReference: {reference}\nRelationship Category: '''}
        ]
        gpt_feedback = gpt4_3party(message)
        if g_label.lower() in gpt_feedback.lower():
            acc_num[g_label] += 1
        
        for k,v in acc_num.items():
            if total[k] != 0:
                acc_rate[k] = round(100*v / total[k],2)
        print('A: ', acc_num)
        print('G:', total)
        print('Acc:', acc_rate)


        pre_gold['gold'].append(g_label)
        pre_gold['pred'].append(gpt_feedback)

    with open("results/chatgpt/2classesfinal" + file_type + GPT_MODEL, 'w') as w_file:
        w_file.write(str(pre_gold))


def evaluate():
    # return None
    with open(file_path + str((progress_id+1)*split_num)+'_' + file_type + '.json', 'r') as fi:
        data = json.load(fi)
    
    with open(file_path + "statement_" +str((progress_id+1)*split_num)+'_' + file_type + '.json', 'r') as fi:
        statements = json.load(fi)


    total_count = 0
    results = [[], [], [], []]
    for _id, item in enumerate(data[0]):
        state = statements[_id]
        question = state.split("\t\t\t")[0]
        answer = state.split("\t\t\t")[1]
        neg1 = data[1][_id]
        neg2 = data[2][_id]
        neg3 = data[3][_id]
        for idx in range(4):
            reference = data[idx][_id]
            if reference == "":
                gpt_feedback = None
            else:
                message=[
                    {"role": "user", "content": f'''Your task is to evaluate the relationship between a provided reference and the answer to a specific question. There are four possible types of relationships: \n\n1. Support: Choose this if the reference directly confirms or is fully in alignment with the answer, providing all necessary information to substantiate it. \n2. Missing: Choose this when the reference provides only partial backing for the answer, lacking some essential details or evidence needed for full support. \n3. Contradictory: Choose this option if the reference is consistent with the intent of the question but directly opposes or contradicts the answer. \n4. Irrelevant: Select this option if the reference does not match the intent of the question and contains information that is not useful for answering. \n\nFor each of the examples provided: \n\nYou will review the given question and the provided answer. \nYou will compare them to the content of the reference text. \nYou will then select the appropriate relationship category based on whether the reference supports, is missing information, contradicts, or is irrelevant to the answer.\n\nExample:\n\nQuestion: {question}\nAnswer: {answer}\nReference: {reference}\nRelationship Category: '''}
                ]
                gpt_feedback = chatgpt_call(message, total_count)

            results[idx].append(gpt_feedback)
            total_count += 1

    w_file = open(file_path + "results/" +str((progress_id+1)*split_num)+'_' + file_type + '.pkl', 'wb')
    pickle.dump(results, w_file)


def main():

    file_type = 'dev' # train or dev
    s_time = time.time()

    ### FOR attributable
    if args.operation == "kg_to_text":
        kg_to_text()
    elif args.operation == "answer_to_text":
        answer_to_text()
    elif args.operation == "evaluate":
        evaluate()
    elif args.operation == "evaluate_final_dev":
        evaluate_final_dev(args.fewshot)

    elif args.operation == "evaluate_final2classes_dev":
        evaluate_final2classes_dev(args.fewshot)

    print('-'*10)
    print('Time cost: ', time.time()-s_time)

if __name__ == '__main__':
    main()
