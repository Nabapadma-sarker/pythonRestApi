node {
   def commit_id
   stage('Preparation') {
     checkout scm
     sh "git rev-parse --short HEAD > .git/commit-id"
     commit_id = readFile('.git/commit-id').trim()
   }
   stage('test with Mysql DB') {
     def mysql = docker.image('mysql').run("-e MYSQL_ALLOW_EMPTY_PASSWORD=yes -e MYSQL_DATABASE=pythonRestApi -e MYSQL_ROOT_PASSWORD=rootpass") 
     def myTestContainer = docker.image('python:3')
     myTestContainer.pull()
     myTestContainer.inside("--link ${mysql.id}:database") { // using linking, mysql will be available at host: mysql, port: 3306     
       sh 'pip install -r requirements.txt'
       sh 'python manage.py makemigrations'
       sh 'python manage.py migrate'
       sh 'DJANGO_SUPERUSER_PASSWORD=testpass python manage.py createsuperuser --username testuser --email admin@email.com --noinput'
       sh 'python manage.py runserver 0.0.0.0:8000'
       sh 'python -m pytest'     
     }    
   }                            
   stage('docker build/push') {            
     docker.withRegistry('https://index.docker.io/v1/', 'dockerhub') {
       def app = docker.build("nabapadma/django-project:${commit_id}", '.').push()
     }                                     
   }                                       
}        
