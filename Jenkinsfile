pipeline {
    agent {
        docker {
            image 'python:3.6.9-alpine'
              }
        }
    stages {
        stage('Build') {
            steps {
                echo 'Building make2..'
                sh 'python --version'
                //sh 'make build'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}