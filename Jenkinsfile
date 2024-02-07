pipeline {
    agent any

    stages {
        stage('Stop DBD App') {
            steps {
                script {
                    // Corrected 'for' loop syntax and consistent directory name
                    bat 'if exist "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Dead-by-Cat-Bot\\app.pid" (for /F %%p in (C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Dead-by-Cat-Bot\\app.pid) do taskkill /F /PID %%p) else echo "DBD App not running."'
                }
            }
        }

        stage('Clone Repository') {
            steps {
                //
                checkout scm
                echo "Repository cloned to: ${pwd()}"
            }
        }

        stage('Start Application') {
            steps {
                // Change directory to the workspace directory
                bat label: 'Change Directory', script: 'cd C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Dead-by-Cat-Bot'

                // Execute the Python script
                bat label: 'Run Python Script', script: 'python app.py'
            }
        }
    }
}