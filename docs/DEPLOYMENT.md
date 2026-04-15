# Diabetes Intelligence Agent - Deployment Guide

## 📋 Prerequisites

Before deploying this solution, ensure you have the following:

### Required Tools:
- **AWS CLI** (v2.0 or later) - [Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- **Node.js** (v18 or later) - [Download](https://nodejs.org/)
- **npm** (v9 or later) - Comes with Node.js
- **Python** (v3.12 or later) - [Download](https://www.python.org/downloads/)
- **pip** (Python package manager)
- **AWS CDK** (v2.147.0 or later)

### AWS Account Requirements:
- Active AWS Account
- IAM user with Administrator access (or equivalent permissions)
- AWS credentials configured locally
- Service quotas for:
  - Lambda: 100+ concurrent executions
  - API Gateway: 10,000 requests/second
  - Bedrock: Access to Claude models

### AWS Services Access:
⚠️ **CRITICAL**: Ensure you have access to **Amazon Bedrock** in your AWS region:
1. Go to AWS Console → Bedrock
2. Click "Model access" in left sidebar
3. Request access to "Anthropic Claude" models
4. Wait for approval (usually instant)

### Supported Regions:
Amazon Bedrock with Claude is available in:
- `us-east-1` (N. Virginia) ✅ **Recommended**
- `us-west-2` (Oregon)
- `eu-west-1` (Ireland)
- `ap-southeast-1` (Singapore)
- `ap-northeast-1` (Tokyo)

Check [latest availability](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)

---

## 🚀 Quick Start (5 Minutes)

### Option A: Deploy with Kiro IDE or Claude Code (Recommended for Hackathon)

```bash
# Simply paste this prompt into your agentic coding tool:

"Deploy the Diabetes Intelligence Agent to AWS. Follow these steps:
1. Configure AWS credentials
2. Install dependencies
3. Build Lambda layers
4. Bootstrap CDK
5. Deploy all stacks to us-east-1 region
6. Output API endpoint and API key"
```

### Option B: Manual Deployment

Follow the detailed steps below.

---

## 📦 Step-by-Step Deployment

### Step 1: Configure AWS Credentials

```bash
# Configure AWS CLI with your credentials
aws configure

# Enter your AWS Access Key ID, Secret Access Key, and default region
# Recommended region: us-east-1

# Verify configuration
aws sts get-caller-identity

# Export account ID for CDK
export CDK_DEFAULT_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export CDK_DEFAULT_REGION=us-east-1
```

### Step 2: Clone/Navigate to Project

```bash
cd diabetes-intelligence-agent
```

### Step 3: Install Node.js Dependencies

```bash
# Install CDK and application dependencies
npm install

# Verify installation
npm run cdk -- --version
```

### Step 4: Build Lambda Layer

The Lambda layer contains shared dependencies (boto3, aws-xray-sdk):

```bash
# Navigate to layer directory
cd lambda/layer

# Make build script executable
chmod +x build.sh

# Build the layer
./build.sh

# Return to project root
cd ../..
```

### Step 5: Bootstrap CDK (First Time Only)

If this is your first time using CDK in this AWS account/region:

```bash
npm run bootstrap

# This creates an S3 bucket and IAM roles for CDK deployments
```

### Step 6: Synthesize CloudFormation Template (Optional)

Preview what will be deployed:

```bash
npm run synth

# This generates CloudFormation templates in cdk.out/
```

### Step 7: Deploy to AWS

#### Development Environment:

```bash
npm run deploy:dev

# Or with CDK directly:
npx cdk deploy --all --context environment=dev
```

#### Production Environment:

```bash
npm run deploy:prod

# Or with CDK directly:
npx cdk deploy --all --context environment=prod
```

**Deployment takes approximately 3-5 minutes.**

During deployment, you'll see:
- ✅ Creating KMS encryption key
- ✅ Creating S3 bucket
- ✅ Creating Lambda functions
- ✅ Creating API Gateway
- ✅ Setting up CloudWatch monitoring
- ✅ Configuring IAM roles

### Step 8: Retrieve Outputs

After successful deployment, CDK will output important values:

```
Outputs:
DiabetesIntelligenceStack-dev.ApiEndpoint = https://xxxxx.execute-api.us-east-1.amazonaws.com/v1/
DiabetesIntelligenceStack-dev.ApiKeyId = xxxxxxxxxxxxx
DiabetesIntelligenceStack-dev.DataBucketName = diabetes-intelligence-data-xxxx-us-east-1
DiabetesIntelligenceStack-dev.DashboardURL = https://console.aws.amazon.com/cloudwatch/...
```

**Save these values!** You'll need them for testing.

### Step 9: Retrieve API Key Value

The API Key ID is output by CDK, but you need the actual key value:

```bash
# Get API Key value (replace KEY_ID with the output from Step 8)
aws apigateway get-api-key --api-key KEY_ID --include-value --query 'value' --output text
```

**Save this API key securely!** It's required for all API requests.

---

## 🧪 Testing the Deployment

### Test 1: Health Check (No API Key Required)

```bash
# Get your API endpoint from deployment outputs
API_ENDPOINT="https://xxxxx.execute-api.us-east-1.amazonaws.com/v1"

# Test health endpoint
curl "${API_ENDPOINT}/health"

# Expected response:
# {"status": "healthy", "timestamp": "..."}
```

### Test 2: Pattern Analysis

```bash
# Set your API key
API_KEY="your-api-key-from-step-9"

# Test pattern analysis
curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "food": "pasta with marinara sauce",
    "timing": "9:00 PM",
    "glucose_trend": "rising",
    "activity": "none"
  }'

# Expected response:
# {
#   "analysis": {
#     "observation": "This meal appears to be high in fast-absorbing carbohydrates...",
#     "explanation": "...",
#     "insight": "...",
#     "suggestion": "...",
#     "confidence": "high"
#   },
#   "timestamp": "2026-04-15T...",
#   "model": "anthropic.claude-sonnet-4-6-v1:0"
# }
```

### Test 3: Food Detection (with Image)

```bash
# Encode an image to base64
IMAGE_BASE64=$(base64 -i your-food-image.jpg)

# Send to food detection endpoint
curl -X POST "${API_ENDPOINT}/food" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d "{
    \"image\": \"${IMAGE_BASE64}\"
  }"
```

### Test 4: Generate Insights

```bash
# After logging several patterns, generate insights
curl -X POST "${API_ENDPOINT}/insights" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "days": 7
  }'
```

---

## 📊 Monitoring

### CloudWatch Dashboard

1. Go to AWS Console → CloudWatch
2. Click "Dashboards" → "Diabetes-Intelligence-Agent"
3. View real-time metrics:
   - API request count
   - Lambda invocations
   - Error rates
   - Latency

Or use the direct link from deployment outputs.

### CloudWatch Logs

```bash
# View Lambda function logs
aws logs tail /aws/lambda/diabetes-pattern-analysis --follow

# View API Gateway logs
aws logs tail API-Gateway-Execution-Logs_xxxxx/v1 --follow
```

### X-Ray Tracing (Production Only)

```bash
# View service map
aws xray get-service-graph --start-time $(date -u -d '1 hour ago' +%s) --end-time $(date +%s)
```

---

## 💰 Cost Estimation

### Expected Monthly Costs (1,000 daily active users):

| Service | Usage | Cost |
|---------|-------|------|
| API Gateway | 30K requests | $0.11 |
| Lambda (3 functions) | 90K invocations, 1GB, 5s avg | $1.65 |
| Bedrock (Claude Sonnet) | 30K requests with caching | $45-75 |
| S3 | 10GB storage, 30K writes | $0.35 |
| CloudWatch | Logs + Metrics | $5.00 |
| Data Transfer | Minimal | $1.00 |
| **Total** | | **~$53-83/month** |

### Free Tier Eligible (First 12 Months):
- Lambda: 1M requests/month free
- API Gateway: 1M requests/month free
- S3: 5GB storage free
- CloudWatch: 10 custom metrics free

### Cost Optimization Tips:

1. **Prompt Caching**: Reduces Bedrock costs by 90% (already enabled)
2. **Lambda Memory**: Adjust in `bin/app.ts` if needed
3. **Log Retention**: Currently 7 days (dev) / 30 days (prod)
4. **S3 Lifecycle**: Automatic deletion after 30 days
5. **Budget Alerts**: Automatically configured

---

## 🔒 Security Best Practices

### Post-Deployment Security Checklist:

- [ ] **Rotate API Keys regularly** (every 90 days)
- [ ] **Restrict API Origins** - Update CORS in `lib/diabetes-intelligence-stack.ts`
- [ ] **Enable WAF** (optional) - Add AWS WAF for API Gateway
- [ ] **Monitor CloudTrail** - Review API access logs
- [ ] **Set up Alerts** - Add email to SNS topic for alerts
- [ ] **Enable MFA** - For AWS Console access
- [ ] **Review IAM Policies** - Ensure least privilege
- [ ] **Encrypt S3 Bucket** - Already enabled with KMS
- [ ] **Enable GuardDuty** (optional) - Threat detection

### API Key Management:

```bash
# Create additional API keys
aws apigateway create-api-key \
  --name "diabetes-intelligence-mobile-app" \
  --enabled

# Revoke compromised key
aws apigateway delete-api-key --api-key-id KEY_ID
```

---

## 🔧 Troubleshooting

### Issue 1: CDK Bootstrap Failed

**Error**: `No bootstrap stack`

**Solution**:
```bash
npx cdk bootstrap aws://ACCOUNT_ID/REGION
```

### Issue 2: Bedrock Access Denied

**Error**: `AccessDeniedException: Could not access model`

**Solution**:
1. Go to AWS Console → Bedrock → Model access
2. Enable "Anthropic Claude" models
3. Wait for approval (usually instant)

### Issue 3: Lambda Layer Build Failed

**Error**: `pip: command not found`

**Solution**:
```bash
# Install Python and pip
# macOS:
brew install python3

# Ubuntu/Debian:
sudo apt-get install python3-pip

# Windows:
# Download from python.org
```

### Issue 4: API Gateway 403 Forbidden

**Error**: `{"message":"Forbidden"}`

**Solution**:
- Verify you're including `x-api-key` header
- Check API key value is correct
- Ensure API key is associated with usage plan

### Issue 5: Lambda Timeout

**Error**: `Task timed out after 60 seconds`

**Solution**:
- Increase timeout in `bin/app.ts` (lambdaTimeout)
- Check Bedrock model availability
- Review Lambda logs for root cause

### Issue 6: High Costs

**Problem**: Unexpected AWS bill

**Solution**:
```bash
# Check current month spending
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '1 month ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=SERVICE

# Destroy stack if needed
npm run destroy
```

---

## 🔄 Updates and Maintenance

### Update Lambda Functions:

```bash
# After modifying Lambda code
npm run deploy:dev

# CDK automatically detects changes and updates only affected resources
```

### Update CDK Stack:

```bash
# After modifying infrastructure
npm run build
npm run deploy:dev
```

### View Deployment Diff:

```bash
# See what will change before deploying
npm run diff
```

---

## 🗑️ Cleanup / Destroy

### Remove All Resources:

```bash
# Destroy the entire stack
npm run destroy

# Confirm when prompted
```

**Note**: S3 buckets with data may fail to delete. Empty them first:

```bash
# Empty S3 bucket
aws s3 rm s3://BUCKET_NAME --recursive

# Then destroy
npm run destroy
```

---

## 🎯 Production Deployment Checklist

Before deploying to production:

- [ ] Update `removalPolicy` to `RETAIN` for S3 and KMS (in stack code)
- [ ] Configure SNS email subscription for alerts
- [ ] Set up custom domain for API Gateway (optional)
- [ ] Enable AWS WAF for API protection
- [ ] Increase Lambda reserved concurrency
- [ ] Set up multi-region deployment (optional)
- [ ] Configure backup strategy for S3
- [ ] Set up CI/CD pipeline (GitHub Actions, CodePipeline)
- [ ] Enable AWS Config for compliance monitoring
- [ ] Review and tighten CORS policies
- [ ] Set up log aggregation (e.g., CloudWatch Insights)
- [ ] Configure DDoS protection (AWS Shield)

---

## 📚 Additional Resources

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

---

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review CloudWatch logs for detailed error messages
3. Check AWS Service Health Dashboard
4. Review CDK deployment logs in CloudFormation console

---

**Next Steps**: See `API_REFERENCE.md` for detailed API documentation and example use cases.
