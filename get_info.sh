#! /bin/bash

ssh -i ~/.ssh/phonelab.pem ec2-user@phone-lab.org /home/ec2-user/query.sh $1
echo $1
scp -i ~/.ssh/phonelab.pem ec2-user@phone-lab.org:/home/ec2-user/out.txt /home/manoj/phone/server/users/Lookup_File/
