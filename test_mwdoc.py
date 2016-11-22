# -*- coding: utf-8 -*-

import unittest
import random
import getpass
from mwdoc import Documentation
Documentation.VERBOSE = True

class TestDocumentation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.host = raw_input('Hostname: ')
        cls.path = raw_input('Path: ')
        cls.user = raw_input('Username: ')
        cls.password = getpass.getpass('Password: ')
        chars = 'abcdedfhijklmnopqrstuvwxyz'
        cls.prefix = 'D' + ''.join(random.choice(chars) for x in range(10))

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

        pages = doc.listPages('/'.join((self.prefix, version)))
        for page in pages:
            self.assertFalse(pages.count > 1)
            self.assertEqual(page.name, '/'.join((self.prefix, version, pagename)))
        self.assertEqual(pages.count, 1)

    def test_listPagesAsTemplate(self):
        doc = Documentation(self.host, self.path)
        doc.login(self.user, self.password)

        templatePrefix = 'Template:' + self.prefix
        pagename = 'testlistPagesAsTemplate'
        version = '0.1'
        self.assertTrue(doc.createPage(version, pagename, 'This is page %s' % pagename, templatePrefix))

        pages = doc.listPages('/'.join((templatePrefix, version)))
        for page in pages:
            self.assertFalse(pages.count > 1)
            self.assertEqual(page.name, '/'.join((templatePrefix, version, pagename)))
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

