# 🩺 Diabetes Intelligence Agent - AWS Infrastructure

> **Production-ready AWS infrastructure for AI-powered diabetes pattern analysis and insights**

[![AWS](https://img.shields.io/badge/AWS-Cloud-orange)](https://aws.amazon.com/)
[![CDK](https://img.shields.io/badge/AWS_CDK-TypeScript-blue)](https://aws.amazon.com/cdk/)
[![Bedrock](https://img.shields.io/badge/Amazon_Bedrock-Claude_4.6-purple)](https://aws.amazon.com/bedrock/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 📖 Overview

This project provides **complete, production-ready AWS infrastructure** to deploy an AI-powered Diabetes Intelligence Agent. It helps users understand behavioral patterns related to chronic condition management through:

- 🧠 **Pattern Analysis** - Analyzes lifestyle signals (food, activity, timing, glucose trends)
- 💡 **Insight Generation** - Creates personalized, human-readable insights from historical data
- 🍔 **Food Detection** - Identifies food items from images using computer vision
- 🔒 **Safety First** - Built-in guardrails to prevent medical advice
- 📊 **Production Monitoring** - Complete observability with CloudWatch and X-Ray

### 🎯 Built for the AWS Prompt the Planet Challenge

This submission demonstrates how to use **agentic coding tools** (like Kiro IDE or Claude Code) to deploy complex AWS infrastructure with a simple prompt.

---

## ✨ Key Features

### Infrastructure
- ☁️ **100% Serverless** - No servers to manage (Lambda, API Gateway, S3)
- 🚀 **Auto-Scaling** - Handles 1,000+ concurrent requests
- 🔐 **Security-Hardened** - KMS encryption, IAM least privilege, API authentication
- 📈 **Fully Monitored** - CloudWatch dashboards, alarms, and X-Ray tracing
- 💰 **Cost-Optimized** - Bedrock prompt caching reduces costs by 90%
- 🏗️ **Infrastructure as Code** - AWS CDK (TypeScript)

### Application
- 🤖 **Powered by Claude 4.6** - State-of-the-art AI reasoning via Amazon Bedrock
- 👁️ **Computer Vision** - Amazon Rekognition for food detection
- 📦 **Data Persistence** - S3 for pattern storage with lifecycle policies
- 🔔 **Alerts & Budgets** - SNS notifications for errors and cost overruns
- 🌍 **Multi-Region Ready** - Deploy to any Bedrock-supported region

---

## 🏛️ Architecture

```
User App → API Gateway → Lambda → Bedrock (Claude) → S3
                ↓           ↓
          CloudWatch   X-Ray Tracing
```

**AWS Services Used:**
- Amazon Bedrock (Claude 4.6 Sonnet)
- AWS Lambda (Python 3.12)
- Amazon API Gateway (REST API)
- Amazon S3 (Encrypted storage)
- Amazon Rekognition (Food detection)
- Amazon CloudWatch (Monitoring)
- AWS X-Ray (Tracing)
- AWS KMS (Encryption)
- AWS IAM (Security)
- AWS Budgets (Cost control)

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture diagrams.

---

## 🚀 Quick Start

### Prerequisites
- AWS Account with Bedrock access
- Node.js 18+
- AWS CLI configured
- Python 3.12+

### Deploy in 5 Minutes

```bash
# 1. Clone/navigate to project
cd diabetes-intelligence-agent

# 2. Install dependencies
npm install

# 3. Build Lambda layer
cd lambda/layer && chmod +x build.sh && ./build.sh && cd ../..

# 4. Set AWS credentials
export CDK_DEFAULT_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export CDK_DEFAULT_REGION=us-east-1

# 5. Bootstrap CDK (first time only)
npm run bootstrap

# 6. Deploy!
npm run deploy:dev
```

**That's it!** 🎉 Your infrastructure is live.

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Complete architecture, AWS services, data flows |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Step-by-step deployment guide |
| [SUBMISSION_PROMPT.md](SUBMISSION_PROMPT.md) | The competition submission prompt |

---

## 🧪 API Examples

### Analyze a Pattern

```bash
curl -X POST "https://YOUR_API.execute-api.us-east-1.amazonaws.com/v1/analyze" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "food": "burger and fries",
    "timing": "11:00 PM",
    "activity": "none",
    "glucose_trend": "rising"
  }'
```

**Response:**
```json
{
  "analysis": {
    "observation": "This meal appears to be high in fast-absorbing carbohydrates and fats, consumed very late in the evening.",
    "explanation": "Eating high-carb meals late at night may lead to higher glucose spikes due to reduced insulin sensitivity during sleep hours.",
    "insight": "You may notice elevated glucose levels after similar late-night meals.",
    "suggestion": "Consider eating earlier in the evening or choosing meals with more protein and fiber to slow digestion.",
    "confidence": "high"
  },
  "timestamp": "2026-04-15T03:45:22Z",
  "model": "anthropic.claude-sonnet-4-6-v1:0"
}
```

### Detect Food from Image

```bash
curl -X POST "https://YOUR_API.execute-api.us-east-1.amazonaws.com/v1/food" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "BASE64_ENCODED_IMAGE"
  }'
```

---

## 💰 Cost Breakdown

**Estimated monthly cost for 1,000 daily active users: $53-83**

| Service | Monthly Cost |
|---------|--------------|
| Amazon Bedrock (with caching) | $45-75 |
| AWS Lambda | $1.65 |
| API Gateway | $0.11 |
| Amazon S3 | $0.35 |
| CloudWatch | $5.00 |
| **Total** | **$52-82** |

**Cost Optimizations Built-In:**
- ✅ Bedrock prompt caching (90% savings)
- ✅ S3 lifecycle policies (30-day expiration)
- ✅ Lambda memory optimization
- ✅ Budget alerts at 80% threshold

---

## 🔒 Security Features

- ✅ **Encryption at Rest** - KMS-encrypted S3 buckets
- ✅ **Encryption in Transit** - TLS 1.2+ enforced
- ✅ **API Authentication** - API key required for all endpoints
- ✅ **IAM Least Privilege** - Minimal permissions per function
- ✅ **No PHI Storage** - No protected health information stored
- ✅ **Bedrock Guardrails** - Prevents medical advice
- ✅ **Input Validation** - Request validators on API Gateway
- ✅ **CloudTrail Logging** - Full audit trail

---

## 📊 Monitoring & Observability

### CloudWatch Dashboard
- API request count and latency
- Lambda invocations and errors
- Bedrock API usage
- Cost tracking

### Alarms
- Lambda error rate > 1%
- API Gateway 5xx errors
- Latency > 5 seconds
- Budget threshold exceeded

### X-Ray Tracing (Production)
- End-to-end request tracing
- Service dependency map
- Performance bottleneck identification

---

## 🎯 Use Cases

1. **Mobile Health Apps** - Integrate as backend API for diabetes management apps
2. **Voice Assistants** - "Alexa, analyze my dinner"
3. **Chatbots** - Slack/Teams bots for health insights
4. **Wearable Devices** - CGM data analysis
5. **Research Platforms** - Anonymized pattern analysis at scale

---

## 🔄 Development Workflow

### Make Changes
```bash
# Modify Lambda code or infrastructure
vim lambda/analysis/handler.py
vim lib/diabetes-intelligence-stack.ts

# See what will change
npm run diff

# Deploy changes
npm run deploy:dev
```

### View Logs
```bash
# Lambda logs
aws logs tail /aws/lambda/diabetes-pattern-analysis --follow

# API Gateway logs
aws logs tail API-Gateway-Execution-Logs_XXXXX/v1 --follow
```

### Destroy Stack
```bash
npm run destroy
```

---

## 🧩 Extension Ideas

Want to extend this project? Here are some ideas:

- **User Authentication** - Add Amazon Cognito for user management
- **Real-time Patterns** - Use DynamoDB for real-time pattern tracking
- **Notifications** - Add SNS/SES for daily insight emails
- **Advanced ML** - Train custom models with SageMaker
- **Multi-tenant** - Add tenant isolation and API Gateway authorizers
- **Web Dashboard** - Deploy a React frontend with Amplify
- **Mobile SDK** - Create iOS/Android SDKs

---

## 🤝 Contributing

This is a hackathon submission, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **AWS Prompt the Planet Challenge** - For inspiring this project
- **Anthropic** - For Claude AI
- **AWS** - For the incredible cloud platform
- **Diabetes Community** - For feedback on pattern analysis needs

---

## 📧 Contact

**Hackathon Submission by:** [Your Name]
**Email:** [Your Email]
**GitHub:** [Your GitHub]

---

## 🚨 Disclaimer

⚠️ **Medical Disclaimer**: This system is for educational and lifestyle support only. It does NOT provide medical advice, diagnosis, or treatment recommendations. Always consult healthcare professionals for medical decisions.

---

<p align="center">
  <strong>Built with ❤️ for the AWS Prompt the Planet Challenge</strong>
</p>

<p align="center">
  <a href="docs/DEPLOYMENT.md">📖 Deployment Guide</a> •
  <a href="docs/ARCHITECTURE.md">🏛️ Architecture</a> •
  <a href="SUBMISSION_PROMPT.md">🎯 Submission Prompt</a>
</p>
