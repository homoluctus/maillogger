# maillogger

![PyPI](https://img.shields.io/pypi/v/maillogger)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/maillogger)
![PyPI - License](https://img.shields.io/pypi/l/maillogger)

Analysis tool for Postfix log in /var/log/maillog

<!-- TOC depthFrom:2 -->

- [Feature](#feature)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
  - [Output a CSV file](#output-a-csv-file)
  - [Output a JSON file](#output-a-json-file)
  - [Output a TSV file](#output-a-tsv-file)
  - [Output a compressed CSV file](#output-a-compressed-csv-file)
- [Use Case](#use-case)
  - [Analysis using MySQL](#analysis-using-mysql)

<!-- /TOC -->

## Feature

- Load maillog file
  - Identify text or gzip automatically
- Parse maillog
  - Use regex
  - Convert to Python dictionary
- Output the parsed maillog to files
  - Supported data format is CSV, TSV and JSON
  - Compression (gzip) is possible

## Installation

```bash
pip install maillogger
```

## Usage

```
usage: maillogger [-h] [-f {csv,tsv,json}] [-c] [-V] source_file target_file

Analysis tool for Postfix log in /var/log/maillog

positional arguments:
  source_file           Specify Postfix maillog file
  target_file           Specify the filename to write parsed maillog. The file
                        extension is automatically added to the end of
                        filename.

optional arguments:
  -h, --help            show this help message and exit
  -f {csv,tsv,json}, --format {csv,tsv,json}
                        File data format to write the parsed maillog (Default:
                        csv)
  -c, --compress        Compress the output file with gzip
  -V, --version         Show maillogger command version
```

## Examples

### Output a CSV file

```bash
maillogger /var/log/maillog result
```

or

```bash
maillogger /var/log/maillog result -f csv
```

Then, `result.csv` is generated in current working directory.

### Output a JSON file

```bash
maillogger /var/log/maillog result -f json
```

### Output a TSV file

```bash
maillogger /var/log/maillog result -f tsv
```

### Output a compressed CSV file

```bash
maillogger /var/log/maillog result -f csv -c
```

Then, `result.csv.gz` is generated in current working directory.

## Use Case

### Analysis using MySQL

1. Convert maillog text to CSV file

```bash
maillogger /var/log/maillog /path/to/any -f csv
```

2. Create Table

```sql
CREATE TABLE maillog
(
    mail_id VARCHAR(15) NOT NULL,
    to_address VARCHAR(50) NOT NULL,
    relay text,
    delay VARCHAR(10),
    delays VARCHAR(20),
    dsn VARCHAR(10),
    status VARCHAR(10),
    description text,
    datetime DATETIME NOT NULL,
    PRIMARY KEY (mail_id, datetime),
    INDEX i_status(status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

3. Load CSV file

```sql
LOAD DATA INFILE '/path/to/any.csv'
IGNORE INTO TABLE maillog
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;
```
