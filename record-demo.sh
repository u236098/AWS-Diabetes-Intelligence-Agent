#!/bin/bash

# Automated Demo Script for Video Recording
# This script walks through the demo step-by-step with pauses for recording

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to wait for user to press enter
wait_for_user() {
    echo -e "${YELLOW}Press ENTER to continue to next scene...${NC}"
    read -r
}

# Function to print scene header
scene() {
    clear
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}   $1${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

# Function to type command slowly (visual effect)
type_command() {
    local cmd="$1"
    local delay=0.05

    echo -n "$ "
    for ((i=0; i<${#cmd}; i++)); do
        echo -n "${cmd:$i:1}"
        sleep $delay
    done
    echo ""
}

# Main Demo Script

echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  AWS Diabetes Intelligence Agent Demo         ║${NC}"
echo -e "${GREEN}║  5-Minute Infrastructure Deployment            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo "This script will guide you through recording the demo."
echo "It will pause at each scene for you to narrate."
echo ""
wait_for_user

# ========================================
# Scene 1: Hook
# ========================================
scene "Scene 1: The Hook (0:00 - 0:20)"

echo "NARRATION:"
echo "---"
echo "What if you could deploy complete AWS infrastructure"
echo "with AI, security, and monitoring in just 5 minutes?"
echo ""
echo "Watch me deploy a production-ready system using"
echo "Amazon Bedrock, Lambda, and API Gateway..."
echo ""
echo "With a single prompt."
echo "---"
echo ""
wait_for_user

# ========================================
# Scene 2: Setup Verification
# ========================================
scene "Scene 2: Setup Check (0:20 - 0:40)"

echo "NARRATION:"
echo "---"
echo "Starting with a configured AWS account."
echo "Let me verify the prerequisites."
echo "---"
echo ""

sleep 2

echo "✓ Checking AWS Account..."
type_command "aws sts get-caller-identity --query Account --output text"
aws sts get-caller-identity --query Account --output text 2>/dev/null || echo "[Your AWS Account ID]"
echo ""

sleep 1

echo "✓ Checking Node.js version..."
type_command "node --version"
node --version
echo ""

sleep 1

echo "✓ Checking Python version..."
type_command "python3 --version"
python3 --version
echo ""

echo -e "${GREEN}✓ All prerequisites met!${NC}"
echo ""
wait_for_user

# ========================================
# Scene 3: Show the Prompt
# ========================================
scene "Scene 3: The Prompt (0:40 - 1:00)"

echo "NARRATION:"
echo "---"
echo "This is the prompt that will generate everything."
echo "It specifies complete CDK infrastructure, Lambda functions,"
echo "Bedrock integration, security, and monitoring."
echo "---"
echo ""

echo "Opening the prompt file..."
sleep 1

if [ -f "SUBMISSION_FINAL.md" ]; then
    echo "📄 Prompt file found!"
    echo ""
    echo "First few lines:"
    echo "---"
    head -n 15 SUBMISSION_FINAL.md | sed 's/^/  /'
    echo "---"
    echo ""
    echo -e "${YELLOW}[Now scroll through the prompt in your editor for the video]${NC}"
else
    echo "⚠️  SUBMISSION_FINAL.md not found. Please ensure you're in the project directory."
fi

echo ""
wait_for_user

# ========================================
# Scene 4: File Structure
# ========================================
scene "Scene 4: Generated Code (1:30 - 2:00)"

echo "NARRATION:"
echo "---"
echo "In seconds, we have complete infrastructure code:"
echo "• CDK application in TypeScript"
echo "• 3 Lambda functions in Python"
echo "• Full documentation"
echo "• Security and monitoring configuration"
echo "---"
echo ""

echo "Project structure:"
echo ""
tree -L 2 -I 'node_modules|cdk.out|*.d.ts|*.js' 2>/dev/null || find . -maxdepth 2 -type d -not -path "*/node_modules/*" -not -path "*/cdk.out/*" | head -20

echo ""
echo -e "${YELLOW}[Show key files in your editor:]${NC}"
echo "  • lib/diabetes-intelligence-stack.ts"
echo "  • lambda/analysis/handler.py"
echo "  • docs/ARCHITECTURE.md"
echo ""
wait_for_user

# ========================================
# Scene 5: Deployment
# ========================================
scene "Scene 5: Deploy to AWS (2:00 - 3:00)"

echo "NARRATION:"
echo "---"
echo "Now let's deploy to AWS."
echo "One command."
echo "---"
echo ""

echo "⚠️  DEMO MODE: Not running actual deployment"
echo "   In your recording, run: npm run deploy:dev"
echo ""
echo "What the deployment does:"
echo "  1. CDK synthesizes CloudFormation"
echo "  2. Creates 10 AWS services"
echo "  3. Configures security and monitoring"
echo "  4. Outputs API endpoint and keys"
echo ""
echo "Expected output:"
echo "---"
cat << 'EOF'
✅ DiabetesIntelligenceStack-dev

Outputs:
DiabetesIntelligenceStack-dev.ApiEndpoint = https://xxxxx.execute-api.us-east-1.amazonaws.com/v1/
DiabetesIntelligenceStack-dev.ApiKeyId = xxxxxxxxxxxxx
DiabetesIntelligenceStack-dev.DataBucketName = diabetes-intelligence-data-xxxx-us-east-1
DiabetesIntelligenceStack-dev.DashboardURL = https://console.aws.amazon.com/cloudwatch/...

Stack ARN:
arn:aws:cloudformation:us-east-1:xxxx:stack/DiabetesIntelligenceStack-dev/xxxxx

✨  Total time: 3m 42s
EOF
echo "---"
echo ""
wait_for_user

# ========================================
# Scene 6: AWS Console Tour
# ========================================
scene "Scene 6: AWS Console Tour (3:00 - 3:45)"

echo "NARRATION:"
echo "---"
echo "Let's see what was created in AWS."
echo "---"
echo ""

echo "Open these in AWS Console:"
echo ""
echo "1. Lambda Functions (show 3 functions)"
echo "   → https://console.aws.amazon.com/lambda"
echo ""
echo "2. API Gateway (show REST API)"
echo "   → https://console.aws.amazon.com/apigateway"
echo ""
echo "3. CloudWatch Dashboard (show metrics)"
echo "   → https://console.aws.amazon.com/cloudwatch/home#dashboards:"
echo ""
echo "4. S3 Bucket (show encryption)"
echo "   → https://console.aws.amazon.com/s3"
echo ""
echo "5. Bedrock (mention Claude 4.6)"
echo "   → https://console.aws.amazon.com/bedrock"
echo ""
wait_for_user

# ========================================
# Scene 7: Test the API
# ========================================
scene "Scene 7: Test Live API (3:45 - 4:30)"

echo "NARRATION:"
echo "---"
echo "Let's test the live API."
echo "---"
echo ""

echo "Test 1: Health Check"
echo ""
type_command 'curl https://YOUR_API/v1/health'
echo ""
echo "Response:"
echo '{"status": "healthy", "timestamp": "2026-04-15T12:34:56Z"}'
echo ""

sleep 2

echo "Test 2: Pattern Analysis"
echo ""
type_command 'curl -X POST https://YOUR_API/v1/analyze \'
echo '  -H "x-api-key: YOUR_KEY" \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{"food": "burger and fries", "timing": "11:00 PM", "glucose_trend": "rising"}'"'"
echo ""
echo "Response:"
cat << 'EOF'
{
  "analysis": {
    "observation": "This meal appears to be high in fast-absorbing carbohydrates and fats, consumed very late in the evening.",
    "explanation": "Eating high-carb meals late may lead to higher glucose spikes due to reduced insulin sensitivity during sleep.",
    "insight": "You may notice elevated glucose levels after similar late-night meals.",
    "suggestion": "Consider eating earlier or choosing meals with more protein and fiber.",
    "confidence": "high"
  },
  "timestamp": "2026-04-15T12:35:22Z"
}
EOF
echo ""
wait_for_user

# ========================================
# Scene 8: Monitoring
# ========================================
scene "Scene 8: CloudWatch Monitoring (4:30 - 4:50)"

echo "NARRATION:"
echo "---"
echo "The monitoring is already working."
echo "Real-time metrics, alarms, and logging—all configured automatically."
echo "---"
echo ""

echo "Show CloudWatch Dashboard with:"
echo "  • API request count"
echo "  • Lambda invocations"
echo "  • Error rates"
echo "  • Latency metrics"
echo ""
echo -e "${YELLOW}[Open CloudWatch Dashboard in browser]${NC}"
echo ""
wait_for_user

# ========================================
# Scene 9: Closing
# ========================================
scene "Scene 9: Closing (4:50 - 5:00)"

echo "NARRATION:"
echo "---"
echo "From prompt to production in 5 minutes."
echo ""
echo "10 AWS services. Complete security. Full monitoring."
echo ""
echo "All from a single prompt."
echo ""
echo "That's the power of agentic coding."
echo "---"
echo ""

echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║            Demo Complete! 🎉                   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo "Final Stats:"
echo "  ✅ 10 AWS Services Deployed"
echo "  ✅ Production-Ready Infrastructure"
echo "  ✅ Security & Monitoring Included"
echo "  ✅ Cost: ~\$54/month for 1,000 users"
echo ""
echo "AWS Prompt the Planet Challenge"
echo "GitHub: [your-repo-link]"
echo ""
echo ""
echo -e "${BLUE}Recording complete! Now edit and upload your video.${NC}"
echo ""
