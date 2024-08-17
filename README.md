# CAQA Benchmark
Code, datasets for the paper ```Can LLMs Evaluate Complex Attribution in QA? Automatic Benchmarking Using Knowledge Graphs```

### News: Adding a scholarly domain attributed QA benchmark

## Evironment
```docker pull huggingface/transformers-pytorch-gpu:4.35.2```

## Dataset
Download the data, including CAQA_train.csv, CAQA_dev.csv and ALCE_finegrained.csv,  from `https://drive.google.com/file/d/12o3bUJw-W9IW-pDT8KZUHxmusssFKg4t/view?usp=drive_link`
Unzip this file and put it in folder ```data```

We also provide a scholarly domain attributed QA benchmark, `https://drive.google.com/file/d/1aSk52cTfvEmjns9UH_ErnH4M_ha86Zrh/view?usp=drive_link`

## Experiments
### Fine-tuning LLMs
Run ```sh train.sh``` to fine-tune LLMs.

Before that, you need to download corresponding open-source LLMs, and modify the ```path_to_your_model``` in ```train.sh```.

Evaluate the fine-tuned LLM by running ```sh inferce.sh```

### Zero/Few-shot LLMs
You can run ```sh inferce.sh``` to directly evaluate open-source LLMs or the fine-tuned LLMs. 

Before that, you need to download corresponding open-source LLMs, and modify the ```path_to_your_model``` in ```inferce.sh```.

Modify the ```prompt_type``` parameter in ```inferce.sh``` to select zero-shot or few-shot settings.

Also, you can run ```sh run_chatgpt.sh``` to select ChatGPT-3.5 or ChatGPT-4 as the attribution evaluator (You have to apply for the API-key first). The parameter ```-fs (True or False)``` is used to control the use of zero-shot or few-shot settings.

## Issues
If you have any questions, please leave a issue and we will respond soon.
