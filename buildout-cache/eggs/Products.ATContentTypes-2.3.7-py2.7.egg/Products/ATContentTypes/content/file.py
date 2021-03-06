# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import AnnotationStorage
from Products.Archetypes.atapi import FileField
from Products.Archetypes.atapi import FileWidget
from Products.Archetypes.atapi import PrimaryFieldMarshaller
from Products.Archetypes.atapi import Schema
from Products.Archetypes.BaseContent import BaseContent
from Products.ATContentTypes import ATCTMessageFactory as _
from Products.ATContentTypes.config import ICONMAP
from Products.ATContentTypes.config import PROJECTNAME
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content.base import ATCTFileContent
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.interfaces import IATFile
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from Products.validation import V_REQUIRED
from Products.validation.config import validation
from Products.validation.validators.SupplValidators import MaxSizeValidator
from urllib import quote
from zope.interface import implementer

import logging


try:
    from Products.MimetypesRegistry.interfaces import MimeTypeException
except ImportError:
    # Products.MimetypesRegistry < 2.1
    from Products.MimetypesRegistry.common import MimeTypeException


LOG = logging.getLogger('ATCT')

validation.register(MaxSizeValidator('checkFileMaxSize',
                                     maxsize=zconf.ATFile.max_file_size))

ATFileSchema = ATContentTypeSchema.copy() + Schema((
    FileField('file',
              required=True,
              primary=True,
              searchable=True,
              languageIndependent=True,
              storage=AnnotationStorage(migrate=True),
              validators=(('isNonEmptyFile', V_REQUIRED),
                          ('checkFileMaxSize', V_REQUIRED)),
              widget=FileWidget(
                  description='',
                  label=_(u'label_file', default=u'File'),
                  show_content_type=False,)),
), marshall=PrimaryFieldMarshaller()
)

# Title is pulled from the file name if we don't specify anything,
# so it's not strictly required, unlike in the rest of ATCT.
ATFileSchema['title'].required = False

finalizeATCTSchema(ATFileSchema)


@implementer(IATFile)
class ATFile(ATCTFileContent):
    """An external file uploaded to the site."""

    schema = ATFileSchema

    portal_type = 'File'
    archetype_name = 'File'
    _atct_newTypeFor = {'portal_type': 'CMF File', 'meta_type': 'Portal File'}
    assocMimetypes = ('application/*', 'audio/*', 'video/*', )
    assocFileExt = ()
    cmf_edit_kws = ()
    inlineMimetypes = ('application/msword',
                       'application/x-msexcel',  # ?
                       'application/vnd.ms-excel',
                       'application/vnd.ms-powerpoint',
                       'application/pdf',
                       'application/x-shockwave-flash',)

    security = ClassSecurityInfo()

    @security.protected(View)
    def index_html(self, REQUEST=None, RESPONSE=None):
        """Download the file
        """
        field = self.getPrimaryField()

        if field.getContentType(self) in self.inlineMimetypes:
            # return the PDF and Office file formats inline
            return ATCTFileContent.index_html(self, REQUEST, RESPONSE)
        # otherwise return the content as an attachment
        # Please note that text/* cannot be returned inline as
        # this is a security risk (IE renders anything as HTML).
        return field.download(self)

    @security.protected(ModifyPortalContent)
    def setFile(self, value, **kwargs):
        # Set id to uploaded id.
        self._setATCTFileContent(value, **kwargs)

    def __str__(self):
        """cmf compatibility
        """
        return self.get_data()

    @security.public
    def getIcon(self, relative_to_portal=0):
        # Calculate the icon using the mime type of the file.
        field = self.getField('file')
        if not field or not self.get_size():
            # field is empty
            return BaseContent.getIcon(self, relative_to_portal)

        contenttype = field.getContentType(self)
        contenttype_major = contenttype and contenttype.split('/')[0] or ''

        mtr = getToolByName(self, 'mimetypes_registry', None)
        utool = getToolByName(self, 'portal_url')

        if contenttype in ICONMAP:
            icon = quote(ICONMAP[contenttype])
        elif contenttype_major in ICONMAP:
            icon = quote(ICONMAP[contenttype_major])
        else:
            mimetypeitem = None
            try:
                mimetypeitem = mtr.lookup(contenttype)
            except MimeTypeException as msg:
                LOG.error('MimeTypeException for %s. Error is: %s' %
                          (self.absolute_url(), str(msg)))
            if not mimetypeitem:
                return BaseContent.getIcon(self, relative_to_portal)
            icon = mimetypeitem[0].icon_path

        if relative_to_portal:
            return icon
        else:
            # Relative to REQUEST['BASEPATH1']
            res = utool(relative=1) + '/' + icon
            while res[:1] == '/':
                res = res[1:]
            return res

    @security.protected(View)
    def icon(self):
        # for ZMI
        return self.getIcon()

    @security.private
    def cmf_edit(self, precondition='', file=None):
        if file is not None:
            self.setFile(file)

registerATCT(ATFile, PROJECTNAME)
