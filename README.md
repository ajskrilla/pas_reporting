# pas_reporting
Reporting tool that will be able to query against the tenant and save a CSV file to path. Can handle both OAUTH and DMC auth. Please install the dependent libraries (requests, cachetools, test.centrify.dmc (OPTIONAL)) via pip.
After that, please alter the config file in auth_main/conf/config.json and input the correct info. Tested on CentOS 8 & Python 3.9. Example of use: ./report.py -p "/var/test/test.csv" -q "Select * FROM Server" -pw "TH3B3stPW!".
