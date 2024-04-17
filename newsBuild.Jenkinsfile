pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh ''' 
                 echo 'build step'
                 ls frontend  
                 cd frontend
                 docker build -t frontendpipelineimage:${BUILD_NUMBER} .
                '''
            }
        }           

    }
}
