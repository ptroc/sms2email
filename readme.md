# SMS to Email Forwarder

This application serves as a bridge between a GAMMU database containing SMS messages and an email recipient. It periodically checks the database for new SMS messages and forwards them to a predefined email address.
Sms2Email is simple yet it works for me. its not intended for mass sms handling, but probably will work for bigger setups if adjusted. 

## Features

- **Database Polling**: Regularly checks the `Gammu DB` database for new SMS messages.
- **Email Forwarding**: Automatically sends new SMS messages to a specified email address.
- **Secure**: Utilizes SSL for secure email transmission.
- **Configurable**: Settings such as database credentials, email credentials, and polling frequency can be easily configured through environment variables.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.12 or higher
- Access to a PostgreSQL database containing the SMS messages
- An email account with SMTP access for sending emails
- Gammu SMSD configured for PostgreSQL. For more information on setting up Gammu with a PostgreSQL backend, refer to the [Gammu PostgreSQL Setup Guide](https://docs.gammu.org/smsd/pgsql.html).
- SMTP is hardcoded to use port 465 for SSL. If you need to use a different port, you will need to modify the `__send_sms_as_email` method in `sms2mail.py`.
## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ptroc/sms2email.git
   cd sms2email
    ```
2. **Build the Docker image**: 
   ```bash
   docker build -t sms2mail .
   ```
3. **Configure the application**: Set the following environment variables according to your setup:

- `DB_HOST`: Hostname of the PostgreSQL database server
- `DB_USER`: Database user
- `DB_NAME`: Database name
- `DB_PASSWORD`: Database user password
- `EMAIL`: Recipient email address
- `EMAIL_LOGIN`: Email account username for SMTP
- `EMAIL_PASSWORD`: Email account password for SMTP
- `EMAIL_HOST`: SMTP server host
- `PING_COUNT`: Number of cycles after which a ping log is generated
- `WAIT_TIME`: Time in seconds to wait between polling cycles
 
or copy `example.env` as .env and edit it 

```bash 
cp example.env .env
```

4. Run the application:

   ```bash
    docker run --env-file .env sms2mail
    ```
5. Verify that the application is running by checking the logs: 
   ```bash
   docker logs sms2mail
   ```

## Usage
Once started, the application will:  
1. Connect to the specified PostgreSQL database.
2. Fetch new SMS messages that have not been forwarded yet.
3. Send each new SMS message as an email to the specified recipient.
4. Update the database to mark messages as forwarded.
5. Sleep for the specified wait time before repeating the process.