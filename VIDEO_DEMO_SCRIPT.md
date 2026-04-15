# Video Demo Script - Diabetes Intelligence Agent

## 🎥 Video Overview

**Title**: "Deploy Production AWS Infrastructure in 5 Minutes with a Single Prompt"  
**Duration**: 3-5 minutes  
**Format**: Screen recording with voiceover or text overlays  
**Tools**: OBS Studio, QuickTime, or Loom  

---

## 📋 Script with Timing

### Scene 1: Hook (0:00 - 0:20)

**Visual**: Show title card or code editor

**Text Overlay / Voiceover**:
```
"What if you could deploy a complete AWS infrastructure 
with AI, security, and monitoring in just 5 minutes?

Watch me deploy a production-ready system using 
Amazon Bedrock, Lambda, and API Gateway...

With a single prompt."
```

**Action**: Show the prompt file being opened

---

### Scene 2: The Setup (0:20 - 0:40)

**Visual**: Terminal showing AWS CLI

**Text Overlay / Voiceover**:
```
"Starting with a configured AWS account and CDK installed.

Let me show you what this prompt will generate."
```

**Action**: Quick terminal commands
```bash
aws sts get-caller-identity
node --version
```

**Show on screen**:
- ✓ AWS Account configured
- ✓ Node.js 18+
- ✓ Python 3.12+

---

### Scene 3: The Prompt (0:40 - 1:00)

**Visual**: Show SUBMISSION_FINAL.md opened, scroll to THE PROMPT section

**Text Overlay / Voiceover**:
```
"This is the prompt. It specifies:
• Complete CDK infrastructure
• 3 Lambda functions  
• Amazon Bedrock integration
• Security and monitoring
• All AWS best practices"
```

**Action**: 
- Highlight key sections of the prompt
- Copy the prompt to clipboard

---

### Scene 4: Paste into Kiro/Claude Code (1:00 - 1:30)

**Visual**: Open Kiro IDE or Claude Code

**Text Overlay / Voiceover**:
```
"I'll paste this into Kiro IDE.

Watch as it generates the entire infrastructure."
```

**Action**: 
- Paste prompt
- Press Enter
- Show the AI starting to work

**Time-lapse** the generation (speed up 2-4x):
- Show files being created
- CDK code appearing
- Lambda functions being written

---

### Scene 5: Generated Code (1:30 - 2:00)

**Visual**: Show the generated project structure

**Text Overlay / Voiceover**:
```
"In seconds, we have:
• Complete CDK application (TypeScript)
• 3 Lambda functions (Python)  
• Full documentation
• Security configuration
• Monitoring setup"
```

**Action**: Quick tour of files
```
diabetes-intelligence-agent/
├── lib/diabetes-intelligence-stack.ts  ← Show this
├── lambda/
│   ├── analysis/handler.py            ← Show this
│   ├── insights/handler.py
│   └── food-detection/handler.py
└── docs/                               ← Show this
```

---

### Scene 6: Deploy to AWS (2:00 - 3:00)

**Visual**: Terminal showing deployment

**Text Overlay / Voiceover**:
```
"Now let's deploy to AWS.

One command."
```

**Action**: Run deployment
```bash
cd diabetes-intelligence-agent
npm install
npm run deploy:dev
```

**Time-lapse** the deployment (speed up 2-3x):
- Show CDK synth
- CloudFormation stack creating
- Resources being created
- Success message

**Show output**:
```
✅ Deployment complete
✅ API Endpoint: https://xxxxx.execute-api.us-east-1.amazonaws.com/v1
✅ 10 AWS services deployed
```

---

### Scene 7: AWS Console Tour (3:00 - 3:45)

**Visual**: Quick tour of AWS Console

**Text Overlay / Voiceover**:
```
"Let's see what was created in AWS."
```

**Action**: Show in AWS Console (quick cuts):

1. **Lambda Functions** (3 seconds)
   - Show 3 functions listed
   - Click into one to show code

2. **API Gateway** (3 seconds)
   - Show REST API
   - Show endpoints

3. **CloudWatch Dashboard** (3 seconds)
   - Show the auto-generated dashboard
   - Show metrics appearing

