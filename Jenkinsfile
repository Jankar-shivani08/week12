pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'shivani0824/week12app:v1'
        PYTHON_EXE = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                // Extra quotes added here
                bat "\"\"${env.PYTHON_EXE}\" -m pip install -r requirements.txt\""
            }
        }

        stage('Run Flask App and Selenium Tests') {
            steps {
                echo 'Running Selenium Tests'
                script {
                    try {
                        bat 'taskkill /F /IM python.exe || exit 0'
                        
                        bat "start /B \"\" \"${env.PYTHON_EXE}\" app.py"
                        
                        bat 'ping 127.0.0.1 -n 6 > nul'
                        
                        // Extra quotes added here
                        bat "\"\"${env.PYTHON_EXE}\" -m pytest -v\""
                    } finally {
                        echo 'Cleaning up: Stopping Flask App'
                        bat 'taskkill /F /IM python.exe || exit 0'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image'
                bat "docker build -t ${env.DOCKER_IMAGE} ."
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )]) {
                    bat 'echo %DOCKERHUB_PASSWORD%| docker login -u %DOCKERHUB_USER% --password-stdin'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                bat "docker push ${env.DOCKER_IMAGE}"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes'
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
        always {
            bat 'docker image prune -f || exit 0'
        }
    }
}