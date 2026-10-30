pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'shivani0824/week12app:v1'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                // Using 'python' relies on the system PATH. If it fails, use the full path to python.exe
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m pip install pytest selenium'
            }
        }

        stage('Run Flask App and Selenium Tests') {
            steps {
                echo 'Running Selenium Tests'
                script {
                    try {
                        // 1. Kill any old python processes to free up port 5000
                        bat 'taskkill /F /IM python.exe || exit 0'
                        
                        // 2. Start Flask app in background
                        bat 'start /B "" python app.py'
                        
                        // 3. Wait 5 seconds for the app to start
                        bat 'ping 127.0.0.1 -n 6 > nul'
                        
                        // 4. Run Tests
                        bat 'python -m pytest -v'
                    } finally {
                        // 5. ALWAYS kill the Flask app after tests (pass or fail)
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
                    // Note: In batch, %VAR% is used instead of $VAR
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
                // Using single quotes so Groovy doesn't mess with the YAML file names
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
            // Ensure Docker doesn't leave dangling build caches
            bat 'docker system prune -f || exit 0'
        }
    }
}