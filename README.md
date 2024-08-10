# DrugTagger
Python code for fast annotation of multiple <ins>small molecules</ins> from the DrugBank database.

## Description
Given a list of small molecules IDs (e.g., DB01076, DB12457, ...), DrugTagger.py allows to isolate the following information from the DrugBank database for each compound:
- Name,
- Average Mass,
- SMILES,
- Drug class 

To circumvent GitHub size limits, the repo does not include the XML dataset (called as drugbank_5-1-12.xml), which which therefore should be downloaded from the website and properly renamed.   

You will be asked to specify the path of the TXT file containing the DrugBank IDs of interest (one ID per line) as well as the pathname of the output file (which in this case is set to TSV format).  

