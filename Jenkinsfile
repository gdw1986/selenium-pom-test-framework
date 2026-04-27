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
        BASE_URL = "${params.base_url}"
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
                script {
                    // 根据测试目录判断是 robot 还是 pytest
                    if (params.test_suite.endsWith('.robot')) {
                        // Robot Framework 测试
                        echo "Running Robot Framework tests: ${params.test_suite}"
                        sh """
                            robot -v TEST_URL:${params.base_url}/test_page.html \
                                  -v BROWSER:chromium \
                                  -v HEADLESS:true \
                                  --outputdir results \
                                  --loglevel DEBUG \
                                  "${params.test_suite}"
                        """
                    } else {
                        // Pytest 测试
                        echo "Running pytest tests: ${params.test_suite}"
                        sh """
                            ${PYTHON_PATH} -m pytest "${params.test_suite}" \
                                --alluredir=allure-results \
                                --clean-alluredir \
                                -v \
                                --tb=short \
                                --headless
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                // 提取测试统计 - 无论成功失败都执行
                def statsJson = sh(
                    script: """
                        python3 -c "
import json, os, glob
passed = failed = skipped = 0
if os.path.exists('allure-results'):
    for f in glob.glob('allure-results/*-result.json'):
        try:
            d = json.load(open(f))
            s = d.get('status','')
            if s == 'passed': passed += 1
            elif s in ('failed','broken'): failed += 1
            elif s == 'skipped': skipped += 1
        except: pass
total = passed + failed + skipped
rate = round(passed/total*100, 1) if total else 0
print(json.dumps({'passed':passed,'failed':failed,'skipped':skipped,'total':total,'rate':rate}))
"
                    """,
                    returnStdout: true
                ).trim()
                
                def stats = readJSON text: statsJson
                env.ALLURE_PASSED = String.valueOf(stats.passed)
                env.ALLURE_FAILED = String.valueOf(stats.failed)
                env.ALLURE_SKIPPED = String.valueOf(stats.skipped)
                env.ALLURE_TOTAL = String.valueOf(stats.total)
                env.ALLURE_PASS_RATE = String.valueOf(stats.rate) + '%'
                
                // 计算耗时
                def durationMs = currentBuild.duration
                def durationSec = (durationMs / 1000).intValue()
                def minutes = (durationSec / 60).intValue()
                def seconds = durationSec % 60
                env.ALLURE_DURATION = "${minutes}分${seconds}秒"
                
                echo "=== Test Statistics ==="
                echo "PASSED: ${env.ALLURE_PASSED}"
                echo "FAILED: ${env.ALLURE_FAILED}"
                echo "TOTAL: ${env.ALLURE_TOTAL}"
                echo "PASS_RATE: ${env.ALLURE_PASS_RATE}"
            }
            
            // 生成 Allure 报告
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
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
                            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>测试环境</b></td><td style="padding: 8px; border: 1px solid #ddd;">${params.base_url}</td></tr>
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
                            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>测试环境</b></td><td style="padding: 8px; border: 1px solid #ddd;">${params.base_url}</td></tr>
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
        
        cleanup {
            cleanWs()
        }
    }
}
