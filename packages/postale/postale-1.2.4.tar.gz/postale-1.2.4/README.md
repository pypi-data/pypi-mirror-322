# Postale

Postale is a simple module that wraps `smtplib` and `email` libraries. It is configured in order to make it easy to create a new mail, and setup attachments, body, etc.

## Installation

```sh
pip install postale
```

## Usage

### Import it

You can either
```python
import postale
```
or
```python
from postale import Mail
```

As for now, `Mail` is the only class in this module.

### Create an e-mail

To create a mail, use de `Mail` constructor:

```python
my_mail = Mail(
    'smtp.host.com',
    port = 25,
    # other kwargs...
)
```

You can specify all the e-mail properties, right in the constructor too:

```python
my_mail = Mail(
    host = 'smtp.host.com',
    sender = 'email@example.com',
    subject = 'My First Mail',
    attachments = 'path/to/attachment.txt'
)
```

The following table shows the properties that class `Mail` has.

Property      | Type                   | Optional | Default
------------- | ---------------------- | -------- | -------
`host`        | `str`                  | No       | -
`port`        | `int`                  | Yes      | `587`
`sender`      | `str`                  | Yes      | `None`
`recipients`  | `str`, `list`, `tuple` | Yes      | `None`
`subject`     | `str`                  | Yes      | `None`
`body`        | `str`                  | Yes      | `None`
`attachments` | `str`, `dict`, `bytes` | Yes      | `None`

### Printing

It is possible to convert a `Mail` object to `str` or simply `print` it. For example, printing `my_mail` defined above:

```python
>>> print(my_mail)
        My First Mail
        From: email@example.com
        To:   

        (no body)

        attachment.txt
```

### Edit an e-mail

You can create an e-mail and later edit its properties, by assigning them:

```python
new_mail = Mail('smtp.host.com')
new_mail.recipients = ['friend@company.com', 'mom@server.com']
new_mail.subject = 'Things I like'
new_mail.body = "Chocolate, pizza and postales!"
```

### Sending

It is necessary to have the sender's password to be able to send the e-mail. In order to do it, use the `send` method, it will return `True` when done.

```python
new_mail.send('supersecurepass1234.')
```

> **Note:** Some SMTP providers (like gmail) need you to set an App Password, different from your e-mail password.
