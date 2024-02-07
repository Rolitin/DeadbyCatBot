pipeline {
    agent any

    triggers {
        // Assumes the GitHub webhook is configured to trigger this job.
        GitHubPushTrigger()
    }

    stages {
        stage('Stop DBD App') {
            steps {
                script {
                    // Attempt to kill the DBDapp.py process. Adjust as necessary for your setup.
                    // This example assumes you have a way to identify and stop the app specifically.
                    // You might need a custom script or command to gracefully stop your application.
                    bat 'taskkill /IM "python.exe" /FI "WINDOWTITLE eq DBDapp" /F || echo "DBD App not running or cannot be stopped."'
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    // Clones the repository to the current workspace
                    // Make sure to replace with your repository URL
                    git 'https://github.com/NuggetSpace/DeadByCat.git'
                    // Prints the location where the repo was cloned
                    echo "Repository cloned to: ${pwd()}"
                }
            }
        }

        stage('Start DBD App') {
            steps {
                script {
                    // Starts the DBDapp.py application. Adjust the command as needed.
                    // This command assumes DBDapp.py is directly runnable with python and does not account for virtual environments.
                    bat 'start "DBDapp" cmd /c "python DBDapp.py"'
                    echo "DBD App started."
                }
            }
        }
    }
}
