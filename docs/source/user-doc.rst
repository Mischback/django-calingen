.. _calingen-user-doc-label:

##################
User Documentation
##################

|calingen| is a pluggable `Django`_  application intended to generate
paper-based calendar pages to be used with analogous calendars. It provides
the means to manage and include (user-provided) events into the generated
calendar pages. Additionally it provides a plugin API with the ability to
provide events, layouts and compilers as external plugins.

.. note::
  Because |calingen| is just a `Django application`_, the actual offered set
  of features is limited by what the project's host choose to offer - or
  specifically: How the project is configured.

If you're hosting |calingen| yourself, you may want to visit the
:ref:`administrator documentation <calingen-admin-doc-label>`. And if you feel
like something important is missing: |calingen| is open source software and
uses `GitHub`_ to host the source code and project management tools, including
the `issue tracker`_. If you want to get your own hands dirty, there is
:ref:`developer documentation <calingen-dev-doc-label>` included aswell.


.. _calingen-user-doc-profile-label:

************
Your Profile
************

Your app-specific profile is tied to your Django user account (that is: the
account you use to log into the website). You may have exactly one profile,
as it serves as the central facility for app-specific settings and reference
for user-provided events.


Choosing External Event Providers
=================================

Your site's administrator may include so called *EventProviders* as plugins
and make them available to users to be selected in their profile.

.. note::
  The original idea of these *EventProviders* was: "Make (national) holidays
  available".

  But the actual plugin interface is really generic. Basically,
  all types of events can be provided by an implementation of the
  :ref:`Event Provider Interface <calingen-dev-doc-plugins-eventprovider-label>`.

On your profile's settings page, you will see a list of available Event
Providers.

You may choose one or several of them by activating the respective checkbox
and hit the button to save your changes.

.. note::
  While you may choose as many of these providers as you like, please be aware
  that the actual generated calendar pages will only include each distinct
  entry once.

  **Example**: If you choose ``ProviderA`` and ``ProviderB``, which both
  include May, 4th as ``"Star Wars Day"`` of type ``"Holiday"``, the day will
  be marked as ``"Star Wars Day"`` one time in the generated output.

  On the other hand, if ``ProviderA`` includes May, 4th as ``"Star Wars Day"``
  and ``ProviderB`` includes May, 4th as ``"May the Force be with you!"``,
  both of them will be included in your generated output.

.. important::
  May the Force be with you!


Adding Events
=============

By adding user-defined events to your profile, you may include them in your
generated output.

Hit the ``Add Event`` page and fill out the presented form, hit the button to
save your changes. You're done. The event will now be included in your
calendar pages, once you generate them.

Event Category
--------------

As of now, |calingen| includes only two categories of events to choose from:

- Holidays
- Annual Anniversaries

Internally, both are treated identically: They are assumed to be events with
a *yearly recurrence*. However, *layouts* may choose to handle these types
differently, i.e. by putting them on different spots in the generated output.

.. note::
  Adding more different types of events is on the developer's ToDo list.

Event Title
-----------

Most likely, this is what will be included in the generated output.

The maximum length is capped at 50 characters. This is a design choice to
force user's to provide meaningful titles to their events, that will actually
fit into generated outputs of any type/format/orientation.

Event Start
-----------

.. note::
  Don't be irritated by the name ``start``. As stated above, adding more types
  of events is on the developer's ToDo list, including a generalized type to
  allow any reccurence of events. Meaning: in a future release there may the
  an ``Event End`` option to events.

This is actually the date/time of the event.

For the event types ``Holiday`` and ``Annual Anniversary``, the time-part of
this may be left empty.


.. _calingen-user-doc-generate-inlays-label:

************************
Generate Calendar Inlays
************************

This is what you came for, isn't it?

Ok, let's get this straight: This documentation will most likely not answer
all questions regarding the generation of calendar inlays, as this is the part
of the application that may differ widely, based on the actual installed
layouts and the provided compiler.

These parts are configured / provided by the app's deployment in the context
of a Django project and are highly customizable by the administrator.


General Description
===================

Choose a Layout and Select the Year
-----------------------------------

Once you :ref:`configured your profile <calingen-user-doc-profile-label>`, head
to **INSERT SOMETHING HERE**.

You will be presented with a form, containing a field to enter your desired
``target_year`` and a list of available layouts. Pick one and proceed.

.. warning::
  The availability of layouts is dependent on the Django project's
  configuration. Your administrator will choose, which layouts are provided
  by activating them in the project's settings.

.. note::
  If you're hosting |calingen| yourself, you may find additional information
  regarding installation and setup of layouts in the
  :ref:`corresponding part <calingen-admin-doc-layouts-label>` of the admin
  documentation.

[Optional] Layout-specific Configuration
----------------------------------------

Layouts may choose to expose certain configuration options to the user. If
your chosen layout provides those options, you are presented with another
form.

User-provided configuration will be skipped automatically, if the chosen
layout doesn't accept user configuration. In this case, you're directly
redirected to the generated output, depending on the project's configured
compiler.

Compilation of the Output
-------------------------

In the background, the application will now fetch your events (user-provided
and plugin-provided), process the selected layout to generate source code for
the compiler and compile the source to generate the actual output.

If you are a non-Tech-person: *This is where the magic happens!* (:

Depending on the compiler, you may be presented with the result directly in
your browser window or a download is provided.

Congratulations, you have completed the whole process of generating calendar
inlays with |calingen|.




.. |calingen| replace:: **django-calingen**
.. _Django: https://djangoproject.com
.. _Django application: https://stackoverflow.com/a/19351042
.. _GitHub: https://github.com/mischback/django-calingen
.. _issue tracker: https://github.com/mischback/django-calingen/issue
