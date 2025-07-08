import openai

openai.api_key = "YOUR_API_KEY"  # Put your OpenAI API key here

def call_gpt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message["content"].strip()
