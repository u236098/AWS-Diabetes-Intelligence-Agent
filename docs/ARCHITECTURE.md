# Diabetes Intelligence Agent - AWS Architecture

## Overview

This system deploys a production-ready AI agent that helps users understand behavioral patterns related to chronic condition management (specifically Type 1 Diabetes). The architecture follows AWS Well-Architected Framework principles across all five pillars.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Applications                            │
│                    (Mobile, Web, Voice Assistant)                    │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ HTTPS
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Amazon API Gateway                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  • REST API with CORS                                        │  │
│  │  • API Key Authentication                                    │  │
│  │  • Request/Response Validation                               │  │
│  │  • Throttling & Rate Limiting (1000 req/sec)                 │  │
│  │  • CloudWatch Logging                                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
         ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
         │   Lambda:    │ │  Lambda:    │ │   Lambda:    │
         │   Pattern    │ │  Insight    │ │    Food      │
         │   Analysis   │ │  Generator  │ │  Detection   │
         └──────┬───────┘ └──────┬──────┘ └──────┬───────┘
                │                │                │
                └────────────────┼────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Amazon Bedrock        │
                    │  ┌──────────────────┐   │
                    │  │ Claude 4.6       │   │
                    │  │ (Sonnet)         │   │
                    │  └──────────────────┘   │
                    │  • Prompt Caching      │
                    │  • Guardrails          │
                    └─────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
         ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
         │  Amazon S3   │ │ CloudWatch  │ │   X-Ray      │
         │  • User Logs │ │  • Metrics  │ │  • Tracing   │
         │  • Patterns  │ │  • Alarms   │ │  • Analysis  │
         │  Encryption  │ │  • Dashboard│ │              │
         └──────────────┘ └─────────────┘ └──────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │   AWS KMS            │
         │   • Encryption Keys  │
         └──────────────────────┘