4. **S3 Bucket** (2 seconds)
   - Show encrypted bucket
   - Show lifecycle policies

5. **Bedrock** (2 seconds)
   - Mention Claude 4.6 integration

---

### Scene 8: Test the API (3:45 - 4:30)

**Visual**: Terminal with curl commands

**Text Overlay / Voiceover**:
```
"Let's test the live API."
```

**Action**: Run test commands

**Test 1: Health Check**
```bash
curl https://YOUR_API/v1/health
```

**Show response**:
```json
{"status": "healthy", "timestamp": "..."}
```

**Test 2: Pattern Analysis**
```bash
curl -X POST https://YOUR_API/v1/analyze \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "food": "burger and fries",
    "timing": "11:00 PM",
    "glucose_trend": "rising"
  }'
```

**Show response** (highlight key parts):
```json
{
  "analysis": {
    "observation": "This meal appears to be high in...",
    "explanation": "Eating high-carb meals late may...",
    "insight": "You may notice elevated glucose...",
    "suggestion": "Consider eating earlier...",
    "confidence": "high"
  }
}
```

---

### Scene 9: CloudWatch Monitoring (4:30 - 4:50)

**Visual**: CloudWatch dashboard updating

**Text Overlay / Voiceover**:
```
"The monitoring is already working.

Real-time metrics, alarms, and logging—all configured automatically."
```

**Action**: Show CloudWatch dashboard with live metrics

---

### Scene 10: Closing (4:50 - 5:00)

**Visual**: Show completed infrastructure diagram or summary

**Text Overlay / Voiceover**:
```
"From prompt to production in 5 minutes.

10 AWS services. Complete security. Full monitoring.

All from a single prompt.

That's the power of agentic coding."
```

**Final Screen**:
```
✅ 10 AWS Services Deployed
✅ Production-Ready Infrastructure  
✅ Security & Monitoring Included
✅ Cost: ~$54/month for 1,000 users

AWS Prompt the Planet Challenge
github.com/[your-repo]
```

---

## 🎬 Recording Instructions

### Tools You'll Need:

1. **Screen Recorder**:
   - **macOS**: QuickTime (free) or ScreenFlow
   - **Windows**: OBS Studio (free) or Camtasia
   - **Linux**: SimpleScreenRecorder or OBS Studio
   - **Web**: Loom (easiest, free tier available)

2. **Video Editor** (optional):
   - **Simple**: iMovie (Mac) or Windows Video Editor
   - **Advanced**: DaVinci Resolve (free, professional)
   - **Web**: Kapwing or Clipchamp

### Recording Steps:

#### Option A: Record with Voiceover

```bash
1. Write out your voiceover script
2. Practice reading it (3-5 times)
3. Start screen recorder
4. Record voiceover while performing actions
5. Edit out pauses/mistakes
```

#### Option B: Record with Text Overlays (Easier)

```bash
1. Record screen silently
2. Speed up slow parts (deployments)
3. Add text overlays in video editor
4. Add background music (royalty-free)
```

### Recommended Approach:

**For fastest results**: Use **Loom**

```bash
1. Go to loom.com
2. Install browser extension
3. Click "Record Screen"
4. Follow the script above
5. Loom auto-uploads and gives you a shareable link
```

---

## 🎥 Actual Recording Commands

### Pre-Recording Setup:

```bash
# 1. Clean up your terminal
clear

# 2. Set up environment
export API_ENDPOINT="https://xxxxx.execute-api.us-east-1.amazonaws.com/v1"
export API_KEY="your-test-key"

# 3. Have these commands ready in a file:
cat > demo-commands.sh << 'EOF'
# Scene 2: Setup verification
aws sts get-caller-identity
node --version
python3 --version

# Scene 6: Deployment
cd diabetes-intelligence-agent
npm install
npm run deploy:dev

# Scene 8: Testing
curl ${API_ENDPOINT}/health

curl -X POST ${API_ENDPOINT}/analyze \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "food": "burger and fries",
    "timing": "11:00 PM",
    "glucose_trend": "rising"
  }' | jq '.'
EOF

chmod +x demo-commands.sh
```

### During Recording:

```bash
# Run commands one at a time
# Pause between sections to add text overlays later
```

---

