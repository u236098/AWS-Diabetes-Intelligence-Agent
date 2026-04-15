# Generate and deploy a production-ready AWS CDK application for a Diabetes Intelligence Agent using Amazon Bedrock, Lambda, API Gateway, S3, CloudWatch, and security best practices.

> **AWS Prompt the Planet Challenge Submission**

---

## ⚡ Why This Prompt Matters

This prompt allows developers to generate a complete, production-ready AI system on AWS in minutes.

Instead of spending days setting up infrastructure, users can:
- ✅ **Generate** a full serverless architecture
- ✅ **Integrate** Amazon Bedrock for AI reasoning  
- ✅ **Deploy** secure, scalable APIs with monitoring
- ✅ **Apply** AWS best practices automatically

**All from a single prompt.**

---

## 🚀 What Happens When You Run This Prompt

Paste this into **Kiro IDE** or **Claude Code**, and it will:

1. ✅ Generate a full AWS CDK application (TypeScript)
2. ✅ Create 3 Lambda functions with production error handling (Python)
3. ✅ Configure Amazon Bedrock with safety guardrails
4. ✅ Set up API Gateway, S3, CloudWatch, and security
5. ✅ Deploy everything to your AWS account

**⏱️ Total time: ~5–10 minutes**  
**💰 Estimated monthly cost: ~$54 for 1,000 users**  
**📊 Services deployed: 10 AWS services**

---

## 📝 THE PROMPT (COPY & USE THIS)

### Primary Prompt for Agentic Coding Tools:

