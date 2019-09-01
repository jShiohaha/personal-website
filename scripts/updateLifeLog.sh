#!/bin/sh

curr_date=$(date +'%m-%d-%Y')
updated_filename="lifeLog-${curr_date}.html"

echo "Changing the name of old life log file to $updated_filename"
mv ../pages/lifeLog.html ../pages/$updated_filename

echo "Moving the old life log file to old_copies directory"
mv ../pages/$updated_filename ../pages/old_copies/

echo "Copying the life log template to pages directory"
cp ../pages/template/lifeLogBlank.html ../pages/

echo "Changing the name of the life log template to lifeLog.html"
mv ../pages/lifeLogBlank.html ../pages/lifeLog.html

echo "Calling Python script to update contents of life log"
python updateLifeLog.py
