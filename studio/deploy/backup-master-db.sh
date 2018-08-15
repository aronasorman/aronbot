#!/bin/bash

set -e

gcloud beta sql backups create --instance=master
