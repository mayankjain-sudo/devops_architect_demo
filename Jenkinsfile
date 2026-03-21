pipeline {
    agent any

    environment {
        // Change this to your preferred Docker registry and repository
        IMAGE_NAME = "devops-demo-app"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        // DOCKER_CREDENTIALS_ID = "docker-credentials"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    reuseNode true
                }
            }
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python -m py_compile app.py'
            }
        }

        stage('Dependency Scan') {
            steps {
                // Assumes Trivy is installed on the Jenkins agent
                sh 'trivy fs --severity HIGH,CRITICAL --exit-code 0 .'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    APP_IMAGE = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Container Scan') {
            steps {
                // Assumes Trivy is installed on the Jenkins agent
                sh "trivy image --severity HIGH,CRITICAL --exit-code 0 ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        /*
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        APP_IMAGE.push()
                        APP_IMAGE.push('latest')
                    }
                }
            }
        }
        */
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}
