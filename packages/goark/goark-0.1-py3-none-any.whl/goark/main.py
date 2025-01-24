import requests
from .utilities import distill, output_to_tools
class Goark:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://akshathnag06--example-web-flask-flask-app.modal.run"
        self.api_endpoints = {
            "view_tools": "/view_tools",
            "output": "/output",
            "delete_tools": "/delete_tools",
            "ingest": "/ingest",
            "json_serializer": "/json_serializer",
        }


    def view_tools(self):
        request_uri = self.base_url + self.api_endpoints["view_tools"]
        payload = {"api_token": self.api_key}
        response = requests.post(request_uri, json=payload)
        response.raise_for_status()
        if response.text == "Invalid API Key":
          raise AttributeError(f"Invalid attribute: API Key")
        else:
          return response.json()
          
    def output(self, tools, query, max_outputs=2):
        request_uri = self.base_url + self.api_endpoints["output"]
        payload = {
            "api_token": self.api_key,
            "query": query,
            "max_outputs": max_outputs
        }
        response = requests.post(request_uri, json=payload)
        response.raise_for_status()
        relevant_text_nodes = response.json()
        print("####################RELEVANT TEXT NODES######################")
        print(relevant_text_nodes)
        print("#############################################################")
        relevant_tools = output_to_tools(tools=tools, output_results=relevant_text_nodes, max_outputs=max_outputs)
        return relevant_tools

    def delete_tools(self):
        request_uri = self.base_url + self.api_endpoints["delete_tools"]
        payload = {"api_token": self.api_key}
        response = requests.post(request_uri, json=payload)
        response.raise_for_status()
        return response.json()

    def ingest(self, tools):
        request_uri = self.base_url + self.api_endpoints["ingest"]
        payload = {
            "tools": distill(tools), #Distlls the tools to a json serializable format that the server can understand.
            "api_token": self.api_key,
        }
        response = requests.post(request_uri, json=payload)
        response.raise_for_status()
        return response.json()