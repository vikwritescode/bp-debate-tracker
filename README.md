# BP Debate Tracker

This is a python program which is designed to use a URL and a name to keep track of BP speeches for speakers. Current work in progress.

## What is this repo?
This is the backend code for my BP debate tracker. Currently, this uses sqlite to store BP debate records. These records are created and fetched using an API. This program uses fastAPI, which allows authenicated users to fetch and record information that is debate related.

This, at the moment, also allows for records to be made through simply a URL and a name, instead of adding the results of all of the rounds manually. 

## Features
- Import from URL
- Get position wide averages
- View Debates Individually
- Sign Up and Login
- Add Individual Records
- Delete Records
- View Motions and Infoslides
- Automatic Categorisation of Debates

## Planned
- Improved Model for Speaker Categories
- Some level of docker support for easy deployment

## Setup Instructions

1. Clone and enter the repository:
```bash
git clone https://github.com/vikwritescode/bp-debate-tracker
cd bp-debate-tracker
```
1. Create and start a python virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
1. Configure Firebase Login
    - head to firebase console
    - create a new project, enable authentication
    - download ServiceAccountKey.json
    - add ServiceAccountKey.json to the root of the src folder
    - add the path to ServiceAccountKey in your .env
    ```bash
    echo "SERVICE_ACCT_KEY = ./serviceAccountKey.json" > .env
    ```

1. Train Classifier
    - You will need a set of motions and their associated categories
    - modify the file in `ai/train_model.py` to extract this data accordingly
    - run the file in train_model.py.
    - This should, ideally, generate `classifier.pkl`, `multilabel_binarizer.pkl`, and `transformer.pkl`. Ensure these files are in the root of the `src` folder.

1. Enter and run `api.py` 
```bash
python3 src/api.py
```

