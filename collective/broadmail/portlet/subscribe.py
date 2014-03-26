from Acquisition import aq_inner
from zope.interface import alsoProvides
from z3c.form.interfaces import IFormLayer
from plone.z3cform.interfaces import IWrappedForm
from plone.z3cform import z2
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import implements
from zope import schema

from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize

from plone.portlets.interfaces import IPortletDataProvider

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base


from Acquisition import aq_inner
#from Products.CMFPlone.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.broadmail import _
#from Products.PloneGazette.interfaces import INewsletterTheme
from plone.app.portlets.portlets import base
#from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.directives.form import Form
from plone.directives.form import Schema
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form.field import Fields
#from zope import schema
#from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope.schema import Choice
from zope.schema import Bool
#from zope.schema import Text
from zope.schema import TextLine

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ISubscribeNewsletterPortlet(IPortletDataProvider):
    """A portlet displaying a subscribe newsletters.
    """

    name = TextLine(
        title=_(u"Name of Portlet"),
        default=u"Subscribe to our Newsletter",
        required=False,
    )

    authcode = TextLine(
        title=_(u"Broadmail Authorization Code"),
        default=u"",
        required=True,
    )

    opt_in_id = TextLine(
        title=_(u"Opt-In-Id"),
        default=u"",
        required=True,
    )

    opt_in_source = TextLine(
        title=_(u"Opt-In-Source"),
        default=u"",
        required=True,
    )


class Assignment(base.Assignment):
    implements(ISubscribeNewsletterPortlet)

    def __init__(self, name=u'', authcode=None, opt_in_id=None,
                 opt_in_source=None):
        self.name = name
        self.authcode = authcode
        self.opt_in_id = opt_in_id
        self.opt_in_source = opt_in_source
        # self.newsletters = newsletters

    def title(self):
        return self.name or _(u'Our newsletter')


class PortletFormView(FormWrapper):
    """ Form view which renders z3c.forms embedded in a portlet.

    Subclass FormWrapper so that we can use custom frame template. """

    index = ViewPageTemplateFile("formwrapper.pt")


# formats = SimpleVocabulary(
#     [
#         SimpleTerm(
#             title=_(u"HTML"),
#             value=u"HTML",
#         ),
#         SimpleTerm(
#             title=_(u"Text"),
#             value=u"Text",
#         ),
#     ]
# )

salutation = SimpleVocabulary(
    [
        SimpleTerm(
            title=_(u"Mr."),
            value=u"male",
        ),
        SimpleTerm(
            title=_(u"Ms."),
            value=u"female",
        ),
    ]
)


class ISubscribeNewsletterForm(Schema):

    salutation = Choice(
        title=_(u"Salutation"),
        required=False,
        vocabulary=salutation
    )

    firstname = TextLine(
        title=_(u"First name"),
        required=True,
    )

    name = TextLine(
        title=_(u"Name"),
        required=True,
    )

    bmRecipientId = TextLine(
        title=_(u"E-mail address"),
        required=True,
    )

#    form.mode(bmOptInId='hidden')
    bmOptInId = TextLine(
        title=_(u"Opt-In-Id"),
        required=True,
    )

    bmFailOnUnsubscribe = Bool(
        title=_(u"FailOnUnsubscribe"),
        required=True,
    )

    bmOverwrite = Bool(
        title=_(u"Overwrite"),
        required=True,
    )

# ### default values ###
# def bmOptInIdDefault(self):
#     return ['F']
# provideAdapter(ComputedWidgetAttribute(
#     bmOptInIdDefault,
#     field=ISubscribeNewsletterForm['bmOptInId']), name='default')


class SubscribeNewsletterForm(Form):

    fields = Fields(ISubscribeNewsletterForm)
    ignoreContext = True
    label = _(u"")

    def __init__(self, context, request, data=None):
        """
        """
        super(form.Form, self).__init__(context, request)

        self.data = data

    def updateWidgets(self):
        super(self.__class__, self).updateWidgets()
        self.prefix = ''

        self.widgets['bmRecipientId'].size = 20
        self.widgets['firstname'].size = 20
        self.widgets['name'].size = 20

        self.widgets['salutation'].name = 'salutation'
        self.widgets['firstname'].name = 'firstname'
        self.widgets['name'].name = 'name'
        self.widgets['bmRecipientId'].name = 'bmRecipientId'
        self.widgets['bmOptInId'].name = 'bmOptInId'

    @property
    def action(self):
        """ Rewrite HTTP POST action.

        If the form is rendered embedded on the others pages we
        make sure the form is posted through the same view always,
        instead of making HTTP POST to the page where the form was rendered.
        """
        target = 'https://api.broadmail.de/http/form/%s/subscribe' \
            % (self.data.authcode)
        return target

    @button.buttonAndHandler(_('Subscribe'), name='subscribe')
    def search(self, action):
        """ Form button hander. """

        data, errors = self.extractData()

        if not errors:
            pass


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('subscribe.pt')

    def __init__(self, *args):
        self.assignment = args[-1]
        super(self.__class__, self).__init__(*args)
        self.form_wrapper = self.createForm()

    def createForm(self):
        """ Create a form instance.

        @return: z3c.form wrapped for Plone view
        """

        context = aq_inner(self.context)

        form = SubscribeNewsletterForm(context, self.request, data=self.data)

        # Wrap a form in Plone view
        view = PortletFormView(context, self.request)
        view = view.__of__(context)  # Make sure acquisition chain is respected
        view.form_instance = form
        return view
        # return form

#    def newsletters(self):
        # return self.form_wrapper.newslettertheme()
        # return self.form_wrapper.form_instance.newslettertheme()

    @property
    def available(self):
        return True

    def title(self):
        return self.data.name or self.data.title()


class AddForm(base.AddForm):

    form_fields = Fields(ISubscribeNewsletterPortlet)
    label = _(u"Add Broadmail Subscription Portlet")
    description = _(u"This portlet displays a Broadmail Subscription Portlet.")

    def __init__(self, context, request):
        super(AddForm, self).__init__(context, request)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = Fields(ISubscribeNewsletterPortlet)
    label = _(u"Edit Broadmail Subscribe Portlet")
    description = _(u"This portlet displays a Broadmail Subscription Portlet.")
