import urllib
import urllib2
from yafowil.plone.form import YAMLForm
from collective.broadmail import _

AUTHCODE = 000000
OPTINID = 000000
OPTINSOURCE = 'WEBSITE'


def perform_request(url, params=None):
    if params:
        query = urllib.urlencode(params)
        url = '%s?%s' % (url, query)
    stream = urllib2.urlopen(url)
    res = stream.read()
    stream.close()
    return res


class SubscriptionForm(YAMLForm):
    form_template = 'collective.broadmail:portlet/form.yaml'
    message_factory = _

    @property
    def salutation_vocab(self):
        return [
            ('', ''),
            ('mrs', _(u'Mrs.')),
            ('mr', _(u'Mr.')),
        ]

    def subscribe(self, widget, data):
        def fetch(name):
            return data.fetch('subscription_form.%s' % name).extracted
        url = 'https://api.broadmail.de/http/form/%s/subscribe' % (AUTHCODE)
        params = {
            'bmRecipientId': fetch('email'),
            'salutation': fetch('salutation'),
            'firstname': fetch('firstname'),
            'lastname': fetch('lastname'),
        }
        self.res = perform_request(url, params)

    def next(self, request):
        if self.res == 'ok':
            resource = '/@@subscription_ok'
        elif self.res == 'duplicate':
            resource = '/@@subscription_duplicate'
        else:
            resource = '/@@subscription_failed'
        self.request.response.redirect(self.context.absolute_url() + resource)
