import imaplib
import email
import re
import twitter

SENDER = "status@myvirtualserver.de"
COMPANY = "myVirtualserver"
SEPERATOR = "Thank you,"

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('mvs.status@gmail.com', 'XXXXXXXXXXXXXXXXXXX')
mail.list()
mail.select("inbox")

result, data = mail.search(None, '(UNSEEN FROM "' + SENDER + '")')

ids = data[0]
id_list = ids.split()
for emailid in id_list:
    result, data = mail.fetch(emailid, "(RFC822)")

    raw_email = data[0][1]
    raw_email = raw_email.decode("utf-8")

    def getTwitter(msg):
        email_message = email.message_from_string(raw_email)
        subject = email_message["Subject"]
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode("UTF-8")
        body = body.replace("\r\n", " ")
        body = body.replace("\r", " ")
        body = body.replace("\n", " ")
        body = body.replace("\t", " ")
        body = re.sub(" +", " ", body)
        body = body.replace(COMPANY + " ", "")
        longT = subject + " " + body
        return longT[:137].split(SEPERATOR, 1)[0] + "..."

    print("Tweete...")
    api = twitter.Api(consumer_key="consumer_key",
                      consumer_secret="consumer_secret",
                      access_token_key="access_token_key",
                      access_token_secret="access_token_secret")
    newStatus = getTwitter(raw_email)
    print(newStatus)
    status = api.PostUpdate(newStatus)
    print(str(status))
