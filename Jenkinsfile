pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'shivani0824/week12app:v1'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                bat 'C:\\Users\\Shivani\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Run Flask App and Selenium Tests') {
            steps {
                echo 'Running Selenium Tests'
                script {
                    try {
                        bat 'taskkill /F /IM python.exe || exit 0'
                        bat 'start /B C:\\Users\\Shivani\\AppData\\Local\\Programs\\Python\\Python313\\python.exe app.py'
                        bat 'ping 127.0.0.1 -n 6 > nul'
                        bat 'C:\\Users\\Shivani\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pytest -v'
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