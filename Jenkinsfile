pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:2-alpine' 
                }
            }
            steps {
                sh 'python -u /var/jenkins_home/DispatchScript/DistributeScripts.py' 
            }
        }
    }
}
