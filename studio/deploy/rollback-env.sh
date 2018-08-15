#!/bin/bash
#
# Rollback an environment (i.e. master, or develop) into the previous successful deploy.

set -e

ENVIRONMENT=$1

# Get the latest deploy that is both superseded, and has an upgrade that's completed (i.e. none of the pods errored out during upgrade)
LATEST_SUCCESSFUL_UPGRADE=`helm history develop | egrep 'SUPERSEDED.*Upgrade\ complete' | tail -n 1`
# Get its number, since that's what we pass in to helm for rollback
LATEST_SUCCESSFUL_NUM=`echo $LATEST_SUCCESSFUL_UPGRADE | awk '{print $1}'`

echo "Last successful upgrade is:"
echo $LATEST_SUCCESSFUL_UPGRADE

# one last check from the caller whether this is the version wee want to roll back to.
echo "Do you wish to roll back to this version? $LATEST_SUCCESSFUL_NUM"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) helm rollback develop $LATEST_SUCCESSFUL_NUM; break;;
        No ) exit;;
    esac
done