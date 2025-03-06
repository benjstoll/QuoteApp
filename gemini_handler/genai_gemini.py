from json import loads, JSONDecodeError
from google import genai
from pydantic import BaseModel


class QuoteSchema(BaseModel):
    quote: str


class GenAi:
    def __init__(self, api_key, prompt):
        self.prompt = prompt

        self.schema = {
            'response_mime_type': 'application/json',
            'response_schema': QuoteSchema
        }

        self.client = genai.Client(api_key=api_key)
        

    # Ensure Gemini's output is proper.
    def validate_json(self, json_dump):
        try:
            # Try parsing the JSON string
            loads(json_dump)
        except JSONDecodeError as e:
            return None

        return(json_dump)    


    # Ask Gemeni for a quote.
    def generate_quote(self, attempts=0):
        if attempts > 2:
            return None

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=self.prompt,
            config=self.schema,
        )
        json_text = self.validate_json(response.text)

        if not json_text:
            self.generate_quote(attempts+1)

        return json_text
    

if __name__ == '__main__':
    api_key = None ### Replace with your API key for prompt tuning
    prompt = 'Generate a quote that is no longer than 30 words in length. The content can either be silly, nonsensical, inspirational, or passive aggressive. Choose only one of these at your discretion.'
    gai = GenAi(api_key, prompt)
    print(gai.generate_quote())