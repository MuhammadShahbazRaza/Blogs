import requests
import logging

# def generate_content(title, category):
#     # Set up API credentials and endpoints
#     api_key = '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'  # Replace with your actual API key
#     completion_endpoint = 'https://api.openai.com/v1/engines/davinci/completions'

#     # Prepare request payload for completion API
#     prompt = f'Title: {title}\nCategory: {category}\nInstructions: Please provide a discussion about "{title}" in {category}.\n\n'
#     completion_payload = {
#         'prompt': prompt,
#         'max_tokens': 400,
#         'temperature': 0.7,
#         'n': 1
#     }

#     # Set up headers with API key
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json'
#     }

#     # Send POST request to completion API
#     completion_response = requests.post(completion_endpoint, headers=headers, json=completion_payload)

#     # Parse response from completion API
#     completion_data = completion_response.json()
#     generated_content = ''
#     if 'choices' in completion_data:
#         try:
#             generated_content = completion_data['choices'][0]['text']
#         except (KeyError, IndexError):
#             pass

#     return generated_content



import openai
def post(title,category):
        
        # message = ''
        
        message = 'what is  '+title +f'in {category}\n also provide me code example please show the content separatelty and make a separate section for code in which you have to provide a code example in reponse do not give the question please and dont show show:'
        
        
        
        completions = openai.Completion.create(
            # engine="text-curie-001",
            engine="text-davinci-003",
            
            prompt=message,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )

        suggestions = completions.choices[0].text.strip().split("\n")
        combined_string = "\n\n".join(s for s in suggestions if s)
        return combined_string
        # response = suggestions[0]
       
