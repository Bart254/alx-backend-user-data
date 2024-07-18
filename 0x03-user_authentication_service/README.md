# User Authentication Service

This is a guided project that shows how to develop session authentication for
web applications. In the industry, one should not implement their own
authentication system, instead, use frameworks or modules. For learning purposes,
tests in this project take us through the mechanism of authentication using flask
and python.


## Table of Contents

- [Requirements](#requirements)
- [Recommendations](#recommendations)
- [Installation](#installation)
- [Usage](#usage)
- [Resources](#resources)
- [Acknowledgements](#acknowledgements)


## Requirements

To use this project you'll need the following installed in your workspace:
- python3 interpreter
```sh
apt update
apt install python3
```

- flask
```sh
pip install flask
```

## Recommendations

To work with sqlite database and understand sqlite commands, if curious, install
sqlite client:
- sqlite3
```sh
apt update
apt install sqlite3
```

## Installation

1. Fork the repository

2. Clone the repository
```sh
git clone https://github.com/your_username/project.git
```

3. Navigate to project directory
```sh
cd project_dir
```

4. Install all dependencies in [requirements](#requirements)


## Usage

To use the app, you'll have to open two terminals.

### Terminal one
In terminal one, open the web application:
```sh
python3 -m app or
python3 app.py or
./app.py
```

### Terminal 2
Test uri using curl
```sh
curl -v localhost:5000/uri [optionals]
```

Alternatively, test the app using main.py file
```sh
python3 -m main or
python3 main.py or
./main.py 
```


## Resources

To gain a deeper understanding on flask module, requests module, http status codes
and how they have been used to create project files. Read or watch

- [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
- [Requests](https://requests.kennethreitz.org/en/latest/user/quickstart/)
- [HTTPS Status Codes](https://www.w3.orh/Protocols/frc2616/rfc2616-sec10.html)


## Acknowledgements

This project is a product of ALX, an organisation whose vision is to tap the
digital talent in Africa.
