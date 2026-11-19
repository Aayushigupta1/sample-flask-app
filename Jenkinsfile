pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checkout completed'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Automated Testing') {
            steps {
                bat 'python -m pytest -v'
            }
        }

        stage('Secure Credential Handling') {
            steps {
                withCredentials([string(credentialsId: 'flask-api-token', variable: 'API_TOKEN')]) {
                    bat '''
                        if defined API_TOKEN (
                            echo SUCCESS: Jenkins credential injected securely
                        ) else (
                            echo ERROR: Credential unavailable
                            exit /b 1
                        )
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t flask-ci-cd-app .'
            }
        }

        stage('Deploy Application') {
            steps {
                bat 'docker rm -f flask-ci-cd-container 2>nul || exit /b 0'
                bat 'docker run -d --name flask-ci-cd-container -p 5000:5000 flask-ci-cd-app'
            }
        }
    }

    post {
        success {
            echo 'Pipeline successful! Application deployed.'
        }
        failure {
            echo 'Pipeline failed! Deployment stopped.'
        }
    }
}
