pipeline {
    agent any

    stages {
        stage('Stop DBD App') {
            steps {
                // Attempt to kill the DBDapp.py process if it is running
                bat 'taskkill /F /IM python.exe /FI "WINDOWTITLE eq DBDapp" || echo "DBD App not running or cannot be stopped."'
            }
        }
        stage('Clone Repository') {
            steps {
                // Clones the repository to the current workspace
                checkout scm
                echo "Repository cloned to: ${pwd()}"
            }
        }
        stage('Start DBD App') {
            steps {
                // Starts the DBDapp.py application.
                bat 'start cmd /c "python DBDapp.py"'
                echo "DBD App started."
            }
        }
    }
}