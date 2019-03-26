Scripts dependency:
- python3
- bash (for main.sh & test.sh only, not really mandatory)

To run the log monitoring, type:
```
./main.sh
``` 
You have access to more options. Please see the script help:
```
./main.sh -h
```

To run the tests, type:
```
./test.sh
```

To make your review clear, I strived to make a clear code, with explicit variables and functions names, and by adding many comments.

# ADDITIONNAL FUNCTIONALITIES

In addition to what has been requested, the script has the following functionnalities:
* Print replied HTTP status code
* Print average response size
* Print average number of request by authentified users
* Print a warning if one badly formatted line is written in log file
* Continue to run even in case of error in script
* release resource on log file when monitoring ends

# POSSIBLE IMPROVEMENTS

* Have a monitoring web UI. This would be possible, by sending the LogPackets objects instead of printing them.
* Add the possibility to monitor log history, instead of ignoring past log lines at start-up
* Add the possibility to set some filters, on some sections or users for example

