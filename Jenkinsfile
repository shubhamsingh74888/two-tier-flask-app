@Library("shared") _
pipeline{
    
    agent none
    
    stages{
        stage("Code Clone ,build and push"){
            agent { label 'agent'}
            steps{
               script{
                   clone("https://github.com/shubhamsingh74888/two-tier-flask-app.git", "main")
                   docker_build("flask-app","latest","shubham74888")
                   docker_push("flask-app","latest","shubham74888")
               }
            }
        }
        stage("Deploy"){
            agent { label "master-node"}
            steps{
                script{
                deploy("flask-app","latest","shubham74888")
            }
         }
    }
   }
}
