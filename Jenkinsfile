pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python-jenkins' 
		    args  '-v /var/jenkins_home:/var/jenkins_home'
                }
            }
            steps {
                sh 'python3 -m /var/jenkins_home/DispatchScript/DistributeScripts.py' 
            }
        }
    }
}
