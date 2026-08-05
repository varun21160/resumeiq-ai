from app.ai.scorer import ATSScorer

resume = [
    "python",
    "sql",
    "git",
]

jd = [
    "python",
    "sql",
    "aws",
    "docker",
]

print(
    ATSScorer.calculate(
        resume,
        jd,
    )
)