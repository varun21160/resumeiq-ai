from app.ai.scorer import ATSScorer

resume = [
    "postgres",
    "tensorflow",
    "javascript",
    "power bi",
]

jd = [
    "postgresql",
    "tensor flow",
    "js",
    "powerbi",
]

result = ATSScorer.calculate(
    resume,
    jd,
)

print(result)