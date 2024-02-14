# DrugTagger
Jupyter notebook for fast annotation of small molecules from the DrugBank database.

## Description
DrugTagger.ipynb allows to isolate information of interest from the DrugBank database (Name, Average Mass, Description, SMILES, etc) given a list of small molecules IDs (e.g., DB00001, DB00002, ...).
To circumvent GitHub size limits,  the present Jupyter Notebook parses a shrinked version of the DrugBank XML database (drugbank_short.xml), which includes only 3 small molecules (DB01076, DB01698, DB12457). 
You will be asked to specify the path of the TXT file containing the DrugBank IDs of interest (one per line) as well as the pathname of the output file (which in this case is set to TSV format). 

