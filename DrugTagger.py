import xml.etree.ElementTree as ET
import time
import re

def print_logo():
    logo = r"""

▓█████▄ ██▀███  █    ██  ▄████                
▒██▀ ██▓██ ▒ ██▒██  ▓██▒██▒ ▀█▒               
░██   █▓██ ░▄█ ▓██  ▒██▒██░▄▄▄░               
░▓█▄   ▒██▀▀█▄ ▓▓█  ░██░▓█  ██▓               
░▒████▓░██▓ ▒██▒▒█████▓░▒▓███▀▒               
 ▒▒▓  ▒░ ▒▓ ░▒▓░▒▓▒ ▒ ▒ ░▒   ▒                
 ░ ▒  ▒  ░▒ ░ ▒░░▒░ ░ ░  ░   ░                
 ░ ░  ░  ░░   ░ ░░░ ░ ░░ ░   ░                
   ░      ░       ░          ░                
▄▄▄█████▓▄▄▄       ▄████  ▄████▓█████ ██▀███  
▓  ██▒ ▓▒████▄    ██▒ ▀█▒██▒ ▀█▓█   ▀▓██ ▒ ██▒
▒ ▓██░ ▒▒██  ▀█▄ ▒██░▄▄▄▒██░▄▄▄▒███  ▓██ ░▄█ ▒
░ ▓██▓ ░░██▄▄▄▄██░▓█  ██░▓█  ██▒▓█  ▄▒██▀▀█▄  
  ▒██▒ ░ ▓█   ▓██░▒▓███▀░▒▓███▀░▒████░██▓ ▒██▒
  ▒ ░░   ▒▒   ▓▒█░░▒   ▒ ░▒   ▒░░ ▒░ ░ ▒▓ ░▒▓░
    ░     ▒   ▒▒ ░ ░   ░  ░   ░ ░ ░  ░ ░▒ ░ ▒░
  ░       ░   ▒  ░ ░   ░░ ░   ░   ░    ░░   ░ 
              ░  ░     ░      ░   ░  ░  ░     
                                                                                                                                                                                                                                                             
    """
    
    print(logo)
    print("\n==================================================================================================================")
    print("DrugTagger v1.0: Python-based tool to annotate ligands named by DrugBank ID")
    print("==================================================================================================================\n")
    time.sleep(5)  

# Print the logo
print_logo()

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip().split() for line in file]
    return [(line[0], line[1], line[2]) for line in lines if len(line) >= 3]

def extract_text_from_element(element):
    return element.text.strip() if element is not None and element.text is not None else ""

def clean_text(text):
    # Remove newlines and multiple spaces
    return re.sub(r'\s+', ' ', text).strip()

def extract_drug_info(xml_file, input_data):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    drugs_info = []
    drug_data = {}
    
    # First, extract all drug data from the XML
    for drug in root.findall(".//{http://www.drugbank.ca}drug"):
        drugbank_id_element = drug.find(".//{http://www.drugbank.ca}drugbank-id[@primary='true']")
        if drugbank_id_element is not None:
            drugbank_id = drugbank_id_element.text.strip()
            name_element = drug.find(".//{http://www.drugbank.ca}name")
            mass_element = drug.find(".//{http://www.drugbank.ca}average-mass")
            smiles_element = drug.find(".//{http://www.drugbank.ca}calculated-properties/"
                                       "{http://www.drugbank.ca}property[{http://www.drugbank.ca}kind='SMILES']")
            categories_element = drug.find(".//{http://www.drugbank.ca}categories")
            
            name = extract_text_from_element(name_element)
            mass = extract_text_from_element(mass_element)
            smiles = extract_text_from_element(smiles_element.find(".//{http://www.drugbank.ca}value")) if smiles_element is not None and smiles_element.find(".//{http://www.drugbank.ca}value") is not None else ""
            
            if categories_element is not None:
                categories = [clean_text(cat.text) for cat in categories_element.findall(".//{http://www.drugbank.ca}category") if cat.text]
                drug_class = " ".join(categories[:3])  # Limit to first 3 categories, join with spaces
            else:
                drug_class = "Unknown"
            
            drug_data[drugbank_id] = {
                "Name": name,
                "Mass": mass,
                "SMILES": smiles,
                "Drug Class": drug_class
            }
    
    # Then, create the drugs_info list based on the input order, including duplicates
    for cluster, drug_id, affinity_1 in input_data:
        if drug_id in drug_data:
            drug_info = drug_data[drug_id].copy()
            drug_info["Cluster"] = cluster
            drug_info["Drug_ID"] = drug_id
            drug_info["Affinity_1"] = affinity_1
            drugs_info.append(drug_info)
        else:
            # If the ID is not found, add a placeholder entry
            drugs_info.append({
                "Cluster": cluster,
                "Drug_ID": drug_id,
                "Affinity_1": affinity_1,
                "Name": "Not found",
                "Mass": "",
                "SMILES": "",
                "Drug Class": "Unknown"
            })
    
    return drugs_info

def save_to_tsv(data, tsv_file):
    with open(tsv_file, 'w', newline='', encoding='utf-8') as tsvfile:
        tsvfile.write("Cluster\tDrug_ID\tAffinity_1\tName\tMass\tSMILES\tDrug Class\n")
        for entry in data:
            tsvfile.write(f"{entry['Cluster']}\t{entry['Drug_ID']}\t{entry['Affinity_1']}\t{entry['Name']}\t{entry['Mass']}\t{entry['SMILES']}\t{entry['Drug Class']}\n")

# Prompt the user for input
xml_file_path = "datasets/drugbank_5-1-12.xml"

# Get the input TXT file path from the user
input_file_path = input("Enter the path to the input TXT file: ")

# Get the output TSV file path from the user
tsv_file_path = input("Enter the path to the output TSV file: ")

# Read input data from the file
input_data = read_input_file(input_file_path)

# Extract drug information for the specified IDs
drugs_info_list = extract_drug_info(xml_file_path, input_data)

# Save the information to a TSV file
save_to_tsv(drugs_info_list, tsv_file_path)

print(f"Data saved to {tsv_file_path}")
