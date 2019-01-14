pipeline {
  agent any
  stages {
    stage('Cleanning workspace') {
      steps {
          deleteDir() 
      }
    }
    stage('Git clone crud-app') {
      steps {
        withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'github', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
          sh 'git clone https://$USERNAME:$PASSWORD@github.com/NoroFerr3ira/crud-app.git'
        }
      }  
    }
    stage('Run crud-app tests') {
      steps {
          sh 'ls'
      }
    }
    stage('Build crud-app container image') {
      steps {
          sh 'cd crud-app && docker build -t ferr3ira/crud-app:${BUILD_NUMBER} .'
      }      
    }
    stage('Publish Container') {
      steps {
        withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
          sh 'docker login -u $USERNAME -p $PASSWORD'
          sh 'docker push ferr3ira/crud-app:${BUILD_NUMBER}' 
        }
      }
    }
    stage('Deploy crud-app in minikube') {
      steps {
          sh 'kubectl set image deployment/crud-app-rs crud-app=ferr3ira/crud-app:${BUILD_NUMBER}' 
      }
      post {
        failure {
          sh 'kubectl rollout undo deployment/crud-app-rs'
        }
      }
    }
  }
}
