pipeline {
    agent none
    stages {

        stage('InstallAPK') {
            agent {
                docker {
                    label 'suzhuji'
                    image 'python-jenkins'
                    args  '-v /var/jenkins_home:/var/jenkins_home'
                }
            }
            steps {
                sh 'python3 -u  /var/jenkins_home/DispatchScript/InstallMain.py $TestAPKName $platform $environment'
            }
        }

        stage('BuildTest') {
            agent {
                docker {
                    label 'suzhuji'
                    image 'python-jenkins'
                    args  '-v /var/jenkins_home:/var/jenkins_home'
	    args '-v /var/jenkins_home/TestResult:/var/jenkins_home/TestResult'
                }
            }
            steps {
                sh 'python3 -u  /var/jenkins_home/DispatchScript/DistributeScripts.py'
            }
        }
    }
}

