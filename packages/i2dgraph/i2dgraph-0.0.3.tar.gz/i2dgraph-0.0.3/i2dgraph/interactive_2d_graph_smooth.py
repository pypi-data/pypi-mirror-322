# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class interactive_2d_graph_smooth(Component):
    """An interactive_2d_graph_smooth component.


Keyword arguments:

- id (string; required)

- additionalData (list of dicts; optional)

    `additionalData` is a list of dicts with keys:

    - x (number; optional)

    - y (number; optional)

- additionalDataColor (list of strings; optional)

- data (list of dicts; default [    { x: 50, y: 50 },    { x: 150, y: 100 },    { x: 250, y: 150 },    { x: 350, y: 200 },    { x: 450, y: 250 },    { x: 550, y: 300 },    { x: -100, y: -100 },])

    `data` is a list of dicts with keys:

    - x (number; required)

    - y (number; required)

- height (number; default 500)

- mainDataColor (string; default 'blue')

- smoothingFactor (number; default 0.1)

- smoothingType (string; default "bellcurve")

- width (number; default 500)

- xLabel (string; default "X Axis Label")

- yLabel (string; default "Y Axis Label")"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'i2dgraph'
    _type = 'interactive_2d_graph_smooth'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, width=Component.UNDEFINED, height=Component.UNDEFINED, xLabel=Component.UNDEFINED, yLabel=Component.UNDEFINED, data=Component.UNDEFINED, mainDataColor=Component.UNDEFINED, smoothingType=Component.UNDEFINED, smoothingFactor=Component.UNDEFINED, additionalData=Component.UNDEFINED, additionalDataColor=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'additionalData', 'additionalDataColor', 'data', 'height', 'mainDataColor', 'smoothingFactor', 'smoothingType', 'width', 'xLabel', 'yLabel']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'additionalData', 'additionalDataColor', 'data', 'height', 'mainDataColor', 'smoothingFactor', 'smoothingType', 'width', 'xLabel', 'yLabel']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(interactive_2d_graph_smooth, self).__init__(**args)