```

## AWS Services Used

### 1. **Amazon Bedrock** (Core AI Engine)
- **Model**: Claude 4.6 Sonnet
- **Purpose**: Pattern analysis, natural language understanding, insight generation
- **Features Used**:
  - Prompt caching for cost optimization
  - Guardrails to prevent medical advice
  - Streaming responses for better UX

### 2. **AWS Lambda** (Compute)
- **Three Functions**:
  1. `PatternAnalysisFunction` - Analyzes lifestyle signals
  2. `InsightGeneratorFunction` - Creates explanations
  3. `FoodDetectionFunction` - Processes food images
- **Configuration**:
  - Runtime: Python 3.12
  - Memory: 1024 MB (adjustable)
  - Timeout: 60 seconds
  - Reserved concurrency: 100

### 3. **Amazon API Gateway** (API Management)
- **Type**: REST API
- **Security**: API Key authentication with usage plans
- **Features**:
  - Request validation
  - CORS support
  - Rate limiting (1000 req/sec burst)
  - CloudWatch integration

### 4. **Amazon S3** (Storage)
- **Buckets**:
  1. User logs and pattern history
  2. Food images (optional)
- **Security**:
  - Server-side encryption (AES-256)
  - Bucket policies with least privilege
  - Versioning enabled
  - Lifecycle policies (30-day retention)

### 5. **Amazon CloudWatch** (Monitoring)
- **Components**:
  - Lambda function logs
  - API Gateway access logs
  - Custom metrics dashboard
  - Alarms for error rates and latency

### 6. **AWS X-Ray** (Distributed Tracing)
- End-to-end request tracing
- Performance bottleneck identification
- Service map visualization

### 7. **AWS KMS** (Encryption)
- Customer-managed keys for S3 encryption
- Automatic key rotation
- CloudTrail logging for key usage

### 8. **Amazon Rekognition** (Optional)
- Food detection from images
- Label detection for meal composition
- Confidence scoring

### 9. **AWS IAM** (Security)
- Least-privilege roles for each Lambda
- Resource-based policies
- Service control policies

### 10. **AWS CloudFormation** (via CDK)
- Infrastructure as Code
- Automated deployments
- Stack updates and rollbacks

## Data Flow

### Pattern Analysis Request Flow:

1. **User** submits input (food, activity, timing, glucose trend)
2. **API Gateway** validates request, checks API key
3. **Lambda** (PatternAnalysis) receives event
4. **Bedrock** analyzes input using Claude with cached system prompt
5. **Lambda** structures response
6. **S3** stores anonymized pattern log
7. **CloudWatch** records metrics
8. **API Gateway** returns response to user

### Time: ~2-4 seconds end-to-end

## Security Architecture

### Defense in Depth Layers:

1. **Network Layer**
   - API Gateway with WAF rules (optional)
   - VPC endpoints for AWS service communication (optional)

2. **Application Layer**
   - Lambda function permissions (least privilege)
   - Input validation and sanitization
   - Rate limiting and throttling

3. **Data Layer**
   - S3 encryption at rest (KMS)
   - TLS 1.2+ encryption in transit
   - No PHI/PII storage

4. **Identity Layer**
   - API key authentication
   - IAM roles for service-to-service communication
   - MFA for AWS console access (recommended)

5. **Compliance**
   - CloudTrail logging enabled
   - GuardDuty for threat detection (optional)
   - Config rules for compliance monitoring

## Cost Optimization

### Estimated Monthly Costs (1,000 daily active users):

| Service | Usage | Estimated Cost |
|---------|-------|----------------|
| API Gateway | ~30K requests/month | $0.11 |
| Lambda | ~90K invocations, 1GB, 5s avg | $1.65 |
| Bedrock (Claude Sonnet) | ~30K requests (cached) | $45-75 |
| S3 | 10GB storage, 30K writes | $0.35 |
| CloudWatch | Logs + Metrics | $5.00 |
| **Total** | | **~$52-82/month** |

### Cost Optimization Features:

- **Bedrock Prompt Caching**: 90% cost reduction on repeated system prompts
- **Lambda Power Tuning**: Right-sized memory allocation
- **S3 Lifecycle Policies**: Auto-deletion of old logs
- **API Gateway Caching**: Reduce Lambda invocations
- **CloudWatch Log Retention**: 7-day retention policy

## Scalability

### Auto-Scaling Configuration:

- **API Gateway**: Auto-scales to 10,000 req/sec
- **Lambda**: Concurrent execution limit = 100 (adjustable to 1000+)
- **Bedrock**: Managed service, auto-scales
- **S3**: Unlimited storage, auto-scaling

### Performance Targets:

- **Latency**: p50 < 2s, p99 < 5s
- **Availability**: 99.9% uptime
- **Error Rate**: < 0.1%
- **Throughput**: 1,000+ requests/sec

## Reliability

### High Availability:

- All services deployed across multiple AZs
- No single point of failure
- Automatic failover for Lambda and API Gateway

### Disaster Recovery:

- **RTO**: < 1 hour
- **RPO**: < 5 minutes
- S3 versioning enabled
- CloudFormation stack exports for quick rebuild

### Monitoring & Alerts:

- CloudWatch alarms for:
  - Lambda error rate > 1%
  - API Gateway 5xx errors
  - Latency > 5 seconds
  - Cost anomalies
- SNS notifications to operations team

## Well-Architected Framework Alignment

### ✅ Operational Excellence
- Infrastructure as Code (CDK)
- Automated deployments
- Comprehensive logging and monitoring

### ✅ Security
- Encryption at rest and in transit
- Least-privilege IAM policies
- API authentication
- Bedrock Guardrails for safety

### ✅ Reliability
- Multi-AZ deployment
- Error handling and retries
- Monitoring and alerting

### ✅ Performance Efficiency
- Serverless architecture (no server management)
- Right-sized Lambda functions
- Bedrock prompt caching

### ✅ Cost Optimization
- Pay-per-use pricing model
- Prompt caching reduces costs by 90%
- S3 lifecycle policies
- Budget alerts

### ✅ Sustainability (6th Pillar)
- Serverless = no idle compute
- Regional deployment (reduced latency, lower carbon)
- Efficient prompt engineering

## Extension Points

### Future Enhancements:

1. **Amazon Cognito** - User authentication and user pools
2. **Amazon DynamoDB** - Real-time pattern tracking per user
3. **Amazon EventBridge** - Event-driven pattern detection
4. **AWS Step Functions** - Multi-step analysis workflows
5. **Amazon QuickSight** - Analytics dashboard for aggregated insights
6. **Amazon SageMaker** - Custom ML models for pattern prediction

## Compliance & Privacy

### Important Notes:

⚠️ **This system does NOT**:
- Store Protected Health Information (PHI)
- Provide medical advice or diagnosis
- Calculate insulin doses
- Replace healthcare providers

✅ **This system DOES**:
- Analyze lifestyle patterns
- Provide educational insights
- Help users understand their data
- Follow HIPAA-aligned best practices (if needed)

### Privacy Features:

- No user identity stored in logs
- Data anonymization
- 30-day automatic log deletion
- Opt-out data collection support
- Clear data retention policies

## Deployment Regions

**Recommended Primary Region**: `us-east-1` (N. Virginia)
- Bedrock Claude availability
- Lower costs
- High availability

**Alternative Regions**:
- `us-west-2` (Oregon)
- `eu-west-1` (Ireland)
- Check Bedrock model availability per region

## Testing Strategy

1. **Unit Tests** - Lambda function logic
2. **Integration Tests** - API Gateway → Lambda → Bedrock flow
3. **Load Tests** - 1,000 concurrent requests
4. **Security Tests** - OWASP Top 10 validation
5. **Cost Tests** - Validate prompt caching effectiveness

---

**Next Steps**: See `DEPLOYMENT.md` for step-by-step deployment instructions.
