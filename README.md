# CSV to DB converter

Converter for reading CSV files containing product_code/quantity to SQL DB.

Python 2.7

## Install

### System requirements

MacOSX: `brew install mysql`

Ubuntu: `sudo apt-get install mysql`

Arch: `sudo pacman -S mysql`

### Python virtual environment

    pip2.7 install virtualenv
    virtualenv -p /usr/bin/python2.7 venv
    source venv/bin/activate
    pip install -r requirements.txt

### Configure

Copy `config.json.example` to `config.json` and set proper values.

## Run

    python main.py

## Tests

    python -m unittest discover tests

## Links

- [sqlite3 in tests](https://docs.python.org/2/library/sqlite3.html)
