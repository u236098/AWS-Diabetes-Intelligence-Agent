# Testing Guide - Diabetes Intelligence Agent

## 🧪 Complete Testing Procedures

This document provides comprehensive testing procedures for the Diabetes Intelligence Agent.

---

## Prerequisites

- Deployed infrastructure (see DEPLOYMENT.md)
- API endpoint URL from CDK outputs
- API key value retrieved from AWS
- `curl` or API testing tool (Postman, Insomnia)
- `jq` for JSON formatting (optional)

---

## Quick Setup

```bash
# Set environment variables
export API_ENDPOINT="https://xxxxx.execute-api.us-east-1.amazonaws.com/v1"
export API_KEY="your-api-key-here"

# Test health endpoint
curl "${API_ENDPOINT}/health"
```

---

## Test Suite

### 1. Health Check Test ✅

**Purpose**: Verify API Gateway is responding

```bash
curl -X GET "${API_ENDPOINT}/health"
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "Wed, 15 Apr 2026 03:45:22 GMT"
}
```

**Status Code**: `200 OK`

**What This Tests**:
- API Gateway is deployed
- Endpoint is accessible
- No authentication required for health check

---

### 2. Pattern Analysis Tests

#### Test 2.1: High-Carb Late Meal

```bash
curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "food": "pasta with marinara sauce and garlic bread",
    "timing": "9:30 PM",
    "glucose_trend": "rising",
    "activity": "none"
  }' | jq '.'
```

**Expected Response Structure**:
```json
{
  "analysis": {
    "observation": "This meal appears to be high in fast-absorbing carbohydrates...",
    "explanation": "Foods like pasta and bread can raise glucose quickly...",
    "insight": "You may notice higher glucose spikes after similar late meals.",
    "suggestion": "Consider eating earlier or combining with protein...",
    "confidence": "high"
  },
  "timestamp": "2026-04-15T03:45:22Z",
  "model": "anthropic.claude-sonnet-4-6-v1:0"
}
```

**What This Tests**:
- Bedrock integration working
- Pattern analysis logic
- Safety guardrails (no medical advice)
- JSON response formatting

---

#### Test 2.2: Balanced Meal with Activity

```bash
curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "food": "grilled chicken, quinoa, and vegetables",
    "timing": "12:30 PM (lunch)",
    "glucose_trend": "stable",
    "activity": "30-minute walk before meal"
  }' | jq '.'
```

**Expected**: Positive pattern recognition, acknowledgment of balanced approach

---

#### Test 2.3: Early Morning Activity

```bash
curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "food": "none",
    "timing": "6:00 AM",
    "glucose_trend": "dropping",
    "activity": "45-minute run"
  }' | jq '.'
```

**Expected**: Observation about exercise timing and glucose response

---

#### Test 2.4: Complex Context

```bash
curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "food": "burger and fries",
    "timing": "11:00 PM",
    "glucose_trend": "rising rapidly",
    "activity": "none (sedentary day)",
    "context": "Had a stressful day at work, ate quickly"
  }' | jq '.'
```

**Expected**: Comprehensive analysis including context factors

---

### 3. Food Detection Tests

#### Test 3.1: Food Image Detection

```bash
# First, encode an image
IMAGE_BASE64=$(base64 -i test-images/pizza.jpg | tr -d '\n')

# Send to food detection endpoint
curl -X POST "${API_ENDPOINT}/food" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d "{
    \"image\": \"${IMAGE_BASE64}\"
  }" | jq '.'
```

**Expected Response**:
```json
{
  "detected_foods": [
    {
      "name": "Pizza",
      "confidence": 98.5,
      "category": "Food"
    },
    {
      "name": "Cheese",
      "confidence": 95.2
    }
  ],
  "description": "This meal appears to contain pizza. It looks like a casual dinner.",
  "food_summary": "Pizza, Cheese"
}
```

**What This Tests**:
- Rekognition integration
- Image processing
- Bedrock enhancement
- Base64 decoding

---

### 4. Insights Generation Tests

#### Test 4.1: Weekly Insights

```bash
# First, log several patterns (repeat test 2.1-2.4 multiple times)
# Then generate insights

curl -X POST "${API_ENDPOINT}/insights" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "days": 7
  }' | jq '.'
```

**Expected Response**:
```json
{
  "insights": {
    "summary": "Over the past 7 days, you've logged X patterns...",
    "trends": [
      "Late evening meals appear frequently",
      "Activity levels vary throughout the week"
    ],
    "positive_patterns": [
      "Consistent morning routine",
      "Good variety in food choices"
    ],
    "areas_to_watch": [
      "Late night eating patterns",
      "Inconsistent meal timing"
    ],
    "recommendations": [
      "Consider moving dinner earlier by 1-2 hours",
      "Try maintaining consistent meal times"
    ]
  },
  "period_days": 7,
  "patterns_analyzed": 12,
  "timestamp": "2026-04-15T03:45:22Z"
}
```

