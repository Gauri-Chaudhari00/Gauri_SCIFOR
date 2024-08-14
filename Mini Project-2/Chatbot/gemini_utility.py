import os 
import json 

import google.generativeai as genai
# get the working directory
working_directory = os.path.dirname(os.path.abspath("C:\\Users\\Admin\\.vscode\\Chatbot"))

config_file_path = f"{working_directory}\\.env"
config_data = json.load(open(config_file_path))

# loading the api key
GoogleAPI = config_data["GoogleAPI"]

print(GoogleAPI)