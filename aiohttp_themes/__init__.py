import os.path
import asyncio
import functools
import mimetypes

from aiohttp import web

from .theme import (THEMES_KEY, THEME_STRATEGY_KEY, DEV_RESOURCE_KEY,
                    COMPILED_RESOURCE_KEY, COMPILED_DIR_KEY)


__version__ = '0.0.2'


def make_response(filename, body):
    resp = web.Response()
    resp.encoding = 'utf-8'
    resp.body = body
    resp.content_type = mimetypes.guess_type(filename)[0]
    return resp


async def asset_dev_view(request):
    app = request.app
    theme = app[THEMES_KEY][request.match_info['theme_key']]
    asset_key = request.match_info['asset_key']
    path = request.match_info['path']
    text = theme.serve_development(asset_key, path)
    return make_response(path, text)


async def asset_compiled_view(request):
    app = request.app
    theme = app[THEMES_KEY][request.match_info['theme_key']]
    asset_key = request.match_info['asset_key']
    path = request.match_info['path']
    dir = app[COMPILED_DIR_KEY]
    abspath = os.path.join(dir, theme.key, asset_key, path)
    async with open(abspath, 'rb') as f:
        buf = await f.read()
        return make_response(path, buf)


def setup(app, themes,
          compiled_asset_dir,
          theme_strategy=None,
          before_render_callback=None,
          debug=False):

    theme_instances = {
        theme.key: theme(app, debug=debug)
        for theme in themes
    }

    app[THEMES_KEY] = theme_instances
    app[THEME_STRATEGY_KEY] = theme_strategy
    app[COMPILED_DIR_KEY] = compiled_asset_dir

    if debug:
        resource = app.router.add_resource(
            '/_themes/dev/{theme_key}/{asset_key}/{path:.+}',
            name=DEV_RESOURCE_KEY)
        resource.add_route('GET', asset_dev_view)
    else:
        resource = app.router.add_resource(
            '/_themes/compiled/{theme_key}/{asset_key}/{path:.+}',
            name=COMPILED_RESOURCE_KEY)
        resource.add_route('GET', asset_compiled_view)


def compile(app, compiled_asset_dir):
    theme_instances = app[THEMES_KEY]
    for theme_key, theme in theme_instances.items():
        theme.compile()


def template(template_name):
    def template_inner(f):
        @asyncio.coroutine
        @functools.wraps(f)
        def wrapped(*args):
            if asyncio.iscoroutine(f):
                coro = f
            else:
                coro = asyncio.coroutine(f)
            params = yield from coro(*args)
            request = args[-1]
            themes = request.app[THEMES_KEY]
            theme_strategy = request.app[THEME_STRATEGY_KEY]
            theme = themes[theme_strategy]
            text = theme.render_template(template_name, request, params)

            resp = theme.response_class()
            resp.content_type = 'text/html'
            resp.charset = 'utf-8'
            resp.text = text
            return resp

        return wrapped
    return template_inner
