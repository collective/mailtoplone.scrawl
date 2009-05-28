Introduction
============

We need manager role for this test::

    >>> self.setRoles(('Manager',))


Configure Folder for Blog Entries
---------------------------------

We use a standard Folder for dropping the emails in::

    >>> self.portal.invokeFactory('Folder', 'blog_entries')
    'blog_entries'
    >>> blog_entries = self.portal.blog_entries

To enable MailDropbox functionality, we equip the 
folder with an additional marker interface::

    >>> from zope.interface import alsoProvides
    >>> from mailtoplone.scrawl.interfaces import IScrawlMailDropBoxMarker
    >>> alsoProvides(blog_entries, IScrawlMailDropBoxMarker)

mailtoplone uses a more generic interface IMailDropBox, to adapt the
context, we use that to call drop::

    >>> from mailtoplone.base.interfaces import IMailDropBox
    >>> IMailDropBox(blog_entries).drop("Subject: my first blog entry")

As result, we wexpect a single blog entry, with the title, id set 
according to the email's subject::
    >>> blog_entries.objectIds()
    ['my-first-blog-entry']
    >>> blog_entry = blog_entries.listFolderContents()[0]
    >>> blog_entry.title
    u'my first blog entry'
    >>> blog_entry.portal_type
    'Blog Entry'
