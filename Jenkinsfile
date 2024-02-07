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
                    bat 'if exist "C:\ProgramData\Jenkins\.jenkins\workspace\Dead-by-Cat-Bot\app.pid" (for /F %p in (C:\ProgramData\Jenkins\.jenkins\workspace\Dead-by-Cat-Bot\app.pid) do taskkill /F /PID %p ) else echo "DBD App not running."'
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
                bat label: 'Change Directory', script: 'cd C:\ProgramData\Jenkins\.jenkins\workspace\Dead-by-Cat-Bot'
                bat label: 'Run Python Script', script: 'start "DBD App" cmd /K "python app.py"'
            }
        }
    }
}
