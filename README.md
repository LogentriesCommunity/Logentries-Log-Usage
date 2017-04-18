# Logentries-Log-Usage
Script that generates a CSV file that shows the Account usage for a given account from a given point in time (DD.MM.YYYY) in humanized form that can help you establish which of your logs is sending the most data to your account.

To use the script you must supply your [Account Key](https://docs.logentries.com/docs/accountkey) and a [Read-Write or Read-Only](https://docs.logentries.com/docs/api-keys) key. API key is also retrieved from `$LOGENTRIES_API_KEY`.

##### To Run

- Install requirements
- run `$ python query_all_logs.py [params]`

example:

`$ LOGENTRIES_API_KEY=aaa-bbb-ccc-ddd python query_all_logs.py --account-key aaa-bbb-ccc-ddd --from-date 15.01.2017 --to-date 15.03.2017 --host-name "Webserver Logs"`

Results will be stored in a csv file (default: `results.csv`) in the same directory where the script is saved.
