pipeline {
    agent any
    
    parameters {
        string(name: 'email', defaultValue: 'gdw86216@163.com', description: '通知邮箱地址')
        string(name: 'test_suite', defaultValue: 'tests_py', description: '测试目录 (tests_py 或 tests 或 tests/simple_test.robot)')
        string(name: 'base_url', defaultValue: 'https://blog.gdw1986.top/wp-content/uploads/2026/04', description: '测试环境 BASE_URL')
    }
    
    tools {
        allure 'allure-commandline'
    }
    environment {
        PYTHON_PATH = 'venv/bin/python3'
        PIP_PATH = 'venv/bin/pip3'
    }
    
    stages {
        stage('Agent Info') {
         steps {
             echo "Running on agent: ${env.NODE_NAME}"
             sh "hostname && uname -a"
             }
        }
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo "Use venv"
                sh """
                   python3 -m venv venv
                   "${PIP_PATH}" install -r requirements.txt
                   venv/bin/playwright install 
                   venv/bin/playwright install-deps
                """
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
<div style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #28a745;">✅ 构建成功</h2>
    <p><b>项目:</b> ${env.JOB_NAME}</p>
    <p><b>构建号:</b> #${env.BUILD_NUMBER}</p>
    <p><b>测试环境:</b> ${params.base_url}</p>
    <p><b>📊 Allure 报告:</b> <a href="${env.BUILD_URL}allure/">${env.BUILD_URL}allure/</a></p>
    <p><b>🔗 控制台日志:</b> <a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a></p>
</div>
                """,
                to: "${params.email}"
            )
        }
        
        failure {
            emailext(
                subject: "❌ 构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
<div style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #dc3545;">❌ 构建失败</h2>
    <p><b>项目:</b> ${env.JOB_NAME}</p>
    <p><b>构建号:</b> #${env.BUILD_NUMBER}</p>
    <p><b>测试环境:</b> ${params.base_url}</p>
    <p><b>📊 Allure 报告:</b> <a href="${env.BUILD_URL}allure/">${env.BUILD_URL}allure/</a></p>
    <p><b>🔗 控制台日志:</b> <a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a></p>
</div>
                """,
                to: "${params.email}"
            )
        }
        
        cleanup {
            cleanWs()
        }
    }
}
