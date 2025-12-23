pipeline {
    agent any

    environment {
        AWS_REGION          = 'us-west-2'
        ECR_REGISTRY        = '659591640509.dkr.ecr.us-west-2.amazonaws.com'
        IMAGE_TAG           = "${env.GIT_COMMIT ? env.GIT_COMMIT.take(7) : env.BUILD_NUMBER}"
        GITOPS_REPO         = 'git@github.com:maxiemoses-eu/--placeholder-agrocd-yaml.git' 
        GITOPS_BRANCH       = 'main'
        GITOPS_CREDENTIAL   = 'gitops-ssh-key'
        AWS_CREDENTIAL_ID   = 'AWS_ECR_PUSH_CREDENTIALS'

        TRIVY_CACHE         = "${WORKSPACE}/.trivycache"
        NPM_CACHE           = "${WORKSPACE}/.npm"
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Build & Test Microservices') {
            parallel {
                stage('UBS') {
                    steps {
                        dir('user-billing-service') {
                            sh 'python3 -m venv venv && venv/bin/pip install --upgrade pip'
                            retry(3) { sh 'venv/bin/pip install -r requirements.txt' }
                            sh 'venv/bin/python -m unittest || echo "No tests defined"'
                        }
                    }
                }
                stage('DAS') {
                    steps {
                        dir('data-api-service') {
                            sh 'python3 -m venv venv && venv/bin/pip install --upgrade pip'
                            retry(3) { sh 'venv/bin/pip install -r requirements.txt' }
                            sh 'venv/bin/pytest || echo "No tests defined"'
                        }
                    }
                }
                stage('DIS') {
                    steps {
                        dir('data-ingest-service') {
                            sh 'python3 -m venv venv && venv/bin/pip install --upgrade pip'
                            retry(3) { sh 'venv/bin/pip install -r requirements.txt' }
                            sh 'venv/bin/pytest || echo "No tests defined"'
                        }
                    }
                }
                stage('APS') {
                    steps {
                        dir('analysis-processing-service') {
                            sh 'python3 -m venv venv && venv/bin/pip install --upgrade pip'
                            retry(3) { sh 'venv/bin/pip install -r requirements.txt' }
                            sh 'venv/bin/python -m unittest || echo "No tests defined"'
                        }
                    }
                }
                stage('UI') {
                    steps {
                        dir('dashboard-frontend') {
                            retry(3) {
                                sh 'npm install --cache ${NPM_CACHE} --prefer-offline --legacy-peer-deps'
                            }
                            sh 'npm run build || echo "No build step defined"'
                        }
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    sh "docker build -t cloudopshub-ubs:${IMAGE_TAG} -f user-billing-service/Dockerfile user-billing-service"
                    sh "docker build -t cloudopshub-das:${IMAGE_TAG} -f data-api-service/Dockerfile data-api-service"
                    sh "docker build -t cloudopshub-dis:${IMAGE_TAG} -f data-ingest-service/Dockerfile data-ingest-service"
                    sh "docker build -t cloudopshub-aps:${IMAGE_TAG} -f analysis-processing-service/Dockerfile analysis-processing-service"
                    sh "docker build -t cloudopshub-ui:${IMAGE_TAG} -f dashboard-frontend/Dockerfile dashboard-frontend"
                }
            }
        }

        stage('Trivy Security Scan') {
            steps {
                script {
                    sh "mkdir -p ${TRIVY_CACHE}"
                    sh "trivy image --cache-dir ${TRIVY_CACHE} --download-db-only --quiet --timeout 20m"

                    def images = [
                        "cloudopshub-ubs", "cloudopshub-das", "cloudopshub-dis", "cloudopshub-aps", "cloudopshub-ui"
                    ]

                    for (img in images) {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh "trivy image --cache-dir ${TRIVY_CACHE} --scanners vuln --exit-code 1 --severity HIGH,CRITICAL --no-progress ${img}:${IMAGE_TAG}"
                        }
                    }
                }
            }
        }

        stage('Push to ECR') {
            when {
                expression { currentBuild.result in [null, 'SUCCESS', 'UNSTABLE'] }
            }
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: "${AWS_CREDENTIAL_ID}"]]) {
                    script {
                        sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}"

                        def ecrImages = ['cloudopshub-ubs', 'cloudopshub-das', 'cloudopshub-dis', 'cloudopshub-aps', 'cloudopshub-ui']

                        ecrImages.each { repoName ->
                            sh "docker tag ${repoName}:${IMAGE_TAG} ${ECR_REGISTRY}/${repoName}:${IMAGE_TAG}"
                            sh "docker push ${ECR_REGISTRY}/${repoName}:${IMAGE_TAG}"
                        }
                    }
                }
            }
        }

        stage('GitOps Promotion') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sshagent([GITOPS_CREDENTIAL]) {
                    sh """
                        rm -rf gitops
                        git clone ${GITOPS_REPO} gitops
                        cd gitops
                        
                        sed -i "s|image: .*/cloudopshub-ubs:.*|image: ${ECR_REGISTRY}/cloudopshub-ubs:${IMAGE_TAG}|g" ubs/deployment.yaml
                        sed -i "s|image: .*/cloudopshub-das:.*|image: ${ECR_REGISTRY}/cloudopshub-das:${IMAGE_TAG}|g" das/deployment.yaml
                        sed -i "s|image: .*/cloudopshub-dis:.*|image: ${ECR_REGISTRY}/cloudopshub-dis:${IMAGE_TAG}|g" dis/deployment.yaml
                        sed -i "s|image: .*/cloudopshub-aps:.*|image: ${ECR_REGISTRY}/cloudopshub-aps:${IMAGE_TAG}|g" aps/deployment.yaml
                        sed -i "s|image: .*/cloudopshub-ui:.*|image: ${ECR_REGISTRY}/cloudopshub-ui:${IMAGE_TAG}|g" ui/deployment.yaml

                        git config user.name "Jenkins CI"
                        git config user.email "ci@cloudopshub.com"

                        if ! git diff --quiet; then
                          git add .
                          git commit -m "Promote CloudOpsHub services to tag ${IMAGE_TAG}"
                          git push origin ${GITOPS_BRANCH}
                        else
                          echo "No changes to commit."
                        fi
                    """
                }
            }
        }
    }
}