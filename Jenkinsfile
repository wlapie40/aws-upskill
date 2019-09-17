pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Building... jenkins 1.1'
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