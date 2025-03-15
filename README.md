# AJD
This repository is a work in progress and will include the full implementation of our paper "Under the Mandate of Heaven: A Historical Study of Omens and Executives" as it develops.

## Instructions for Using the Dataset and Extracting the King's Decisions

### 1. Unzip the Data
First, extract the contents of `data.zip` before proceeding. After extraction, the data files must be located in the `data` folder.
- `pp_kor_docs_json` (directory): Include the Veritable Records of Joseon Dynasty(`Annals`) file translated into Modern Korean Language
  - In files named in the format `k**_1**.json`, `k**` represents the specific king and `1**` represents year of reign.
- `pp_chi_docs_json` (directory): Include the Veritable Records of Joseon Dynasty(`Annals`) file written in Classical Chinese
  - In files named in the format `w**_1**.json`, `w**` represents the specific king and `1**` represents year of reign.
- `categorized_words_speakers.txt`: This file categorizes whether each last word was spoken by a king or not.
  - This file is tab-separated(`\t`), with two columns: words and speaker(king_or_not)
  - If speaker = 1, the words were spoken by the king, and if speaker = 0, the words were not spoken by the king.
- `king_code_name.txt`: This file is a mapping file that allows you to find the king's name corresponding to the king's code in the `Annals` file.
  - This file is tab-separated(`\t`) and consists of three columns:
    1. The first column: The king's code
    2. The second column: The king's name in Korean
    3. The third column: The king's name in English
- `categorized_words_decisions.txt`: This file is a mapping file that assigns a decision to each last word.
  - This file is tab-separated(`\t`) and consists of three columns:
    1. decision - The classification of the king's decision:
       - `0`: Direct order
       - `1`: Agreement
       - `2`: Disagreement
    2. way - The location where the expression appears (e.g., title, main text, Chinese, etc.).
    3. string - The corresponding last word.

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
