### Hexlet tests and linter status:
[![Actions Status](https://github.com/KlyaksaOFF/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/KlyaksaOFF/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=KlyaksaOFF_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=KlyaksaOFF_python-project-83)
### Page Analyzer is a web application for analyzing web pages. Users can add URLs that will be checked for availability and extract important information: headers (h1), meta descriptions, and response status codes.
## 🚀 Features

    Add URLs for analysis

    Automatic page availability checking

    SEO data extraction:

        Page title

        First-level header (h1)

        Meta description

    Check history for each URL

    URL input validation

    Visual success/error notifications

## 🛠 Technologies

    Backend: Python 3.13, Flask

    Frontend: HTML, Jinja2, Bootstrap

    Database: PostgreSQL

    HTTP requests: requests, BeautifulSoup4

    Environment management: python-dotenv

📦 Commands
bash

### Clone the repository
git clone https://github.com/KlyaksaOFF/python-project-83.git \
cd python-project-83

### Install dependencies
make install

### Run linter
make lint

### Start the application
make start