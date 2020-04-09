#! /bin/sh
host_name=`hostname -s`
date_strg=`date +%Y%m%d_%H%M%S`
file_name=${host_name}_${date_strg}
dir_name=${HOME}/njmon

cd ${dir_name}/log

ssh usa-art01.lab.wagerworks.com \
	find /home/wworks/njmon/log -cmin +60 -cmin -120 -name "\*.json" | \
	while read line; do scp usa-art01.lab.wagerworks.com:$line .; done


