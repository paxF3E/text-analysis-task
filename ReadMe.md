### Workflow
1. `Input.csv` is the provided `.xlsx` file converted to `.csv` for easy interpretation using python
2. All the links to the articles provided in `Input.csv` are fetched and extracted using `selenium` and written to `./Input/<ID>.txt` respective to their article ID
3. Each `.txt` file(referred to as `doc`) is read one by one. Content of every `doc` is **tokenized** using `nltk.tokenizer` and then **lemmatized** using `nltk.WordNetLemmatizer`
4. On these `lemmas`, the characteristic measures are applied and calculated using the rules and formulae mentioned in `Text Analysis.docx`
5. All the measures calculated for a `doc` are then appened to their respective IDs and URLs, to make generate an output string for the doc, ready to be written into the final `Output.csv` based on exact structure mentioned in `Output Data Structure.xlsx`

### Directory tree
- The root directory `blackcoffer` contains all the provided files, and two python code files `extract_data.py` and `text_analysis.py` for better readability.
- `blackcoffer/Input` directory contains all the `.txt` docs; `chromedriver` is the driver-binary for `selenium`; and a `Output.csv` with all the final results

### Steps to run the files
1. `cd blackcoffer/`
2. `python3 extract_data.py`
3. `python3 text_analysis.py`