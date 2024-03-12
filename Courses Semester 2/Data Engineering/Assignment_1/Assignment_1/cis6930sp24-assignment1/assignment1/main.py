import nltk
from commonregex import CommonRegex
import pyap
import re
import spacy
from snorkel.labeling import LabelingFunction
from spacy_download import load_spacy
import en_core_web_md

from warnings import filterwarnings
filterwarnings("ignore")

# Load the spaCy model with medium English language capabilities
nlp = en_core_web_md.load()

# Function to censor dates in the input text
def censor_dates(data):
    # Process the input text with the spaCy model
    data1 = nlp(data)
    # Extract entities recognized as dates by spaCy
    dates_ent_list = []
    for i in [ent.text.split('\n') for ent in data1.ents if ent.label_ == "DATE"]:
        for j in i:
            dates_ent_list.append(j)
    # Define a regular expression pattern to capture date formats
    pattern = r'(\d{1,4}/\d{1,2}/\d{1,4})'
    # Find all matches of the pattern in the input text
    dates_re_list = re.findall(pattern,data)
    # Combine spaCy recognized dates and regex matched dates
    dates_list = set(dates_ent_list + dates_re_list)
    # List of common terms to exclude from date detection
    list_to_excluded = ["day", "tomorrow","yesterday","today","Day","Today","Tomorrow","century","weeks","week","Week","Weeks","week's","Week's","year", "Year","Year's","year's","month","Month","month's","Month's","months","Months"]
    # Remove excluded terms from the detected dates
    for i in list_to_excluded:
        if i in dates_list:
            dates_list.remove(i)
    # Replace detected dates in the input text with censor characters
    for items in dates_list:
        data = data.replace(items,'\u2588'* len(items))
    return data,dates_list
    
# Function to censor phone numbers in the input text
def censor_phones(data):
    # Use CommonRegex library to identify phone numbers
    data1 = CommonRegex(data)
    phones_list = data1.phones
    # Replace detected phone numbers with censor characters
    for item in phones_list:
        data = data.replace(item,'\u2588'* len(item))
    return data, phones_list

# Function to censor addresses in the input text
def censor_address(data):
    address_list = []
    # Use pyap library to parse addresses from the input text
    addresses = pyap.parse(data,country = 'US')
    # Iterate over detected addresses
    for address in addresses:
        # Determine start and end indices of the address in the input text
        start_index = data.index(str(address).split(',')[0].strip())
        end_index = data.index(str(address).split(',')[-1].strip()) + len(str(address).split(',')[-1].strip())
        address_list.append(data[start_index:end_index])
        # Replace detected address with censor characters
        data = data[:start_index] + '\u2588'* len(str(address)) + data[end_index:]
    return data, address_list

# Function to extract entities from text using spaCy
def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Labeling function to identify potential names preceded by titles
def lf_title_before_capitalized_word(x):
    titles = ['Mr.', 'Mrs.', 'Dr.', 'Prof.']
    words = x.split()
    # Check if a title is followed by a capitalized word
    for i, word in enumerate(words[:-1]):  
        if word in titles and words[i + 1][0].isupper():
            return 1  
    return 0 

# Refinement function to filter entities based on labeling function
def refine_with_snorkel(sentences, extract_entities_fn, labeling_fn):
    refined_entities = []
    for sentence in sentences:
        entities = extract_entities_fn(sentence)
        for entity in entities:
            # Apply labeling function to each entity
            label = labeling_fn(entity[0])
            if label == 1 or entity[1] == 'PERSON':
                refined_entities.append(entity)
    return refined_entities

# Function to censor names using Snorkel for weak supervision
def censor_names_snorkel(data):
    # Define labeling function for potential names
    title_before_name_lf = LabelingFunction(
    name="title_before_capitalized_word",
    f=lf_title_before_capitalized_word
    )
    # Split text into sentences
    sentences = data.split('.')
    # Refine entity extraction using snorkel labeling function
    refined_entities = refine_with_snorkel(sentences, extract_entities, lf_title_before_capitalized_word)
    # Extract names from refined entities
    names_list = [entity[0] for entity in refined_entities]
    # Replace detected names with censor characters
    for item in names_list:
        data = data.replace(item, '\u2588'* len(item))
    return data, names_list