from app.models import Lesson

from botocore.exceptions import ClientError


class Reminder:
    def __init__(self, template: str, lesson: Lesson):
        self._message = template.format(
            start=lesson.start_datetime.astimezone().strftime("%m/%d/%Y, %H:%M"),
            end=lesson.end_datetime.astimezone().strftime("%m/%d/%Y, %H:%M"),
            sfname=lesson.student.first_name,
            slname=lesson.student.last_name,
            description=lesson.description,
            place=lesson.place,
            subject=lesson.subject,
            address=lesson.student.address,
        )

        if lesson.place == Lesson.ONLINE:
            self._message += (
                f"\n\nLink do zajęć online: {lesson.teachingroom.get_absolute_url()}"
            )

    def get_content(self):
        return self._message


class SesMailSender:
    """Encapsulates functions to send emails with Amazon SES."""
    def __init__(self, ses_client):
        """
        :param ses_client: A Boto3 Amazon SES client.
        """
        self.ses_client = ses_client

    def send_email(self, source, destination, subject, text, html, reply_tos=None):
        """
        Sends an email.

        Note: If your account is in the Amazon SES  sandbox, the source and
        destination email accounts must both be verified.

        :param source: The source email account.
        :param destination: The destination email account.
        :param subject: The subject of the email.
        :param text: The plain text version of the body of the email.
        :param html: The HTML version of the body of the email.
        :param reply_tos: Email accounts that will receive a reply if the recipient
                          replies to the message.
        :return: The ID of the message, assigned by Amazon SES.
        """
        send_args = {
            'Source': source,
            'Destination': destination.to_service_format(),
            'Message': {
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': text}, 'Html': {'Data': html}}}}
        if reply_tos is not None:
            send_args['ReplyToAddresses'] = reply_tos
        try:
            response = self.ses_client.send_email(**send_args)
            message_id = response['MessageId']
        except ClientError:
            raise
        else:
            return message_id