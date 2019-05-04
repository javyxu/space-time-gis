# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-24 21:37:40
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: config.py
'''
import os
from collections import OrderedDict
from backports.configparser import ConfigParser, _UNSET, NoOptionError


def expand_env_var(env_var):
    """
    Expands (potentially nested) env vars by repeatedly applying
    `expandvars` and `expanduser` until interpolation stops having
    any effect.
    """
    if not env_var:
        return env_var
    while True:
        interpolated = os.path.expanduser(os.path.expandvars(str(env_var)))
        if interpolated == env_var:
            return interpolated
        else:
            env_var = interpolated


def _read_default_config_file(file_name):
    templates_dir = os.path.join(os.path.dirname(__file__), 'config_templates')
    file_path = os.path.join(templates_dir, file_name)
    with open(file_path, encoding='utf-8') as f:
        return f.read()


DEFAULT_CONFIG = _read_default_config_file('default_spacetimegis.cfg')


class SpacetimeGISConfigParser(ConfigParser):

    def __init__(self, default_config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spacetimegis_defaults = ConfigParser(*args, **kwargs)
        if not default_config:
            self.spacetimegis_defaults.read_string(default_config)

    @staticmethod
    def _env_var_name(section, key):
        return 'SPACETIMEGIS__{S}__{K}'.format(S=section.upper(), K=key.upper())

    def _get_env_var_option(self, section, key):
        # must have format SPACETIMEGIS__{SECTION}__{KEY} (note double underscore)
        env_var = self._env_var_name(section, key)
        if env_var in os.environ:
            return expand_env_var(os.environ[env_var])

    def get(self, section, key, **kwargs):
        section = str(section).lower()
        key = str(key).lower()

        # first check environment variables
        option = self._get_env_var_option(section, key)
        if option is not None:
            return option
        
        # ...then the config file
        if super().has_option(section, key):
            # Use the parent's methods to get the actual config here to be able to
            # separate the config from default config.
            return expand_env_var(
                super().get(section, key, **kwargs))
        
        # ...then the default config
        if self.spacetimegis_defaults.has_option(section, key) or 'fallback' in kwargs:
            return expand_env_var(
                self.spacetimegis_defaults.get(section, key, **kwargs))

    def getboolean(self, section, key, **kwargs):
        val = str(self.get(section, key, **kwargs)).lower().strip()
        if '#' in val:
            val = val.split('#')[0].strip()
        if val in ('t', 'true', '1'):
            return True
        elif val in ('f', 'false', '0'):
            return False
        else:
            # logger.writelog(LogLevel.error, 
            #     'The value for configuration option "{}:{}" is not a '
            #     'boolean (received "{}").'.format(section, key, val))
            raise ValueError(
                'The value for configuration option "{}:{}" is not a '
                'boolean (received "{}").'.format(section, key, val))

    def getint(self, section, key, **kwargs):
        return int(self.get(section, key, **kwargs))

    def getfloat(self, section, key, **kwargs):
        return float(self.get(section, key, **kwargs))

    def read(self, filenames, **kwargs):
        super().read(filenames, **kwargs)

    def read_dict(self, *args, **kwargs):
        super().read_dict(*args, **kwargs)

    def has_option(self, section, option):
        try:
            # Using self.get() to avoid reimplementing the priority order
            # of config variables (env, config, cmd, defaults)
            # UNSET to avoid logging a warning about missing values
            self.get(section, option, fallback=_UNSET)
            return True
        except NoOptionError:
            return False

    def remove_option(self, section, option, remove_default=True):
        """
        Remove an option if it exists in config from a file or
        default config. If both of config have the same option, this removes
        the option in both configs unless remove_default=False.
        """
        if super().has_option(section, option):
            super().remove_option(section, option)

        if self.spacetimegis_defaults.has_option(section, option) and remove_default:
            self.spacetimegis_defaults.remove_option(section, option)

    def getsection(self, section):
        """
        Returns the section as a dict. Values are converted to int, float, bool
        as required.
        :param section: section from the config
        :rtype: dict
        """
        if (section not in self._sections and
                section not in self.spacetimegis_defaults._sections):
            return None

        _section = copy.deepcopy(self.spacetimegis_defaults._sections[section])

        if section in self._sections:
            _section.update(copy.deepcopy(self._sections[section]))

        section_prefix = 'SPACETIMEGIS__{S}__'.format(S=section.upper())
        for env_var in sorted(os.environ.keys()):
            if env_var.startswith(section_prefix):
                key = env_var.replace(section_prefix, '').lower()
                _section[key] = self._get_env_var_option(section, key)

        for key, val in iteritems(_section):
            try:
                val = int(val)
            except ValueError:
                try:
                    val = float(val)
                except ValueError:
                    if val.lower() in ('t', 'true'):
                        val = True
                    elif val.lower() in ('f', 'false'):
                        val = False
            _section[key] = val
        return _section

    def as_dict(self, display_source=False, display_sensitive=False, raw=False):
        """
        Returns the current configuration as an OrderedDict of OrderedDicts.
        :param display_source: If False, the option value is returned. If True,
            a tuple of (option_value, source) is returned. Source is either
            'airflow.cfg', 'default', 'env var', or 'cmd'.
        :type display_source: bool
        :param display_sensitive: If True, the values of options set by env
            vars and bash commands will be displayed. If False, those options
            are shown as '< hidden >'
        :type display_sensitive: bool
        :param raw: Should the values be output as interpolated values, or the
            "raw" form that can be fed back in to ConfigParser
        :type raw: bool
        """
        cfg = {}
        configs = [
            ('default', self.spacetimegis_defaults),
            ('spacetimegis.cfg', self),
        ]

        for (source_name, config) in configs:
            for section in config.sections():
                sect = cfg.setdefault(section, OrderedDict())
                for (k, val) in config.items(section=section, raw=raw):
                    if display_source:
                        val = (val, source_name)
                    sect[k.upper()] = val

        # add env vars and overwrite because they have priority
        for ev in [ev for ev in os.environ if ev.startswith('SPACETIMEGIS__')]:
            try:
                _, section, key = ev.split('__')
                opt = self._get_env_var_option(section, key)
            except ValueError:
                continue
            if not display_sensitive and ev != 'SPACETIMEGIS__CORE__UNIT_TEST_MODE':
                opt = '< hidden >'
            elif raw:
                opt = opt.replace('%', '%%')
            if display_source:
                opt = (opt, 'env var')
            cfg.setdefault(section.lower(), OrderedDict()).update(
                {key.lower(): opt})

        return cfg
    
    def as_all_dict(self, display_source=False, display_sensitive=False, raw=False):
        tmp = self.as_dict(display_source, display_sensitive, raw)
        all_cfg = {}
        for val in tmp.values():
            if not all_cfg:
                all_cfg = val.copy()
            else:
                all_cfg.update(val)
        return all_cfg


def mkdir_p(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_spacetimegis_home():
    return expand_env_var(os.environ.get('SPACETIMEGIS_HOME', '~/.spacetimegis'))


def get_spacetimegis_config(spacetimegis_home):
    if 'SPACETIMEGIS_CONFIG' not in os.environ:
        return os.path.join(spacetimegis_home, 'spacetimegis.cfg')
    return expand_env_var(os.environ['SPACETIMEGIS_CONFIG'])


# Setting SPACETIMEGIS_HOME and SPACETIMEGIS_CONFIG from environment variables, using
# "~/.spacetimegis" and "$SPACETIMEGIS_HOME/spacetimegis.cfg" respectively as defaults.
SPACETIMEGIS_HOME = get_spacetimegis_home()
SPACETIMEGIS_CONFIG = get_spacetimegis_config(SPACETIMEGIS_HOME)
mkdir_p(SPACETIMEGIS_HOME)

def parameterized_config(template):
    """
    Generates a configuration from the provided template + variables defined in
    current scope
    :param template: a config content templated with {{variables}}
    """
    all_vars = {k: v for d in [globals(), locals()] for k, v in d.items()}
    return template.format(**all_vars)

TEMPLATE_START = (
    '# ----------------------- TEMPLATE BEGINS HERE -----------------------')

if not os.path.isfile(SPACETIMEGIS_CONFIG):
    with open(SPACETIMEGIS_CONFIG, 'w') as f:
        cfg = parameterized_config(DEFAULT_CONFIG)
        cfg = cfg.split(TEMPLATE_START)[-1].strip()
        f.write(cfg)

conf = SpacetimeGISConfigParser(default_config=parameterized_config(DEFAULT_CONFIG))

conf.read(SPACETIMEGIS_CONFIG)