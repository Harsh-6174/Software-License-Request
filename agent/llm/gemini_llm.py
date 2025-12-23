from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash",
    google_api_key = os.getenv("GOOGLE_API_KEY")
)

def run_llm(prompt):
    # response = await llm.ainvoke(prompt)
    # return response.content

    return '{"requester_id": "", "software_requested": "pycharm", "request_reason": "coding"}'