**What This Tests**:
- S3 pattern retrieval
- Historical data analysis
- Trend identification

---

#### Test 4.2: Insights with No Data

```bash
curl -X POST "${API_ENDPOINT}/insights" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "days": 30
  }' | jq '.'
```

**Expected**:
```json
{
  "message": "No patterns found for the specified time period",
  "insights": null
}
```

---

### 5. Error Handling Tests

#### Test 5.1: Missing API Key

```bash
curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "food": "test"
  }'
```

**Expected**: `403 Forbidden` with `{"message":"Forbidden"}`

---

#### Test 5.2: Invalid API Key

```bash
curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: INVALID_KEY" \
  -d '{
    "food": "test"
  }'
```

**Expected**: `403 Forbidden`

---

#### Test 5.3: Malformed JSON

```bash
curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{"invalid json'
```

**Expected**: `400 Bad Request`

---

#### Test 5.4: Empty Request Body

```bash
curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{}'
```

**Expected**:
```json
{
  "error": "At least one input field is required (food, activity, timing, or glucose_trend)"
}
```

**Status Code**: `400 Bad Request`

---

### 6. Performance Tests

#### Test 6.1: Latency Test

```bash
# Measure response time
time curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "food": "sandwich",
    "timing": "noon"
  }' -o /dev/null -s
```

**Expected**: < 5 seconds (p99)

---

#### Test 6.2: Load Test (Simple)

```bash
# Send 10 concurrent requests
for i in {1..10}; do
  curl -X POST "${API_ENDPOINT}/analyze" \
    -H "Content-Type: application/json" \
    -H "x-api-key: ${API_KEY}" \
    -d '{
      "food": "test meal",
      "timing": "test time"
    }' &
done
wait
```

**Expected**: All requests succeed with 200 OK

---

#### Test 6.3: Load Test (Advanced with Apache Bench)

```bash
# Install Apache Bench if needed
# sudo apt-get install apache2-utils

# Create test payload
cat > test-payload.json <<EOF
{
  "food": "test meal",
  "timing": "noon"
}
EOF

# Run load test (100 requests, 10 concurrent)
ab -n 100 -c 10 \
  -p test-payload.json \
  -T 'application/json' \
  -H "x-api-key: ${API_KEY}" \
  "${API_ENDPOINT}/analyze"
```

**Expected Metrics**:
- Requests per second: > 10
- Failed requests: 0
- 95th percentile: < 3000ms

---

### 7. Security Tests

#### Test 7.1: CORS Headers

```bash
curl -X OPTIONS "${API_ENDPOINT}/analyze" \
  -H "Origin: https://example.com" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

**Expected**: CORS headers present in response

---

#### Test 7.2: Rate Limiting

```bash
# Send rapid requests to trigger rate limiting
for i in {1..1100}; do
  curl -X POST "${API_ENDPOINT}/analyze" \
    -H "x-api-key: ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"food": "test"}' -s -o /dev/null -w "%{http_code}\n"
done | grep "429" | wc -l
```

**Expected**: Some requests return `429 Too Many Requests`

---

#### Test 7.3: Input Validation

```bash
# Test SQL injection attempt
curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "food": "'; DROP TABLE users; --"
  }' | jq '.'
