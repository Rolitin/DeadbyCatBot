pipeline {
    agent any

    triggers {
        GitHubPushTrigger()
    }

    stages {
        stage('Stop DBD App') {
            steps {
                script {
                    // Attempt to kill the DBDapp.py process if it is running
                    bat 'taskkill /IM "python.exe" /FI "WINDOWTITLE eq DBDapp" /F || echo "DBD App not running or cannot be stopped."'
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    // Clones the repository to the current workspace
                    git 'https://github.com/NuggetSpace/DeadByCat.git'
                    echo "Repository cloned to: ${pwd()}"
                }
            }
        }

        stage('Start DBD App') {
            steps {
                script {
                    // Starts the DBDapp.py application.
                    bat 'start "DBDapp" cmd /c "python DBDapp.py"'
                    echo "DBD App started."
                }
            }
        }
    }
}
