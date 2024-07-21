import logging
import os
import signal
import smtplib
import ssl
import sys
import time
import traceback
from email.message import EmailMessage

import psycopg2

log_level = logging.INFO

logger = logging
logger.basicConfig(format='%(asctime)s %(levelname)s %(process)d --- [%(threadName)s] %(funcName)s: %(message)s',
                   level=log_level)


def terminate_process(signal_number, _):
    logger.info(f'(SIGTERM) {signal_number} terminating the process')
    sys.exit(0)


config = {
    'db_host': os.getenv('DB_HOST'),
    'db_user': os.getenv('DB_USER'),
    'db_name': os.getenv('DB_NAME'),
    'db_password': os.getenv('DB_PASSWORD'),
    'email': os.getenv("EMAIL"),
    'email_login': os.getenv("EMAIL_LOGIN"),
    'email_password': os.getenv("EMAIL_PASSWORD"),
    'email_host': os.getenv("EMAIL_HOST"),
    'ping_count': int(os.getenv("PING_COUNT")),
    'wait_time': int(os.getenv("WAIT_TIME"))
}


class Sms2Mail:

    def __init__(self, cls_config):
        self.config = cls_config
        self.conn = psycopg2.connect(
            host=self.config['db_host'],
            dbname=self.config['db_name'],
            user=self.config['db_user'],
            password=self.config['db_password'])
        self.cur = self.conn.cursor()

    # public methods

    # main method triggering all actions
    def main(self):
        for sms in self.__fetch_new_sms():
            sms_id = sms[0]
            self.__store_sms_in_db(sms_id=sms_id, email=self.config['email'])
            result = self.__send_sms_as_email(sms_text=sms[1], sms_sender=sms[2], sms_date=sms[3])
            self.__update_sms_record(sms_id=sms_id, result=result)
            self.conn.commit()
            # wait for 1 sec to avoid db lock (just in case)
            time.sleep(1)

    # private methods

    # fetch new sms from gamud db inbox table
    def __fetch_new_sms(self):
        query = """select "ID", "TextDecoded", "SenderNumber", "ReceivingDateTime" from inbox
                    where "ID" not in (
                    select sms_id from s2e.sms2email
                    )"""
        self.cur.execute(query)
        return self.cur.fetchall()

    # send sms as email
    def __send_sms_as_email(self, sms_text:str, sms_sender:str, sms_date:str):
        port = 465  # For SSL
        context = ssl.create_default_context()
        logger.info(f"Sending EMAIL to:{self.config['email']}")
        logger.info(f"Sending EMAIL text:{sms_text}")
        message = EmailMessage()
        message["Subject"] = f"SMS from: {sms_sender}"
        message["From"] = {self.config['email_login']}
        message["To"] = self.config['email']
        message.set_content(f"Received at: {sms_date}\nMessage: {sms_text}")

        # Send the message via our own SMTP server.
        with smtplib.SMTP_SSL(self.config['email_host'], port, context=context) as server:
            logger.info(server.login(self.config['email_login'], self.config['email_password']))
            logger.info(server.send_message(
                from_addr=self.config['email_login'],
                to_addrs=self.config['email'],
                msg=message))
        return "DONE"

    # store sms2email record in db before sending email
    def __store_sms_in_db(self, sms_id, email):
        query = """INSERT 
         INTO s2e.sms2email
         (sms_id, email, status, created_on)
            VALUES (%s, %s, %s, now()) RETURNING id;
         """
        self.cur.execute(query, (sms_id, email, 'PENDING'))
        return self.cur.fetchone()[0]

    # update sms2email record in db after sending email
    def __update_sms_record(self, sms_id, result):
        query = "UPDATE s2e.sms2email SET status = %s WHERE sms_id = %s;"
        self.cur.execute(query, (result, sms_id))


if __name__ == '__main__':

    logger.info(f'Starting with PID:{os.getpid()}')
    logger.info(f'Config:{config}')

    s2m = Sms2Mail(cls_config=config)

    # add signal handlers
    signal.signal(signal.SIGALRM, terminate_process)
    signal.signal(signal.SIGTERM, terminate_process)

    try:
        i = 0
        while True:
            s2m.main()
            time.sleep(config['wait_time'])
            i = i + 1
            if i > config['ping_count']:
                logger.info('Ping, All good')
                i = 0
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        tb = traceback.format_exc()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"{exc_type}:{e} — Line no: {exc_tb.tb_lineno}\n{tb}")
        time.sleep(1)
        sys.exit(100)
