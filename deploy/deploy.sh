#! /bin/bash

function initialize_worker() {
    printf "***************************************************\n\t\t Setting up host \n***************************************************\n"
    printf "***************************************************\n\t\t G'day mate ^^ \n***************************************************\n"
    # Update packages
    echo ======= AWS Upskill sfigiel ========
    echo ======= Updating packages ========
    sudo apt-get update

    # Export language locale settings
    echo ======= Exporting language locale settings =======
    export LC_ALL=C.UTF-8
    export LANG=C.UTF-8

    # Install pip3
    echo ======= Installing pip3 =======
    sudo apt-get install -y python3-pip
    echo ======= Installing pipenv =======
    sudo pip3 install pipenv

    # Install docker and docker-compose
    echo ======= Installing Docker =======
    sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
    sudo apt update
    sudo apt install docker-ce -y

    echo ======= Installing Docker-Compose =======
    sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo docker-compose --version
}

function clone_app_repository() {
    printf "***************************************************\n\t\tFetching App \n***************************************************\n"
    # Clone and access project directory

    cd ~/
    git clone https://simonfigiel@bitbucket.org/simonfigiel/flask-aws-s3.git
}

function setup_python_pipenv() {
    printf "***************************************************\n    Installing App dependencies and Env Variables \n***************************************************\n"
    cd ~/flask-s3-win/
    sudo pipenv shell
    echo ======= Installing required packages ========
    sudo pipenv install -r requirements.txt

}

# Create and Export required environment variable
function setup_env() {
    export FLASK_APP=app.py
    export FLASK_ENV=dev
}

function run_docker_containers() {
  printf "***************************************************\n    Running Docker \n***************************************************\n"
    cd ~/flask-s3-win/
    sudo docker-compose down
    pipenv run python utils.py
    sudo docker-compose up --build -d
}
function fireup() {
    sudo pipenv run python app.py
}

######################################################################
########################      RUNTIME       ##########################
######################################################################