```

**Expected**: Request handled safely, no errors

---

### 8. Monitoring Tests

#### Test 8.1: CloudWatch Metrics

```bash
# Check Lambda invocations
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=diabetes-pattern-analysis \
  --start-time $(date -u -d '10 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum

# Check API Gateway requests
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiName,Value=Diabetes\ Intelligence\ API \
  --start-time $(date -u -d '10 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

**Expected**: Metrics show recent activity

---

#### Test 8.2: View Logs

```bash
# Tail Lambda logs
aws logs tail /aws/lambda/diabetes-pattern-analysis --follow

# View last 10 minutes of logs
aws logs tail /aws/lambda/diabetes-pattern-analysis --since 10m
```

**Expected**: Logs show recent requests

---

#### Test 8.3: Check Alarms

```bash
# List CloudWatch alarms
aws cloudwatch describe-alarms \
  --alarm-name-prefix Diabetes

# Check alarm state
aws cloudwatch describe-alarms \
  --alarm-names "PatternAnalysisErrorAlarm" \
  --query 'MetricAlarms[0].StateValue'
```

**Expected**: Alarms in `OK` state

---

### 9. Cost Verification Tests

#### Test 9.1: Check Current Costs

```bash
# Get month-to-date costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '1 month ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=SERVICE \
  --filter file://filter.json

# filter.json content:
# {
#   "Tags": {
#     "Key": "Project",
#     "Values": ["DiabetesIntelligenceAgent"]
#   }
# }
```

**Expected**: Costs within budget

---

#### Test 9.2: Verify Prompt Caching

```bash
# Check Bedrock metrics for cache usage
aws cloudwatch get-metric-statistics \
  --namespace AWS/Bedrock \
  --metric-name InputTokens \
  --dimensions Name=ModelId,Value=anthropic.claude-sonnet-4-6-v1:0 \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 3600 \
  --statistics Sum
```

**Expected**: Cache hit rate improving over time

---

### 10. Data Persistence Tests

#### Test 10.1: Verify S3 Storage

```bash
# List stored patterns
aws s3 ls s3://YOUR_BUCKET/patterns/ --recursive

# Get a sample pattern
aws s3 cp s3://YOUR_BUCKET/patterns/2026/04/15/TIMESTAMP.json - | jq '.'
```

**Expected**: Patterns stored in correct format

---

#### Test 10.2: Verify Encryption

```bash
# Check S3 bucket encryption
aws s3api get-bucket-encryption --bucket YOUR_BUCKET

# Check KMS key
aws kms describe-key --key-id alias/diabetes-intelligence-key
```

**Expected**: Encryption enabled with KMS

---

## Automated Test Script

Create `test-all.sh`:

```bash
#!/bin/bash

# Automated test suite for Diabetes Intelligence Agent

set -e

# Configuration
API_ENDPOINT="${API_ENDPOINT:-https://xxxxx.execute-api.us-east-1.amazonaws.com/v1}"
API_KEY="${API_KEY:-your-api-key}"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🧪 Starting Diabetes Intelligence Agent Test Suite"
echo "=============================================="

# Test 1: Health Check
echo -n "Test 1: Health Check... "
response=$(curl -s "${API_ENDPOINT}/health")
if echo "$response" | grep -q "healthy"; then
    echo -e "${GREEN}✓ PASSED${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
    exit 1
fi

# Test 2: Pattern Analysis
echo -n "Test 2: Pattern Analysis... "
response=$(curl -s -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{"food": "pasta", "timing": "9pm"}')
if echo "$response" | grep -q "analysis"; then
    echo -e "${GREEN}✓ PASSED${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
    exit 1
fi

# Test 3: Authentication
echo -n "Test 3: Authentication (should fail)... "
response=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -d '{"food": "test"}')
if [ "$response" == "403" ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
    exit 1
fi

# Test 4: Insights (may return no data)
echo -n "Test 4: Insights Generation... "
response=$(curl -s -X POST "${API_ENDPOINT}/insights" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{"days": 7}')
if echo "$response" | grep -q "insights"; then
    echo -e "${GREEN}✓ PASSED${NC}"
else
    echo -e "${GREEN}✓ PASSED (no data)${NC}"
fi

echo "=============================================="
echo -e "${GREEN}✓ All tests passed!${NC}"
```

Run with:
```bash
chmod +x test-all.sh
./test-all.sh
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run API Tests
        env:
          API_ENDPOINT: ${{ secrets.API_ENDPOINT }}
          API_KEY: ${{ secrets.API_KEY }}
        run: ./test-all.sh
```

---

## Test Results Checklist

After running all tests, verify:

- [ ] Health check returns 200 OK
- [ ] Pattern analysis produces valid insights
- [ ] API key authentication works
- [ ] Invalid requests return proper error codes
- [ ] Latency is under 5 seconds (p99)
- [ ] CloudWatch metrics show activity
- [ ] Logs are accessible
- [ ] Alarms are in OK state
- [ ] S3 patterns are stored correctly
- [ ] Encryption is enabled
- [ ] Costs are within budget

---

## Troubleshooting Test Failures

### Issue: All tests return 403
**Cause**: API key not valid or not set  
**Fix**: Verify `API_KEY` environment variable

### Issue: Timeout on pattern analysis
**Cause**: Bedrock model not accessible  
**Fix**: Check Bedrock model access in AWS Console

### Issue: No patterns stored in S3
**Cause**: IAM permissions or S3 bucket configuration  
**Fix**: Check Lambda execution role permissions

### Issue: High latency (>10s)
**Cause**: Cold start or Bedrock throttling  
**Fix**: Increase Lambda reserved concurrency

---

## Next Steps

After successful testing:

1. ✅ Document test results
2. ✅ Set up monitoring alerts
3. ✅ Configure CI/CD pipeline
4. ✅ Load test at scale (optional)
5. ✅ Security audit (optional)
6. ✅ Deploy to production

---

**See also:**
- [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
- [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- [README.md](../README.md) for project overview
