pipeline {
  agent any

  parameters {
    string(name: 'revision_number', description: 'Ex: 5')
  }
  stages {
    stage('Rolling back deploy crud-app in minikube') {
      steps {
        sh "kubectl rollout undo deployment/crud-app-rs --to-revision=${params.revision_number}"
      }
    }
  }
}
