# DrugTagger
Jupyter notebook for fast annotation of multiple <ins>small molecules</ins> from the DrugBank database.

## Description
Given a list of small molecules IDs (e.g., DB01076, DB12457, ...), DrugTagger.ipynb allows to isolate the following information from the DrugBank database for each compound:
- Name,
- Average Mass,
- SMILES,
- Description (in this case limited to 75 characters)

To circumvent GitHub size limits, the present Jupyter Notebook parses a shrinked version of the DrugBank XML database (drugbank_short.xml), which includes only 3 small molecules (DB01076, DB01698, DB12457). Once you cloned the present repository, download the latest version of the Drugbank database and modify   

You will be asked to specify the path of the TXT file containing the DrugBank IDs of interest (one ID per line) as well as the pathname of the output file (which in this case is set to TSV format). 

Feel free to use and modify this script to isolate any information you might be interested in. 

