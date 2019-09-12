pipeline {
    agent { docker { image 'python:3.6.8' } }
    environment
        {
            FLASK_APP             = 'app.py'
            FLASK_ENV             = 'dev'
            VIRTUAL_ENV           = "${env.WORKSPACE}/venv"
            //AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
            //AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
        }
    stages {
        stage('Install_Requirements') {
            steps {
                echo 'Creating virtualenv ...'
                    sh 'printenv'
                    sh """
                        echo ${SHELL}
                        [ -d venv ] && rm -rf venv
                        #virtualenv --python=python3.6 venv
                        virtualenv venv
                        #. venv/bin/activate
                        export PATH=${VIRTUAL_ENV}/bin:${PATH}
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        make clean
                    """
            }
            }
        }
        stage('Test') {
            steps {
                echo 'Test'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploy'
            }
        }
    }
}