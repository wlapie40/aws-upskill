pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building make..'
                sh 'echo "$PATH"'
                sh 'export PATH=$PATH:/usr/local/bin/docker-compose'
                sh 'python --version'
                sh 'make build'
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