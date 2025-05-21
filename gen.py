from g4f.client import Client

client = Client()

response = client.images.generate(
    model="flux",
    prompt=input(),
    response_format="url"
)

print({response.data[0].url})