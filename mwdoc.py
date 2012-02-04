import mwclient
import os.path
import re

class Documentation(object):
  
  NS_MAIN = '0'
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
    pageFullPath = os.path.join(prefix, version, pageName)
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
    
    The page identified by [<prefix>/]<sourceVersion>/<pageBaseName> will be copied
    to [<prefix>/]<targetVersion>/<pageBaseName>
    
    The summary associated with each page will be '<versionSource> -> <versionTarget>'
    """
    pageFullPath = os.path.join(prefix, sourceVersion, pageBaseName)
    sourcePage = self.site.Pages[pageFullPath]
    if not sourcePage.exists:
      if self.VERBOSE:
        print "[WARNING] Skip versioning: Source page doesn't exist: '%s'" % pageFullPath
      return False
    text = sourcePage.edit()
    return self.createPage(targetVersion, pageBaseName, text, prefix = prefix, summary = sourceVersion + ' -> ' + targetVersion)
    
  def listPages(self, prefix, namespace = None):
    """List page associated with a given namespace.
    
    By default, the function will try to guess the namespace using the 
    provided prefix. 
    
    It is also possible to specify a namespace using the defined constants 'NS_*'
    """
    if namespace == None:
      namespace = self.site.Pages.guess_namespace(prefix)
    
    prefix_without_ns = mwclient.page.Page.strip_namespace(prefix)
    
    pages = self.site.allpages(prefix=prefix_without_ns, namespace=namespace)
    return pages
  
  def versionPages(self, sourceVersion, targetVersion, prefixes = []):
    """Create a new version of given documention set
    
    A documentation set correspond to a collection of pages identified by a
    a <sourceVersion> and a list of prefixes.
    
    By providing:
      sourceVersion = '0.1'
      targetVersion = '0.2'
      prefixes = ['Documentation', 'Template:Documentation']
        
    All pages matching both 'Documentation/0.1*' and 'Template:Documentation/0.1*'
    will be copied into pages having prefixes 'Documentation/0.2' and
    'Template:Documentation/0.2'.
    """
    result = []
    for prefix in prefixes:
      prefix_without_ns = mwclient.page.Page.strip_namespace(prefix)
      sourcePages = self.listPages(os.path.join(prefix_without_ns, sourceVersion))
      for sourcePage in sourcePages:
        sourcePageNamePrefix = os.path.join(prefix, sourceVersion)
        targetPageNamePrefix = os.path.join(prefix, targetVersion)
        targetPageBaseName = re.sub(r'^'+sourcePageNamePrefix+'\/', '', sourcePage.name)
        result.append(self.versionPage(sourceVersion, targetVersion, targetPageBaseName, prefix))
    return result

if __name__ == '__main__':
  import unittest
  suite = unittest.TestLoader().loadTestsFromName('mwdoc_test')
  result = unittest.TextTestRunner(verbosity=2).run(suite)
  
