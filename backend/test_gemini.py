from app.ai.gemini_client import gemini_client

response = gemini_client.generate(
    "Explain FastAPI in one sentence."
)

print(response)