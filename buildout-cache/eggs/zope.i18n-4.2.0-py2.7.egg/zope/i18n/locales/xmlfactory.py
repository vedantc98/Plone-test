##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""XML Locale-related objects and functions
"""
from datetime import datetime, date, time
from xml.dom.minidom import parse as parseXML
from zope.i18n.locales import Locale, LocaleDisplayNames, LocaleDates
from zope.i18n.locales import LocaleVersion, LocaleIdentity, LocaleTimeZone
from zope.i18n.locales import LocaleCalendar, LocaleCurrency, LocaleNumbers
from zope.i18n.locales import LocaleFormat, LocaleFormatLength, dayMapping
from zope.i18n.locales import LocaleOrientation, LocaleDayContext
from zope.i18n.locales import LocaleMonthContext, calendarAliases
from zope.i18n.locales.inheritance import InheritingDictionary
from .._compat import _u

_BLANK = _u('')

class LocaleFactory(object):
    """This class creates a Locale object from an ICU XML file."""

    def __init__(self, path):
        """Initialize factory."""
        self._path = path
        # Mainly for testing
        if path:
            self._data = parseXML(path).documentElement

    def _getText(self, nodelist):
        rc = _BLANK
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc


    def _extractVersion(self, identity_node):
        """Extract the Locale's version info based on data from the DOM
        tree.

        Example::

          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <identity>
          ...   <version number="1.0">Some notes</version>
          ...   <generation date="2003-12-19" />
          ...   <language type="de" />
          ...   <territory type="DE" />
          ... </identity>''')
          >>> dom = parseString(xml)

          >>> version = factory._extractVersion(dom.documentElement)
          >>> version.number
          u'1.0'
          >>> version.generationDate
          datetime.date(2003, 12, 19)
          >>> version.notes
          u'Some notes'
        """
        number = generationDate = notes = None
        # Retrieve the version number and notes of the locale
        nodes = identity_node.getElementsByTagName('version')
        if nodes:
            number = nodes[0].getAttribute('number')
            notes = self._getText(nodes[0].childNodes)
        # Retrieve the generationDate of the locale
        nodes = identity_node.getElementsByTagName('generation')
        if nodes:
            year, month, day = nodes[0].getAttribute('date').split('-')
            generationDate = date(int(year), int(month), int(day))

        return LocaleVersion(number, generationDate, notes)


    def _extractIdentity(self):
        """Extract the Locale's identity object based on info from the DOM
        tree.

        Example::

          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <ldml>
          ...   <identity>
          ...     <version number="1.0"/>
          ...     <generation date="2003-12-19" />
          ...     <language type="en" />
          ...     <territory type="US" />
          ...     <variant type="POSIX" />
          ...   </identity>
          ... </ldml>''')
          >>> factory = LocaleFactory(None)
          >>> factory._data = parseString(xml).documentElement

          >>> id = factory._extractIdentity()
          >>> id.language
          u'en'
          >>> id.script is None
          True
          >>> id.territory
          u'US'
          >>> id.variant
          u'POSIX'
          >>> id.version.number
          u'1.0'
        """
        id = LocaleIdentity()
        identity = self._data.getElementsByTagName('identity')[0]
        # Retrieve the language of the locale
        nodes = identity.getElementsByTagName('language')
        if nodes != []:
            id.language = nodes[0].getAttribute('type')  or None
        # Retrieve the territory of the locale
        nodes = identity.getElementsByTagName('territory')
        if nodes != []:
            id.territory = nodes[0].getAttribute('type') or None
        # Retrieve the varriant of the locale
        nodes = identity.getElementsByTagName('variant')
        if nodes != []:
            id.variant = nodes[0].getAttribute('type') or None

        id.version = self._extractVersion(identity)
        return id


    def _extractTypes(self, names_node):
        """Extract all types from the names_node.

        Example::

          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <displayNames>
          ...   <types>
          ...     <type type="Fallback" key="calendar"></type>
          ...     <type type="buddhist" key="calendar">BUDDHIST</type>
          ...     <type type="chinese" key="calendar">CHINESE</type>
          ...     <type type="gregorian" key="calendar">GREGORIAN</type>
          ...     <type type="stroke" key="collation">STROKE</type>
          ...     <type type="traditional" key="collation">TRADITIONAL</type>
          ...   </types>
          ... </displayNames>''')
          >>> dom = parseString(xml)

          >>> types = factory._extractTypes(dom.documentElement)
          >>> keys = types.keys()
          >>> keys.sort()
          >>> keys[:2]
          [(u'Fallback', u'calendar'), (u'buddhist', u'calendar')]
          >>> keys[2:4]
          [(u'chinese', u'calendar'), (u'gregorian', u'calendar')]
          >>> keys[4:]
          [(u'stroke', u'collation'), (u'traditional', u'collation')]
          >>> types[(_u('chinese'), _u('calendar'))]
          u'CHINESE'
          >>> types[(_u('stroke'), _u('collation'))]
          u'STROKE'
        """
        # 'types' node has not to exist
        types_nodes = names_node.getElementsByTagName('types')
        if types_nodes == []:
            return
        # Retrieve all types
        types = InheritingDictionary()
        for type_node in types_nodes[0].getElementsByTagName('type'):
            type = type_node.getAttribute('type')
            key = type_node.getAttribute('key')
            types[(type, key)] = self._getText(type_node.childNodes)
        return types


    def _extractDisplayNames(self):
        """Extract all display names from the DOM tree.

        Example::

          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <ldml>
          ...   <localeDisplayNames>
          ...     <languages>
          ...       <language type="Fallback"></language>
          ...       <language type="aa">aa</language>
          ...       <language type="ab">ab</language>
          ...     </languages>
          ...     <scripts>
          ...       <script type="Arab">Arab</script>
          ...       <script type="Armn">Armn</script>
          ...     </scripts>
          ...     <territories>
          ...       <territory type="AD">AD</territory>
          ...       <territory type="AE">AE</territory>
          ...     </territories>
          ...     <variants>
          ...       <variant type="Fallback"></variant>
          ...       <variant type="POSIX">POSIX</variant>
          ...     </variants>
          ...     <keys>
          ...       <key type="calendar">CALENDAR</key>
          ...       <key type="collation">COLLATION</key>
          ...     </keys>
          ...     <types>
          ...       <type type="buddhist" key="calendar">BUDDHIST</type>
          ...       <type type="stroke" key="collation">STROKE</type>
          ...     </types>
          ...   </localeDisplayNames>
          ... </ldml>''')
          >>> factory = LocaleFactory(None)
          >>> factory._data = parseString(xml).documentElement

          >>> names = factory._extractDisplayNames()

          >>> keys = names.languages.keys()
          >>> keys.sort()
          >>> keys
          [u'Fallback', u'aa', u'ab']
          >>> names.languages[_u("aa")]
          u'aa'

          >>> keys = names.scripts.keys()
          >>> keys.sort()
          >>> keys
          [u'Arab', u'Armn']
          >>> names.scripts[_u("Arab")]
          u'Arab'

          >>> keys = names.territories.keys()
          >>> keys.sort()
          >>> keys
          [u'AD', u'AE']
          >>> names.territories[_u("AD")]
          u'AD'

          >>> keys = names.variants.keys()
          >>> keys.sort()
          >>> keys
          [u'Fallback', u'POSIX']
          >>> names.variants[_u("Fallback")]
          u''

          >>> keys = names.keys.keys()
          >>> keys.sort()
          >>> keys
          [u'calendar', u'collation']
          >>> names.keys[_u("calendar")]
          u'CALENDAR'

          >>> names.types[(_u("stroke"), _u("collation"))]
          u'STROKE'
        """
        displayNames = LocaleDisplayNames()
        # Neither the 'localeDisplayNames' or 'scripts' node has to exist
        names_nodes = self._data.getElementsByTagName('localeDisplayNames')
        if names_nodes == []:
            return displayNames

        for group_tag, single_tag in (('languages', 'language'),
                                      ('scripts', 'script'),
                                      ('territories', 'territory'),
                                      ('variants', 'variant'),
                                      ('keys', 'key')):
            group_nodes = names_nodes[0].getElementsByTagName(group_tag)
            if group_nodes == []:
                continue
            # Retrieve all children
            elements = InheritingDictionary()
            for element in group_nodes[0].getElementsByTagName(single_tag):
                type = element.getAttribute('type')
                elements[type] = self._getText(element.childNodes)
            setattr(displayNames, group_tag, elements)

        types = self._extractTypes(names_nodes[0])
        if types is not None:
            displayNames.types = types
        return displayNames


    def _extractMonths(self, months_node, calendar):
        """Extract all month entries from cal_node and store them in calendar.

        Example::

          >>> class CalendarStub(object):
          ...     months = None
          >>> calendar = CalendarStub()
          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <months>
          ...   <default type="format" />
          ...   <monthContext type="format">
          ...     <default type="wide" />
          ...     <monthWidth type="wide">
          ...       <month type="1">Januar</month>
          ...       <month type="2">Februar</month>
          ...       <month type="3">Maerz</month>
          ...       <month type="4">April</month>
          ...       <month type="5">Mai</month>
          ...       <month type="6">Juni</month>
          ...       <month type="7">Juli</month>
          ...       <month type="8">August</month>
          ...       <month type="9">September</month>
          ...       <month type="10">Oktober</month>
          ...       <month type="11">November</month>
          ...       <month type="12">Dezember</month>
          ...     </monthWidth>
          ...     <monthWidth type="abbreviated">
          ...       <month type="1">Jan</month>
          ...       <month type="2">Feb</month>
          ...       <month type="3">Mrz</month>
          ...       <month type="4">Apr</month>
          ...       <month type="5">Mai</month>
          ...       <month type="6">Jun</month>
          ...       <month type="7">Jul</month>
          ...       <month type="8">Aug</month>
          ...       <month type="9">Sep</month>
          ...       <month type="10">Okt</month>
          ...       <month type="11">Nov</month>
          ...       <month type="12">Dez</month>
          ...     </monthWidth>
          ...   </monthContext>
          ... </months>''')
          >>> dom = parseString(xml)
          >>> factory._extractMonths(dom.documentElement, calendar)

        The contexts and widths were introduced in CLDR 1.1, the way
        of getting month names is like this::

          >>> calendar.defaultMonthContext
          u'format'

          >>> ctx = calendar.monthContexts[_u("format")]
          >>> ctx.defaultWidth
          u'wide'

          >>> names = [ctx.months[_u("wide")][type] for type in range(1,13)]
          >>> names[:7]
          [u'Januar', u'Februar', u'Maerz', u'April', u'Mai', u'Juni', u'Juli']
          >>> names[7:]
          [u'August', u'September', u'Oktober', u'November', u'Dezember']

          >>> abbrs = [ctx.months[_u("abbreviated")][type] for type in range(1,13)]
          >>> abbrs[:6]
          [u'Jan', u'Feb', u'Mrz', u'Apr', u'Mai', u'Jun']
          >>> abbrs[6:]
          [u'Jul', u'Aug', u'Sep', u'Okt', u'Nov', u'Dez']

        The old, CLDR 1.0 way of getting month names and abbreviations::

          >>> names = [calendar.months.get(type, (None, None))[0]
          ...          for type in range(1, 13)]
          >>> names[:7]
          [u'Januar', u'Februar', u'Maerz', u'April', u'Mai', u'Juni', u'Juli']
          >>> names[7:]
          [u'August', u'September', u'Oktober', u'November', u'Dezember']

          >>> abbrs = [calendar.months.get(type, (None, None))[1]
          ...          for type in range(1, 13)]
          >>> abbrs[:6]
          [u'Jan', u'Feb', u'Mrz', u'Apr', u'Mai', u'Jun']
          >>> abbrs[6:]
          [u'Jul', u'Aug', u'Sep', u'Okt', u'Nov', u'Dez']


        """

        defaultMonthContext_node = months_node.getElementsByTagName('default')
        if defaultMonthContext_node:
            calendar.defaultMonthContext = defaultMonthContext_node[0].getAttribute('type')

        monthContext_nodes = months_node.getElementsByTagName('monthContext')
        if not monthContext_nodes:
            return

        calendar.monthContexts = InheritingDictionary()
        names_node = abbrs_node = None # BBB

        for node in monthContext_nodes:
            context_type = node.getAttribute('type')
            mctx = LocaleMonthContext(context_type)
            calendar.monthContexts[context_type] = mctx

            defaultWidth_node = node.getElementsByTagName('default')
            if defaultWidth_node:
                mctx.defaultWidth = defaultWidth_node[0].getAttribute('type')

            widths = InheritingDictionary()
            mctx.months = widths
            for width_node in node.getElementsByTagName('monthWidth'):
                width_type = width_node.getAttribute('type')
                width = InheritingDictionary()
                widths[width_type] = width

                for month_node in width_node.getElementsByTagName('month'):
                    mtype = int(month_node.getAttribute('type'))
                    width[mtype] = self._getText(month_node.childNodes)

                if context_type == 'format':
                    if width_type == 'abbreviated':
                        abbrs_node = width_node
                    elif width_type == 'wide':
                        names_node = width_node

        if not (names_node and abbrs_node):
            return

        # Get all month names
        names = {}
        for name_node in names_node.getElementsByTagName('month'):
            type = int(name_node.getAttribute('type'))
            names[type] = self._getText(name_node.childNodes)

        # Get all month abbrs
        abbrs = {}
        for abbr_node in abbrs_node.getElementsByTagName('month'):
            type = int(abbr_node.getAttribute('type'))
            abbrs[type] = self._getText(abbr_node.childNodes)

        # Put the info together
        calendar.months = InheritingDictionary()
        for type in range(1, 13):
            calendar.months[type] = (names.get(type, None),
                                     abbrs.get(type, None))


    def _extractDays(self, days_node, calendar):
        """Extract all day entries from cal_node and store them in
        calendar.

        Example::

          >>> class CalendarStub(object):
          ...     days = None
          >>> calendar = CalendarStub()
          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <days>
          ...   <default type="format" />
          ...   <dayContext type="format">
          ...     <default type="wide" />
          ...     <dayWidth type="wide">
          ...       <day type="sun">Sonntag</day>
          ...       <day type="mon">Montag</day>
          ...       <day type="tue">Dienstag</day>
          ...       <day type="wed">Mittwoch</day>
          ...       <day type="thu">Donnerstag</day>
          ...       <day type="fri">Freitag</day>
          ...       <day type="sat">Samstag</day>
          ...     </dayWidth>
          ...     <dayWidth type="abbreviated">
          ...       <day type="sun">So</day>
          ...       <day type="mon">Mo</day>
          ...       <day type="tue">Di</day>
          ...       <day type="wed">Mi</day>
          ...       <day type="thu">Do</day>
          ...       <day type="fri">Fr</day>
          ...       <day type="sat">Sa</day>
          ...     </dayWidth>
          ...   </dayContext>
          ... </days>''')
          >>> dom = parseString(xml)
          >>> factory._extractDays(dom.documentElement, calendar)

        Day contexts and widths were introduced in CLDR 1.1, here's
        how to use them::

          >>> calendar.defaultDayContext
          u'format'

          >>> ctx = calendar.dayContexts[_u("format")]
          >>> ctx.defaultWidth
          u'wide'

          >>> names = [ctx.days[_u("wide")][type] for type in range(1,8)]
          >>> names[:4]
          [u'Montag', u'Dienstag', u'Mittwoch', u'Donnerstag']
          >>> names[4:]
          [u'Freitag', u'Samstag', u'Sonntag']

          >>> abbrs = [ctx.days[_u("abbreviated")][type] for type in range(1,8)]
          >>> abbrs
          [u'Mo', u'Di', u'Mi', u'Do', u'Fr', u'Sa', u'So']

        And here's the old CLDR 1.0 way of getting day names and
        abbreviations::

          >>> names = [calendar.days.get(type, (None, None))[0]
          ...          for type in range(1, 8)]
          >>> names[:4]
          [u'Montag', u'Dienstag', u'Mittwoch', u'Donnerstag']
          >>> names[4:]
          [u'Freitag', u'Samstag', u'Sonntag']

          >>> abbrs = [calendar.days.get(type, (None, None))[1]
          ...          for type in range(1, 8)]
          >>> abbrs
          [u'Mo', u'Di', u'Mi', u'Do', u'Fr', u'Sa', u'So']
        """

        defaultDayContext_node = days_node.getElementsByTagName('default')
        if defaultDayContext_node:
            calendar.defaultDayContext = defaultDayContext_node[0].getAttribute('type')

        dayContext_nodes = days_node.getElementsByTagName('dayContext')
        if not dayContext_nodes:
            return

        calendar.dayContexts = InheritingDictionary()
        names_node = abbrs_node = None # BBB

        for node in dayContext_nodes:
            context_type = node.getAttribute('type')
            dctx = LocaleDayContext(context_type)
            calendar.dayContexts[context_type] = dctx

            defaultWidth_node = node.getElementsByTagName('default')
            if defaultWidth_node:
                dctx.defaultWidth = defaultWidth_node[0].getAttribute('type')

            widths = InheritingDictionary()
            dctx.days = widths
            for width_node in node.getElementsByTagName('dayWidth'):
                width_type = width_node.getAttribute('type')
                width = InheritingDictionary()
                widths[width_type] = width

                for day_node in width_node.getElementsByTagName('day'):
                    dtype = dayMapping[day_node.getAttribute('type')]
                    width[dtype] = self._getText(day_node.childNodes)

                if context_type == 'format':
                    if width_type == 'abbreviated':
                        abbrs_node = width_node
                    elif width_type == 'wide':
                        names_node = width_node

        if not (names_node and abbrs_node):
            return

        # Get all weekday names
        names = {}
        for name_node in names_node.getElementsByTagName('day'):
            type = dayMapping[name_node.getAttribute('type')]
            names[type] = self._getText(name_node.childNodes)
        # Get all weekday abbreviations
        abbrs = {}
        for abbr_node in abbrs_node.getElementsByTagName('day'):
            type = dayMapping[abbr_node.getAttribute('type')]
            abbrs[type] = self._getText(abbr_node.childNodes)

        # Put the info together
        calendar.days = InheritingDictionary()
        for type in range(1, 13):
            calendar.days[type] = (names.get(type, None),
                                   abbrs.get(type, None))


    def _extractWeek(self, cal_node, calendar):
        """Extract all week entries from cal_node and store them in
        calendar.

        Example::

          >>> class CalendarStub(object):
          ...     week = None
          >>> calendar = CalendarStub()
          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <calendar type="gregorian">
          ...   <week>
          ...     <minDays count="1"/>
          ...     <firstDay day="sun"/>
          ...     <weekendStart day="fri" time="18:00"/>
          ...     <weekendEnd day="sun" time="18:00"/>
          ...   </week>
          ... </calendar>''')
          >>> dom = parseString(xml)
          >>> factory._extractWeek(dom.documentElement, calendar)

          >>> calendar.week['minDays']
          1
          >>> calendar.week['firstDay']
          7
          >>> calendar.week['weekendStart']
          (5, datetime.time(18, 0))
          >>> calendar.week['weekendEnd']
          (7, datetime.time(18, 0))
        """
        # See whether we have week entries
        week_nodes = cal_node.getElementsByTagName('week')
        if not week_nodes:
            return

        calendar.week = InheritingDictionary()

        # Get the 'minDays' value if available
        for node in week_nodes[0].getElementsByTagName('minDays'):
            calendar.week['minDays'] = int(node.getAttribute('count'))

        # Get the 'firstDay' value if available
        for node in week_nodes[0].getElementsByTagName('firstDay'):
            calendar.week['firstDay'] = dayMapping[node.getAttribute('day')]

        # Get the 'weekendStart' value if available
        for node in week_nodes[0].getElementsByTagName('weekendStart'):
            day = dayMapping[node.getAttribute('day')]
            time_args = map(int, node.getAttribute('time').split(':'))
            calendar.week['weekendStart'] = (day, time(*time_args))

            # Get the 'weekendEnd' value if available
        for node in week_nodes[0].getElementsByTagName('weekendEnd'):
            day = dayMapping[node.getAttribute('day')]
            time_args = map(int, node.getAttribute('time').split(':'))
            calendar.week['weekendEnd'] = (day, time(*time_args))


    def _extractEras(self, cal_node, calendar):
        """Extract all era entries from cal_node and store them in
        calendar.

        Example::

          >>> class CalendarStub(object):
          ...     days = None
          >>> calendar = CalendarStub()
          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <calendar type="gregorian">
          ...   <eras>
          ...      <eraAbbr>
          ...       <era type="0">BC</era>
          ...       <era type="1">AD</era>
          ...      </eraAbbr>
          ...      <eraName>
          ...       <era type="0">Before Christ</era>
          ...      </eraName>
          ...   </eras>
          ... </calendar>''')
          >>> dom = parseString(xml)
          >>> factory._extractEras(dom.documentElement, calendar)

          >>> names = [calendar.eras.get(type, (None, None))[0]
          ...          for type in range(2)]
          >>> names
          [u'Before Christ', None]

          >>> abbrs = [calendar.eras.get(type, (None, None))[1]
          ...          for type in range(2)]
          >>> abbrs
          [u'BC', u'AD']
        """
        # See whether we have era names and abbreviations
        eras_nodes = cal_node.getElementsByTagName('eras')
        if not eras_nodes:
            return
        names_nodes = eras_nodes[0].getElementsByTagName('eraName')
        abbrs_nodes = eras_nodes[0].getElementsByTagName('eraAbbr')

        # Get all era names
        names = {}
        if names_nodes:
            for name_node in names_nodes[0].getElementsByTagName('era'):
                type = int(name_node.getAttribute('type'))
                names[type] = self._getText(name_node.childNodes)
        # Get all era abbreviations
        abbrs = {}
        if abbrs_nodes:
            for abbr_node in abbrs_nodes[0].getElementsByTagName('era'):
                type = int(abbr_node.getAttribute('type'))
                abbrs[type] = self._getText(abbr_node.childNodes)

        calendar.eras = InheritingDictionary()
        for type in abbrs.keys():
            calendar.eras[type] = (names.get(type, None), abbrs.get(type, None))


    def _extractFormats(self, formats_node, lengthNodeName, formatNodeName):
        """Extract all format entries from formats_node and return a
        tuple of the form (defaultFormatType, [LocaleFormatLength, ...]).

        Example::

          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <dateFormats>
          ...   <default type="medium"/>
          ...   <dateFormatLength type="full">
          ...     <dateFormat>
          ...       <pattern>EEEE, MMMM d, yyyy</pattern>
          ...     </dateFormat>
          ...   </dateFormatLength>
          ...   <dateFormatLength type="medium">
          ...     <default type="DateFormatsKey2"/>
          ...     <dateFormat type="DateFormatsKey2">
          ...       <displayName>Standard Date</displayName>
          ...       <pattern>MMM d, yyyy</pattern>
          ...     </dateFormat>
          ...     <dateFormat type="DateFormatsKey3">
          ...       <pattern>MMM dd, yyyy</pattern>
          ...     </dateFormat>
          ...   </dateFormatLength>
          ... </dateFormats>''')
          >>> dom = parseString(xml)

          >>> default, lengths = factory._extractFormats(
          ...     dom.documentElement, 'dateFormatLength', 'dateFormat')
          >>> default
          u'medium'
          >>> lengths[_u("full")].formats[None].pattern
          u'EEEE, MMMM d, yyyy'
          >>> lengths[_u("medium")].default
          u'DateFormatsKey2'
          >>> lengths[_u("medium")].formats['DateFormatsKey3'].pattern
          u'MMM dd, yyyy'
          >>> lengths[_u("medium")].formats['DateFormatsKey2'].displayName
          u'Standard Date'
        """
        formats_default = None
        default_nodes = formats_node.getElementsByTagName('default')
        if default_nodes:
            formats_default = default_nodes[0].getAttribute('type')

        lengths = InheritingDictionary()
        for length_node in formats_node.getElementsByTagName(lengthNodeName):
            type = length_node.getAttribute('type') or None
            length = LocaleFormatLength(type)

            default_nodes = length_node.getElementsByTagName('default')
            if default_nodes:
                length.default = default_nodes[0].getAttribute('type')

            if length_node.getElementsByTagName(formatNodeName):
                length.formats = InheritingDictionary()

            for format_node in length_node.getElementsByTagName(formatNodeName):
                format = LocaleFormat()
                format.type = format_node.getAttribute('type') or None
                pattern_node = format_node.getElementsByTagName('pattern')[0]
                format.pattern = self._getText(pattern_node.childNodes)
                name_nodes = format_node.getElementsByTagName('displayName')
                if name_nodes:
                    format.displayName = self._getText(name_nodes[0].childNodes)
                length.formats[format.type] = format

            lengths[length.type] = length

        return (formats_default, lengths)

    def _extractCalendars(self, dates_node):
        """Extract all calendars and their specific information from the
        Locale's DOM tree.

        Example::

          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <dates>
          ...   <calendars>
          ...     <calendar type="gregorian">
          ...       <monthNames>
          ...         <month type="1">January</month>
          ...         <month type="12">December</month>
          ...       </monthNames>
          ...       <monthAbbr>
          ...         <month type="1">Jan</month>
          ...         <month type="12">Dec</month>
          ...       </monthAbbr>
          ...       <dayNames>
          ...         <day type="sun">Sunday</day>
          ...         <day type="sat">Saturday</day>
          ...       </dayNames>
          ...       <dayAbbr>
          ...         <day type="sun">Sun</day>
          ...         <day type="sat">Sat</day>
          ...       </dayAbbr>
          ...       <week>
          ...         <minDays count="1"/>
          ...         <firstDay day="sun"/>
          ...       </week>
          ...       <am>AM</am>
          ...       <pm>PM</pm>
          ...       <eras>
          ...         <eraAbbr>
          ...           <era type="0">BC</era>
          ...           <era type="1">AD</era>
          ...         </eraAbbr>
          ...       </eras>
          ...       <dateFormats>
          ...         <dateFormatLength type="full">
          ...           <dateFormat>
          ...             <pattern>EEEE, MMMM d, yyyy</pattern>
          ...           </dateFormat>
          ...         </dateFormatLength>
          ...       </dateFormats>
          ...       <timeFormats>
          ...         <default type="medium"/>
          ...         <timeFormatLength type="medium">
          ...           <timeFormat>
          ...             <pattern>h:mm:ss a</pattern>
          ...           </timeFormat>
          ...         </timeFormatLength>
          ...       </timeFormats>
          ...       <dateTimeFormats>
          ...         <dateTimeFormatLength>
          ...           <dateTimeFormat>
          ...             <pattern>{0} {1}</pattern>
          ...           </dateTimeFormat>
          ...         </dateTimeFormatLength>
          ...       </dateTimeFormats>
          ...     </calendar>
          ...     <calendar type="buddhist">
          ...       <eras>
          ...         <era type="0">BE</era>
          ...       </eras>
          ...     </calendar>
          ...   </calendars>
          ... </dates>''')
          >>> dom = parseString(xml)

          >>> calendars = factory._extractCalendars(dom.documentElement)
          >>> keys = calendars.keys()
          >>> keys.sort()
          >>> keys
          [u'buddhist', u'gregorian', 'thai-buddhist']

        Note that "thai-buddhist" are added as an alias to "buddhist".

          >>> calendars['buddhist'] is calendars['thai-buddhist']
          True

        """
        cals_nodes = dates_node.getElementsByTagName('calendars')
        # no calendar node
        if cals_nodes == []:
            return

        calendars = InheritingDictionary()
        for cal_node in cals_nodes[0].getElementsByTagName('calendar'):
            # get the calendar type
            type = cal_node.getAttribute('type')
            calendar = LocaleCalendar(type)

            # get month names and abbreviations
            months_nodes = cal_node.getElementsByTagName('months')
            if months_nodes:
                self._extractMonths(months_nodes[0], calendar)

            # get weekday names and abbreviations
            days_nodes = cal_node.getElementsByTagName('days')
            if days_nodes:
                self._extractDays(days_nodes[0], calendar)

            # get week information
            self._extractWeek(cal_node, calendar)

            # get am/pm designation values
            nodes = cal_node.getElementsByTagName('am')
            if nodes:
                calendar.am = self._getText(nodes[0].childNodes)
            nodes = cal_node.getElementsByTagName('pm')
            if nodes:
                calendar.pm = self._getText(nodes[0].childNodes)

            # get era names and abbreviations
            self._extractEras(cal_node, calendar)

            for formatsName, lengthName, formatName in (
                ('dateFormats', 'dateFormatLength', 'dateFormat'),
                ('timeFormats', 'timeFormatLength', 'timeFormat'),
                ('dateTimeFormats', 'dateTimeFormatLength', 'dateTimeFormat')):

                formats_nodes = cal_node.getElementsByTagName(formatsName)
                if formats_nodes:
                    default, formats = self._extractFormats(
                        formats_nodes[0], lengthName, formatName)
                    setattr(calendar,
                            'default'+formatName[0].upper()+formatName[1:],
                            default)
                    setattr(calendar, formatsName, formats)

            calendars[calendar.type] = calendar
            if calendar.type in calendarAliases:
                for alias in calendarAliases[calendar.type]:
                    calendars[alias] = calendar

        return calendars


    def _extractTimeZones(self, dates_node):
        """Extract all timezone information for the locale from the DOM
        tree.

        Example::

          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <dates>
          ...   <timeZoneNames>
          ...     <zone type="America/Los_Angeles" >
          ...       <long>
          ...         <generic>Pacific Time</generic>
          ...         <standard>Pacific Standard Time</standard>
          ...         <daylight>Pacific Daylight Time</daylight>
          ...       </long>
          ...       <short>
          ...         <generic>PT</generic>
          ...         <standard>PST</standard>
          ...         <daylight>PDT</daylight>
          ...       </short>
          ...       <exemplarCity>San Francisco</exemplarCity>
          ...     </zone>
          ...     <zone type="Europe/London">
          ...       <long>
          ...         <generic>British Time</generic>
          ...         <standard>British Standard Time</standard>
          ...         <daylight>British Daylight Time</daylight>
          ...       </long>
          ...       <exemplarCity>York</exemplarCity>
          ...     </zone>
          ...   </timeZoneNames>
          ... </dates>''')
          >>> dom = parseString(xml)
          >>> zones = factory._extractTimeZones(dom.documentElement)

          >>> keys = zones.keys()
          >>> keys.sort()
          >>> keys
          [u'America/Los_Angeles', u'Europe/London']
          >>> zones[_u("Europe/London")].names[_u("generic")]
          (u'British Time', None)
          >>> zones[_u("Europe/London")].cities
          [u'York']
          >>> zones[_u("America/Los_Angeles")].names[_u("generic")]
          (u'Pacific Time', u'PT')
        """
        tz_names = dates_node.getElementsByTagName('timeZoneNames')
        if not tz_names:
            return

        zones = InheritingDictionary()
        for node in tz_names[0].getElementsByTagName('zone'):
            type = node.getAttribute('type')
            zone = LocaleTimeZone(type)

            # get the short and long name node
            long = node.getElementsByTagName('long')
            short = node.getElementsByTagName('short')
            for type in (_u("generic"), _u("standard"), _u("daylight")):
                # get long name
                long_desc = None
                if long:
                    long_nodes = long[0].getElementsByTagName(type)
                    if long_nodes:
                        long_desc = self._getText(long_nodes[0].childNodes)
                # get short name
                short_desc = None
                if short:
                    short_nodes = short[0].getElementsByTagName(type)
                    if short_nodes:
                        short_desc = self._getText(short_nodes[0].childNodes)
                if long_desc is not None or short_desc is not None:
                    zone.names[type] = (long_desc, short_desc)

            for city in node.getElementsByTagName('exemplarCity'):
                zone.cities.append(self._getText(city.childNodes))

            zones[zone.type] = zone

        return zones


    def _extractDates(self):
        """Extract all date information from the DOM tree"""
        dates_nodes = self._data.getElementsByTagName('dates')
        if dates_nodes == []:
            return

        dates = LocaleDates()
        calendars = self._extractCalendars(dates_nodes[0])
        if calendars is not None:
            dates.calendars = calendars
        timezones = self._extractTimeZones(dates_nodes[0])
        if timezones is not None:
            dates.timezones = timezones
        return dates


    def _extractSymbols(self, numbers_node):
        """Extract all week entries from cal_node and store them in
        calendar.

        Example::

          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <numbers>
          ...   <symbols>
          ...     <decimal>.</decimal>
          ...     <group>,</group>
          ...     <list>;</list>
          ...     <percentSign>%</percentSign>
          ...     <nativeZeroDigit>0</nativeZeroDigit>
          ...     <patternDigit>#</patternDigit>
          ...     <plusSign>+</plusSign>
          ...     <minusSign>-</minusSign>
          ...     <exponential>E</exponential>
          ...     <perMille>o/oo</perMille>
          ...     <infinity>oo</infinity>
          ...     <nan>NaN</nan>
          ...   </symbols>
          ... </numbers>''')
          >>> dom = parseString(xml)
          >>> symbols = factory._extractSymbols(dom.documentElement)

          >>> symbols['list']
          u';'
          >>> keys = symbols.keys()
          >>> keys.sort()
          >>> keys[:5]
          [u'decimal', u'exponential', u'group', u'infinity', u'list']
          >>> keys[5:9]
          [u'minusSign', u'nan', u'nativeZeroDigit', u'patternDigit']
          >>> keys[9:]
          [u'perMille', u'percentSign', u'plusSign']
        """
        # See whether we have symbols entries
        symbols_nodes = numbers_node.getElementsByTagName('symbols')
        if not symbols_nodes:
            return

        symbols = InheritingDictionary()
        for name in (_u("decimal"), _u("group"), _u("list"), _u("percentSign"),
                     _u("nativeZeroDigit"), _u("patternDigit"), _u("plusSign"),
                     _u("minusSign"), _u("exponential"), _u("perMille"),
                     _u("infinity"), _u("nan")):
            nodes = symbols_nodes[0].getElementsByTagName(name)
            if nodes:
                symbols[name] = self._getText(nodes[0].childNodes)

        return symbols


    def _extractNumberFormats(self, numbers_node, numbers):
        """Extract all number formats from the numbers_node and save the data
        in numbers.

        Example::

          >>> class Numbers(object):
          ...     defaultDecimalFormat = None
          ...     decimalFormats = None
          ...     defaultScientificFormat = None
          ...     scientificFormats = None
          ...     defaultPercentFormat = None
          ...     percentFormats = None
          ...     defaultCurrencyFormat = None
          ...     currencyFormats = None
          >>> numbers = Numbers()
          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <numbers>
          ...   <decimalFormats>
          ...     <decimalFormatLength type="long">
          ...       <decimalFormat>
          ...         <pattern>#,##0.###</pattern>
          ...       </decimalFormat>
          ...     </decimalFormatLength>
          ...   </decimalFormats>
          ...   <scientificFormats>
          ...     <default type="long"/>
          ...     <scientificFormatLength type="long">
          ...       <scientificFormat>
          ...         <pattern>0.000###E+00</pattern>
          ...       </scientificFormat>
          ...     </scientificFormatLength>
          ...     <scientificFormatLength type="medium">
          ...       <scientificFormat>
          ...         <pattern>0.00##E+00</pattern>
          ...       </scientificFormat>
          ...     </scientificFormatLength>
          ...   </scientificFormats>
          ...   <percentFormats>
          ...     <percentFormatLength type="long">
          ...       <percentFormat>
          ...         <pattern>#,##0%</pattern>
          ...       </percentFormat>
          ...     </percentFormatLength>
          ...   </percentFormats>
          ...   <currencyFormats>
          ...     <currencyFormatLength type="long">
          ...       <currencyFormat>
          ...         <pattern>$ #,##0.00;($ #,##0.00)</pattern>
          ...       </currencyFormat>
          ...     </currencyFormatLength>
          ...   </currencyFormats>
          ... </numbers>''')
          >>> dom = parseString(xml)
          >>> factory._extractNumberFormats(dom.documentElement, numbers)

          >>> numbers.decimalFormats[_u("long")].formats[None].pattern
          u'#,##0.###'

          >>> numbers.defaultScientificFormat
          u'long'
          >>> numbers.scientificFormats[_u("long")].formats[None].pattern
          u'0.000###E+00'
          >>> numbers.scientificFormats[_u("medium")].formats[None].pattern
          u'0.00##E+00'

          >>> numbers.percentFormats[_u("long")].formats[None].pattern
          u'#,##0%'
          >>> numbers.percentFormats.get(_u("medium"), None) is None
          True

          >>> numbers.currencyFormats[_u("long")].formats[None].pattern
          u'$ #,##0.00;($ #,##0.00)'
          >>> numbers.currencyFormats.get(_u("medium"), None) is None
          True
        """

        for category in ('decimal', 'scientific', 'percent', 'currency'):
            formatsName = category+'Formats'
            lengthName = category+'FormatLength'
            formatName = category+'Format'
            defaultName = 'default'+formatName[0].upper()+formatName[1:]

            formats_nodes = numbers_node.getElementsByTagName(formatsName)
            if formats_nodes:
                default, formats = self._extractFormats(
                    formats_nodes[0], lengthName, formatName)
                setattr(numbers, defaultName, default)
                setattr(numbers, formatsName, formats)


    def _extractCurrencies(self, numbers_node):
        """Extract all currency definitions and their information from the
        Locale's DOM tree.

        Example::

          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <numbers>
          ...   <currencies>
          ...     <currency type="USD">
          ...       <displayName>Dollar</displayName>
          ...       <symbol>$</symbol>
          ...     </currency>
          ...     <currency type ="JPY">
          ...       <displayName>Yen</displayName>
          ...       <symbol>Y</symbol>
          ...     </currency>
          ...     <currency type ="INR">
          ...       <displayName>Rupee</displayName>
          ...       <symbol choice="true">0&lt;=Rf|1&lt;=Ru|1&lt;Rf</symbol>
          ...     </currency>
          ...     <currency type="PTE">
          ...       <displayName>Escudo</displayName>
          ...       <symbol>$</symbol>
          ...     </currency>
          ...   </currencies>
          ... </numbers>''')
          >>> dom = parseString(xml)
          >>> currencies = factory._extractCurrencies(dom.documentElement)

          >>> keys = currencies.keys()
          >>> keys.sort()
          >>> keys
          [u'INR', u'JPY', u'PTE', u'USD']

          >>> currencies['USD'].symbol
          u'$'
          >>> currencies['USD'].displayName
          u'Dollar'
          >>> currencies['USD'].symbolChoice
          False
        """
        currs_nodes = numbers_node.getElementsByTagName('currencies')
        if not currs_nodes:
            return

        currencies = InheritingDictionary()
        for curr_node in currs_nodes[0].getElementsByTagName('currency'):
            type = curr_node.getAttribute('type')
            currency = LocaleCurrency(type)

            nodes = curr_node.getElementsByTagName('symbol')
            if nodes:
                currency.symbol = self._getText(nodes[0].childNodes)
                currency.symbolChoice = \
                                      nodes[0].getAttribute('choice') == _u("true")

            nodes = curr_node.getElementsByTagName('displayName')
            if nodes:
                currency.displayName = self._getText(nodes[0].childNodes)

            currencies[type] = currency

        return currencies


    def _extractNumbers(self):
        """Extract all number information from the DOM tree"""
        numbers_nodes = self._data.getElementsByTagName('numbers')
        if not numbers_nodes:
            return

        numbers = LocaleNumbers()
        symbols = self._extractSymbols(numbers_nodes[0])
        if symbols is not None:
            numbers.symbols = symbols
        self._extractNumberFormats(numbers_nodes[0], numbers)
        currencies = self._extractCurrencies(numbers_nodes[0])
        if currencies is not None:
            numbers.currencies = currencies
        return numbers


    def _extractDelimiters(self):
        """Extract all delimiter entries from the DOM tree.

        Example::

          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <ldml>
          ...   <delimiters>
          ...     <quotationStart>``</quotationStart>
          ...     <quotationEnd>''</quotationEnd>
          ...     <alternateQuotationStart>`</alternateQuotationStart>
          ...     <alternateQuotationEnd>'</alternateQuotationEnd>
          ...   </delimiters>
          ... </ldml>''')
          >>> dom = parseString(xml)
          >>> factory._data = parseString(xml).documentElement
          >>> delimiters = factory._extractDelimiters()

          >>> delimiters[_u("quotationStart")]
          u'``'
          >>> delimiters[_u("quotationEnd")]
          u"''"
          >>> delimiters[_u("alternateQuotationStart")]
          u'`'
          >>> delimiters[_u("alternateQuotationEnd")]
          u"'"

          Escape: "'"
        """
        # See whether we have symbols entries
        delimiters_nodes = self._data.getElementsByTagName('delimiters')
        if not delimiters_nodes:
            return

        delimiters = InheritingDictionary()
        for name in (_u('quotationStart'), _u("quotationEnd"),
                     _u("alternateQuotationStart"), _u("alternateQuotationEnd")):
            nodes = delimiters_nodes[0].getElementsByTagName(name)
            if nodes:
                delimiters[name] = self._getText(nodes[0].childNodes)

        return delimiters


    def _extractOrientation(self):
        """Extract orientation information.

          >>> factory = LocaleFactory(None)
          >>> from xml.dom.minidom import parseString
          >>> xml = _u('''
          ... <ldml>
          ...   <layout>
          ...     <orientation lines="bottom-to-top" characters="right-to-left" />
          ...   </layout>
          ... </ldml>''')
          >>> dom = parseString(xml)
          >>> factory._data = parseString(xml).documentElement
          >>> orientation = factory._extractOrientation()
          >>> orientation.lines
          u'bottom-to-top'
          >>> orientation.characters
          u'right-to-left'
        """
        orientation_nodes = self._data.getElementsByTagName('orientation')
        if not orientation_nodes:
            return
        orientation = LocaleOrientation()
        for name in (_u("characters"), _u("lines")):
            value = orientation_nodes[0].getAttribute(name)
            if value:
                setattr(orientation, name, value)
        return orientation


    def __call__(self):
        """Create the Locale."""
        locale = Locale(self._extractIdentity())

        names = self._extractDisplayNames()
        if names is not None:
            locale.displayNames = names

        dates = self._extractDates()
        if dates is not None:
            locale.dates = dates

        numbers = self._extractNumbers()
        if numbers is not None:
            locale.numbers = numbers

        delimiters = self._extractDelimiters()
        if delimiters is not None:
            locale.delimiters = delimiters

        orientation = self._extractOrientation()
        if orientation is not None:
            locale.orientation = orientation

        # Unmapped:
        #
        #   - <characters>
        #   - <measurement>
        #   - <collations>, <collation>

        return locale