import unittest
import os
from mwdoc import Documentation
Documentation.VERBOSE = False
  
class TestDocumentation(unittest.TestCase):
  
  def setUp(self):
    self.host = 'localhost'
    self.path = '/mediawiki-1.15.1/'
    self.user = 'mwdoc';
    self.password = 'password'
    self.prefix = 'Documentation'
  
  def test_login(self):
    doc = Documentation(self.host, self.path)
    doc.login(self.user, self.password)
  
  def test_createPage(self):
    doc = Documentation(self.host, self.path)
    doc.login(self.user, self.password)
    
    for pagename in ['Page1', 'Page2', 'Page3']:
      self.assertTrue(doc.createPage('0.1', pagename, 'This is page %s' % pagename, self.prefix))
      
  def test_createPageAsTemplate(self):
    doc = Documentation(self.host, self.path)
    doc.login(self.user, self.password)

    for pagename in ['template1', 'template2']:
      self.assertTrue(doc.createPage('0.1', pagename, 'This is page %s' % pagename, 'Template:' + self.prefix))
  
  def test_listPages(self):
    doc = Documentation(self.host, self.path)
    doc.login(self.user, self.password)
    
    pagename = 'testlistPages'
    version = '0.1'
    self.assertTrue(doc.createPage(version, pagename, 'This is page %s' % pagename, self.prefix))
    
    pages = doc.listPages(os.path.join(self.prefix, version))
    for page in pages:
      self.assertFalse(pages.count > 1)
      self.assertEqual(page.name, os.path.join(self.prefix, version, pagename))
    self.assertEqual(pages.count, 1)
    
  def test_listPagesAsTemplate(self):
    doc = Documentation(self.host, self.path)
    doc.login(self.user, self.password)
    
    templatePrefix = 'Template:' + self.prefix
    pagename = 'testlistPagesAsTemplate'
    version = '0.1'
    self.assertTrue(doc.createPage(version, pagename, 'This is page %s' % pagename, templatePrefix))

    pages = doc.listPages(os.path.join(templatePrefix, version))
    for page in pages:
      self.assertFalse(pages.count > 1)
      self.assertEqual(page.name, os.path.join(templatePrefix, version, pagename))
    self.assertEqual(pages.count, 1)
          
  def test_versionPages(self):
    doc = Documentation(self.host, self.path)
    doc.login(self.user, self.password)
    
    sourceVersion = '0.1'
    for pagename in ['Page1', 'Page2', 'Page3']:
      doc.createPage(sourceVersion, pagename, 'This is page %s' % pagename, self.prefix)
    
    targetVersion = '0.2'
    result = doc.versionPages(sourceVersion, targetVersion, [self.prefix])
    self.assertFalse(False in result)
      
  def test_versionPagesAsTemplate(self):
    doc = Documentation(self.host, self.path)
    doc.login(self.user, self.password)
    
    templatePrefix = 'Template:' + self.prefix
      
    sourceVersion = '0.1'
    for pagename in ['template1', 'template2']:
      doc.createPage(sourceVersion, pagename, 'This is page %s' % pagename, templatePrefix)
      
    targetVersion = '0.2'
    result = doc.versionPages(sourceVersion, targetVersion, [templatePrefix])
    self.assertFalse(False in result)

  def tearDown(self):
    doc = Documentation(self.host, self.path)
    doc.login(self.user, self.password)

    pages = doc.listPages(self.prefix)
    for p in pages: 
      p.delete()
      
    pages = doc.listPages(self.prefix, Documentation.NS_TEMPLATE)
    for p in pages:
      p.delete()
