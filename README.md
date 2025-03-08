# AJD
This repository contains the implementation of our paper "Under the Mandate of Heaven: A Historical Study of Omens and Executives"

## Instructions for Using the Dataset and Extracting the King's Decisions

### 1. Unzip the Data
First, extract the contents of `data.zip` before proceeding. After extraction, the data files must be located in the `data` folder.

### 2. Extracting Decisions Using the Rule-Based Model
Run the `extract_decisions.py` script to extract the king's decisions using the rule-based model.

- After execution, a `.csv` file will be generated.
- The **`max_count_candidate`** column in the CSV file contains the final king’s decision:
  - `0` → **Direct Order**
  - `1` → **Agreement**
  - `2` → **Disagreement**
- The CSV file only includes results for documents that contain a decision.

### 3. Extracting Decisions Using GPT-4o Two-Shot Learning
Use the `gpt-4o-two-shot.ipynb` Jupyter Notebook file to extract the king's decisions using GPT-4o two-shot learning.

- You need to enter your OpenAI key in `YOUR_API_KEY` before using it. Please note that OpenAI charges for usage.
- Run each cell in order.
- After execution, a `.csv` file will be generated.
- The **`gpt_answer`** column in the CSV file contains the final king’s decision.
- Since this method is based on a generative model, **post-processing may be required**.
