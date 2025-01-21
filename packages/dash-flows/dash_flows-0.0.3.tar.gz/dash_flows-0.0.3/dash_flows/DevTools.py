# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DevTools(Component):
    """A DevTools component.
DevTools component for displaying debug information about the flow

Keyword arguments:

- nodes (list of dicts; required):
    Array of nodes to display information about.

    `nodes` is a list of dicts with keys:

    - id (string; required)

    - type (string; optional)

- viewport (dict; required):
    Current viewport information including position and zoom level.

    `viewport` is a dict with keys:

    - x (number; required)

    - y (number; required)

    - zoom (number; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'DevTools'
    @_explicitize_args
    def __init__(self, viewport=Component.REQUIRED, nodes=Component.REQUIRED, **kwargs):
        self._prop_names = ['nodes', 'viewport']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['nodes', 'viewport']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['nodes', 'viewport']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DevTools, self).__init__(**args)
