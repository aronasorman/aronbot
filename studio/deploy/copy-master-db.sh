#!/bin/bash

set -e

TARGET_INSTANCE_NAME=$1
MASTER_INSTANCE_NAME=master

LATEST_MASTER_BACKUP=`gcloud beta sql backups list --instance=$MASTER_INSTANCE_NAME --format='value(id)' | head -n 1`

# copy the latest backup of master over to the target instance
#this restore operation might take longer, so run it async, then wait on the next command
gcloud beta sql backups restore $LATEST_MASTER_BACKUP --restore-instance=$TARGET_INSTANCE_NAME --backup-instance=$MASTER_INSTANCE_NAME --quiet --async

# wait two times
OPERATION=$(gcloud beta sql operations list --instance $TARGET_INSTANCE_NAME | grep RUNNING | awk '{print $1}')
while [[ "$OPERATION" ]]; do
    gcloud beta sql operations wait $OPERATION || true
    OPERATION=$(gcloud beta sql operations list --instance $TARGET_INSTANCE_NAME | grep RUNNING | awk '{print $1}')
done

# reset the target instance's SSL config, so we can connect to it again.
gcloud beta sql ssl server-ca-certs create --instance $TARGET_INSTANCE_NAME
gcloud beta sql ssl server-ca-certs rotate --instance $TARGET_INSTANCE_NAME
