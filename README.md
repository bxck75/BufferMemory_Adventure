# LangChain BufferMemory Adventure

# Setup
Make a account on https://www.datastax.com/lp/astra-registration
Create a vector storage in your account and follow the install install instructions on the website
No need  to copy the python script that is cassandr_db_connect.py in the project folder
Place both your downloaded secure-connect bundle zip and the db_token.json from the astra db website into the project folder
Add a value to the db_token.json file like 

```json
"keyspace": "your key space here"
```
# Create the env and install requirements

```bash
python -m venv adventure_env
source adventure_env/bin/activate
pip install -r requirements.txt
```
# Run the program
run 
```bash
python adventure.py
```

# Customize

the templates for the game prompts are in templates.py
you can customize them as you want
