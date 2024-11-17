from fastapi import FastAPI, HTTPException
import scraper
import chatgpt_api_client
import openai

app = FastAPI()

pages_data = scraper.crawl_site()

@app.get("/source_info")
def getSourceInfo():
    try:
        return pages_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.post("/ask")
def askQuestion(user_question: str):
    user_question = user_question.strip()
    if len(user_question)<1:
        raise HTTPException(status_code=400, detail="The input is missing or invalid. Please provide a valid question.")
    try:
        response = chatgpt_api_client.ask_chatgpt(user_question, pages_data)
        return response
    except openai.OpenAIError as e:
        # Catch for openai API related issues
        raise HTTPException(status_code=502, detail=f"Unexpected OpenAI API error: {str(e)}")
    except Exception as e:
        # Generic catch-all for unhandled server-side issues
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")