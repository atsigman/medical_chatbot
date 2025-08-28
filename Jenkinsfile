pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'medical-chatbot-repo'
        IMAGE_TAG = 'latest'
        SERVICE_NAME = 'llmops-medical-service'
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/atsigman/medical_chatbot']])
                }
            }
        }

       stage('Build, Scan, and Push Docker Image to ECR') {
           steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
            script {
                def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
                def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                sh """
                # Authenticate with ECR
                aws ecr get-login-password --region ${AWS_REGION} \
                    | docker login --username AWS --password-stdin ${ecrUrl}

                # Create buildx builder if not exists
                docker buildx create --name multiarch-builder --driver docker-container || true
                docker buildx use multiarch-builder
                docker buildx inspect --bootstrap
              

                # Build multi-arch image (amd64 for App Runner, arm64 for local/dev)
                docker buildx build \
                    --platform linux/amd64,linux/arm64 \
                    -t ${env.ECR_REPO}:${IMAGE_TAG} \
                    --push \
                    .

                # Scan the image with Trivy (use ECR fully qualified tag)
                trivy image --severity HIGH,CRITICAL --format json -o trivy-report.json ${imageFullTag}
                """
            }
        }
    }
}

        // stage('Build, Scan, and Push Docker Image to ECR') {
        //     steps {
        //         withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
        //             script {
        //                 def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
        //                 def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
        //                 def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

        //                 sh """
        //                 aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
        //                 docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
        //                 trivy image --severity HIGH,CRITICAL --format json -o trivy-report.json ${env.ECR_REPO}:${IMAGE_TAG} || true
        //                 docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${imageFullTag}
        //                 docker push ${imageFullTag}
        //                 """

        //                 archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
        //             }
        //         }
        //     }
        // }

        //  stage('Deploy to AWS App Runner') {
        //     steps {
        //         withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
        //             script {
        //                 def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
        //                 def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
        //                 def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

        //                 echo "Triggering deployment to AWS App Runner..."

        //                 sh """
        //                 SERVICE_ARN=\$(aws apprunner list-services --query "ServiceSummaryList[?ServiceName=='${SERVICE_NAME}'].ServiceArn" --output text --region ${AWS_REGION})
        //                 echo "Found App Runner Service ARN: \$SERVICE_ARN"

        //                 aws apprunner start-deployment --service-arn \$SERVICE_ARN --region ${AWS_REGION}
        //                 """
        //             }
        //         }
        //     }
        // }
    }
}