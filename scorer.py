from questions import QUESTIONS
def judge (question: str, expects: str, answer: str, results: list) -> bool:
    if not expects: 
        return False
    return expects.strip().lower() in answer.strip().lower()

