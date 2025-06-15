import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Parse an event from either API Gateway or direct Lambda invocation
    
    Args:
        event (dict): The event to parse, either from API Gateway or direct Lambda
        context (LambdaContext): Lambda context object
        
    Returns:
        dict: Response containing status code and parsed data
        {
            "statusCode": int,
            "body": dict
        }
    """
    try:
        parsed_data = {}
        
        # Check if this is an API Gateway event
        if 'body' in event:
            # Parse the body if it's a string
            if isinstance(event['body'], str):
                try:
                    parsed_data.update(json.loads(event['body']))
                except json.JSONDecodeError:
                    # If body is not JSON, use it as is
                    parsed_data['body'] = event['body']
            else:
                parsed_data.update(event['body'])
                
            # Handle cookies from API Gateway
            if 'headers' in event and 'Cookie' in event['headers']:
                cookies = event['headers']['Cookie']
                # Parse cookies into a dictionary
                cookie_dict = dict(
                    cookie.split('=', 1) for cookie in cookies.split('; ')
                )
                parsed_data.update(cookie_dict)
                
        else:
            # Direct Lambda invocation - use event as is
            parsed_data.update(event)
            
        return {
            "statusCode": 200,
            "body": parsed_data
        }
        
    except Exception as e:
        logger.error(f"Error parsing event: {str(e)}")
        return {
            "statusCode": 400,
            "body": {
                "error": "Failed to parse event",
                "message": str(e)
            }
        }
