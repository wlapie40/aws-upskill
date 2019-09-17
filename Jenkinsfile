pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Building..'
        sh 'make build'
      }
    }
    stage('Test') {
      steps {
        echo 'Testing..'
      }
    }
    stage('Destroy') {
      steps {
        echo 'Destroying....'
        sh 'make down'
      }
    }
  }
}