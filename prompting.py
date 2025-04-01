import os
from dotenv import load_dotenv, dotenv_values
from google import genai
from google.genai import types
from google.api_core import retry
from IPython.display import HTML, Markdown, display

# SETUP
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Retry helper, Prevents maxing out quota
is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})
genai.models.Models.generate_content = retry.Retry(
    predicate=is_retriable)(genai.models.Models.generate_content)

client = genai.Client(api_key=GOOGLE_API_KEY)

model_config = types.GenerateContentConfig(
    temperature=1.0,
    top_p=0.95
)

story_prompt = "You are a creative writer. Write a short story about a cat who goes on an adventure."
response = client.models.generate_content(
    model='gemini-2.0-flash',
    config=model_config,
    contents=story_prompt)

print(response.text)