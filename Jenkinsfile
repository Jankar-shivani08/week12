pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'shivani0824/week12app:v1'
        // Defining the exact path to Python here so we only write it once
        PYTHON_EXE = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                bat "\"${env.PYTHON_EXE}\" -m pip install -r requirements.txt"
            }
        }

        stage('Run Flask App and Selenium Tests') {
            steps {
                echo 'Running Selenium Tests'
                script {
                    try {
                        // 1. Kill any old python processes to free up port 5000
                        bat 'taskkill /F /IM python.exe || exit 0'
                        
                        // 2. Start Flask app in background using the hardcoded path
                        bat "start /B \"\" \"${env.PYTHON_EXE}\" app.py"
                        
                        // 3. Wait 5 seconds for the app to start
                        bat 'ping 127.0.0.1 -n 6 > nul'
                        
                        // 4. Run Tests using the hardcoded path
                        bat "\"${env.PYTHON_EXE}\" -m pytest -v"
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
            // Changed this to image prune so you don't delete all your containers/networks every time
            bat 'docker image prune -f || exit 0'
        }
    }
}