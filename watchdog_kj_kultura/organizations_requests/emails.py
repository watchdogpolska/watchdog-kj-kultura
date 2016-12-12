from djmail import template_mail


class RequestOrganizationEmail(template_mail.TemplateMail):
    name = "request_organization"


class RequestUserEmail(template_mail.TemplateMail):
    name = "request_user"


class RequestNotificationEmail(template_mail.TemplateMail):
    name = "request_notification"
