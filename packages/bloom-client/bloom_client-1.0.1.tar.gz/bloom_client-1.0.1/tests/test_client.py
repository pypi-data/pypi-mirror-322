from bloom_client import BloomClient

# Initialize the client with API version, client key, and client secret
client = BloomClient("v3.0", "C3XDX8kihYd2gGtEkeI1jS21s0g1!1H0d9H0IURFbnl_ecfyh-lZBtpLvK-1FO45vfhXOi55c", "8f365a1d3098e269b41b497f7b8594db463381a9a7be6173010f34e7a2441da8")

client.set_inputs({
    "Inputs AC-DC!B2": 10,
    "Inputs AC-DC!B3": 300000
}).set_outputs([
    "Output Information!B5",
    "Output Information!B6"
])

client.add_input("Inputs AC-DC!B12", "Manitoba").add_input("Inputs AC-DC!B4", 0.1)
client.add_output("Output Information!B7").add_output("Output Information!B8")

results = client.calculate()
output_value = results.get("Output Information!B5")
print(results.response)