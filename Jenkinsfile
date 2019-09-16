pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building make..'
                sh "echo $(whereis make)"
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