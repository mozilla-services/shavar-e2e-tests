pipeline {
  agent {
      dockerfile {
        filename 'Dockerfile' 
        args '-u root:root' 
        additionalBuildArgs '--no-cache'
      }
  }
  libraries {
    lib('fxtest@1.9')
  }
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }
  environment {
    TEST_ENV = "${TEST_ENV ?: JOB_NAME.split('\\.')[1]}"
    SHAVAR_EMAIL_RECIPIENT = credentials('SHAVAR_EMAIL_RECIPIENT')
    //GITHUB_ACCESS_TOKEN = credentials('GITHUB_ACCESS_TOKEN')
    GITHUB_ACCESS_TOKEN = credentials('GITHUB_ACCESS_TOKEN_RPAPA')
  }
  stages {
    stage('Test list-edit') {
      steps {
	script {
	  sh "MOZ_HEADLESS=1 pytest --driver='Firefox' --channel='nightly' tests/test_list_edit.py -s"
        }
      } 
    } 
    stage('Test shield-display') {
      steps {
	script {
	  sh "MOZ_HEADLESS=1 pytest --driver='Firefox' --channel='nightly' tests/test_shield_display.py -s"
        }
      } 
    }
    stage('Test tracking-protection') {
      steps {
	script {
	  sh "MOZ_HEADLESS=1 pytest --driver='Firefox' --channel='nightly' tests/test_tracking_protection.py -s"
        }
      } 
    }
    stage('Test filesize') {
      steps {
	script {
	  sh "MOZ_HEADLESS=1 pytest --driver='Firefox' --channel='nightly' tests/test_filesize.py -s"
        }
      } 
    }
    stage('Test itisatrap') {
      steps {
	script {
	  sh "MOZ_HEADLESS=1 pytest --driver='Firefox' --channel='nightly' tests/test_itisatrap_page.py -s"
        }
      } 
    }
  }
  post {
    success {
      emailext(
        body: 'Test summary: $BUILD_URL\n\n',
        replyTo: '$DEFAULT_REPLYTO',
        subject: "shavar ${env.TEST_ENV} succeeded!!",
        to: '$SHAVAR_EMAIL_RECIPIENT')
    }
    failure {
      emailext(
        body: 'Test summary: $BUILD_URL\n\n',
        replyTo: '$DEFAULT_REPLYTO',
        subject: "shavar ${env.TEST_ENV} failed!",
        to: '$SHAVAR_EMAIL_RECIPIENT')
    }
    changed {
      ircNotification('#fx-test-alerts')
    }
  }
}
