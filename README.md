# Derivative : An Open Source BP Debate Tracker

Currently live on [derivative.lol](https://derivative.lol). This is the backend of a [tracker](https://github.com/vikwritescode/bp-debate-tracker) designed for British Parliamentary debating, allowing users record and import results, view their history, and access summary statistics.

Built with Python, FastAPI, Pydantic, pandas, Uvicorn, scikit-learn, and Firebase. All code is made available under the [GNU AGPLv3](https://github.com/vikwritescode/bp-tracker-frontend/blob/main/LICENSE.md) license.

## Features
- Add debate results
- Import from [TabbyCat](https://tabbycat.readthedocs.io/en/stable/) URLs
- Track performance over time
- View and manage history
- User registration and authentication
- Automatic motion categorisation

## Planned
- Improved motion categorisation model
- Docker support for easier deployment

## Setup Instructions

1. Clone and enter the repository:
```bash
git clone https://github.com/vikwritescode/bp-debate-tracker
cd bp-debate-tracker
```
2. Create and start a python virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Configure Firebase Login
    - head to firebase console
    - create a new project, enable authentication
    - download ServiceAccountKey.json
    - add ServiceAccountKey.json to the root of the src folder
    - add the path to ServiceAccountKey in your .env
    ```bash
    echo "SERVICE_ACCT_KEY = ./serviceAccountKey.json" > .env
    ```

4. Train Classifier
    - You will need a set of motions and their associated categories
    - modify the file in `ai/train_model.py` to extract this data accordingly
    - run the file in train_model.py.
    - This should, ideally, generate `classifier.pkl`, `multilabel_binarizer.pkl`, and `transformer.pkl`. Ensure these files are in the root of the `src` folder.

5. Enter and run `api.py` 
```bash
python3 src/api.py
```