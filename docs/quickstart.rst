Quick Start
===========

Install
-------

Install with pip::

    $ pip install aiohttp_themes


Integrate with an aiohttp App
-----------------------------

.. code-block:: python

    from aiohttp_themes.theme import Theme
    from aiohttp_themes.asset import SASSAsset

    class ExampleTheme(Theme):
        key = 'example'
        assets = {
            'hello.css': SASSAsset('scss/main.scss'),
            'alt.css': SASSAsset('scss/alt/different.scss'),
        }

    aiohttp_themes.setup(app,
                         themes=[ExampleTheme],
                         debug=True,
                         theme_strategy='example',
                         compiled_asset_dir='/tmp/compiled/')


Dynamically Switch Themes
-------------------------

The ``theme_strategy`` argument can be a callable that returns a theme key:

.. code-block:: python

    def mobile_theme_strategy(request):
        if request.is_mobile and not request.session.get('use_desktop'):
            return 'my-mobile-theme'
        else:
            return 'my-desktop-theme'

    aiohttp_themes.setup(app,
                         ...,
                         theme_strategy=mobile_theme_strategy)


Compile Assets
--------------

After configuring your app, call:

.. code-block:: python

    aiohttp_themes.compile(app, compiled_asset_dir=dir)
