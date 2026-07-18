import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def get_ai_advice(customer, question):
    prompt = f"""
You are an experienced UK financial adviser.

Customer Details

Name: {customer.name}

Current Age: {customer.age}

Retirement Age: {customer.retirement_age}

Current Pension: £{customer.pension:,.2f}

Monthly Contribution: £{customer.monthly_contribution:,.2f}

Expected Annual Return: {customer.annual_return}%

Question:

{question}

Provide practical, easy-to-understand financial guidance.

Do not guarantee investment returns.

Include:
- Retirement assessment
- Strengths
- Risks
- Recommendations
- Next steps

Use bullet points where appropriate.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional UK financial planning assistant. "
                        "Provide educational financial guidance only and never "
                        "guarantee investment returns."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.4,
            max_tokens=700,
        )

        return response.choices[0].message.content

    except Exception as e:
        error = str(e)

        if "insufficient_quota" in error:
            return """
⚠️ OpenAI API quota exceeded.

Your application is working correctly.

However, your OpenAI API account currently has no available API credits.

Please visit the OpenAI Platform and:
• Check Billing
• Add a payment method if required
• Increase your usage limit

After enabling billing, the AI Advisor will start working automatically.
"""

        elif "invalid_api_key" in error:
            return """
⚠️ Invalid OpenAI API Key.

Please check your .env file.

Example:

OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""

        elif "authentication" in error.lower():
            return "⚠️ Authentication failed. Please verify your OpenAI API key."

        else:
            return f"⚠️ OpenAI Error:\n\n{error}"