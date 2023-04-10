import requests
r = requests.post(
    "https://api.deepai.org/api/stable-diffusion",
    data={
        'text': 'Ufa',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())
