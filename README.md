# le-query-all-logs
Script that runs a query against all logs in account and prints results in csv file. Can be used to query your Logentries account to find out the logs with the most usage.

You will need your account key and read only api key.

Default query is `where(/.*/) calculate(bytes)`

FROM_TS is in miliseconds and can be configurable. 

##### To Run

$ python query_all_logs.py ACCOUNT_KEY READ_ONLY_API_KEY results.csv

Results will be stored in a csv file in the same directory where the script is saved.

Default query is `where(/.*/) calculate(bytes)`
