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


def init():
    app = aiohttp.web.Application()
    app.router.add_route('GET', '/{name}', hello_view)
    app.router.add_route('GET', '/', hello_view)

    aiohttp_themes.setup(app,
                         themes={'light': LightTheme},
                         debug=True,
                         theme_strategy='light',
                         compiled_asset_dir='/var/compiled')
    return app


def serve():
    app = init()
    aiohttp.web.run_app(app)


def compile():
    app = init()
    aiohttp_themes.compile(app)


if __name__ == '__main__':
    serve()
