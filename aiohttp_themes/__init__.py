import asyncio
import functools

from aiohttp import web

from .theme import THEMES_KEY, THEME_STRATEGY_KEY


__version__ = '0.0.1.dev'


def make_response(filename, text):
    resp = web.Response()
    resp.encoding = 'utf-8'
    resp.text = text
    if filename.endswith('.css'):
        resp.content_type = 'text/css'
    elif filename.endswith('.js'):
        resp.content_type = 'text/javascript'
    else:
        resp.content_type = 'text/plain'

    return resp


async def asset_dev_view(request):
    app = request.app
    theme = app[THEMES_KEY][request.match_info['theme']]
    filename = request.match_info['filename']
    text = theme.serve_asset(filename, debug=True)
    return make_response(filename, text)


async def asset_compiled_view(request):
    raise NotImplementedError


def setup(app, themes,
          compiled_asset_dir,
          theme_strategy=None,
          before_render_callback=None,
          debug=False):

    theme_instances = {
        key: theme(app, debug=debug)
        for key, theme in themes.items()
    }

    app[THEMES_KEY] = theme_instances
    app[THEME_STRATEGY_KEY] = theme_strategy

    if debug:
        resource = app.router.add_resource(
            '/_themes/dev/{theme}/{filename:.+}',
            name='aiohttp_themes.dev')
        resource.add_route('GET', asset_dev_view)
    else:
        raise NotImplementedError


def compile(themes, compiled_asset_dir):
    raise NotImplementedError


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
