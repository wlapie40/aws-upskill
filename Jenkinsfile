pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building.. new'
                sh 'python3 -m database_conf_gen.py'
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