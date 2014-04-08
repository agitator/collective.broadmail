from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from yafowil.base import UNSET
from yafowil.controller import Controller
from yafowil.yaml import parse_from_YAML

from collective.broadmail import _

DEFAULTS = {
    'title': UNSET,
    'description': UNSET,
}


class SubscriptionForm(BrowserView):

    template = ViewPageTemplateFile('form.pt')

    def _fetch_form(self):
        return parse_from_YAML('collective.broadmail:portlet/form.yaml',
                               self, _)

    def __call__(self):
        form = self._fetch_form()
        controller = Controller(form, self.request)
        return controller.rendered

    @property
    def action(self):
        target = 'https://api.broadmail.de/http/form/%s/subscribe' \
            % (self.data.authcode)
        return target
