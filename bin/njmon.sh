#! /bin/sh
host_name=`hostname -s`
date_strg=`date +%Y%m%d_%H%M%S`
file_name=${host_name}_${date_strg}
dir_name=${HOME}/njmon

cd ${dir_name}/log

${dir_name}/bin/njmon -f -s 60 -c 60


#find . -mmin +5 -type f -name "*.json" -exec ${dir_name}/bin/njmonchart {} ../html/{}.html \;

find . -mtime +365 -type f -delete

