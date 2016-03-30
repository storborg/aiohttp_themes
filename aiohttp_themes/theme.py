import os.path
import inspect

from mako.lookup import TemplateLookup
from aiohttp.web import Response


THEMES_KEY = 'aiohttp_themes.themes'
THEME_STRATEGY_KEY = 'aiohttp_themes.default_theme'


class Theme:
    response_class = Response
    template_dir = 'templates'
    static_dir = 'static'

    def __init__(self, app, debug=False):
        self.app = app
        self.debug = debug
        template_dir = self.qualify_path(self.template_dir)
        self.lookup = TemplateLookup(
            directories=[template_dir],
            input_encoding='utf-8',
            output_encoding='utf-8',
            default_filters=['decode.utf8'],
        )

    @classmethod
    def qualify_path(cls, path):
        theme_file = os.path.abspath(inspect.getfile(cls))
        return os.path.join(os.path.dirname(theme_file), path)

    def asset_tag(self, key, **kw):
        asset = self.assets[key]
        if self.debug:
            resource = self.app.router.named_resources()['aiohttp_themes.dev']
            url = resource.url(parts={
                'theme': self.key,
                'filename': key,
            })
            return asset.tag_development(url, **kw)
        else:
            raise NotImplementedError

    def serve_asset(self, key, debug):
        asset = self.assets[key]
        return asset.serve()

    def populate_template_vars(self, request, params):
        params.update({
            'request': request,
            'theme': self,
        })

    def render_template(self, template_name, request, params):
        self.populate_template_vars(request, params)
        templ = self.lookup.get_template(template_name)
        return templ.render_unicode(**params)
