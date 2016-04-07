import sass
import os.path


default_sentinel = object()


class SafeLiteral:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    __html__ = __str__


class Asset:
    pass


class SASSAsset(Asset):
    def __init__(self, relpath, basename='file.css'):
        self.relpath = relpath
        self.basename = basename

    def __repr__(self):
        return '<SASSAsset %s>' % self.relpath

    def tag_development(self, asset_key, theme):
        url = theme.make_url(asset_key, self.basename, debug=True)
        return SafeLiteral('<link rel="stylesheet" href="%s">' % url)

    def _compile_sass(self, theme):
        localpath = os.path.join(theme.static_dir, self.relpath)
        abspath = theme.expand_fs_path(localpath)
        return sass.compile(filename=abspath)

    def compile(self, asset_key, theme):
        compiled = self._compile_sass(theme)
        filename = theme.write_compiled(asset_key, self.basename, compiled)
        url = theme.make_url(asset_key, filename, debug=False)
        return SafeLiteral('<link rel="stylesheet" href="%s">' % url)

    def serve_development(self, key, theme, path):
        return self._compile_sass(theme).encode('utf-8')


class RequireJSAsset(Asset):
    def __init__(self, relpath,
                 requirejs_path='js/require.js',
                 requirejs_config_path=None):
        self.relpath = relpath
        self.requirejs_path = requirejs_path
        self.requirejs_config_path = requirejs_config_path

    def __repr__(self):
        return '<RequireJSAsset %s>' % self.relpath

    def tag_development(self, asset_key, theme):
        if self.requirejs_config_path:
            config_url = theme.make_url(asset_key, self.requirejs_config_path,
                                        debug=True)
            config_tag = '<script src="%s"></script>' % config_url
        else:
            config_tag = ''
        requirejs_url = theme.make_url(asset_key, self.requirejs_path,
                                       debug=True)
        main_url = theme.make_url(asset_key, self.relpath, debug=True)
        main_tag = '<script data-main="%s" src="%s"></script>' % (
            main_url, requirejs_url)
        return SafeLiteral(config_tag + main_tag)

    def compile(self, key, theme):
        raise NotImplementedError

    def serve_development(self, key, theme, relpath):
        localpath = os.path.join(theme.static_dir, relpath)
        abspath = theme.expand_fs_path(localpath)
        with open(abspath, 'rb') as f:
            return f.read()
