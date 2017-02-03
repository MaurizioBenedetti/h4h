#!/bin/bash

DEPLOYMENT_ZIP='all_lambda_functions.zip'

SOURCE_CODE_FOLDERS_ARRAY=('get-session' 'facebook-gateway' 'nlp-engine' 'twilio-gateway')
SOURCE_CODE_FOLDERS_STRING=${SOURCE_CODE_FOLDERS_ARRAY[*]// ' '}

DEPENDENCY_FOLDERS_ARRAY=('requests' 'pymessenger' 'requests_toolbelt' 'six.py')
DEPENDENCY_FOLDERS_STRING=${DEPENDENCY_FOLDERS_ARRAY[*]// ' '}

AWS_LAMBDA_FUNCTION_NAMES=('NLP-WFP-PostFunction-1TLQKXKB3H2QU' 'Facebook-Gateway' 'get_session' 'twilio-PostFunction-VFP52AMSPEPO')

# delete original folder
rm -f $DEPLOYMENT_ZIP

# create symlinks to virutal environment for pip dependencies
for DEP in "${DEPENDENCY_FOLDERS_ARRAY[@]}"
do
	ln -s ../venv/lib/python2.7/site-packages/$DEP $DEP
	echo 
done

# package source and dependencies together
zip -r $DEPLOYMENT_ZIP $DEPENDENCY_FOLDERS_STRING $SOURCE_CODE_FOLDERS_STRING

# update all lambda functions with the same zip file
for FUNC in "${AWS_LAMBDA_FUNCTION_NAMES[@]}"
do 
	aws lambda update-function-code --function-name $FUNC --zip-file fileb://$PWD/$DEPLOYMENT_ZIP
done
