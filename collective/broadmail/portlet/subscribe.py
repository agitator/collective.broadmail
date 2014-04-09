from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.broadmail import _
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.formlib import form
from zope.interface import implements
from zope.schema import TextLine


class ISubscribeNewsletterPortlet(IPortletDataProvider):
    """A portlet displaying a subscribe newsletters.
    """

    name = TextLine(
        title=_(u"Name of Portlet"),
        default=u"Subscribe to our Newsletter",
        required=False,
    )


class Assignment(base.Assignment):
    implements(ISubscribeNewsletterPortlet)

    def __init__(self, name=u'', authcode=None,
                 opt_in_id=None, opt_in_source=None):
        self.name = name

    def title(self):
        return self.name or _(u'Our newsletter')


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('subscribe.pt')

    def __init__(self, *args):
        self.assignment = args[-1]
        super(self.__class__, self).__init__(*args)

    @property
    def available(self):
        return True

    def title(self):
        return self.data.name or self.data.title()


class AddForm(base.AddForm):
    form_fields = form.Fields(ISubscribeNewsletterPortlet)
    label = _(u"Add Broadmail Subscription Portlet")
    description = _(u"This portlet displays a Broadmail Subscription Portlet.")

    def __init__(self, context, request):
        super(AddForm, self).__init__(context, request)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(ISubscribeNewsletterPortlet)
    label = _(u"Edit Broadmail Subscribe Portlet")
    description = _(u"This portlet displays a Broadmail Subscription Portlet.")
