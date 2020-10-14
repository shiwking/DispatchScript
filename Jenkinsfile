pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python-jenkins' 
                }
            }
            steps {
                sh 'python3 -m /var/jenkins_home/DispatchScript/DistributeScripts.py' 
            }
        }
    }
}
