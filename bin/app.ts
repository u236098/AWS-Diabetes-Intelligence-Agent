#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DiabetesIntelligenceStack } from '../lib/diabetes-intelligence-stack';

const app = new cdk.App();

// Get context values
const environment = app.node.tryGetContext('environment') || 'dev';
const region = app.node.tryGetContext('region') || process.env.CDK_DEFAULT_REGION || 'us-east-1';
const account = process.env.CDK_DEFAULT_ACCOUNT;

// Validate required context
if (!account) {
  throw new Error('CDK_DEFAULT_ACCOUNT environment variable must be set. Run: export CDK_DEFAULT_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)');
}

// Stack configuration based on environment
const stackConfig = {
  dev: {
    lambdaMemory: 1024,
    lambdaTimeout: 60,
    reservedConcurrency: 10,
    logRetentionDays: 7,
    enableXRay: false,
    costAlertThreshold: 50,
  },
  prod: {
    lambdaMemory: 2048,
    lambdaTimeout: 60,
    reservedConcurrency: 100,
    logRetentionDays: 30,
    enableXRay: true,
    costAlertThreshold: 500,
  },
};

const config = stackConfig[environment as keyof typeof stackConfig] || stackConfig.dev;

// Deploy the stack
new DiabetesIntelligenceStack(app, `DiabetesIntelligenceStack-${environment}`, {
  env: {
    account,
    region,
  },
  stackName: `diabetes-intelligence-${environment}`,
  description: `Diabetes Intelligence Agent - ${environment} environment (AWS Prompt the Planet Challenge)`,
  tags: {
    Project: 'DiabetesIntelligenceAgent',
    Environment: environment,
    ManagedBy: 'CDK',
    Challenge: 'AWS-Prompt-the-Planet',
    CostCenter: 'HealthTech',
  },
  config,
});

app.synth();
