from app.ai.text_cleaner import TextCleaner

sample = """
PowerBI
Postgres
JS
NodeJS
ML
GenAI
REST
"""

print(TextCleaner.clean(sample))