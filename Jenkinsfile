pipeline {
    agent { label 'macbookair' }
    
    parameters {
        string(name: 'email', defaultValue: '', description: '通知邮箱地址')
        string(name: 'test_suite', defaultValue: 'tests_py', description: '测试目录 (tests_py 或 tests 或 tests/simple_test.robot)')
        string(name: 'base_url', defaultValue: 'https://blog.gdw1986.top/wp-content/uploads/2026/04', description: '测试环境 BASE_URL')
    }
    
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
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '"${PIP_PATH}" install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    if (params.test_suite.endsWith('.robot')) {
                        // Robot Framework
                        sh "robot -v TEST_URL:${params.base_url}/test_page.html -v BROWSER:chromium -v HEADLESS:true --outputdir allure-results '${params.test_suite}'"
                        // Robot 结果转 Junit XML 给 Allure
                        sh "robot --outputdir allure-results --log NONE --report NONE --xunit test-results.xml '\${params.test_suite}' || true"
                    } else {
                        // Pytest
                        sh "${PYTHON_PATH} -m pytest '${params.test_suite}' --alluredir=allure-results --clean-alluredir -v --tb=short --headless"
                    }
                }
            }
        }
    }
    
    post {
        always {
            // 生成 Allure 报告（已有 allure-results 就生成，没有就跳过）
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
        
        success {
            emailext(
                subject: "✅ 构建成功: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
构建成功！

项目: ${env.JOB_NAME}
构建号: #${env.BUILD_NUMBER}
测试环境: ${params.base_url}

📊 Allure 测试报告: ${env.BUILD_URL}allure/

🔗 控制台日志: ${env.BUILD_URL}console
                """,
                to: "${params.email}"
            )
        }
        
        failure {
            emailext(
                subject: "❌ 构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
构建失败！

项目: ${env.JOB_NAME}
构建号: #${env.BUILD_NUMBER}
测试环境: ${params.base_url}

📊 Allure 测试报告: ${env.BUILD_URL}allure/
🔗 控制台日志: ${env.BUILD_URL}console
                """,
                to: "${params.email}"
            )
        }
        
        cleanup {
            cleanWs()
        }
    }
}
