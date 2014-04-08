from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from yafowil.base import UNSET
from yafowil.controller import Controller
from yafowil.yaml import parse_from_YAML

from collective.broadmail import _

DEFAULTS = {
    'title': UNSET,
    'description': UNSET,
    'asset_data': UNSET,
    'track_type': UNSET,
    'genre': UNSET,
    'tag_list': "",
    'license': 'all-rights-reserved',
    'label_name': UNSET,
    'release_year': UNSET,
    'release_month': UNSET,
    'release_day': UNSET,
    'release': UNSET,
    'isrc': UNSET,
    'bpm': UNSET,
    'key_signature': UNSET,
    'purchase_url': UNSET,
    'video_url': UNSET,
    'sharing': UNSET,
    'downloadable': UNSET,
}


class SubscriptionForm(BrowserView):

    template = ViewPageTemplateFile('subscribe.pt')

    def _fetch_form(self):
        return parse_from_YAML('collective.broadmail:form.yaml',
                               self, _)

    def __call__(self):
        form = self._fetch_form()
        self.controller = Controller(form, self.request)

    @property
    def action(self):
        url = self.context.absolute_url()
        return '%s/@@soundcloud_%s' % (url)