## 🎨 Visual Enhancements

### Text Overlays to Add:

**At various points, overlay:**
```
⏱️ Time: 2 minutes elapsed
💰 Cost: ~$54/month
📊 10 AWS Services
✅ Production-Ready
🔒 Security Included
```

### Highlight Effects:

- **Zoom in** on important code sections
- **Highlight** key terminal output (green boxes)
- **Arrows** pointing to important UI elements
- **Checkmarks** appearing as services deploy

### Background Music:

Use royalty-free music from:
- YouTube Audio Library
- Epidemic Sound
- Bensound.com (free with attribution)

**Recommendation**: Upbeat, tech-focused instrumental

---

## 📱 Quick Mobile Demo Alternative

If you want a **super fast** demo without editing:

### Use asciinema (Terminal Recording):

```bash
# Install asciinema
pip install asciinema

# Record terminal session
asciinema rec demo.cast

# Upload and share
asciinema upload demo.cast
# Returns a shareable URL

# Or convert to GIF
sudo npm install -g asciicast2gif
asciicast2gif demo.cast demo.gif
```

This creates a **lightweight, shareable terminal recording**.

---

## 🎯 Pro Tips

### 1. Speed Things Up
- Use **2-3x speed** for:
  - npm install
  - CDK deployment
  - File generation

### 2. Hide Sensitive Info
- Blur out:
  - AWS Account IDs
  - API keys
  - Endpoint URLs (if needed)

### 3. Keep It Short
- Aim for **3 minutes**, max 5
- Judges have limited time
- Focus on the "wow" factor

### 4. Show Real Results
- Don't fake anything
- Actual deployment
- Real API responses
- Live CloudWatch metrics

### 5. Add Captions
- Many people watch without sound
- Text overlays are crucial

---

## 📤 Where to Upload

### YouTube
```
Title: "Deploy AWS Infrastructure in 5 Minutes with One Prompt"
Description: [Link to GitHub repo]
Tags: AWS, CDK, Bedrock, Serverless, AI, Infrastructure
Visibility: Unlisted (share link in submission)
```

### Loom
```
- Records + uploads automatically
- Get shareable link instantly
- Easy trimming tool built-in
```

### GitHub
```
- Upload to repo as demo.mp4
- Add to README with thumbnail
- Embed in submission docs
```

---

## 🎬 Example Video Outline (Copy-Paste)

```
0:00 - Hook: "Deploy AWS in 5 minutes"
0:20 - Show AWS setup
0:40 - Show the prompt
1:00 - Paste into Kiro IDE
1:30 - Show generated code
2:00 - Deploy with one command
3:00 - AWS Console tour
3:45 - Test live API
4:30 - CloudWatch monitoring
4:50 - Closing + call to action
```

---

## ✅ Pre-Recording Checklist

- [ ] AWS account configured and tested
- [ ] All prerequisites installed (Node, Python, CDK)
- [ ] Demo commands prepared in a file
- [ ] Screen recorder tested
- [ ] Terminal font size increased (for visibility)
- [ ] Browser tabs closed (clean desktop)
- [ ] Notifications disabled
- [ ] Test API endpoints working
- [ ] CloudWatch dashboard open in browser tab

---

## 🚀 Quick Start: Record in 30 Minutes

**Fastest path to a demo video:**

1. **Install Loom** (5 min)
2. **Run through the demo once** without recording (10 min)
3. **Record with Loom** (5 min)
4. **Watch and trim** any mistakes (5 min)
5. **Upload to YouTube** or share Loom link (5 min)

**Total: 30 minutes to a shareable demo**

---

## 💡 Alternative: GIF Demo

If video feels like too much, create an **animated GIF**:

```bash
# Use Kap (macOS) or ScreenToGif (Windows)
# Record 30-second clips
# Export as GIF
# Add to README.md
```

**Examples of what to GIF**:
1. Pasting prompt → code generation
2. Running deploy command → success
3. Testing API → getting response

---

## 📧 Need Help?

If you want me to:
- Write specific voiceover lines
- Create text overlay suggestions
- Generate thumbnail ideas
- Review your video

Just ask! I can help refine the demo.

---

**Next Step**: Pick your recording tool and let's make this demo! 🎥
