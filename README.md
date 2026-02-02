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
2. Initialise a python virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Configure Firebase
    - head to Firebase console
    - create a new project, enable Authentication
    - under project settings, go to the service accounts tab
    - generate a new private key and rename it to `ServiceAccountKey.json`
    - place it in the /src folder
    - add the path to `ServiceAccountKey` in your `.env`
    ```bash
    echo "SERVICE_ACCT_KEY='./serviceAccountKey.json'" > .env
    ```

4. Train Classifier
    - a set of motions and their associated categories are required
    - modify the file in `ai/train_model.py` to extract this data accordingly
    - run `train_model.py`
    - this should generate three files in /src: `classifier.pkl`, `multilabel_binarizer.pkl`, and `transformer.pkl`

5. Enter /src and run `api.py` 
```bash
cd src
python3 api.py
```