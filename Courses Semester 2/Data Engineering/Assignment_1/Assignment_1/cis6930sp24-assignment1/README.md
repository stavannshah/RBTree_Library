# CIS6930SP24-ASSIGNMENT1

# Author: Malay Bhatt

# Assignment Description 

Sensitive information is frequently included in documents such as police reports, court transcripts, and medical records. To safeguard privacy, it's essential to redact or censor this information before sharing documents publicly. However, manual redaction processes are often costly and time-consuming. To address this challenge, the Redaction Pipeline System automates the detection and censoring of sensitive information within plain text documents.

## Table of Contents

- How to Install
- How to Run 
- Functions
- Output

## How to Install
  1. Clone repository to your local machine:
    $ git clone 
    $ cd cis6930sp24-assignment1
  2. Using Pipenv and Installing prerequisites:
    $ pipenv install
  3. Verify Installation: Once the command in step 3 is completed, verify if the dependencies are installed correctly by runing the following command:
    $ pipenv --version
## How to Run
- We must execute the following command in order to run the censor:
  ```
  pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --genders --address\
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr
  ```                  
## censoror.py
   This script provides functionality to censor sensitive information like names, dates, phone   numbers, and addresses from input files. It leverages various libraries and tools for natural language processing (NLP) and weak supervision.

- **Dependencies:**
   - `argparse`: Used for parsing command-line arguments.
   - `glob`: Used for file pattern matching.
   - `sys`: Provides access to some variables used or maintained by the Python interpreter.
   - `os`: Used for interacting with the operating system, such as file operations.
   - `assignment1.main`: Imports the functions defined in the `main.py` file of an `assignment1` module.

- **Functions:**
   - `main(args)`: The main function orchestrates the entire censoring process. It reads input files, censors sensitive information based on specified options, writes the censored files, and generates statistics.
   - `write_censored_file(input_file, output_dir, censored_text)`: Writes the censored text to an output file.
   - `write_to_files_stats(raw_file, stats)`: Writes the censoring statistics to a file.
   - `censor_stats(args, censor_counts, censor_list)`: Generates statistics about the censoring process.
   
- **Censoring Functions:**
   - `censor_dates(data)`, `censor_phones(data)`, `censor_address(data)`, and `censor_names_snorkel(data)`: These functions individually censor dates, phone numbers, addresses, and names from the input text. They utilize different techniques, such as regular expressions, NER, and weak supervision with Snorkel, to identify and censor sensitive information.
         
      - `censor_dates(data):`This method uses regular expression matching and named entity recognition (NER) with spaCy to identify and censor dates in the input text. It gives back a list of detected dates together with the suppressed content.
      - `censor_phones(data):`Using the CommonRegex library, this function finds and filters phone numbers found in the input text. The redacted text and a list of phone numbers that were found are returned.
      - `censor_address(data):`This method uses the pyap package for address parsing to identify and suppress addresses in the supplied text. The censored text and a list of addresses that were found are returned.
      - `censor_names_snorkel(data):`This method uses the weak supervision library Snorkel to fine-tune the identification of possible names in the input text by looking for patterns like titles coming before capitalized terms. The suppressed text and a list of names that were found are returned.

- **Execution from Command Line**:
   Users can run the script from the command line by specifying input files, types of information to censor, output formats, and where to print statistics.


## Output
- [Video Output](https://drive.google.com/file/d/1j9iyU4fUAfKgeKfpaBxFv0A6T9k7wXXb/view?usp=sharing)

## Author 
  - Malay Bhatt
  - Email: m.bhatt@ufl.edu 
  - UFID: 4707-0863
