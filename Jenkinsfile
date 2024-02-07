pipeline {
    agent any

    stages {
        stage('Stop DBD App') {
            steps {
                script {
                    // Assuming app.py writes its PID to app.pid upon starting
                    bat script: 'if exist "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Dead by Cat Bot\\app.pid" (for /F %p in (C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Dead by Cat Bot\\app.pid) do taskkill /F /PID %p) else echo "DBD App not running."', returnStatus: true
                }
            }
        }

        stage('Clone Repository') {
            steps {
                checkout scm
                echo "Repository cloned to: ${pwd()}"
            }
        }

        stage('Start DBD App') {
            steps {
                script {
                    // Navigate to the directory where the repository is cloned and start app.py
                    bat 'cd C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Dead by Cat Bot && python app.py > app.log 2>&1 &'
                    echo "DBD App started."
                }
            }
        }
    }
}
