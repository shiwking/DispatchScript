pipeline {
    agent any 
    stages {
        stage('Build DockerFile') {
            steps { 
                echo 'python3 -u /var/jenkins_home/DispatchScript/BuildDockerFile.py'
            }

        stage('Run Case') {
            steps {
                echo 'python3 -u /var/jenkins_home/DispatchScript/DistributeScripts.py'
            }

        }
    }
  }
