# Logentries-Log-Usage
Script that generates a CSV file that shows the Account usage for a given account from a given point in time (DD.MM.YYYY) in humanized form that can help you establish which of your logs is sending the most data to your account.

To use the script you must supply your [Account Key](https://docs.logentries.com/docs/accountkey) and a [Read-Write or Read-Only](https://docs.logentries.com/docs/api-keys) key. 

##### To Run

$ python query_all_logs.py ACCOUNT_KEY READ_ONLY_API_KEY results.csv DD.MM.YYYY

Results will be stored in a csv file in the same directory where the script is saved.
