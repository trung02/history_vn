key="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"

# ID	REQUESTS PER MINUTE	REQUESTS PER DAY	TOKENS PER MINUTE
# gemma-7b-it	30	14,400	15,000
# mixtral-8x7b-32768	30	14,400	5,000
# llama3-70b-8192	30	14,400	6,000
# llama3-8b-8192

from groq import Groq

client = Groq(api_key=key)
completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "system",
            "content": "Hãy trả lời bằng tiếng Việt"
        },
        {
            "role": "user",
            "content": "hồ chí minh quê quán ở đâu?"
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
