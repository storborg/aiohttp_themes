Quick Start
===========

Install
-------

Install with pip::

    $ pip install aiohttp_themes


Integrate with an Aiohttp App
-----------------------------

WIP

Add Themes
----------

WIP

Use a Theme
-----------

Configure your application to use a theme, with one of the following methods:

* Specify the ``default_theme`` setting key.
* Add a ``theme_callback`` function.

.. code-block:: python

    def mobile_theme_strategy(request):
        if request.is_mobile and not request.session.get('use_desktop'):
            return 'my-mobile-theme'
        else:
            return 'my-desktop-theme'

    aiohttp_themes.setup(app,
                         ...,
                         theme_callback=mobile_theme_strategy)


Compile Assets
--------------

After configuring your app, call:

.. code-block:: python

    aiohttp_themes.compile(app)
