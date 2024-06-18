# CAQA Benchmark
Code, datasets for the paper ```Can LLMs Evaluate Complex Attribution in QA? Automatic Benchmarking Using Knowledge Graphs```

## Evironment
```docker pull huggingface/transformers-pytorch-gpu:4.35.2```

## Dataset
Download the data, including CAQA_train.csv, CAQA_dev.csv and ALCE_finegrained.csv,  from `https://drive.google.com/file/d/12o3bUJw-W9IW-pDT8KZUHxmusssFKg4t/view?usp=drive_link`
Unzip this file and put it in folder ```data```

### Fine-tuning LLMs
Run ```sh train.sh```

Evaluate the fine-tuned LLM by running ```sh inferce.sh```

### Zero/Few-shot LLMs
You can run ```sh inferce.sh``` to directly evaluate small LLMs. 
Modify the prompt_type parameter to select zero-shot or few-shot settings.

Also, you can run ```sh run_chatgpt.sh``` to select ChatGPT-3.5 or ChatGPT-4 as the attribution evaluator. The parameter ```-fs (True or False)``` is used to control the use of zero-shot or few-shot settings.

## Issues
If you have any questions, please leave a issue and we will respond as soon as possible.
