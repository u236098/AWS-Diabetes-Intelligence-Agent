import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as cloudwatch_actions from 'aws-cdk-lib/aws-cloudwatch-actions';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as sns_subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';
import * as kms from 'aws-cdk-lib/aws-kms';
import * as budgets from 'aws-cdk-lib/aws-budgets';
import { Tracing } from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';

export interface DiabetesIntelligenceStackProps extends cdk.StackProps {
  config: {
    lambdaMemory: number;
    lambdaTimeout: number;
    reservedConcurrency: number;
    logRetentionDays: number;
    enableXRay: boolean;
    costAlertThreshold: number;
  };
}

export class DiabetesIntelligenceStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: DiabetesIntelligenceStackProps) {
    super(scope, id, props);

    const { config } = props;

    // ========================================
    // 1. KMS Encryption Key
    // ========================================
    const encryptionKey = new kms.Key(this, 'EncryptionKey', {
      description: 'KMS key for Diabetes Intelligence Agent data encryption',
      enableKeyRotation: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Change to RETAIN for production
      alias: 'diabetes-intelligence-key',
    });

    // ========================================
    // 2. S3 Buckets for Storage
    // ========================================
    const dataStorageBucket = new s3.Bucket(this, 'DataStorageBucket', {
      bucketName: `diabetes-intelligence-data-${this.account}-${this.region}`,
      encryption: s3.BucketEncryption.KMS,
      encryptionKey: encryptionKey,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      versioned: true,
      lifecycleRules: [
        {
          id: 'DeleteOldLogs',
          enabled: true,
          expiration: cdk.Duration.days(30),
        },
        {
          id: 'TransitionToInfrequentAccess',
          enabled: true,
          transitions: [
            {
              storageClass: s3.StorageClass.INFREQUENT_ACCESS,
              transitionAfter: cdk.Duration.days(7),
            },
          ],
        },
      ],
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Change to RETAIN for production
      autoDeleteObjects: true, // Only for demo purposes
    });

    // ========================================
    // 3. SNS Topic for Alerts
    // ========================================
    const alertTopic = new sns.Topic(this, 'AlertTopic', {
      displayName: 'Diabetes Intelligence Agent Alerts',
      topicName: 'diabetes-intelligence-alerts',
    });

    // Add email subscription (replace with actual email)
    // alertTopic.addSubscription(
    //   new sns_subscriptions.EmailSubscription('your-email@example.com')
    // );

