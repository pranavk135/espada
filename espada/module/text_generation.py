import requests

def call_groq_llama(prompt, api_key, max_tokens=512, top_p=0.95, temperature=0.7):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",  # or "llama3-70b-8192"
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Groq API Error {response.status_code}: {response.text}")

# if __name__ == "__main__":
#     job_role = "Software Engineer"
#     prompt = prompt = f"""
#     Write a single ATS-friendly 'About the Applicant' section in 30–40 words
#     for the role: {job_role}. 
#     Return only the text. Do not add titles, labels, or extra sentences.
# """

#     api_key = "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"
#     max_tokens = 512
#     top_p = 0.95
#     temperature = 0.7
#     output = call_groq_llama(prompt, api_key, max_tokens, top_p, temperature)
#     print(output)