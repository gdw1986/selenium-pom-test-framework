pipeline {
    agent { label 'macbookair' }
    
    tools {
        allure 'allure-commandline'
    }
    environment {
        PYTHON_PATH = 'python3'
        PIP_PATH = 'pip3'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh """
                    "${PIP_PATH}" install -r requirements.txt
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                sh """
                    ${PYTHON_PATH} -m pytest "${params.test_suite}" \
                        --alluredir=allure-results \
                        --clean-alluredir \
                        -v \
                        --tb=short \
                        --headless
                """
            }
            post {
                always {
                    script {
                        currentBuild.result = 'SUCCESS'
                    }
                }
            }
        }
        
        stage('Generate Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            emailext (
                subject: "✅ 构建成功: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <p>构建成功</p>
                    <p>项目: ${env.JOB_NAME}</p>
                    <p>构建号: ${env.BUILD_NUMBER}</p>
                    <p>地址: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                """,
                to: "${params.email}"
            )
            echo '✅ All tests passed!'
        }
        failure {
            emailext (
                subject: "❌ 构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <p>构建失败，请检查</p>
                    <p>项目: ${env.JOB_NAME}</p>
                    <p>构建号: ${env.BUILD_NUMBER}</p>
                    <p>地址: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                """,
                to: "${params.email}"
            )
            echo '❌ Tests failed!'
        }
    }
}
