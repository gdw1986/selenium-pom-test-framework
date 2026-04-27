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
        }
    }
    
    post {
        always {
            script {
                // 提取测试统计 - 无论成功失败都执行
                sh '''
                    python3 -c "
import json
import os
import glob

results_dir = 'allure-results'
passed = 0
failed = 0
skipped = 0

if os.path.exists(results_dir):
    result_files = glob.glob(os.path.join(results_dir, '*-result.json'))
    for f in result_files:
        try:
            with open(f, 'r') as file:
                data = json.load(file)
                status = data.get('status', 'unknown')
                if status == 'passed':
                    passed += 1
                elif status in ['failed', 'broken']:
                    failed += 1
                elif status == 'skipped':
                    skipped += 1
        except Exception as e:
            print('Error reading ' + f + ': ' + str(e))

total = passed + failed + skipped
pass_rate = (passed / total * 100) if total > 0 else 0

# 写入属性文件
with open('test_stats.properties', 'w') as f:
    f.write('PASSED=' + str(passed) + chr(10))
    f.write('FAILED=' + str(failed) + chr(10))
    f.write('SKIPPED=' + str(skipped) + chr(10))
    f.write('TOTAL=' + str(total) + chr(10))
    f.write('PASS_RATE=' + str(round(pass_rate, 1)) + chr(10))

print('=== Test Statistics ===')
print('PASSED: ' + str(passed))
print('FAILED: ' + str(failed))
print('SKIPPED: ' + str(skipped))
print('TOTAL: ' + str(total))
print('PASS_RATE: ' + str(round(pass_rate, 1)) + '%')
"
                '''
                
                // 读取统计结果
                if (fileExists('test_stats.properties')) {
                    def props = readProperties file: 'test_stats.properties'
                    env.ALLURE_PASSED = props['PASSED'] ?: '0'
                    env.ALLURE_FAILED = props['FAILED'] ?: '0'
                    env.ALLURE_SKIPPED = props['SKIPPED'] ?: '0'
                    env.ALLURE_TOTAL = props['TOTAL'] ?: '0'
                    env.ALLURE_PASS_RATE = (props['PASS_RATE'] ?: '0') + '%'
                } else {
                    env.ALLURE_PASSED = '0'
                    env.ALLURE_FAILED = '0'
                    env.ALLURE_SKIPPED = '0'
                    env.ALLURE_TOTAL = '0'
                    env.ALLURE_PASS_RATE = '0%'
                }
                
                // 计算耗时
                def durationMs = currentBuild.duration
                def durationSec = (durationMs / 1000).intValue()
                def minutes = (durationSec / 60).intValue()
                def seconds = durationSec % 60
                env.ALLURE_DURATION = "${minutes}分${seconds}秒"
                
                echo "=== Final Statistics ==="
                echo "PASSED: ${env.ALLURE_PASSED}"
                echo "FAILED: ${env.ALLURE_FAILED}"
                echo "TOTAL: ${env.ALLURE_TOTAL}"
                echo "PASS_RATE: ${env.ALLURE_PASS_RATE}"
                echo "DURATION: ${env.ALLURE_DURATION}"
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
        
        cleanup {
            cleanWs()
        }
    }
}
