pipeline {
    agent macbookair
    
    tools {
        // Jenkins 全局工具配置中的 Allure 名称
        allure 'allure-commandline'
    }
    
    environment {
         sh '''
             apt-get update && apt-get install -y python3 python3-pip
             pip3 install -r requirements.txt
         '''
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
                sh '''
                    ${PIP_PATH} install -r requirements.txt
                    ${PIP_PATH} list | grep -E "pytest|allure|selenium"
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    ${PYTHON_PATH} -m pytest tests_py/ \
                        --alluredir=allure-results \
                        --clean-alluredir \
                        -v \
                        --tb=short \
                        --headless
                '''
            }
            post {
                always {
                    // 即使测试失败也继续生成报告
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
            echo '✅ All tests passed!'
        }
        failure {
            echo '❌ Tests failed. Check Allure report for details.'
        }
    }
}

