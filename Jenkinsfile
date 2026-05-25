pipeline {
    agent { label 'python' }

    environment {
        IMAGE_NAME = "dockerhubusername/python-login-app"
    }

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                url: 'https://github.com/USERNAME/python-login-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {

                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                }
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker push $IMAGE_NAME:$BUILD_NUMBER'
            }
        }

        stage('Deploy Container') {
            steps {

                sh '''
                docker stop python-app || true
                docker rm python-app || true

                docker run -d \
                --name python-app \
                -p 5000:5000 \
                $IMAGE_NAME:$BUILD_NUMBER
                '''
            }
        }
    }
}