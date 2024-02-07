pipeline {
    agent any
    
    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                checkout scm
            }
        }
        stage('Stop DBD App') {
            steps {
                script {
                    bat 'if exist "C:\\Users\\rolando\\Documents\\Jenkins\\.jenkins\\workspace\\Dead-by-Cat-Bot\\app.pid" (for /F %%p in (C:\\Users\\rolando\\Documents\\Jenkins\\.jenkins\\workspace\\Dead-by-Cat-Bot\\app.pid) do taskkill /F /PID %%p ) else echo "DBD App not running."'
                }
            }
        }
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('Start Application') {
            steps {
                script {
                    bat 'start cmd /c C:\\Users\\rolando\\Desktop\\start.bat'
                }
            }
        }
    }
}