    // ========================================
    // 4. IAM Role for Lambda Functions
    // ========================================
    const lambdaRole = new iam.Role(this, 'LambdaExecutionRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      description: 'Execution role for Diabetes Intelligence Lambda functions',
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
      ],
    });

    // Add Bedrock permissions
    lambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'bedrock:InvokeModel',
          'bedrock:InvokeModelWithResponseStream',
        ],
        resources: [
          `arn:aws:bedrock:${this.region}::foundation-model/anthropic.claude-*`,
        ],
      })
    );

    // Add S3 permissions
    dataStorageBucket.grantReadWrite(lambdaRole);

    // Add KMS permissions
    encryptionKey.grantEncryptDecrypt(lambdaRole);

    // Add X-Ray permissions if enabled
    if (config.enableXRay) {
      lambdaRole.addToPolicy(
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: [
            'xray:PutTraceSegments',
            'xray:PutTelemetryRecords',
          ],
          resources: ['*'],
        })
      );
    }

    // Add Rekognition permissions (optional)
    lambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'rekognition:DetectLabels',
        ],
        resources: ['*'],
      })
    );

    // ========================================
    // 5. Lambda Layer for Shared Dependencies
    // ========================================
    const dependenciesLayer = new lambda.LayerVersion(this, 'DependenciesLayer', {
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/layer')),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_12],
      description: 'Shared dependencies for Lambda functions (boto3, aws-xray-sdk)',
      layerVersionName: 'diabetes-intelligence-dependencies',
    });

    // ========================================
    // 6. Lambda Functions
    // ========================================

    // Common Lambda configuration
    const lambdaCommonProps = {
      runtime: lambda.Runtime.PYTHON_3_12,
      memorySize: config.lambdaMemory,
      timeout: cdk.Duration.seconds(config.lambdaTimeout),
      role: lambdaRole,
      layers: [dependenciesLayer],
      tracing: config.enableXRay ? Tracing.ACTIVE : Tracing.DISABLED,
      environment: {
        DATA_BUCKET: dataStorageBucket.bucketName,
        BEDROCK_MODEL_ID: 'anthropic.claude-sonnet-4-6-v1:0',
        LOG_LEVEL: 'INFO',
        POWERTOOLS_SERVICE_NAME: 'diabetes-intelligence',
      },
      logRetention: logs.RetentionDays.ONE_WEEK,
    };

    // Pattern Analysis Function
    const patternAnalysisFunction = new lambda.Function(this, 'PatternAnalysisFunction', {
      ...lambdaCommonProps,
      functionName: 'diabetes-pattern-analysis',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/analysis')),
      handler: 'handler.lambda_handler',
      description: 'Analyzes lifestyle patterns from user inputs',
      reservedConcurrentExecutions: config.reservedConcurrency,
    });

    // Insight Generator Function
    const insightGeneratorFunction = new lambda.Function(this, 'InsightGeneratorFunction', {
      ...lambdaCommonProps,
      functionName: 'diabetes-insight-generator',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/insights')),
      handler: 'handler.lambda_handler',
      description: 'Generates human-readable insights from patterns',
      reservedConcurrentExecutions: config.reservedConcurrency,
    });

    // Food Detection Function
    const foodDetectionFunction = new lambda.Function(this, 'FoodDetectionFunction', {
      ...lambdaCommonProps,
      functionName: 'diabetes-food-detection',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/food-detection')),
      handler: 'handler.lambda_handler',
      description: 'Detects food from images using Rekognition',
      reservedConcurrentExecutions: config.reservedConcurrency,
    });

    // ========================================
    // 7. API Gateway REST API
    // ========================================
    const api = new apigateway.RestApi(this, 'DiabetesIntelligenceAPI', {
      restApiName: 'Diabetes Intelligence API',
      description: 'API for Diabetes Intelligence Agent',
      deployOptions: {
        stageName: 'v1',
        throttlingRateLimit: 1000,
        throttlingBurstLimit: 2000,
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        metricsEnabled: true,
        tracingEnabled: config.enableXRay,
      },
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS, // Restrict in production
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          'Authorization',
          'X-Api-Key',
          'X-Amz-Security-Token',
        ],
      },
      cloudWatchRole: true,
    });

    // API Key and Usage Plan
    const apiKey = api.addApiKey('ApiKey', {
      apiKeyName: 'diabetes-intelligence-api-key',
      description: 'API Key for Diabetes Intelligence Agent',
    });

    const usagePlan = api.addUsagePlan('UsagePlan', {
      name: 'Standard Usage Plan',
      description: 'Standard usage plan with rate limiting',
      throttle: {
        rateLimit: 1000,
        burstLimit: 2000,
      },
      quota: {
        limit: 100000,
        period: apigateway.Period.MONTH,
      },
    });

    usagePlan.addApiKey(apiKey);
    usagePlan.addApiStage({
      stage: api.deploymentStage,
    });

    // ========================================
    // 8. API Resources and Methods
    // ========================================

    // Request validator for input validation
    const requestValidator = new apigateway.RequestValidator(this, 'RequestValidator', {
      restApi: api,
      validateRequestBody: true,
      validateRequestParameters: true,
    });

    // /analyze endpoint
    const analyzeResource = api.root.addResource('analyze');
    analyzeResource.addMethod(
      'POST',
      new apigateway.LambdaIntegration(patternAnalysisFunction, {
        proxy: true,
        integrationResponses: [
          {
            statusCode: '200',
            responseParameters: {
              'method.response.header.Access-Control-Allow-Origin': "'*'",
            },
          },
        ],
      }),
      {
        apiKeyRequired: true,
        requestValidator: requestValidator,
        methodResponses: [
          {
            statusCode: '200',
            responseParameters: {
              'method.response.header.Access-Control-Allow-Origin': true,
            },
          },
        ],
      }
    );

    // /insights endpoint
    const insightsResource = api.root.addResource('insights');
    insightsResource.addMethod(
      'POST',
      new apigateway.LambdaIntegration(insightGeneratorFunction, {
        proxy: true,
      }),
      {
        apiKeyRequired: true,
        requestValidator: requestValidator,
      }
    );

    // /food endpoint
    const foodResource = api.root.addResource('food');
    foodResource.addMethod(
      'POST',
      new apigateway.LambdaIntegration(foodDetectionFunction, {
        proxy: true,
      }),
      {
        apiKeyRequired: true,
        requestValidator: requestValidator,
      }
    );

    // Health check endpoint (no API key required)
    const healthResource = api.root.addResource('health');
    healthResource.addMethod(
      'GET',
      new apigateway.MockIntegration({
        integrationResponses: [
          {
            statusCode: '200',
            responseTemplates: {
              'application/json': '{"status": "healthy", "timestamp": "$context.requestTime"}',
            },
          },
        ],
        requestTemplates: {
          'application/json': '{"statusCode": 200}',
        },
      }),
      {
        apiKeyRequired: false,
        methodResponses: [{ statusCode: '200' }],
      }
    );

    // ========================================
    // 9. CloudWatch Alarms
    // ========================================

    // Lambda Error Rate Alarm
    const patternAnalysisErrorAlarm = new cloudwatch.Alarm(this, 'PatternAnalysisErrorAlarm', {
      metric: patternAnalysisFunction.metricErrors({
        period: cdk.Duration.minutes(5),
        statistic: 'Sum',
      }),
      threshold: 5,
      evaluationPeriods: 2,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      alarmDescription: 'Pattern Analysis function error rate is too high',
      actionsEnabled: true,
    });
    patternAnalysisErrorAlarm.addAlarmAction(new cloudwatch_actions.SnsAction(alertTopic));

    // Lambda Duration Alarm
    const patternAnalysisDurationAlarm = new cloudwatch.Alarm(this, 'PatternAnalysisDurationAlarm', {
      metric: patternAnalysisFunction.metricDuration({
        period: cdk.Duration.minutes(5),
        statistic: 'Average',
      }),
      threshold: 5000, // 5 seconds
      evaluationPeriods: 2,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      alarmDescription: 'Pattern Analysis function duration is too high',
      actionsEnabled: true,
    });
    patternAnalysisDurationAlarm.addAlarmAction(new cloudwatch_actions.SnsAction(alertTopic));

    // API Gateway 5xx Errors
    const api5xxAlarm = new cloudwatch.Alarm(this, 'Api5xxErrorAlarm', {
      metric: api.metricServerError({
        period: cdk.Duration.minutes(5),
        statistic: 'Sum',
      }),
      threshold: 10,
      evaluationPeriods: 2,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      alarmDescription: 'API Gateway 5xx error rate is too high',
      actionsEnabled: true,
    });
    api5xxAlarm.addAlarmAction(new cloudwatch_actions.SnsAction(alertTopic));

    // ========================================
    // 10. CloudWatch Dashboard
    // ========================================
    const dashboard = new cloudwatch.Dashboard(this, 'DiabetesIntelligenceDashboard', {
      dashboardName: 'Diabetes-Intelligence-Agent',
    });

    dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'API Request Count',
        left: [api.metricCount()],
        width: 12,
      }),
      new cloudwatch.GraphWidget({
        title: 'API Latency',
        left: [api.metricLatency()],
        width: 12,
      }),
      new cloudwatch.GraphWidget({
        title: 'Lambda Invocations',
        left: [
          patternAnalysisFunction.metricInvocations(),
          insightGeneratorFunction.metricInvocations(),
          foodDetectionFunction.metricInvocations(),
        ],
        width: 12,
      }),
      new cloudwatch.GraphWidget({
        title: 'Lambda Errors',
        left: [
          patternAnalysisFunction.metricErrors(),
          insightGeneratorFunction.metricErrors(),
          foodDetectionFunction.metricErrors(),
        ],
        width: 12,
      })
    );

    // ========================================
    // 11. Budget Alert
    // ========================================
    new budgets.CfnBudget(this, 'MonthlyBudget', {
      budget: {
        budgetName: 'diabetes-intelligence-monthly-budget',
        budgetType: 'COST',
        timeUnit: 'MONTHLY',
        budgetLimit: {
          amount: config.costAlertThreshold,
          unit: 'USD',
        },
      },
      notificationsWithSubscribers: [
        {
          notification: {
            notificationType: 'ACTUAL',
            comparisonOperator: 'GREATER_THAN',
            threshold: 80, // Alert at 80% of budget
            thresholdType: 'PERCENTAGE',
          },
          subscribers: [
            {
              subscriptionType: 'SNS',
              address: alertTopic.topicArn,
            },
          ],
        },
      ],
    });

    // ========================================
    // 12. CloudFormation Outputs
    // ========================================
    new cdk.CfnOutput(this, 'ApiEndpoint', {
      value: api.url,
      description: 'API Gateway endpoint URL',
      exportName: 'DiabetesIntelligenceApiEndpoint',
    });

    new cdk.CfnOutput(this, 'ApiKeyId', {
      value: apiKey.keyId,
      description: 'API Key ID (retrieve value from AWS Console)',
      exportName: 'DiabetesIntelligenceApiKeyId',
    });

    new cdk.CfnOutput(this, 'DataBucketName', {
      value: dataStorageBucket.bucketName,
      description: 'S3 bucket for data storage',
      exportName: 'DiabetesIntelligenceDataBucket',
    });

    new cdk.CfnOutput(this, 'DashboardURL', {
      value: `https://console.aws.amazon.com/cloudwatch/home?region=${this.region}#dashboards:name=Diabetes-Intelligence-Agent`,
      description: 'CloudWatch Dashboard URL',
    });

    new cdk.CfnOutput(this, 'PatternAnalysisFunctionName', {
      value: patternAnalysisFunction.functionName,
      description: 'Pattern Analysis Lambda function name',
    });

    new cdk.CfnOutput(this, 'InsightGeneratorFunctionName', {
      value: insightGeneratorFunction.functionName,
      description: 'Insight Generator Lambda function name',
    });

    new cdk.CfnOutput(this, 'FoodDetectionFunctionName', {
      value: foodDetectionFunction.functionName,
      description: 'Food Detection Lambda function name',
    });
  }
}
