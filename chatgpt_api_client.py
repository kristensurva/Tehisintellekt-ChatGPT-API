import openai
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OpenAI API key not found. Ensure it's set in the .env file.")
else:
    openai.api_key = API_KEY

class GPTAnswer(BaseModel):
    answer: str = Field(..., description="The answer provided by the GPT based on the domain data.")
    used_subdomains: list[str] = Field(..., description="List of subdomains that were referenced to generate the answer.")

def ask_chatgpt(question, pagesData):
    """Send a question with context to the ChatGPT API and return the response."""
    response = openai.beta.chat.completions.parse(
        messages=[
            {"role": "system", "content": "You are a specialised assistant, designed to answer questions about the company Tehisintellekt OÜ. You have been provided scraped text from the main page and subpages of this company's website https://tehisintellekt.ee/ so you can answer these questions. Use this information to answer the user's questions about the company."+"\n---\n" + str(pagesData)},
            {"role": "user", "content": question}
        ],    
        model="gpt-4o-mini",
        response_format=GPTAnswer
    )
    print(str(response))
    processedResponse = process_response(question, response)
    return processedResponse

def process_response(question, response):
    processedResponse = {"response": {}}
    processedResponse["response"]["user_question"] = question
    processedResponse["response"]["answer"] = response.choices[0].message.parsed.answer
    processedResponse["response"]["usage"] = {}
    processedResponse["response"]["usage"]["input_tokens"] = response.usage.prompt_tokens
    processedResponse["response"]["usage"]["output_tokens"] = response.usage.completion_tokens
    processedResponse["response"]["sources"] = response.choices[0].message.parsed.used_subdomains
    return processedResponse
