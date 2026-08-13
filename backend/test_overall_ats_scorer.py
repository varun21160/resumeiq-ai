from app.ai.overall_ats_scorer import OverallATSScorer


def test_overall_ats_score():

    scores = {
        "skills": 81,
        "experience": 70,
        "projects": 100,
        "education": 100,
        "certifications": 90,
        "resume_quality": 88,
    }

    result = OverallATSScorer.calculate(scores)

    print("\n========== OVERALL ATS SCORER ==========")
    print("Category scores:")
    print(scores)
    print("----------------------------------------")
    print(f"Overall ATS Score: {result}")
    print("========================================")

    assert result == 85


def test_score_bounds():

    scores = {
        "skills": 150,
        "experience": -20,
        "projects": 100,
        "education": 100,
        "certifications": 100,
        "resume_quality": 100,
    }

    result = OverallATSScorer.calculate(scores)

    print("\n========== SCORE BOUND TEST ==========")
    print(f"Overall ATS Score: {result}")
    print("======================================")

    assert 0 <= result <= 100


def test_missing_category():

    scores = {
        "skills": 100,
        "experience": 100,
    }

    result = OverallATSScorer.calculate(scores)

    print("\n========== MISSING CATEGORY TEST ==========")
    print(f"Overall ATS Score: {result}")
    print("===========================================")

    assert 0 <= result <= 100


if __name__ == "__main__":
    test_overall_ats_score()
    test_score_bounds()
    test_missing_category()

    print("\nAll Overall ATS Scorer tests passed.")