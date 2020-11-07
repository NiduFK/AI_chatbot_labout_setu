#AI chatbot for employee
import pymysql
import requests

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

# enable less secure aap @https://www.google.com/settings/security/lesssecureapps
def send_gmail():

    mail_content = '''From: From Person <laboursetuapk@gmail.com>
            To: To Person <laboursetuapk@gmail.com>
            Subject: AI Chatbot needs more answers/
            Could not provide appropriate answer
            This is a test e-mail message. '''

    # The mail addresses and password
    sender_address = 'laboursetuapk@gmail.com'
    sender_pass = 'labour123'
    receiver_address = 'laboursetuapk@gmail.com'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'
    try:
        # The subject line #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))

        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        print('connected to smtp.gmail.com')
        session.login(sender_address, sender_pass)  # login with mail_id and password
        print('login passed!')
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')

    except smtplib.SMTPException as e:
        print("Error: unable to send email",e)


def setdb():

    # Reading from already existing question and answers
    question_file = open("Questions.txt", "r")
    answer_file = open("Answers.txt", "r")
    answer = answer_file.read().split(',')
    question = question_file.read().split(',')

    # database connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="labour_setu_db")
    cursor = connection.cursor()

    # Storing the newly read question & answer lists to db
    # sql = "INSERT INTO chatbot_table (id, question, answer) VALUES (%s, %s, %s)"

    # cursor.execute(sql, val)
    # for i,(q,a) in enumerate(zip(question,answer)):
    #     val = ("00000"+str(i), q, a)
    #     cursor.execute(sql, val)
    #     connection.commit()
    # print('sucessfully inserted!')

    # connection.commit()

    cursor.execute('select question from chatbot_table')
    user_question = input('question: ').lower()
    cursor.execute('select answer from chatbot_table where question like "%' + user_question + '%";')

    # Use the bot answer if other logic (user_question_keywords) gives redundant and unnecessary response
    bot_answer = cursor.fetchall()

    user_question_keywords = user_question.split(' ')
    answer_list = []
    data_list = []
    match_found = 0

    for word in user_question_keywords:
        cursor.execute('select answer from chatbot_table where question like "%' + word + '%";')
        db_value = cursor.fetchall()
        if not db_value:
            pass
        else:
            match_found += 1
            data_list.append(db_value)

    if match_found > 3:
        answer_list.append(list(dict.fromkeys(data_list)))

    if not answer_list:
        print("answer from db: ",answer_list)

        request_body = {"name":"Nida","text":user_question}
        url = "https://nithapi.azurewebsites.net/sid/nquery"

        response = requests.post(url, json=request_body)
        response_answer =json.loads(response.text)
        response_reply = response_answer["reply"]
        if "500E" in response_reply:
            print('Error 500E')
            send_gmail()

        else:
            print('answer from POST= ',response_answer["reply"])
            return response_answer["reply"]

    else:
        print('Answer: ',answer_list)

    # some other statements  with the help of cursor
    connection.close()


if __name__ == '__main__':
    setdb()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# To-Do: Use OAuth2 to send emails follow: https://blog.mailtrap.io/send-emails-with-gmail-api/
# To-Do: enhance DB to search and find suitable answers for only question resembling the question's of the user
'''bot_anser logic: It works only for short key-strings eg. help, job or something which is short and continuously match
Right now the db does not return values if the substring is long, this needs to be resolved'''
