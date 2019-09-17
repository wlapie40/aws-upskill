pipeline {
  agent any
    environment {
                AWS_BIN = '/home/ec2-user/.local/bin/aws'
                }
  stages {
    stage('Build') {
      steps {
        echo 'Building... jenkins 1.1'
        sh 'make build'
        sh 'AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}'
        sh 'AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY'
        sh 'echo AWS_ACCESS_KEY_ID'
        sh 'echo AWS_SECRET_ACCESS_KEY'
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

