#!/bin/bash
export PGPASSWORD='*****'
rm -r /home/sftp-dev/linelist/*
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region X (Northern Mindanao)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Northern_Mindanao_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region IX (Zamboanga Peninsula)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Zamboanga_Peninsula_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region IV-B (Mimaropa)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Mimaropa_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region III (Central Luzon)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Central_Luzon_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region V (Bicol)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Bicol_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region VI (Western Visayas)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Western_Visayas_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region VIII (Eastern Visayas)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Eastern_Visayas_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region XI (Davao Region)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Davao_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region XII (Soccsksargen)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Soccsksargen_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region XIII (Caraga)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Caraga_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region VII (Central Visayas)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Central_Visayas_`date +%d-%m-%y`.csv.gz
psql -U pro01 -d pmnpis_dev_v240 -c "Copy (select * from _pmnp_linelist where region='Region IV-A (Calabarzon)') To STDOUT With CSV HEADER DELIMITER ',';" | gzip > /home/sftp-dev/linelist/Calabarzon_`date +%d-%m-%y`.csv.gz
unset PGPASSWORD