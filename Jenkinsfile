pipeline {
    agent any 
    stages {
        stage('BuildDockerFile') { 
            steps { 
                sh 'echo  python3 /var/jenkins_home/DispatchScript/BuildDockerFile.py' 
            }
        }
        stage('runCase') {
            steps {
                sh 'echo  python3 /var/jenkins_home/DispatchScript/DistributeScripts.py'
            }
        }

    }
  }
