# chrome2pass

Import Chrome passwords to pass (the standard unix password manager) via an exported CSV file.

Also works for Chrome based browsers (Chromium, Brave).

# Requirements

[pass](https://www.passwordstore.org/)

Python3

# How to use

Export the passwords from your browser to CSV, copy the CSV into this directory, and run

Run 

```python chrome2pass.py  *.csv```

Optionally pass --confirm to ask for confirmation before adding each username/password.

```python chrome2pass.py --confirm *.csv```


