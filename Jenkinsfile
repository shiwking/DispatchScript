pipeline {
    agent none
    stages {

        stage('install_pkg') {
            agent {
                docker {
                    image 'pkginstall'
                    args  '-v /var/jenkins_home:/var/jenkins_home'
                }
            }
            steps {
                sh 'python3 -u  /var/jenkins_home/Install_PKG/run.py $TestAPKName $platform $environment'
            }
        }

        stage('Build') {
            agent {
                docker {
                    image 'python-jenkins'
                    args  '-v /var/jenkins_home:/var/jenkins_home'
                }
            }
            steps {
                sh 'python3 -u  /var/jenkins_home/DispatchScript/DistributeScripts.py'
            }
        }
    }
}
