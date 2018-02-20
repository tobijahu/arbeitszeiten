# arbeitszeiten
A little tool set to calculate and track labor time.

Unit tests can be executed by executing
```
python -m unittest discover
```


This script may be used to...
Or to process a file with a record of start and end times as well as breaks.
In a linux environment this may be called using
```
cat example-arbeitszeiten.csv | awk '{ $1=""; print}' | sed -e 's/,//g' \
| sed -e 's/\"Gleitzeit\"//g;s/\"Feiertag\"//g;s/\"Urlaub\"//g;s/\"Krank\"//g' \
| python arbeitcli.py
```
