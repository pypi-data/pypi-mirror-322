# Pydgeon v0.1.3
A simple Python library to simplify sending emails using `smtplib`.

---

# DISCLAIMER!
**ALWAYS USE ENVIRONMENT VARIABLES OR OTHER METHODS OF SAFELY STORING PASSKEYS AND EMAILS.**  
**NEVER HARD-CODE PASSWORDS INTO YOUR CODE. ALWAYS USE ENVIRONMENT VARIABLES TO STORE GMAIL-SPECIFIC PASSKEYS.**

---

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Planned-features](#planned-features)

---

## Installation
Install Pydgeon using pip:
```bash
pip install pydgeon
```

---

## Usage
Here are examples of how to use Pydgeon:  

### Set up the Sender Email and Passkey
**Always use environment variables to store sensitive data like passkeys and emails.**  
```python
import pydgeon

# Set up the sender email and passkey
pydgeon.dovecot("testSender@gmail.com", "<PASSKEY-HERE>")
```

### Send a Basic Email!
Send a simple email with a subject and message:  
```python
# Send a basic email
pydgeon.coo("Test Subject", "Coo!", "testReceiver@gmail.com")
```

### Send an Email with an Attachment!
Include a file attachment with your email:  
```python
# Send an email with an attachment
pydgeon.hoot("Test Subject", "Hoot!", r"C:\Example\Path\To\File.txt", "testReceiver@gmail.com")
```

### Send multiple emails at the same time!
Send to multiple recievers at a time:  
```python
# Define list of recievers
receivers = ["testReceiver1@gmail.com", "testReceiver2@gmail.com", "testReceiver3@gmail.com"]

# Send multiple emails to multiple receivers
pydgeon.coo("Test Subject", "Coo!", receivers)
pydgeon.hoot("Test Subject", "Hoot!", r"C:\Example\Path\To\File.txt", receivers)
```


---

## Features
- **Simplified email sending!**: Use simple methods to send emails quickly.
- **Send to multiple emails at one time!**: Use a ist to send multiple emails at the same time
- **Attachment support!**: Send emails with file attachments.

---

## Planned-features
- **Schedule email sending!**: Enter time to send emails!