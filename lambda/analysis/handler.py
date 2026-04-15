"""
Pattern Analysis Lambda Function
Analyzes lifestyle signals and detects behavioral patterns for diabetes management.
"""

import json
import os
import logging
import boto3
from datetime import datetime
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

# Initialize AWS clients
bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
s3_client = boto3.client('s3')

# Environment variables
DATA_BUCKET = os.environ.get('DATA_BUCKET')
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-sonnet-4-6-v1:0')

# System prompt for pattern analysis (will be cached)
SYSTEM_PROMPT = """You are an AI assistant designed to help users understand patterns in their daily lifestyle related to diabetes management.

Your role is NOT to provide medical advice, diagnosis, or insulin recommendations.

Your role is to:
1. Analyze simple user inputs such as:
   - food (text or image description)
   - activity (exercise type, duration)
   - timing (time of day)
   - glucose trend (if provided, e.g., rising, stable, dropping)

2. Identify simple, human-understandable patterns such as:
   - meals that may lead to faster glucose spikes
   - timing-related effects (late meals, early workouts)
   - lifestyle consistency or irregularity

3. Explain the pattern clearly in plain language.

4. Provide safe, general suggestions such as:
   - timing adjustments
   - food composition ideas (e.g., adding protein/fiber)
   - observation suggestions (e.g., "monitor how this affects you next time")

You must follow these rules:
- Do NOT calculate insulin doses
- Do NOT provide medical or clinical recommendations
- Do NOT claim certainty — always use probabilistic language (e.g., "may", "likely")
- Use a supportive, non-judgmental tone

Response format (JSON):
{
  "observation": "What was detected from the input",
  "explanation": "Why this may happen (simple reasoning)",
  "insight": "What the user can take away",
  "suggestion": "Simple, safe, non-medical advice",
  "confidence": "low|medium|high"
}
"""


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for pattern analysis.

    Args:
        event: API Gateway event containing user input
        context: Lambda context

    Returns:
        API Gateway response with pattern analysis
    """
    try:
        logger.info(f"Received event: {json.dumps(event)}")

        # Parse request body
        body = json.loads(event.get('body', '{}'))

        # Extract input parameters
        food = body.get('food', '')
        activity = body.get('activity', '')
        timing = body.get('timing', '')
        glucose_trend = body.get('glucose_trend', '')
        additional_context = body.get('context', '')

        # Validate input
        if not any([food, activity, timing, glucose_trend]):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'At least one input field is required (food, activity, timing, or glucose_trend)'
                })
            }

        # Construct user prompt
        user_prompt = construct_user_prompt(food, activity, timing, glucose_trend, additional_context)

        logger.info(f"Calling Bedrock with prompt: {user_prompt}")

        # Call Bedrock for pattern analysis
        analysis_result = call_bedrock(user_prompt)

        # Store pattern in S3 (anonymized)
        if DATA_BUCKET:
            store_pattern(body, analysis_result)

        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'analysis': analysis_result,
                'timestamp': datetime.utcnow().isoformat(),
                'model': BEDROCK_MODEL_ID
            })
        }

    except Exception as e:
        logger.error(f"Error in pattern analysis: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }


def construct_user_prompt(food: str, activity: str, timing: str, glucose_trend: str, context: str) -> str:
    """Construct user prompt from input parameters."""
    prompt_parts = []

    if food:
        prompt_parts.append(f"Food: {food}")
    if activity:
        prompt_parts.append(f"Activity: {activity}")
    if timing:
        prompt_parts.append(f"Time: {timing}")
    if glucose_trend:
        prompt_parts.append(f"Glucose trend: {glucose_trend}")
    if context:
        prompt_parts.append(f"Additional context: {context}")

    return "\n".join(prompt_parts)


def call_bedrock(user_prompt: str) -> Dict[str, Any]:
    """
    Call Amazon Bedrock with Claude for pattern analysis.
    Uses prompt caching for cost optimization.
    """
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.7,
        "system": [
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"}  # Enable prompt caching
            }
        ],
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }

    response = bedrock_runtime.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=json.dumps(request_body)
    )

    response_body = json.loads(response['body'].read())

    # Extract the response text
    content = response_body.get('content', [])
    if content and len(content) > 0:
        response_text = content[0].get('text', '{}')

        # Parse JSON response
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            # If response is not JSON, wrap it
            return {
                "observation": response_text,
                "explanation": "",
                "insight": "",
                "suggestion": "",
                "confidence": "medium"
            }

    return {}


def store_pattern(user_input: Dict[str, Any], analysis: Dict[str, Any]) -> None:
    """Store anonymized pattern data in S3 for future analysis."""
    try:
        timestamp = datetime.utcnow().isoformat()
        date_prefix = datetime.utcnow().strftime('%Y/%m/%d')

        # Remove any PII (if accidentally included)
        sanitized_input = {k: v for k, v in user_input.items() if k not in ['email', 'name', 'user_id']}

        # Create pattern record
        pattern_record = {
            'timestamp': timestamp,
            'input': sanitized_input,
            'analysis': analysis
        }

        # Store in S3
        key = f"patterns/{date_prefix}/{timestamp}.json"
        s3_client.put_object(
            Bucket=DATA_BUCKET,
            Key=key,
            Body=json.dumps(pattern_record),
            ContentType='application/json'
        )

        logger.info(f"Stored pattern in S3: {key}")

    except Exception as e:
        logger.warning(f"Failed to store pattern in S3: {str(e)}")
        # Don't fail the request if storage fails
