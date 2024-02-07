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

                // Start the Python script in a new window
                bat label: 'Run Python Script', script: 'start "DBD App" cmd /K "python app.py"'

                // Wait for the desired message in the console output
                timeout(time: 5, unit: 'MINUTES') {
                    waitUntil {
                        def output = bat(script: 'type app.log', returnStdout: true).trim()
                        return output.contains("Logged in as Dead by Cat")
                    }
                }
            }
        }
    }
}