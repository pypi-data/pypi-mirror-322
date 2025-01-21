# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class interactive_bar_chart(Component):
    """An interactive_bar_chart component.


Keyword arguments:

- id (string; required)

- additionalData (list of dicts; optional)

    `additionalData` is a list of list of dicts with keys:

    - x (string | number; optional)

    - y (number; optional)s

- additionalDataColor (list of strings; optional)

- data (list of dicts; default [    { x: "cat", y: 50 },    { x: "dog", y: 100 },    { x: "human", y: 150 },    { x: "whale", y: 200 },    { x: "bear", y: 250 },    { x: "chimp", y: 300 },    { x: "Tiger", y: -100 },])

    `data` is a list of dicts with keys:

    - x (string | number; required)

    - y (number; required)

- height (number; default 500)

- mainDataColor (string; default "blue")

- width (number; default 500)

- xLabel (string; default "X Axis Label")

- yLabel (string; default "Y Axis Label")"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'i2dgraph'
    _type = 'interactive_bar_chart'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, width=Component.UNDEFINED, height=Component.UNDEFINED, xLabel=Component.UNDEFINED, yLabel=Component.UNDEFINED, data=Component.UNDEFINED, mainDataColor=Component.UNDEFINED, additionalData=Component.UNDEFINED, additionalDataColor=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'additionalData', 'additionalDataColor', 'data', 'height', 'mainDataColor', 'width', 'xLabel', 'yLabel']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'additionalData', 'additionalDataColor', 'data', 'height', 'mainDataColor', 'width', 'xLabel', 'yLabel']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(interactive_bar_chart, self).__init__(**args)
