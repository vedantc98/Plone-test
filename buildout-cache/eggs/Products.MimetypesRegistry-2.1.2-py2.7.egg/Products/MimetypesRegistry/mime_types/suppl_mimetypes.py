# -*- coding: utf-8 -*-
from Products.MimetypesRegistry.interfaces import MimeTypeException
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem


map = {
    # '.extension' : 'mimetype',
    '.pjpg': 'image/pjpeg',  # progressive jpeg - is this is still a thing?
    '.woff2': 'font/woff2'
}


def initialize(registry):
    # Find things that are not in the specially registered mimetypes
    # and add them using some default policy, none of these will impl
    # iclassifier
    for ext, mt in map.items():
        if ext[0] == '.':
            ext = ext[1:]

        if registry.lookupExtension(ext):
            continue

        try:
            mto = registry.lookup(mt)
        except MimeTypeException:
            # malformed MIME type
            continue
        if mto:
            mto = mto[0]
            if ext not in mto.extensions:
                registry.register_extension(ext, mto)
                mto.extensions += (ext, )
            continue
        isBin = mt.split('/', 1)[0] != "text"
        registry.register(MimeTypeItem(mt, (mt,), (ext,), isBin))
