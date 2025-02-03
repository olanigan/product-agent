import pandas as pd
from httpx import Client
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.exceptions import UnexpectedModelBehavior
from .model_lib import GEMINI_MODEL, OLLAMA_MODEL, GROQ_MODEL, OPENAI_MODEL
import datetime

class Product(BaseModel):
    brand_name: str = Field(title="Brand Name", description="The brand name of the product")
    product_name: str = Field(title="Product Name", description="The name of the product")
    price: str | None = Field(title="Price", description="The price of the product")
    rating_count: int | None = Field(title="Rating Count", description="The rating count of the product")

class Event(BaseModel):
    event: str = Field(title="Event", description="The event that occurred")
    date: datetime.datetime = Field(title="Date", description="The date of the event")
    time: str = Field(title="Time", description="The start time of the event")
    location: str = Field(title="Location", description="The location of the event")
    category: str = Field(title="Category", description="Type of event")
    speakers: list[str] = Field(title="Speakers", description="List of speakers at the event")

class Results(BaseModel):
    # dataset: list[Product] = Field(title="Dataset", description="The list of products")
    dataset: list[Event] = Field(title="Dataset", description="The list of events")
    category: str = Field(title="Category", description="The type of data in dataset")

web_scraping_agent = Agent(
    name="Web Scraping Agent",
    # model=OPENAI_MODEL,
    model=GEMINI_MODEL,
    system_prompt="""
    Your task is to convert a data string into a list of dictionaries.
    
    Step 1. Fetch the HTML text from the given URL using the fetch_html_text() function.
    Step 2. Takes the output from Step 1 and clean it up for the final output
    """,
    retries=2,
    result_type=Results,
    model_settings=ModelSettings(
        max_tokens=8000,
        temperature=0.1
    ),
)

@web_scraping_agent.tool_plain(retries=1)
def fetch_html_text(url: str) -> str:
    """
    Fetches the HTML text from a given URL
    
    args:
        url: str - The page's URL to fetch the HTML text from
        
    returns:
        str: The HTML text from the given URL
    """
    print(f'Calling URL:', url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    with Client(headers=headers) as client:
        response = client.get(url, timeout=20)
        if response.status_code != 200:
            return f'Failed to fetch the HTML text from {url}. Status code: {response.status_code}'
            
        soup = BeautifulSoup(response.text, 'html.parser')
        with open('soup.txt', 'w', encoding='utf-8') as f:
            f.write(soup.get_text())
        print('Soup file saved')
        return soup.get_text().replace('\n', '').replace('\r', '')

@web_scraping_agent.result_validator
def validate_result(result: Results) -> Results:
    print('Validating result...')
    if isinstance(result, Results):
        print('Validation passed')
        return result
    print('Validation failed')
    return None
