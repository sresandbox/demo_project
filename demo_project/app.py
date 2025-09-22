Here are the contents for the file: `.github/workflows/deploy.yml`

name: Deploy Flask Application

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run application
        run: |
          nohup python app.py &

      - name: Notify deployment
        run: echo "Deployment completed!"