#!/usr/bin/env bash

####################################################
# Setup AWS using command-line tool
####################################################
aws configure
# copy paste access key that was created on AWS website
# copy paste secret key
# will be stored in ~/.aws/credentials and will be available to AWS or EB command line tools

####################################################
# Initialize Elastic Beanstalk environment
####################################################
eb init
# Configure initialization settings
# select region (us-east-1)
# create new application
# enter application name (whatever you want)
# Yes, using Python
# 3) Python 2.7
# Yes, setup SSH
# Yes, create new keypair
# Yes, make keypair name (whatever you want)
# Yes, enter passphrase for keypair (whatever you want)

###########################################################
# Create Elastic Beanstalk environment and attach Database
###########################################################
# specify database engine, database instance type (t2.micro is free-tier)
eb create -db -db.engine postgres -db.i db.t2.micro 
# create environment name (whatever you want)
# create dns cname prefix (whatever you want, will show as yourname.elasticbeanstalk.com)
# create RDS DB username (whatever you want)
# create RDS DB password (whatever you want)
# wait for creation of security groups, load balancers, etc., to finish, may take some time

#############################################################
# Create IAM user to access AWS resources within application
#############################################################
# Create a group name -- you will attach policies granting privileges to it
# aws iam create-group --group-name YourGroupName
# Attach policies (access privileges) to group that was created
# aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess--group-name YourGroupName
# aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonRDSFullAccess --group-name YourGroupName
# aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --group-name YourGroupName
# aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AWSElasticBeanstalkFullAccess --group-name YourGroupName

# IAM user and password will be used later, remember these!
# Create an IAM user
# aws iam create-user --user-name YourUserName
# Give IAM user a password
# aws iam create-login-profile --user-name YourUserName --password YourPassword

# Add IAM user to group that was created
# aws iam add-user-to-group --group-name YourGroupName --user-name YourUserName

############################################################
# Deploy the application
############################################################
eb deploy

############################################################
# Terminate the application, environment
############################################################
# Only do this when you're ready to permanently delete the web application and database
# eb terminate
