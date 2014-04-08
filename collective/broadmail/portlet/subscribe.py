from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base

from plone.z3cform.layout import FormWrapper

class ISubscriptionPortlet(IPortletDataProvider):
    """A portlet displaying a subscribe newsletters.
    """

    name = schema.TextLine(
        title=_(u"Name of Portlet"),
        default=u"Subscribe to our Newsletter",
        required=False,
    )

    authcode = schema.TextLine(
        title=_(u"Broadmail Authorization Code"),
        default=u"",
        required=True,
    )

    opt_in_id = schema.TextLine(
        title=_(u"Opt-In-Id"),
        default=u"",
        required=True,
    )

    opt_in_source = schema.TextLine(
        title=_(u"Opt-In-Source"),
        default=u"",
        required=True,
    )



class Assignment(base.Assignment):
    implements(ISubscriptionPortlet)

    def __init__(self, name=u'', authcode=None, opt_in_id=None,
                 opt_in_source=None):
        self.name = name
        self.authcode = authcode
        self.opt_in_id = opt_in_id
        self.opt_in_source = opt_in_source
        # self.newsletters = newsletters

    @property
    def title(self):
        import ipdb; ipdb.set_trace()
        return self.name or _(u'Our newsletter')


class PortletFormView(FormWrapper):
    """ Form view which renders z3c.forms embedded in a portlet.

    Subclass FormWrapper so that we can use custom frame template. """

    index = ViewPageTemplateFile("formwrapper.pt")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('subscribe.pt')

    def __init__(self, *args):
        self.assignment = args[-1]
        super(self.__class__, self).__init__(*args)
#        self.form_wrapper = self.createForm()
#
#    def createForm(self):
#        """ Create a form instance.
#
#        @return: z3c.form wrapped for Plone view
#        """
#
#        context = aq_inner(self.context)
#
#        form = SubscribeNewsletterForm(context, self.request, data=self.data)
#
#        # Wrap a form in Plone view
#        view = PortletFormView(context, self.request)
#        view = view.__of__(context)  # Make sure acquisition chain is respected
#        view.form_instance = form
#        return view

    @property
    def title(self):
        return self.name or _(u'Our newsletter')



class AddForm(base.AddForm):
    form_fields = form.Fields(ISubscriptionPortlet)
    label = _(u"Add Broadmail Subscription Portlet")
    description = _(u"This portlet displays a Broadmail Subscription Portlet.")

#    def create(self, data):
#        return Assignment(count=data.get('count', 5), state=data.get('state', ('published', )))
    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(ISubscriptionPortlet)
    label = _(u"Edit Broadmail Subscribe Portlet")
    description = _(u"This portlet displays a Broadmail Subscription Portlet.")
