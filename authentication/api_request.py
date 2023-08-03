import requests

# Set the API endpoint URL
url = "http://localhost:8000/profile/detail/create_profile"

# Set the API key
api_key = "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"

# Set the headers with the API key
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Make the request
response = requests.get(url, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Request was successful
    data = response.json()
    # Process the response data
else:
    # Request failed
    print(f"Request failed with status code {response.status_code}")
    print(response.text)