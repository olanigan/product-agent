from scrapers import web_scraping_agent
from pydantic_ai.exceptions import UnexpectedModelBehavior
import datetime
import pandas as pd
import sys

def main() -> None:
    if len(sys.argv) < 2:
        print("Please provide URLs as command line arguments, separated by commas")
        print("Example: python hello.py https://www.ikea.com/url1,https://www.ikea.com/url2")
        return

    urls = sys.argv[1].split(',')
    
    for prompt in urls:
        prompt = prompt.strip()
        try:
            response = web_scraping_agent.run_sync(prompt)
            if response.data is None:
                raise UnexpectedModelBehavior('No data returned from the model')
                continue
                
            print('-' * 50)
            print(f'Processing URL: {prompt}')
            print('Input tokens:', response.usage().request_tokens)
            print('Output tokens:', response.usage().response_tokens)
            print('Total tokens:', response.usage().total_tokens)
            
            lst = []
            for item in response.data.dataset:
                lst.append(item.model_dump())
                
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            df = pd.DataFrame(lst)
            category = response.data.category
            df.to_csv(f'files/{category}_listings_{timestamp}.csv', index=False)
        except UnexpectedModelBehavior as e:
            print(f'Error processing {prompt}: {e}')


if __name__ == "__main__":
    main()
