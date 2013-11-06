django-xheditor
===============

xheditor: http://xheditor.com/

xhtml editor wrapped for django html content editing.

Warning
=======

official xheditor can only use jQuery 1.4.4 now.

Usage
=====

Please see the xhsample project for usage.

modify this line of manage.py in xhsample project:

    sys.path.insert(0,'/path/to/django-xheditor')

then:

    manage.py syncdb
    manage.py runserver

then open your browser, visit admin to login:

    http://localhost:8000/admin/

after you'v logged in, try to add News in admin.

    http://localhost:8000/admin/news/news/add/

or you can add a news at frontend, just visit:

    http://localhost:8000/news/post/

