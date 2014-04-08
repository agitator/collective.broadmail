from zExceptions import Redirect
from yafowil.plone.form import YAMLForm
from collective.broadmail import _


class SubscriptionForm(YAMLForm):
    form_template = 'collective.broadmail:portlet/form.yaml'
    message_factory = _

    def subscribe(self, widget, data):
        print 'subscribe'

    def next(self, request):
        print 'next'
        raise Redirect(self.context.absolute_url())
