#################
Release Checklist
#################

#. Is CI completing successfully?
#. If changes to the app's models were performed: ::

    $ make django django_command="squashmigrations calingen [from] [to]"

#. Are localizations up-to-date? ::

    $ make django/makemessages

   Check the modifications of the language files, e.g.
   :source:`calingen/locale/de/LC_MESSAGES/django.po`.

#. Bump version in :source:`calingen/__init__.py`
#. Merge into ``main`` and push ::

    $ git checkout main
    $ git merge --no-ff development
    $ git tag -a [VERSION] "Release: [VERSION]"
    $ git push --follow-tags origin main
