"""
Insight Generator Lambda Function
Generates personalized insights from historical patterns.
"""

import json
import os
import logging
import boto3
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Configure logging
logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

# Initialize AWS clients
bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
s3_client = boto3.client('s3')

# Environment variables
DATA_BUCKET = os.environ.get('DATA_BUCKET')
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-sonnet-4-6-v1:0')

# System prompt for insight generation
SYSTEM_PROMPT = """You are an AI assistant that helps users understand their lifestyle patterns over time.

Your role is to:
1. Analyze historical pattern data
2. Identify trends and recurring behaviors
3. Generate actionable, non-medical insights
4. Highlight positive patterns and areas for improvement

Response format (JSON):
{
  "summary": "Brief summary of patterns over the time period",
  "trends": ["List of observed trends"],
  "positive_patterns": ["Behaviors that are working well"],
  "areas_to_watch": ["Patterns that may need attention"],
  "recommendations": ["Safe, general suggestions for improvement"]
}

Remember:
- Do NOT provide medical advice
- Focus on lifestyle patterns, not clinical outcomes
- Be supportive and encouraging
- Use probabilistic language ("may", "could", "likely")
"""


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for insight generation.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response with insights
    """
    try:
        logger.info(f"Received event: {json.dumps(event)}")

        # Parse request body
        body = json.loads(event.get('body', '{}'))

        # Get time range for insights (default: last 7 days)
        days = body.get('days', 7)

        # Retrieve historical patterns from S3
        patterns = retrieve_patterns(days)

        if not patterns:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'No patterns found for the specified time period',
                    'insights': None
                })
            }

        # Generate insights using Bedrock
        insights = generate_insights(patterns)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'insights': insights,
                'period_days': days,
                'patterns_analyzed': len(patterns),
                'timestamp': datetime.utcnow().isoformat()
            })
        }

    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}", exc_info=True)
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


def retrieve_patterns(days: int) -> List[Dict[str, Any]]:
    """Retrieve pattern data from S3 for the specified time period."""
    patterns = []

    if not DATA_BUCKET:
        logger.warning("DATA_BUCKET not configured, skipping pattern retrieval")
        return patterns

    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # List objects in the date range
        current_date = start_date
        while current_date <= end_date:
            date_prefix = current_date.strftime('%Y/%m/%d')
            prefix = f"patterns/{date_prefix}/"

            try:
                response = s3_client.list_objects_v2(
                    Bucket=DATA_BUCKET,
                    Prefix=prefix
                )

                for obj in response.get('Contents', []):
                    # Retrieve and parse each pattern
                    pattern_obj = s3_client.get_object(
                        Bucket=DATA_BUCKET,
                        Key=obj['Key']
                    )
                    pattern_data = json.loads(pattern_obj['Body'].read())
                    patterns.append(pattern_data)

            except Exception as e:
                logger.warning(f"Error retrieving patterns for {date_prefix}: {str(e)}")

            current_date += timedelta(days=1)

        logger.info(f"Retrieved {len(patterns)} patterns from S3")

    except Exception as e:
        logger.error(f"Error retrieving patterns: {str(e)}", exc_info=True)

    return patterns


def generate_insights(patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate insights using Bedrock based on historical patterns."""

    # Summarize patterns for Bedrock
    pattern_summary = summarize_patterns(patterns)

    user_prompt = f"""Analyze the following lifestyle patterns and generate insights:

Number of patterns: {len(patterns)}
Time period: Last {len(patterns)} records

Pattern Summary:
{json.dumps(pattern_summary, indent=2)}

Generate insights based on these patterns."""

    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1500,
        "temperature": 0.7,
        "system": [
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"}
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

        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {
                "summary": response_text,
                "trends": [],
                "positive_patterns": [],
                "areas_to_watch": [],
                "recommendations": []
            }

    return {}


def summarize_patterns(patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a summary of patterns for analysis."""
    summary = {
        'total_patterns': len(patterns),
        'food_entries': 0,
        'activity_entries': 0,
        'common_foods': [],
        'common_activities': [],
        'timing_distribution': {
            'morning': 0,
            'afternoon': 0,
            'evening': 0,
            'night': 0
        }
    }

    foods = []
    activities = []

    for pattern in patterns:
        user_input = pattern.get('input', {})

        if user_input.get('food'):
            summary['food_entries'] += 1
            foods.append(user_input['food'])

        if user_input.get('activity'):
            summary['activity_entries'] += 1
            activities.append(user_input['activity'])

        # Categorize timing
        timing = user_input.get('timing', '').lower()
        if any(word in timing for word in ['morning', 'breakfast', 'am']):
            summary['timing_distribution']['morning'] += 1
        elif any(word in timing for word in ['afternoon', 'lunch', 'noon']):
            summary['timing_distribution']['afternoon'] += 1
        elif any(word in timing for word in ['evening', 'dinner', 'pm']):
            summary['timing_distribution']['evening'] += 1
        elif any(word in timing for word in ['night', 'late', 'midnight']):
            summary['timing_distribution']['night'] += 1

    # Get most common items (simple frequency)
    if foods:
        summary['common_foods'] = list(set(foods))[:5]
    if activities:
        summary['common_activities'] = list(set(activities))[:5]

    return summary
