"""
Food Detection Lambda Function
Detects food items from images using Amazon Rekognition.
"""

import json
import os
import logging
import boto3
import base64
from typing import Dict, Any, List

# Configure logging
logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

# Initialize AWS clients
rekognition_client = boto3.client('rekognition', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

# Environment variables
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-sonnet-4-6-v1:0')

# Confidence threshold for food detection
CONFIDENCE_THRESHOLD = 70.0


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for food detection.

    Args:
        event: API Gateway event containing image data
        context: Lambda context

    Returns:
        API Gateway response with detected food items
    """
    try:
        logger.info(f"Received food detection request")

        # Parse request body
        body = json.loads(event.get('body', '{}'))

        # Get image data (base64 encoded)
        image_data = body.get('image')
        image_url = body.get('image_url')

        if not image_data and not image_url:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Either "image" (base64) or "image_url" is required'
                })
            }

        # Detect labels using Rekognition
        if image_data:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            labels = detect_labels_from_bytes(image_bytes)
        else:
            # For URL-based images, you'd need to download first
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'URL-based detection not yet implemented. Please use base64 encoded images.'
                })
            }

        # Filter food-related labels
        food_items = filter_food_labels(labels)

        if not food_items:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'detected_foods': [],
                    'message': 'No food items detected in the image',
                    'all_labels': [label['Name'] for label in labels]
                })
            }

        # Enhance food description using Bedrock
        enhanced_description = enhance_food_description(food_items)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'detected_foods': food_items,
                'description': enhanced_description,
                'food_summary': ', '.join([item['name'] for item in food_items])
            })
        }

    except Exception as e:
        logger.error(f"Error in food detection: {str(e)}", exc_info=True)
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


def detect_labels_from_bytes(image_bytes: bytes) -> List[Dict[str, Any]]:
    """Detect labels in an image using Amazon Rekognition."""
    response = rekognition_client.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=20,
        MinConfidence=CONFIDENCE_THRESHOLD
    )

    labels = response.get('Labels', [])
    logger.info(f"Detected {len(labels)} labels from Rekognition")

    return labels


def filter_food_labels(labels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter labels to identify food-related items."""
    # Common food-related categories
    food_categories = {
        'Food', 'Meal', 'Dish', 'Cuisine', 'Dessert', 'Beverage',
        'Fruit', 'Vegetable', 'Bread', 'Breakfast', 'Lunch', 'Dinner',
        'Snack', 'Pizza', 'Pasta', 'Salad', 'Burger', 'Sandwich'
    }

    food_items = []

    for label in labels:
        label_name = label.get('Name', '')
        confidence = label.get('Confidence', 0)

        # Check if label is food-related
        if label_name in food_categories:
            food_items.append({
                'name': label_name,
                'confidence': round(confidence, 2)
            })
            continue

        # Check parent categories
        parents = label.get('Parents', [])
        for parent in parents:
            if parent.get('Name') in food_categories:
                food_items.append({
                    'name': label_name,
                    'confidence': round(confidence, 2),
                    'category': parent.get('Name')
                })
                break

    # Sort by confidence
    food_items.sort(key=lambda x: x['confidence'], reverse=True)

    return food_items


def enhance_food_description(food_items: List[Dict[str, Any]]) -> str:
    """Use Bedrock to create a natural food description."""
    food_names = [item['name'] for item in food_items[:5]]  # Top 5 items

    prompt = f"""Based on these detected food items: {', '.join(food_names)}

Create a brief, natural description of this meal in 1-2 sentences. Focus on what the meal contains, not detailed nutrition information.

Example format: "This meal appears to contain [food items]. It looks like [meal type]."

Keep it simple and conversational."""

    try:
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 150,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = bedrock_runtime.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body)
        )

        response_body = json.loads(response['body'].read())
        content = response_body.get('content', [])

        if content and len(content) > 0:
            return content[0].get('text', ', '.join(food_names))

    except Exception as e:
        logger.warning(f"Error enhancing description with Bedrock: {str(e)}")

    # Fallback to simple description
    return f"Detected: {', '.join(food_names)}"
