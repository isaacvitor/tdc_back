from dotenv import load_dotenv
load_dotenv()

import json

#API CONFIG JSON
with open('./config/api_config.json') as json_file:
    api_config = json.load(json_file)

#API CONFIG JSON
with open('./config/business_rules.json') as json_file:
    business_rules = json.load(json_file)
