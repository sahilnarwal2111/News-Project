
pipeline {
    agent any

     parameters { string(name: 'FRONT_IMAGE_URL', defaultValue: '', description: '') }

     environment {
        AWS_REGION_K8S='us-east-2'
        K8S_CLUSTER_NAME='k8s-batch1'
        K8S_NAMESPACE='sahilnarwal-ns'
    }

    stages {
        stage('Setting default namespace') {
            steps {
                    sh '''
                    aws eks --region ${AWS_REGION_K8S} update-kubeconfig --name ${K8S_CLUSTER_NAME} 
                        kubectl config set-context --current --namespace=${K8S_NAMESPACE}
                    '''
            }
        }
        stage('Deploy') {
            steps {

                sh ''' 
                    cd frontend
		            temp=$FRONT_IMAGE_URL yq eval 'select(.kind == "Deployment").spec.template.spec.containers[0].image = env(temp)' frontend.yaml > test2.yaml
                    mv test2.yaml frontend.yaml
                    kubectl apply -f frontend.yaml  
                    
                '''
            }
        }
    }
}
