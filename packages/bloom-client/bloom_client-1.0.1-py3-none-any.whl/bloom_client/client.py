import requests

class BloomClient:
    def __init__(self, api_version, client_key, client_secret):
        if not api_version or not client_key or not client_secret:
            raise ValueError("API version, client key, and client secret are required.")
        self.api_url = f"https://bloom-engine.netlify.app/.netlify/functions/api/{api_version}"
        self.client_key = client_key
        self.client_secret = client_secret
        self.inputs = {}
        self.outputs = []
        self.response = {}

    def set_inputs(self, inputs):
        self.inputs.update(inputs)
        return self

    def set_outputs(self, outputs):
        self.outputs.extend(outputs)
        return self

    def add_input(self, key, value):
        self.inputs[key] = value
        return self

    def add_output(self, output):
        self.outputs.append(output)
        return self

    def calculate(self):
        payload = {
            "inputs": self.inputs,
            "outputs": self.outputs
        }
        headers = {
            "x-client-key": self.client_key,
            "x-client-secret": self.client_secret,
            "Content-Type": "application/json"
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        self.response = response.json().get("data", {})
        return self

    def get(self, key):
        return self.response.get(key)
