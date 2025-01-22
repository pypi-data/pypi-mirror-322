import base64
import io
import pandas as pd
from office365.outlook.mail.messages.message import Message
from office365.outlook.mail.folders.folder import MailFolder
from office365.outlook.mail.item_body import ItemBody


def open_mailbox(user, base_folder) -> MailFolder:
    """
Select a user's mailbox for accessing mail folders
    :param user: GraphClient.user
    :param base_folder: the parent folder eg: Inbox
    :return: MailFolder
    """
    inbox = user.mail_folders.filter(f"displayName eq '{base_folder}'").get().execute_query()
    return inbox


def open_folder(folder: MailFolder, subfolder: list) -> MailFolder:
    """
Select a subfolder for reading or writing to
    :param folder: The parent folder
    :param subfolder: the route of the subfolder eg: Royalties\\Archive
    :return: MailFolder
    """
    for f in subfolder:
        # print('mso_outlook_mail.open_folder', str(f))
        folder = folder[0].child_folders.filter(f"displayName eq '{f}'").get().execute_query()
    return folder[0]


def _fetch_mail(folder, message_max):
    return folder.messages.top(message_max).get().order_by('createdDateTime asc').execute_query()


def get_mail(context, email_user, folder, message_max=1000):
    """
Return mail messages from a specific folder
    :param context: MSO connection context
    :param email_user: email user account 
    :param folder: source folder eg: Inbox\Royalties\Archive would be "Royalties|Archive"
    :param message_max: max no of messages to return
   """
    folders = folder.split('|')
    user = context.users[email_user]
    mailbox = open_mailbox(user, folders.pop(0))
    subfolder = open_folder(mailbox, folders)
    messages = _fetch_mail(subfolder, message_max)
    return messages


def move_mail(context, email_user, message: Message, folder):
    """
Move a mail message from one folder to another
    :param context: MSO connection context
    :param email_user: email user account 
    :param message: mail message
    :param folder: source folder eg: Inbox\Royalties\Archive would be "Royalties|Archive"
    """
    folders = folder.split('|')
    user = context.users[email_user]
    mailbox = open_mailbox(user, folders.pop(0))
    subfolder = open_folder(mailbox, folders)
    message.move(subfolder.id).execute_query()


def parse_message(message: Message):
    """
Find attachment to an email message and convert them to a Pandas DataFrame
    :param message: office365.outlook.mail.messages.message.Message
    :return: dict - {file_name: pd.DataFrame}
    """
    if message.properties['hasAttachments']:
        file_count = 0
        attachment_dict = {}
        for att in message.attachments.get().execute_query():
            if file_count > 99:
                print("I think we've seen enough of those!")
                return attachment_dict
            if not att.properties['isInline']:
                file_name = message.properties['subject'] + '_' + str(file_count).zfill(2)
                file_type = att.properties['name'].split('.')[1]
                if file_type in ['xls', 'xlsx']:
                    file_count += 1
                    xld = pd.read_excel(io.BytesIO(base64.b64decode(att.properties['contentBytes'])), engine='openpyxl')
                    attachment_dict[file_name] = {'FileType': file_type, 'Data': xld}
                elif file_type == 'csv':
                    file_count += 1
                    df_csv = pd.read_csv(io.BytesIO(base64.b64decode(att.properties['contentBytes'])), sep='\t')
                    attachment_dict[file_name] = {'FileType': file_type, 'Data': df_csv}
                elif file_type == 'pdf':
                    file_count += 1
                    # content = io.BytesIO(base64.b64decode(att.properties['contentBytes']))
                    attachment_dict[file_name] = {'FileType': file_type, 'Data': att.properties,
                                                  'name': '.'.join([file_name, file_type])}

        return attachment_dict


def send_email(client, sender: str, recipient: str, subject: str, body_content: str):
    """
    Send an email using Microsoft Graph API with a specified sender.
    Example usage:
    send_email(client, "sender@example.com", "recipient@example.com", "Test Subject", "<p>This is a test email.</p>")
    :param client: Authenticated GraphClient object.
    :param sender: Sender email address.
    :param recipient: Recipient email address.
    :param subject: Subject of the email.
    :param body_content: Body content of the email.
    """
    try:
        # Create the email message
        email = Message(client)
        email.subject = subject
        email.body = {
            "contentType": "HTML",  # Use "Text" for plain text
            "content": body_content
        }
        email.set_property('toRecipients', [{"emailAddress": {"address": recipient}}]) # = [{"emailAddress": {"address": recipient}}]

        # Send the email through the specified sender
        client.users[sender].send_mail(
            subject=email.subject,
            body=ItemBody(body_content, 'html'),
            to_recipients=[recipient],
            save_to_sent_items=True
        ).execute_query()

        print(f"Email sent successfully from {sender} to {recipient}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

