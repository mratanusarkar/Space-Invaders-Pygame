@echo off
cmd /k "py -m pip install --user virtualenv & py -m venv env .\env\Scripts\activate & pip install -r requirements.txt & cls & cd Space Invaders && python main.py"
