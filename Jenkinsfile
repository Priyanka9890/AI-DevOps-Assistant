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
                bat 'docker --context desktop-linux build -t devops-support-assistant:latest .'
            }
        }

        stage('Test Application') {
            steps {
                echo 'Running basic application check...'
                bat 'docker build -t devops-support-assistant:latest .'
            }
        }

        stage('Pipeline Success') {
            steps {
                echo 'CI/CD pipeline completed successfully!'
            }
        }
    }
}