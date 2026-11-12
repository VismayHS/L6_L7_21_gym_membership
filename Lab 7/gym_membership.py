import math


def parse_plan(code):
    """Return (uppercase plan, positive months), or None for invalid input."""
    if not isinstance(code, str):
        return None
    parts = code.split('-')
    if len(parts) != 2:
        return None
    plan, months_text = (part.strip() for part in parts)
    if not (plan.isascii() and plan.isalpha()):
        return None
    if not (months_text.isascii() and months_text.isdigit()):
        return None
    try:
        months = int(months_text)
    except ValueError:
        # Python also rejects integer strings beyond its conversion limit.
        return None
    if months <= 0:
        return None
    return plan.upper(), months

def calculate_bmi(data):
    """Return BMI rounded to one decimal, or None for invalid/unsafe input."""
    if not isinstance(data, str):
        return None
    parts = data.split(',')
    if len(parts) != 2:
        return None
    try:
        weight, height = (float(part) for part in parts)
    except ValueError:
        return None
    if not all(math.isfinite(value) and value > 0 for value in (weight, height)):
        return None
    try:
        height_squared = height ** 2
    except OverflowError:
        return None
    if height_squared == 0 or not math.isfinite(height_squared):
        return None
    bmi = weight / height_squared
    if not math.isfinite(bmi) or bmi <= 0:
        return None
    return round(bmi, 1)

def average_workout(minutes):
    """Return the floor average of nonnegative integer minutes, else None."""
    if not isinstance(minutes, str):
        return None
    tokens = minutes.split()
    if not tokens:
        return None
    try:
        values = [int(token) for token in tokens]
    except ValueError:
        return None
    if any(value < 0 for value in values):
        return None
    return sum(values) // len(values)

def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter a plan code (e.g. GOLD-12): ")
    result = parse_plan(user_input)
    print("Invalid plan code." if result is None else f"Plan and Months: {result}")

    print("\n==== Running calculate_bmi ====")
    user_input = input("Enter weight and height (e.g. 70,1.75): ")
    result = calculate_bmi(user_input)
    print("Invalid weight or height." if result is None else f"BMI: {result}")

    print("\n==== Running average_workout ====")
    user_input = input("Enter workout minutes separated by spaces (e.g. 45 60 30): ")
    result = average_workout(user_input)
    print("Invalid workout minutes." if result is None else f"Average Minutes: {result}")

if __name__ == "__main__":
    main()
