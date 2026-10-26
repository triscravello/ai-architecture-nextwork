from dotenv import load_dotenv
from fastapi import HTTPException
from google import genai
from google.genai import errors

# Load the local key before creating the Gemini client.
load_dotenv()
MODEL_ID = "gemini-3.8-flash"
client = genai.Client()

# Call Gemini without blocking the FastAPI event loop.

async def generate(prompt: str) -> str:
    try:
        response = await client.aio.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
        )
    except errors.APIError as error:
        # 💡 DEBUG: Print the raw error details so we can inspect them in the terminal logs
        print("\n=== GEMINI API ERROR DETECTED ===")
        print(f"Error Type: {type(error)}")
        print(f"Error Message: {error}")
        print("=================================\n")
        
        raise HTTPException(
            status_code=502,
            detail="Gemini request failed.",
        ) from error

    return response.text
