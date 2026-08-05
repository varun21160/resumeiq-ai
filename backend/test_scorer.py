from app.ai.scorer import ATSScorer

resume = [
    "python",
    "sql",
    "power bi",
    "docker",
    "fastapi"
]

jd = [
    "python",
    "sql",
    "docker",
    "aws",
    "kafka"
]

result = ATSScorer.calculate(
    resume,
    jd,
)

print(result)