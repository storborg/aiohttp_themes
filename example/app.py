import sys

import aiohttp
import aiohttp.web
import aiohttp_themes

from aiohttp_themes.theme import Theme
from aiohttp_themes.asset import SASSAsset, RequireJSAsset


@aiohttp_themes.template('index.html')
async def hello_view(request):
    name = request.match_info.get('name', 'Anonymous')
    return {'name': name}


class LightTheme(Theme):
    key = 'light'
    assets = {
        'main.css': SASSAsset('scss/main.scss'),
        'main.js': RequireJSAsset('js/main.js'),
    }


def init(debug):
    app = aiohttp.web.Application()
    app.router.add_route('GET', '/{name}', hello_view)
    app.router.add_route('GET', '/', hello_view)

    aiohttp_themes.setup(app,
                         themes=[LightTheme],
                         debug=debug,
                         theme_strategy='light',
                         compiled_asset_dir='/tmp/compiled')
    return app


def serve(debug):
    app = init(debug)
    aiohttp.web.run_app(app)


def compile():
    app = init(debug=False)
    aiohttp_themes.compile(app, compiled_asset_dir='/tmp/compiled')


if __name__ == '__main__':
    if (len(sys.argv) > 1) and (sys.argv[1] == 'compile'):
        print("Compiling...")
        compile()
    elif (len(sys.argv) > 1) and (sys.argv[1] == 'production'):
        serve(debug=False)
    else:
        serve(debug=True)
