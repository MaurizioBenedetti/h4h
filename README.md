# WFP Chatbot Infrastructure
## Deployment Guide
This repository contains deployment infrastructure and application code for a Chatbot that allows for the creation of rules-based surveys to be administered via a chat application, such as Facebook Messanger.  This document describes how to deploy this application.
### Prerequisites
To get started, you will need the following:
- an [AWS](https://aws.amazon.com/) account, with credentials to manage Elastic Beanstalk, RDS, Lambda, and API Gateway services
- an account on IBM's [Bluemix](https://www.ibm.com/cloud-computing/bluemix/)
- a Facebook Developer account, and a Facebook Page for your app
- this git repo
- a python virtual environment we like [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) for managing this)
- the [awscli](https://aws.amazon.com/cli/) and [awsebcli](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html) installed on your development machine

### Deploying the Backend
The backend API is responsible for serving survey questions, storing responses, and routing from one question to the next.  The business logic lives here.  The API is a Python application, leverages the [Django](https://www.djangoproject.com/) application framework, and is meant to be deployed on Amazon's [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) service.  To deploy the base application:
#### 1. clone this repo to your local development machine
```
$ cd /path/to/your/dev/directory/
$ git clone https://github.com/hostdp6/h4h
```
#### 2. create a virtual environment and install the requirements file
We've packaged up all the python dependencies in the requirements.txt file.  If you make changes to the code and add new dependencies, be sure to update the requirements file.
```
$ mkvirtualenv h4h
$(h4h) pip install -r requirements.txt
```
#### 3. build an initial set of Django migrations to test that everything works locally
This step will create a local sqlite database that contains all the tables you need to run the application locally.  Whenever you actually deploy the application, these commands will be run automatically.
```
$(h4h) python manage.py make migrations
$(h4h) python manage.py migrate
```
#### 4. start the dev server and make sure everything works
We can run the dev server on port 8000 with a simple command.  If all goes smoothly, you should see something like this:
```
$(h4h) python manage.py runserver
System check identified 0 issues (0 silenced).
...
April 04, 2017 - 15:45:29
Django version 1.9.1, using settings 'h4h.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```
If the application does not start, check the error message in your terminal; you are likely missing a dependency.  Once started, you should see a listing of all the available api endpoints when you navigate to the [root page](http://localhost:8000/api/).  At this point, you are ready to deploy to Elastic Beanstalk
#### 5. create the beanstalk environment
Before getting started, you might want to familiarize yourself with [this](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html) tutorial, which explains how to deploy a Django application on Elastic Beanstalk.  We're already done most of this stuff for you, so you can basically skip to [deploying the site](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html#python-django-deploy).  To do so, you'll want to initialize a new environment using the commands:
```
$(h4h) eb init -p python2.7 h4h
...
$(h4h) eb create h4h-env
...
$(h4h) eb open
```
This will guide you through a set of prompts to setup your environment (the defaults will do for now).  By the end of this, you should the django application running in your browser.
#### 6. create the database
We need to create an Amazon RDS instance to store data for our application.  Follow [this tutorial](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html#python-rds-create) to create a MySQL database and attach it to your Elastic Beanstalk environment.  Make sure you do this from the Elastic Beanstalk console to let AWS take care of the setup for you.  Once done, you'll want to re-deploy the application again with the following command:
```
$(h4h) eb deploy
```
At this point, the backend is setup and ready to go.  You can modify the code as you see fit and re-deploy as above.  For production, we recomend that you have at least two instances behind the load balancer to ensure stable service.

### Deploying the Orchestrator
The Orchestrator is responsible for routing messages between the chat clients, the backend APIs, and the NLP engine.  It is a single AWS Lambda function written in Python, and is attached to API Gateway for communication with other components.
#### 1. Deploying the lambda function
TODO: write this section
#### 2. Configuring the API Gateway
TODO: write this section

### Deploying the NLP Engine
The NLP engine takes raw survey responses from end users and translates them to machine-readable metrics.  It is a single AWS Lambda function written in Python, leverages the IBM Watson NLP APIs, and is attached to the API Gateway for communication with other components.
### 1. Setting up the Watson Integration
TODO: write this section
### 2. Deploying the lambda function
TODO: write this section
### 3. Configuring the API Gateway
TODO: write this section

### Deploying the Facebook Messenger Bot
As an example, this repository includes a chatbot adapter for Facebook Messenger, which can be used as a template for other chat clients.  It is a single AWS Lambda function written in Python, and is attached to the API Gateway for communication with the outside world and other components
TODO: complete this section

### Connecting the Components
TODO: write this section

### Writing a Test Survey
TODO: write this section
