pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/Priyanka9890/AI-DevOps-Assistant.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                bat 'docker build -t devops-support-assistant:latest .'
            }
        }

        stage('Test Application') {
            steps {
                echo 'Checking Docker image...'
                bat 'docker images devops-support-assistant:latest'
            }
        }

        stage('Deploy Container') {
            steps {
                echo 'Deploying application container...'
                bat 'docker rm -f devops-assistant 2>nul || exit 0'
                bat 'docker run -d --name devops-assistant -p 5000:5000 devops-support-assistant:latest'
            }
        }

        stage('Pipeline Success') {
            steps {
                echo 'CI/CD pipeline completed successfully!'
                echo 'Application deployed on http://localhost:5000'
            }
        }
    }
}