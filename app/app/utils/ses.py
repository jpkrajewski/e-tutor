from botocore.exceptions import ClientError

from app.constants.templates import (
    LESSON_REMIDER_TO_STUDENT_EMAIL_HTML,
    LESSON_REMIDER_TO_STUDENT_EMAIL_TEXT,
    LESSON_REMIDER_TO_TUTOR_EMAIL_HTML,
    LESSON_REMIDER_TO_TUTOR_EMAIL_TEXT,
)
from app.models import Lesson


class TemplatePopulator:
    def __init__(self, lesson: Lesson):
        self._data = dict(
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
            self._data["link"] = lesson.teachingroom.get_absolute_url()

    def get_email_to_tutor(self):
        return LESSON_REMIDER_TO_TUTOR_EMAIL_HTML.format(
            **self._data
        ), LESSON_REMIDER_TO_TUTOR_EMAIL_TEXT.format(**self._data)

    def get_email_to_student(self):
        return LESSON_REMIDER_TO_STUDENT_EMAIL_HTML.format(
            **self._data
        ), LESSON_REMIDER_TO_STUDENT_EMAIL_TEXT.format(**self._data)

    def get_sms_to_tutor(self):
        raise NotImplementedError

    def get_sms_to_student(self):
        raise NotImplementedError


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
            "Source": source,
            "Destination": destination.to_service_format(),
            "Message": {
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": text}, "Html": {"Data": html}},
            },
        }
        try:
            response = self.ses_client.send_email(**send_args)
            message_id = response["MessageId"]
        except ClientError:
            raise
        else:
            return message_id