```
Generate and deploy a production-ready AWS CDK application for a Diabetes Intelligence Agent 
using Amazon Bedrock, Lambda, API Gateway, S3, CloudWatch, and security best practices.

OBJECTIVE:
Create complete AWS infrastructure for an AI-powered agent that helps users understand 
behavioral patterns related to diabetes management through lifestyle analysis.

REQUIREMENTS:

1. INFRASTRUCTURE (AWS CDK - TypeScript):
   - Use AWS CDK v2.147.0 or later
   - Deploy to us-east-1 region (Bedrock availability)
   - Create separate stacks for dev/prod environments
   - All infrastructure as code with proper typing

2. COMPUTE & API LAYER:
   - API Gateway REST API with:
     * API key authentication
     * CORS enabled
     * Rate limiting: 1000 req/sec
     * Request/response validation
     * CloudWatch logging
   
   - Three Lambda functions (Python 3.12):
     a) Pattern Analysis (analyzes lifestyle inputs)
     b) Insight Generator (creates personalized insights)
     c) Food Detection (identifies food from images)
   
   - Lambda configuration:
     * Memory: 1024MB (dev), 2048MB (prod)
     * Timeout: 60 seconds
     * Reserved concurrency: 10 (dev), 100 (prod)
     * X-Ray tracing enabled in prod
     * Shared Lambda layer for dependencies

3. AI & ML SERVICES:
   - Amazon Bedrock integration:
     * Model: Claude 4.6 Sonnet (anthropic.claude-sonnet-4-6-v1:0)
     * Enable prompt caching for cost reduction
     * System prompt that enforces:
       - NO medical advice or insulin calculations
       - Probabilistic language only
       - Educational insights focus
       - Supportive, non-judgmental tone
   
   - Amazon Rekognition:
     * Food label detection
     * Confidence threshold: 70%
     * Integration with Bedrock for enhanced descriptions

4. STORAGE & DATA:
   - S3 bucket with:
     * KMS encryption (customer-managed key)
     * Versioning enabled
     * Lifecycle policy: delete after 30 days
     * No PHI/PII storage
     * Block all public access
   
   - Store anonymized pattern logs as JSON:
     patterns/YYYY/MM/DD/timestamp.json

5. SECURITY:
   - IAM roles with least-privilege policies:
     * Lambda execution role with Bedrock, S3, KMS access
     * API Gateway service role
   
   - Encryption:
     * KMS with automatic key rotation
     * TLS 1.2+ for all API traffic
     * S3 server-side encryption
   
   - Bedrock Guardrails:
     * Block medical advice
     * Block dosage calculations
     * Enforce disclaimers

6. MONITORING & OBSERVABILITY:
   - CloudWatch Dashboard with:
     * API request count and latency
     * Lambda invocations and errors
     * Bedrock API usage metrics
     * Cost tracking
   
   - CloudWatch Alarms for:
     * Lambda error rate > 1%
     * API Gateway 5xx errors > 10 in 5 min
     * Average latency > 5 seconds
   
   - SNS topic for alert notifications
   
   - X-Ray tracing (production only):
     * Service map visualization
     * Performance analysis

7. COST MANAGEMENT:
   - AWS Budget:
     * Monthly limit: $50 (dev), $500 (prod)
     * Alert at 80% threshold
     * SNS notification
   
   - Cost optimizations:
     * Bedrock prompt caching
     * S3 lifecycle policies
     * Right-sized Lambda memory
     * CloudWatch log retention: 7 days (dev), 30 days (prod)

8. API ENDPOINTS:
   
   POST /analyze
   - Analyzes lifestyle pattern
   - Input: food, activity, timing, glucose_trend, context
   - Output: observation, explanation, insight, suggestion, confidence
   - Requires API key
   
   POST /insights
   - Generates insights from historical patterns
   - Input: days (time range)
   - Output: summary, trends, positive_patterns, areas_to_watch, recommendations
   - Requires API key
   
   POST /food
   - Detects food from image
   - Input: base64 encoded image
   - Output: detected_foods, description
   - Requires API key
   
   GET /health
   - Health check endpoint
   - No authentication required

9. DEPLOYMENT OUTPUTS:
   - API Gateway endpoint URL
   - API Key ID (value retrievable via AWS CLI)
   - S3 bucket name
   - CloudWatch dashboard URL
   - Lambda function names

10. DOCUMENTATION:
    Create comprehensive docs:
    - README.md (project overview, quick start)
    - docs/ARCHITECTURE.md (detailed architecture, AWS services, data flows)
    - docs/DEPLOYMENT.md (step-by-step deployment, troubleshooting)
    - Include cost estimates, security best practices

DELIVERABLES:
- Complete CDK application (TypeScript)
- Lambda function code (Python 3.12)
- Deployment scripts
- Comprehensive documentation
- Example API requests
- Testing procedures

CONSTRAINTS:
- Must follow AWS Well-Architected Framework
- Must be deployable with single command
- Must work in regions where Bedrock is available
- Target monthly cost under $100 for 1000 daily active users
- Designed to scale to high request volumes

TESTING:
After deployment, verify:
1. Health endpoint returns 200
2. Pattern analysis correctly processes input
3. Bedrock responses include safety guardrails
4. CloudWatch dashboard shows metrics
5. Budget alerts are configured

Execute deployment and provide API endpoint and testing instructions.
```

---

## 💡 The Problem This Solves

Many diabetes management tools collect data well, but they do not help users understand it clearly.

Users can log meals, activity, and glucose trends, yet still struggle to:
- Understand **why** changes happen
- Recognize repeatable **patterns**
- Turn data into safer **day-to-day decisions**

This prompt generates infrastructure for an AI system that focuses on explanation rather than prediction, helping users interpret behavior patterns in simple, human language.

---

## 👥 Who This Is For

This prompt is designed for:
- Developers building health or behavior-focused AI applications
- Startup teams creating AWS-native MVP backends
- Learners who want a real example of serverless + Bedrock architecture
- Builders using Kiro IDE, Claude Code, or similar agentic coding tools

---

## 🏗️ What Gets Generated

### AWS Services Deployed (10 services):

| Service | Purpose | Configuration |
|---------|---------|---------------|
| **Amazon Bedrock** | AI reasoning (Claude 4.6) | Prompt caching, guardrails |
| **AWS Lambda** | 3 serverless functions | Python 3.12, auto-scaling |
| **API Gateway** | REST API | API key auth, throttling |
| **Amazon S3** | Pattern storage | KMS encrypted, lifecycle policies |
| **Amazon Rekognition** | Food detection | Label detection |
| **CloudWatch** | Monitoring | Dashboard + 3 alarms |
| **AWS X-Ray** | Distributed tracing | Service map |
| **AWS KMS** | Encryption | Auto-rotation |
| **AWS IAM** | Security | Least-privilege roles |
| **AWS Budgets** | Cost control | 80% threshold alert |

