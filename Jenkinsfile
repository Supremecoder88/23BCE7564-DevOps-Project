pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "techsymp-website"
        DOCKER_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Supremecoder88/23BCE7564-DevOps-Project.git'
            }
        }

        stage('Maven Validate') {
            steps {
                sh 'mvn validate'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Assuming DOCKER_HUB_CREDENTIALS is set in Jenkins
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DUSER', passwordVariable: 'DPASS')]) {
                        sh "echo $DPASS | docker login -u $DUSER --password-stdin"
                        sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} $DUSER/${DOCKER_IMAGE}:${DOCKER_TAG}"
                        sh "docker push $DUSER/${DOCKER_IMAGE}:${DOCKER_TAG}"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh "kubectl apply -f k8s/manifests.yaml"
                    sh "kubectl rollout restart deployment/techsymp-deployment"
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment Complete!'
        }
        failure {
            echo 'Deployment Failed. Check logs.'
        }
    }
}
