#################
Release Checklist
#################

#. Is CI completing successfully?
#. Are localizations up-to-date? ::

    $ make django/makemessages

   Check the modifications of the language files, e.g.
   :source:`calingen/locale/de/django.po`.

#. Bump version in :source:`calingen/__init__.py`
#. Merge into ``main`` and push ::

    $ git checkout main
    $ git merge --no-ff development
    $ git tag -a [VERSION] "Release: [VERSION]"
    $ git push --follow-tags origin main