### Code Generated:
- **2,500+ lines** of infrastructure and application code
- **CDK Infrastructure** (TypeScript)
- **Lambda Functions** (Python)
- **Complete documentation** (8,000+ words)

---

## 🔁 Reusability & Adaptability

**This prompt is not limited to diabetes management.**

The infrastructure can be adapted to build:

### Healthcare:
- Nutrition tracking systems
- Fitness pattern analysis
- Mental health journaling
- Sleep pattern monitoring

### Beyond Healthcare:
- Behavioral analysis tools
- Habit tracking applications
- Personal coaching systems
- Any AI-powered pattern detection

**By modifying the prompt context, developers can reuse this across domains.**

### Example Adaptations:

**Fitness Tracking:**
```
Replace:
- "diabetes management" → "fitness goals"
- "glucose trend" → "energy levels"
- "food" → "workout routine"
```

**Mental Health:**
```
Replace:
- "diabetes" → "mental wellness"
- "glucose" → "mood"
- "food" → "activities"
```

**The infrastructure stays the same. Only the domain context changes.**

---

## 📊 Architecture Generated

```
User App
   │ HTTPS
   ▼
API Gateway (REST)
   │
   ├──► Lambda: Pattern Analysis ──┐
   │                                │
   ├──► Lambda: Insight Generator ──┼──► Amazon Bedrock
   │                                │     (Claude 4.6)
   ├──► Lambda: Food Detection ─────┘
   │                                │
   ▼                                ▼
CloudWatch                     Amazon S3
Monitoring                    (Encrypted)
```

---

## 🧪 Example Usage After Deployment

### Test Pattern Analysis:
```bash
curl -X POST "https://YOUR_API/v1/analyze" \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "food": "burger and fries",
    "timing": "11:00 PM",
    "glucose_trend": "rising"
  }'
```

### Response:
```json
{
  "analysis": {
    "observation": "This meal appears to be high in fast-absorbing carbohydrates and fats, consumed very late in the evening.",
    "explanation": "Eating high-carb meals late may lead to higher glucose spikes due to reduced insulin sensitivity during sleep.",
    "insight": "You may notice elevated glucose levels after similar late-night meals.",
    "suggestion": "Consider eating earlier or choosing meals with more protein and fiber.",
    "confidence": "high"
  },
  "timestamp": "2026-04-15T03:45:22Z"
}
```

---

## 💰 Cost Breakdown

**Estimated monthly cost for 1,000 daily active users: ~$54**

| Component | Cost |
|-----------|------|
| Bedrock (cached) | $45 |
| Lambda | $1.65 |
| API Gateway | $0.11 |
| S3 | $0.35 |
| CloudWatch | $5.00 |
| Other | $2.00 |

**Cost Optimizations Built-In:**
- ✅ Bedrock prompt caching
- ✅ S3 lifecycle policies (30-day deletion)
- ✅ Right-sized Lambda memory
- ✅ Budget alerts

---

## 🔒 Security & Safety

### Technical Security:
- ✅ Encryption at rest (KMS)
- ✅ Encryption in transit (TLS 1.2+)
- ✅ API key authentication
- ✅ IAM least privilege
- ✅ No PHI/PII storage

### AI Safety Guardrails:
- ✅ NO medical advice
- ✅ NO insulin calculations
- ✅ Probabilistic language only
- ✅ Educational focus
- ✅ Built-in disclaimers

**⚠️ Medical Disclaimer**: This system is for educational purposes only. Not medical advice.

---

## 🎯 How to Use This Prompt

### Option 1: Kiro IDE (Recommended)
1. Open Kiro IDE
2. Paste the PRIMARY PROMPT above
3. Press Enter
4. Wait ~5–10 minutes
5. Get API endpoint + key

