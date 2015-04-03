Facebook continuous news feed monitor which raises email alerts.

Uses Gmail SMTP over SSL to send mail (configured in gmail_smtp.ssl), and a Facebook Graph API access token with read_stream permissions. To set up, create a file credentials.ini in the main directory with:

[mail]
    username = sending_gmail_address
    password = sending_gmail_password
    send_to = recipient_email_address

[facebook]
    access_token = graph_api_access_token
