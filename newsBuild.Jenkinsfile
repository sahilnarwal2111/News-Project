pipeline {
    agent any
    environment{
        ECR_REPO = 'frontendcors'
        ECR_URL='854171615125.dkr.ecr.us-west-1.amazonaws.com/frontendcors'
        
    }

    stages {
        stage('Authentication') {
            steps {
                sh 'aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin ${ECR_URL}'


            }
        }

       

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
        stage('Push to ECR') {
            steps {
                 sh '''
                 echo 'build step'
                 docker tag frontendpipelineimage:${BUILD_NUMBER} ${ECR_URL}:${BUILD_NUMBER}
                    docker push ${ECR_URL}:${BUILD_NUMBER}
                     '''
            }
        }
        
        stage('Trigger Deploy') {
            steps {
                build job: 'NewsDeploy', wait: false, parameters: [
                    string(name: 'FRONT_IMAGE_URL', value: "854171615125.dkr.ecr.us-west-1.amazonaws.com/frontendcors:${BUILD_NUMBER}"),
                ]
            }
        }


    }
}