### Option 2: Claude Code
```bash
# Start Claude Code
claude-code

# Paste the PRIMARY PROMPT
# Claude will generate and deploy everything
```

### Option 3: Manual
```bash
# Use the generated code
npm install
npm run deploy:dev
```

---

## ✅ AWS Well-Architected Framework Compliance

| Pillar | Implementation |
|--------|----------------|
| **Operational Excellence** | IaC (CDK), CloudWatch monitoring, automated deployments |
| **Security** | KMS encryption, IAM least privilege, Bedrock guardrails |
| **Reliability** | Multi-AZ deployment, error handling, CloudWatch alarms |
| **Performance Efficiency** | Serverless architecture, Lambda tuning, prompt caching |
| **Cost Optimization** | Pay-per-use, lifecycle policies, budget alerts |
| **Sustainability** | Serverless (no idle compute), regional deployment |

---

## 🧪 Testing the Generated System

### Quick Tests:

**1. Health Check:**
```bash
curl https://YOUR_API/v1/health
# Expected: {"status": "healthy"}
```

**2. Pattern Analysis:**
```bash
curl -X POST https://YOUR_API/v1/analyze \
  -H "x-api-key: KEY" \
  -d '{"food": "pasta", "timing": "9pm"}'
# Expected: JSON with analysis
```

**3. Verify Logs and Metrics:**
- Confirm Lambda logs are written to CloudWatch
- Confirm API requests appear in monitoring dashboards
- Confirm alarms and budget notifications are configured

---

## 📋 Prerequisites

Before running this prompt:

### Required:
- AWS Account with Bedrock access
- AWS CLI configured
- Node.js 18+
- Python 3.12+

### AWS Services Access:
- Amazon Bedrock model access enabled (Claude models)
- Sufficient service quotas

### Supported Regions:
- us-east-1 (recommended)
- us-west-2
- eu-west-1
- ap-southeast-1

---

## 🔧 Common Issues

**Issue**: Bedrock access denied  
**Fix**: Enable Claude models in AWS Console → Bedrock → Model access

**Issue**: Deployment timeout  
**Fix**: Check CloudFormation console for detailed error messages

**Issue**: Costs higher than expected  
**Fix**: Verify prompt caching is enabled in CloudWatch metrics

---

## 📚 Generated Documentation

The prompt generates complete documentation:

- **README.md** - Project overview
- **ARCHITECTURE.md** - Detailed design
- **DEPLOYMENT.md** - Step-by-step guide
- **Example code** - CDK + Lambda functions
- **Testing guide** - Comprehensive tests

---

## 🎓 Learning Outcomes

Developers using this prompt will learn:

- **AWS CDK** - Complete application structure
- **Serverless Architecture** - Lambda, API Gateway, S3
- **AI/ML on AWS** - Bedrock integration
- **Security** - KMS, IAM, encryption
- **Monitoring** - CloudWatch, X-Ray

---

<p align="center">
  <strong>Ready to deploy? Copy the PRIMARY PROMPT above and paste into Kiro IDE.</strong>
</p>

<p align="center">
  <a href="#-the-prompt-copy--use-this">📝 Copy Prompt</a> •
  <a href="#-how-to-use-this-prompt">🚀 Deploy Now</a> •
  <a href="#-reusability--adaptability">🔁 Adapt for Your Use Case</a>
</p>

---

## 📝 Submission Metadata

**Title**: Generate a Production-Ready Diabetes Intelligence Agent on AWS (Full CDK + Bedrock Stack)  
**Category**: Health Tech / AI Infrastructure / Serverless  
**AWS Services**: Bedrock, Lambda, API Gateway, S3, Rekognition, CloudWatch, X-Ray, KMS, IAM, Budgets  
**Estimated Deployment Time**: 5–10 minutes  
**Estimated Monthly Cost**: ~$54 (1,000 users)  
**Lines of Code Generated**: 2,500+  
**Documentation Generated**: 8,000+ words  

**Submitted to**: AWS Prompt the Planet Challenge  
**Date**: April 15, 2026  
**Challenge Period**: March 1 - June 1, 2026

---

**Built for the AWS Prompt the Planet Challenge**
