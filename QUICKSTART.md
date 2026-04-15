# ⚡ Quick Start - Diabetes Intelligence Agent

> **Get from zero to deployed in 5 minutes**

## Prerequisites Check ✅

Before starting, verify you have:

```bash
# Check Node.js (need 18+)
node --version

# Check AWS CLI (need 2.0+)
aws --version

# Check Python (need 3.12+)
python3 --version

# Check AWS credentials
aws sts get-caller-identity
```

If any command fails, see [full prerequisites](docs/DEPLOYMENT.md#prerequisites).

---

## Option 1: Deploy with Agentic Tool (Recommended) 🤖

### Using Kiro IDE:

1. Open Kiro IDE
2. Paste this into the chat:

```
Deploy the Diabetes Intelligence Agent to AWS from the code in this directory.
Follow the deployment steps:
1. Install dependencies with npm install
2. Build Lambda layer
3. Bootstrap CDK if needed
4. Deploy to us-east-1 region (dev environment)
5. Retrieve and show API endpoint and API key

After deployment, test the /health endpoint.
```

3. Press Enter
4. Wait 5 minutes
5. Copy the API endpoint and API key from output

**Done!** ✅

### Using Claude Code:

```bash
cd diabetes-intelligence-agent

# Start Claude Code
claude-code

# Paste in chat:
"Deploy this CDK application to AWS. Install deps, build layer, 
bootstrap if needed, then deploy to us-east-1. Show me the API 
endpoint and how to get the API key."
```

---

## Option 2: Manual Deployment 🛠️

### Step 1: Configure AWS (30 seconds)

```bash
# Set your AWS credentials (if not already configured)
aws configure

# Export account info for CDK
export CDK_DEFAULT_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export CDK_DEFAULT_REGION=us-east-1
```

### Step 2: Install Dependencies (1 minute)

```bash
cd diabetes-intelligence-agent

# Install Node.js dependencies
npm install
```

### Step 3: Build Lambda Layer (1 minute)

```bash
cd lambda/layer
chmod +x build.sh
./build.sh
cd ../..
```

### Step 4: Bootstrap CDK (1 minute, first time only)

```bash
# Only needed once per AWS account/region
npm run bootstrap
```

### Step 5: Deploy! (3 minutes)

```bash
# Deploy to dev environment
npm run deploy:dev

# Or deploy to production
npm run deploy:prod
```

### Step 6: Get Your API Info

CDK will output your API endpoint. Get your API key:

```bash
# Replace KEY_ID with the ApiKeyId from CDK output
aws apigateway get-api-key \
  --api-key YOUR_KEY_ID \
  --include-value \
  --query 'value' \
  --output text
```

**Save these values!**

---

## Test Your Deployment 🧪

### Test 1: Health Check

```bash
curl https://YOUR_API.execute-api.us-east-1.amazonaws.com/v1/health
```

Expected: `{"status": "healthy", ...}`

### Test 2: Analyze a Pattern

```bash
export API_ENDPOINT="https://YOUR_API.execute-api.us-east-1.amazonaws.com/v1"
export API_KEY="your-api-key-here"

curl -X POST "${API_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d '{
    "food": "burger and fries",
    "timing": "11:00 PM",
    "glucose_trend": "rising"
  }'
```

Expected: JSON with `analysis` containing `observation`, `explanation`, `insight`, `suggestion`

---

## View Your Infrastructure 📊

### CloudWatch Dashboard

```bash
# Get dashboard URL from CDK outputs, or:
echo "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=Diabetes-Intelligence-Agent"
```

### Lambda Logs

```bash
aws logs tail /aws/lambda/diabetes-pattern-analysis --follow
```

### API Gateway Metrics

```bash
open "https://console.aws.amazon.com/apigateway/home?region=us-east-1"
```

---

## What You Just Deployed 🎉

- ✅ **3 Lambda Functions** (Pattern Analysis, Insights, Food Detection)
- ✅ **REST API** with 4 endpoints
- ✅ **AI Integration** (Amazon Bedrock with Claude 4.6)
- ✅ **Storage** (S3 bucket with encryption)
- ✅ **Monitoring** (CloudWatch dashboard + alarms)
- ✅ **Security** (KMS encryption, IAM roles, API authentication)
- ✅ **Cost Controls** (Budget alerts, lifecycle policies)

**Total Cost**: ~$50-80/month for 1,000 daily active users

---

## Common Issues & Fixes 🔧

### Issue: "No bootstrap stack found"

```bash
npm run bootstrap
```

### Issue: "Access denied to Bedrock"

1. Go to AWS Console → Bedrock
2. Click "Model access"
3. Enable "Anthropic Claude" models

### Issue: "API returns 403"

- Make sure you're including the `x-api-key` header
- Verify your API key is correct

### Issue: Deployment taking forever

- First deployment is slowest (2-3 minutes)
- Lambda cold starts can add latency
- Check CloudFormation console for progress

---

## Next Steps 📚

✅ **You're done!** Your infrastructure is live.

Optional next steps:

1. **Read the docs**: [ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. **Run tests**: [TESTING.md](docs/TESTING.md)
3. **Customize**: Edit Lambda functions or infrastructure
4. **Scale up**: Increase concurrency for production
5. **Add users**: Integrate with your app

---

## Clean Up 🗑️

When you're done testing:

```bash
# Destroy all resources
npm run destroy

# Confirm when prompted
```

---

## Get Help 🆘

- **Full docs**: See [DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Architecture**: See [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Testing**: See [TESTING.md](docs/TESTING.md)
- **Issues**: Check CloudWatch logs

---

## 5-Command Deployment Summary

For the impatient:

```bash
npm install
cd lambda/layer && ./build.sh && cd ../..
npm run bootstrap  # first time only
npm run deploy:dev
aws apigateway get-api-key --api-key YOUR_KEY_ID --include-value
```

**That's it!** 🚀

---

<p align="center">
  <strong>Deployed in 5 minutes or less? Share your experience!</strong><br>
  Built for the AWS Prompt the Planet Challenge
</p>

<p align="center">
  <a href="docs/DEPLOYMENT.md">📖 Full Guide</a> •
  <a href="docs/ARCHITECTURE.md">🏛️ Architecture</a> •
  <a href="SUBMISSION_PROMPT.md">🎯 Submission</a>
</p>
