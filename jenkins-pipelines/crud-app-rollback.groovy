pipeline {
  agent any

  parameters {
    string(name: 'image_rollback', description: 'Ex: ferr3ira/crud-app:5')
  }
  stages {
    stage('Rolling back deploy crud-app in minikube') {
      steps {
        sh "kubectl set image deployment/crud-app-rs crud-app=${params.image_rollback}"
      }
    }
  }
}
