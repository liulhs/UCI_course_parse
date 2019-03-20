import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "jasonliuofficial@gmail.com"
receiver_email = "shiyuq@uci.edu"
password = "112131415161lhs"
message = """\
Subject: Hi there
You are Now on the watchlist of the following class(es):
34210
34211
34212
34213
34214
This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)