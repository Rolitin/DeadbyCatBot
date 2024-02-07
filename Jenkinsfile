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

                // Wait for the desired message in the console output
                script {
                    def found = false
                    def output = currentBuild.rawBuild.getLog(1000)
                    for (line in output) {
                        if (line.contains("Logged in as Dead by Cat")) {
                            found = true
                            break
                        }
                    }
                    if (found) {
                        echo "Application started successfully."
                    } else {
                        error "Application did not start successfully."
                    }
                }
            }
        }
    }
}