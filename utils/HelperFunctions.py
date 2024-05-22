import random
import string


# Checks whether the string has passed the token limit of PaLM
def check_token(input: str, limit: int = 4096) -> int:
    chars = len(input)
    return (chars / 4) <= limit


def parse_response(
    response: string,
    keys_to_check: list = ["AI", "Observation", "Action", "Action Input", "Thought"],
):
    for key in keys_to_check:
        if key in response:
            answer = response.split(f"{key}:")
            if answer[-1]:
                answer = answer[-1]
                return answer

    return ""


def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))
