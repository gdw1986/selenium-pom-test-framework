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
        
        stage('Extract Test Statistics') {
            steps {
                script {
                    // 统计 allure-results 目录下的测试结果
                    def passed = 0
                    def failed = 0
                    def skipped = 0
                    def totalDuration = 0
                    
                    if (fileExists('allure-results')) {
                        def files = findFiles(glob: 'allure-results/*-result.json')
                        files.each { f ->
                            try {
                                def content = readFile file: f.path
                                def json = new groovy.json.JsonSlurper().parseText(content)
                                totalDuration += json.start ?: 0
                                totalDuration += json.stop ?: 0
                                
                                if (json.status == 'passed') {
                                    passed++
                                } else if (json.status == 'failed' || json.status == 'broken') {
                                    failed++
                                } else if (json.status == 'skipped') {
                                    skipped++
                                }
                            } catch (Exception e) {
                                echo "Error parsing ${f.path}: ${e.message}"
                            }
                        }
                    }
                    
                    def total = passed + failed + skipped
                    env.ALLURE_PASSED = passed
                    env.ALLURE_FAILED = failed
                    env.ALLURE_SKIPPED = skipped
                    env.ALLURE_TOTAL = total
                    
                    if (total > 0) {
                        env.ALLURE_PASS_RATE = String.format("%.1f%%", (passed / total) * 100)
                    } else {
                        env.ALLURE_PASS_RATE = "N/A"
                    }
                    
                    // 计算总耗时
                    def durationSec = currentBuild.duration / 1000
                    env.ALLURE_DURATION = String.format("%d分%d秒", (durationSec / 60).intValue(), durationSec % 60)
                }
            }
        }
    }
    
    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            cleanWs()
        }
        success {
            emailext (
                subject: "✅ 构建成功: ${env.JOB_NAME} #${env.BUILD_NUMBER} - 通过率 ${env.ALLURE_PASS_RATE}",
                body: """
                    <div style="font-family: Arial, sans-serif; max-width: 600px;">
                        <h2 style="color: #28a745; border-bottom: 2px solid #28a745; padding-bottom: 10px;">🎉 构建成功</h2>
                        
                        <h3 style="color: #333; margin-top: 20px;">📋 构建信息</h3>
                        <table style="border-collapse: collapse; width: 100%; background: #f9f9f9;">
                            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>项目</b></td><td style="padding: 8px; border: 1px solid #ddd;">${env.JOB_NAME}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>构建号</b></td><td style="padding: 8px; border: 1px solid #ddd;">#${env.BUILD_NUMBER}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>耗时</b></td><td style="padding: 8px; border: 1px solid #ddd;">${env.ALLURE_DURATION}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>触发原因</b></td><td style="padding: 8px; border: 1px solid #ddd;">${currentBuild.getBuildCauses()[0].shortDescription}</td></tr>
                        </table>
                        
                        <h3 style="color: #333; margin-top: 20px;">📊 测试结果</h3>
                        <table style="border-collapse: collapse; width: 100%; text-align: center;">
                            <tr style="background: #333; color: white;">
                                <th style="padding: 10px; border: 1px solid #ddd;">总计</th>
                                <th style="padding: 10px; border: 1px solid #ddd;">通过</th>
                                <th style="padding: 10px; border: 1px solid #ddd;">失败</th>
                                <th style="padding: 10px; border: 1px solid #ddd;">跳过</th>
                                <th style="padding: 10px; border: 1px solid #ddd;">通过率</th>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border: 1px solid #ddd;"><b>${env.ALLURE_TOTAL}</b></td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: #28a745;"><b>${env.ALLURE_PASSED}</b></td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: #dc3545;">${env.ALLURE_FAILED}</td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: #ffc107;">${env.ALLURE_SKIPPED}</td>
                                <td style="padding: 10px; border: 1px solid #ddd; background: #28a745; color: white;"><b>${env.ALLURE_PASS_RATE}</b></td>
                            </tr>
                        </table>
                        
                        <h3 style="color: #333; margin-top: 20px;">🔗 链接</h3>
                        <ul style="line-height: 1.8;">
                            <li><a href="${env.BUILD_URL}" style="color: #0366d6;">构建详情</a></li>
                            <li><a href="${env.BUILD_URL}allure/" style="color: #0366d6;">Allure 测试报告</a></li>
                            <li><a href="${env.BUILD_URL}console" style="color: #0366d6;">控制台日志</a></li>
                        </ul>
                        
                        <hr style="margin-top: 20px; border: none; border-top: 1px solid #ddd;">
                        <p style="color: #666; font-size: 12px;">此邮件由 Jenkins 自动发送 | ${new Date().format("yyyy-MM-dd HH:mm:ss")}</p>
                    </div>
                """,
                to: "${params.email}"
            )
            echo '✅ All tests passed!'
        }
        failure {
            emailext (
                subject: "❌ 构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <div style="font-family: Arial, sans-serif; max-width: 600px;">
                        <h2 style="color: #dc3545; border-bottom: 2px solid #dc3545; padding-bottom: 10px;">⚠️ 构建失败</h2>
                        
                        <h3 style="color: #333; margin-top: 20px;">📋 构建信息</h3>
                        <table style="border-collapse: collapse; width: 100%; background: #f9f9f9;">
                            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>项目</b></td><td style="padding: 8px; border: 1px solid #ddd;">${env.JOB_NAME}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>构建号</b></td><td style="padding: 8px; border: 1px solid #ddd;">#${env.BUILD_NUMBER}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>耗时</b></td><td style="padding: 8px; border: 1px solid #ddd;">${env.ALLURE_DURATION}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>触发原因</b></td><td style="padding: 8px; border: 1px solid #ddd;">${currentBuild.getBuildCauses()[0].shortDescription}</td></tr>
                        </table>
                        
                        <h3 style="color: #333; margin-top: 20px;">📊 测试结果</h3>
                        <table style="border-collapse: collapse; width: 100%; text-align: center;">
                            <tr style="background: #333; color: white;">
                                <th style="padding: 10px; border: 1px solid #ddd;">总计</th>
                                <th style="padding: 10px; border: 1px solid #ddd;">通过</th>
                                <th style="padding: 10px; border: 1px solid #ddd;">失败</th>
                                <th style="padding: 10px; border: 1px solid #ddd;">跳过</th>
                                <th style="padding: 10px; border: 1px solid #ddd;">通过率</th>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border: 1px solid #ddd;"><b>${env.ALLURE_TOTAL}</b></td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: #28a745;"><b>${env.ALLURE_PASSED}</b></td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: #dc3545;"><b>${env.ALLURE_FAILED}</b></td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: #ffc107;">${env.ALLURE_SKIPPED}</td>
                                <td style="padding: 10px; border: 1px solid #ddd; background: #dc3545; color: white;"><b>${env.ALLURE_PASS_RATE}</b></td>
                            </tr>
                        </table>
                        
                        <h3 style="color: #333; margin-top: 20px;">🔗 链接</h3>
                        <ul style="line-height: 1.8;">
                            <li><a href="${env.BUILD_URL}" style="color: #0366d6;">构建详情</a></li>
                            <li><a href="${env.BUILD_URL}allure/" style="color: #0366d6;">Allure 测试报告</a></li>
                            <li><a href="${env.BUILD_URL}console" style="color: #0366d6;">控制台日志</a></li>
                        </ul>
                        
                        <hr style="margin-top: 20px; border: none; border-top: 1px solid #ddd;">
                        <p style="color: #666; font-size: 12px;">此邮件由 Jenkins 自动发送 | ${new Date().format("yyyy-MM-dd HH:mm:ss")}</p>
                    </div>
                """,
                to: "${params.email}"
            )
            echo '❌ Tests failed!'
        }
    }
}
