Mwdoc
=====

Overview
--------

Think of [mwdoc][mwdoc] as a tool that allows to easily version mediawiki pages.

For example, pages like:

    Documentation/0.2/mypage
    Template:Documentation/0.2/mytemplate

... could be automatically created from:

    Documentation/0.1/mypage
    Template:Documentation/0.1/mytemplate


Usage
-----

* Create pages:

``` python
import mwdoc
doc = mwdoc.Documentation('somewhere.org', '/wiki/')
doc.login('john', 'password')
doc.createPage('0.1', 'mypage', 'This is content of my page', 'Documentation')
doc.createPage('0.1', 'mytemplate', 'This is content of my template', 'Template:Documentation')
```


* Version pages from 0.1 to 0.2:

``` python
import mwdoc
doc = mwdoc.Documentation('somewhere.org', '/wiki/')
doc.login('john', 'password')
doc.versionPages('0.1', '0.2', ['Documentation', 'Template:Documentation'])
```


* List pages:

``` python
import mwdoc
doc = mwdoc.Documentation('somewhere.org', '/wiki/')
doc.login('john', 'password')
pages = doc.listPages('Documentation')
for page in pages: print page
templatepages = doc.listPages('Template:Documentation')
for page in templatepages: print page
```

* Delete pages:

``` python
import mwdoc
doc = mwdoc.Documentation('somewhere.org', '/wiki/')
doc.login('john', 'password')
pages = doc.listPages('Documentation')
for page in pages: 
  page.delete()
```

Prerequisites
-------------

* [mwclient][mwclient], the client to [MediaWiki API][mwapi]

 `pip install mwclient`

Installation
------------

* [Download mwdoc.py][mwdoc]

 `wget https://raw.github.com/jcfr/mwdoc/mwdoc/master/mwdoc.py`


Test
----

Do **NOT** run this test against a production installation. We mean it.

The test will create pages, version them and delete them afterward.

To run the test:

```
git clone git://github.com/jcfr/mwdoc && cd $_
pip install -r requirements.txt
python -m unittest test_mwdoc
```

It will then ask for:

* Hostname (e.g `localhost`)
* Path (e.g `/wiki/`)
* Username
* Password


Contributing
------------

Once you've made your great commits:

1. [Fork][fk] mwdoc
2. Create a topic branch - `git checkout -b my_branch`
3. Push to your branch - `git push origin my_branch`
4. Create an [Issue][is] with a link to your branch
5. That's it!


Meta
----

* Code: `git clone git://github.com/jcfr/mwdoc.git`
* Home: <http://jcfr.github.com>
* Bugs: <http://github.com/jcfr/mwdoc/issues>

License
-------

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

[fk]: http://help.github.com/forking/
[is]: http://github.com/jcfr/mwdoc/issues
[mwclient]: http://sourceforge.net/apps/mediawiki/mwclient
[mwapi]: https://www.mediawiki.org/wiki/API
[mwdoc]: https://raw.github.com/jcfr/mwdoc/master/mwdoc/mwdoc.py

