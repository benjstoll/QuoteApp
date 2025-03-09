from json import loads, JSONDecodeError
from google import genai
from pydantic import BaseModel
from os import environ

import logging
logger = logging.getLogger(__name__)


class QuoteSchema(BaseModel):
    quote: str


class GenAi:
    def __init__(self, api_key, prompt):
        self.prompt = prompt
        self.history = []

        if not environ['GEMINI_API_KEY']:
            logger.error('Please set up GEMINI_API_KEY in environment variables.')
            exit(1)

        logger.info('Attempting to start client with Gemini...')
        try: 
            self.schema = {
                'response_mime_type': 'application/json',
                'response_schema': QuoteSchema,
                'temperature': 0.5,
                'top_p': 0.7
            }

            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            logger.error('Initialization failed with Gemini, exiting...')
            logger.error(e)
            exit(1)

        
    # Ensure Gemini's output is proper.
    def validate_json(self, json_dump):
        logger.info('Validating Gemini\'s output...')
        try:
            # Try parsing the JSON string
            json_dump = loads(json_dump)
            logger.info('Output valid, returning...')
        except JSONDecodeError as e:
            logger.error('Output invalid, will attempt again...')
            logger.error(e)
            return None

        return(json_dump)    


    # Ask Gemeni for a quote.
    def generate_quote(self, attempts=0):
        if attempts > 2:
            return None
        
        prompt_with_context = self.prompt + ' ' + str(self.history)

        logger.info('Sending prompt to Gemini...')
        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt_with_context,
            config=self.schema,
        )
        json_text = self.validate_json(response.text)

        if not json_text and attempts < 3:
            logger.error(f'Attempt Count: {attempts+1}')
            self.generate_quote(attempts+1)


        if len(self.history) == 15:
            self.history.pop(0)
        
        self.history.append(json_text)
        return json_text
    

if __name__ == '__main__':
    api_key = None ### Replace with your API key for prompt tuning
    prompt = 'Generate a quote that is no longer than 30 words in length. The content can either be silly, nonsensical, inspirational, or passive aggressive. Choose only one of these at your discretion.'
    gai = GenAi(api_key, prompt)
    print(gai.generate_quote())