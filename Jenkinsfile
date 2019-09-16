pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building.. new jenkins'
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
