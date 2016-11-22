# -*- coding: utf-8 -*-

"""
mwdoc allows to easily version mediawiki pages.
"""

import mwclient

class Documentation(object):

    N_MAIN = '0'
    NS_TALK = '1'
    NS_USER = '2'
    NS_USERTALK = '3'
    NS_TEST = '4'
    NS_TESTTALK = '5'
    NS_FILE = '6'
    NS_FILETALK = '7'
    NS_MEDIAWIKI = '8'
    NS_MEDIAWIKITALK = '9'
    NS_TEMPLATE = '10'
    NS_TEMPLATETALK = '11'
    NS_HELP = '12'
    NS_HELPTALK = '13'
    NS_CATEGORY = '14'
    NS_CATEGORYTALK = '15'

    VERBOSE = True

    def __init__(self, host, path = ''):
        self.site = mwclient.Site(host, path=path)

    def login(self, username, password):
        self.site.login(username, password)

    def createPage(self, version, pageName, text, prefix = '', summary = ''):
        """Create a new documentation page

        A page is identified by its fullpath [<prefix>/]<version>/<pageName>

        If no summary is provided, it will default to 'Create page <fullpath>'
        """
        if len(pageName) == 0:
            pageFullPath = '/'.join((prefix, version))
        else:
            pageFullPath = '/'.join((prefix, version, pageName))
        page = self.site.Pages[pageFullPath]
        if page.exists:
            if self.VERBOSE:
                print "[WARNING] Skip page creation: Page already exists: '%s'" % pageFullPath
            return False
        if not summary:
            summary = 'Create page %s' % pageFullPath
        page.save(text, summary = summary)
        if self.VERBOSE:
            print "[INFO] Page successfully created: '%s'" % pageFullPath
        return True

    def versionPage(self, sourceVersion, targetVersion, pageBaseName, prefix = ''):
        """Create a new version of a page

        The page identified by [<prefix>/]<sourceVersion>/<pageBaseName> will
        be copied to [<prefix>/]<targetVersion>/<pageBaseName>

        The summary associated with each page will be '<versionSource> ->
        <versionTarget>'
        """
        if len(pageBaseName) == 0:
            pageFullPath = '/'.join((prefix, sourceVersion))
        else:
            pageFullPath = '/'.join((prefix, sourceVersion, pageBaseName))
        sourcePage = self.site.Pages[pageFullPath]
        if not sourcePage.exists:
            if self.VERBOSE:
                print "[WARNING] Skip versioning: Source page doesn't exist: '%s'" % pageFullPath
            return False
        text = sourcePage.text()
        return self.createPage(targetVersion, pageBaseName, text, prefix = prefix, summary = sourceVersion + ' -> ' + targetVersion)

    def listPages(self, prefix, namespace = None):
        """List page associated with a given namespace.

        By default, the function will try to guess the namespace using the
        provided prefix.

        It is also possible to specify a namespace using the defined
        constants 'NS_*'
        """
        if namespace == None:
            namespace = self.site.Pages.guess_namespace(prefix)

        prefix_without_ns = mwclient.page.Page.strip_namespace(prefix)

        pages = self.site.allpages(prefix=prefix_without_ns, namespace=namespace)
        return pages

    def versionPages(self, sourceVersion, targetVersion, prefixes = None):
        """Create a new version of given documention set

        A documentation set correspond to a collection of pages identified by a
        a <sourceVersion> and a list of prefixes.

        By providing:
          sourceVersion = '0.1'
          targetVersion = '0.2'
          prefixes = ['Documentation', 'Template:Documentation']

        All pages matching both 'Documentation/0.1*' and
        'Template:Documentation/0.1*' will be copied into pages having prefixes
        'Documentation/0.2' and
        'Template:Documentation/0.2'.
        """
        prefixes = prefixes or []
        results = []
        for prefix in prefixes:
            sourcePageNamePrefix = '/'.join((prefix, sourceVersion))
            sourcePages = self.listPages(sourcePageNamePrefix)
            for sourcePage in sourcePages:
                parts = sourcePage.name.split(sourcePageNamePrefix + '/')
                targetPageBaseName = ''
                if len(parts) == 2:
                  targetPageBaseName = parts[1]
                results.append(self.versionPage(sourceVersion, targetVersion, targetPageBaseName, prefix))
        return results

