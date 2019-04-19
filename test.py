from tcg_py import api
import json

with open("keys.json", "r") as file:
    data = json.loads(file.read())

api = api.Handler(public=data["public"], private=data["private"])
# print(api.login_data)
print(api.check_bearer())
