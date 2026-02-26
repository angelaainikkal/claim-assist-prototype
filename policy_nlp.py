def convert_policy_to_rules(text):
    prompt = f"""
    Convert this insurance policy text into structured JSON rules:
    - Required documents
    - Claim limits
    - Rejection conditions

    Policy:
    {text}
    """

    response = model.generate_content(prompt)
    return response.text