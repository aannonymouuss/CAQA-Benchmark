# CAQA Benchmark
Code, datasets for the paper ```Can LLMs Evaluate Complex Attribution in QA? Automatic Benchmarking Using Knowledge Graphs```

## Evironment
Docker pull huggingface/transformers-pytorch-gpu:4.35.2

## Dataset
All datasets are in the dataset folder, including CAQA_train.csv, CAQA_dev.csv and ALCE_finegrained.csv.

### Fine-tuning LLMs
Run sh train.sh

Evaluate the fine-tuned LLM by running sh inferce.sh

### Zero/Few-shot LLMs
You can run sh inferce.sh to directly evaluate small LLMs. 
Modify the prompt_type parameter to select zero-shot or few-shot settings.

Also, you can run run_chatgpt.sh to select ChatGPT-3.5 or ChatGPT-4 as the attribution evaluator. The parameter -fs (True or False) is used to control the use of zero-shot or few-shot settings.
