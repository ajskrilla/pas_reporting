#! /usr/bin/env python3
import argparse
import os
import csv
import errno
from auth_main.funct_tools import *
from auth_main.logger import logging as log
from auth_main.logger import f_check
from auth_main.utility import Cache

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Save a query as a csv. Please give valid SQL query to tenant.")
	parser.add_argument('-p','--Path', type=str, required=True, help= 'Path to the csv file. Point to csv in arg path and use forward slashes in the path if using windows.')
	parser.add_argument('-q','--Query', type=str, required=True, help= 'Query against the tenant (i.e "Select * From Server").')
	parser.add_argument('-pw','--Password', type=str, required=False, help= 'Password of service account from config file.')
	args = parser.parse_args()

# Create the object for the file
f = f_check()

# Build cache
c = Cache(args.Password, **f.loaded['tenants'][0])

# Security test
sec_test(**c.ten_info)

# Write CSV file
def write_to_csv(wanted):
	if ".csv" in args.Path:
		path = os.path.abspath(args.Path)
		if not os.path.exists(os.path.dirname(path)):
			try:
				os.makedirs(os.path.dirname(path))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		with open(path, 'w') as f:
			writer= csv.DictWriter(f, fieldnames=wanted[0].keys(), delimiter=',')
			writer.writeheader()
			writer.writerows(wanted)
		log.info("Query Saved to {0}".format(path))
	else:
		log.error("Need to have file end in .csv")

# Query Function
def Query(sql, tenant, header,**ignored):
	log.info("SQL Query is: {0}".format(args.Query))
	try:
		query = query_request(sql, tenant, header).parsed_json
		wanted = [dict(x["Row"]) for x in query["Result"]["Results"]]
		write_to_csv(wanted)
	except Exception as e:
		log.error("Error occurred on reports.py, error being {0}".format(e))

Query(args.Query, **c.ten_info)