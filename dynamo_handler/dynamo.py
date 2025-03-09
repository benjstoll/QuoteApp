import boto3
from botocore.exceptions import ClientError
from os import getenv

class DynamoDb:
    def __init__(self, table_name='words_to_live_by'):
        aws_access_key = getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = getenv("AWS_REGION", "us-east-2")
        table_name = getenv("TABLE_NAME", table_name)

        # Initialize the DynamoDB resource and the table
        self.dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region,  # Ensure the region is set
        
        )
        self.table = self.dynamodb.Table(table_name)


    def insert_quote(self, quote_id, quote):
        """Insert a new quote into the DynamoDB table."""
        try:
            response = self.table.put_item(
                Item={
                    'quote_id': quote_id,
                    'quote': quote
                }
            )
            return response
        except ClientError as e:
            print(f"Error inserting quote: {e}")
            return None


    def get_quote_count(self):
        """Retrieve the count of current entries in the DynamoDB table."""
        try:
            response = self.table.scan()
            return len(response.get('Items', []))  # Return the count of items
        except ClientError as e:
            print(f"Error retrieving quote count: {e}")
            return 0


    def clear_all_quotes(self):
        """Clear all quotes from the DynamoDB table."""
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            for item in items:
                self.table.delete_item(
                    Key={'quote_id': item['quote_id']}
                )
            return f"Deleted {len(items)} items."
        except ClientError as e:
            print(f"Error clearing quotes: {e}")
            return None
        

    def get_last_quote(self, quote_id):
        """Retrieve the last quote by its quote_id with error handling."""
        try:
            # Try to get the item from DynamoDB using the partition key (quote_id)
            response = self.table.get_item(Key={"quote_id": quote_id})
            
            # Check if the item is present in the response
            if 'Item' in response:
                return response['Item']['quote']
            else:
                print(f"Quote with quote_id {quote_id} not found.")
                return None
        except ClientError as e:
            # Handle DynamoDB client errors
            print(f"Error retrieving quote: {e.response['Error']['Message']}")
            return None
        except KeyError as e:
            # Catch cases where the 'quote' field is missing
            print(f"Error: Missing field 'quote' in the response for quote_id {quote_id}.")
            return None
        except Exception as e:
            # Catch all other exceptions
            print(f"Unexpected error occurred: {str(e)}")
            return None
        

if __name__ == '__main__':
    # Initialize the DynamoDb class
    db = DynamoDb()

    # Insert a new quote
    db.insert_quote(quote_id=1, quote="The only limit to our realization of tomorrow is our doubts of today.")

    print(db.get_last_quote(1))

    # Retrieve the count of quotes
    count = db.get_quote_count()
    print(f"Number of quotes: {count}")

    # Clear all quotes
    result = db.clear_all_quotes()
    print(result)

    count = db.get_quote_count()
    print(f"Number of quotes: {count}")
