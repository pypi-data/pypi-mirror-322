# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tree(Component):
    """A Tree component.


Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- allowRangeSelection (boolean; optional):
    Determines whether tree nodes range can be selected with click
    when Shift key is pressed, `True` by default.

- aria-* (string; optional):
    Wild card aria attributes.

- bd (string | number; optional):
    Border.

- bg (boolean | number | string | dict | list; optional):
    Background, theme key: theme.colors.

- bga (boolean | number | string | dict | list; optional):
    BackgroundAttachment.

- bgp (string | number; optional):
    BackgroundPosition.

- bgr (boolean | number | string | dict | list; optional):
    BackgroundRepeat.

- bgsz (string | number; optional):
    BackgroundSize.

- bottom (string | number; optional)

- c (boolean | number | string | dict | list; optional):
    Color.

- checkOnSpace (boolean; optional):
    Determines whether tree node should be checked on space key press,
    `False` by default.

- checkboxes (boolean; optional):
    Determines if checkboxes should be rendered, `False` by default.

- checked (list of strings; optional):
    Determines checked nodes as a list of values (note that only
    leaves can be checked), `[]` by default.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds class names to Mantine components.

- clearSelectionOnOutsideClick (boolean; optional):
    Determines whether selection should be cleared when user clicks
    outside of the tree, `False` by default.

- collapsedIcon (a list of or a singular dash component, string or number; optional):
    Collapsed state icon.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data (list of dicts; required):
    Data used to render nodes.

    `data` is a list of dicts with keys:

    - label (a list of or a singular dash component, string or number; required)

    - value (string; required)

    - nodeProps (dict with strings as keys and values of type boolean | number | string | dict | list; optional)

    - children (list of boolean | number | string | dict | lists; optional)

- data-* (string; optional):
    Wild card data attributes.

- display (boolean | number | string | dict | list; optional)

- expandOnClick (boolean; default True):
    Determines whether tree node with children should be expanded on
    click, `True` by default.

- expandOnSpace (boolean; optional):
    Determines whether tree node with children should be expanded on
    space key press, `True` by default.

- expanded (list of strings; optional):
    Determines expanded nodes as a list of values or `'*'` for all,
    `[]` by default.

- expandedIcon (a list of or a singular dash component, string or number; default <AccordionChevron />):
    Expanded state icon.

- ff (boolean | number | string | dict | list; optional):
    FontFamily.

- flex (string | number; optional)

- fs (boolean | number | string | dict | list; optional):
    FontStyle.

- fw (boolean | number | string | dict | list; optional):
    FontWeight.

- fz (number; optional):
    FontSize, theme key: theme.fontSizes.

- h (string | number; optional):
    Height, theme key: theme.spacing.

- hiddenFrom (boolean | number | string | dict | list; optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- iconSide (a value equal to: 'left', 'right', 'none'; default 'left'):
    Side to display expanded/collapsed state icon on, `'left'` by
    default.

- inset (string | number; optional)

- left (string | number; optional)

- levelOffset (string | number; optional):
    Horizontal padding of each subtree level, key of `theme.spacing`
    or any valid CSS value, `'lg'` by default.

- lh (number; optional):
    LineHeight, theme key: lineHeights.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - is_loading (boolean; required):
        Determines if the component is loading or not.

    - prop_name (string; required):
        Holds which property is loading.

    - component_name (string; required):
        Holds the name of the component that is loading.

- lts (string | number; optional):
    LetterSpacing.

- m (number; optional):
    Margin, theme key: theme.spacing.

- mah (string | number; optional):
    MaxHeight, theme key: theme.spacing.

- maw (string | number; optional):
    MaxWidth, theme key: theme.spacing.

- mb (number; optional):
    MarginBottom, theme key: theme.spacing.

- me (number; optional):
    MarginInlineEnd, theme key: theme.spacing.

- mih (string | number; optional):
    MinHeight, theme key: theme.spacing.

- miw (string | number; optional):
    MinWidth, theme key: theme.spacing.

- ml (number; optional):
    MarginLeft, theme key: theme.spacing.

- mod (string | dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- mr (number; optional):
    MarginRight, theme key: theme.spacing.

- ms (number; optional):
    MarginInlineStart, theme key: theme.spacing.

- mt (number; optional):
    MarginTop, theme key: theme.spacing.

- mx (number; optional):
    MarginInline, theme key: theme.spacing.

- my (number; optional):
    MarginBlock, theme key: theme.spacing.

- opacity (boolean | number | string | dict | list; optional)

- p (number; optional):
    Padding, theme key: theme.spacing.

- pb (number; optional):
    PaddingBottom, theme key: theme.spacing.

- pe (number; optional):
    PaddingInlineEnd, theme key: theme.spacing.

- pl (number; optional):
    PaddingLeft, theme key: theme.spacing.

- pos (boolean | number | string | dict | list; optional):
    Position.

- pr (number; optional):
    PaddingRight, theme key: theme.spacing.

- ps (number; optional):
    PaddingInlineStart, theme key: theme.spacing.

- pt (number; optional):
    PaddingTop, theme key: theme.spacing.

- px (number; optional):
    PaddingInline, theme key: theme.spacing.

- py (number; optional):
    PaddingBlock, theme key: theme.spacing.

- right (string | number; optional)

- selectOnClick (boolean; optional):
    Determines whether node should be selected on click, `False` by
    default.

- selected (list of strings; optional):
    Determines selected nodes as a list of values, `[]` by default.

- style (optional):
    Inline style added to root component element, can subscribe to
    theme defined on MantineProvider.

- styles (boolean | number | string | dict | list; optional):
    Mantine styles API.

- ta (boolean | number | string | dict | list; optional):
    TextAlign.

- tabIndex (number; optional):
    tab-index.

- td (string | number; optional):
    TextDecoration.

- top (string | number; optional)

- tt (boolean | number | string | dict | list; optional):
    TextTransform.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- variant (string; optional):
    variant.

- visibleFrom (boolean | number | string | dict | list; optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- w (string | number; optional):
    Width, theme key: theme.spacing."""
    _children_props = ['data[].label', 'expandedIcon', 'collapsedIcon']
    _base_nodes = ['expandedIcon', 'collapsedIcon', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Tree'
    @_explicitize_args
    def __init__(self, allowRangeSelection=Component.UNDEFINED, checkboxes=Component.UNDEFINED, checked=Component.UNDEFINED, checkOnSpace=Component.UNDEFINED, clearSelectionOnOutsideClick=Component.UNDEFINED, data=Component.REQUIRED, expanded=Component.UNDEFINED, expandOnClick=Component.UNDEFINED, expandOnSpace=Component.UNDEFINED, levelOffset=Component.UNDEFINED, selected=Component.UNDEFINED, selectOnClick=Component.UNDEFINED, expandedIcon=Component.UNDEFINED, collapsedIcon=Component.UNDEFINED, iconSide=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, hiddenFrom=Component.UNDEFINED, visibleFrom=Component.UNDEFINED, lightHidden=Component.UNDEFINED, darkHidden=Component.UNDEFINED, mod=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ms=Component.UNDEFINED, me=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, ps=Component.UNDEFINED, pe=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, bd=Component.UNDEFINED, bg=Component.UNDEFINED, c=Component.UNDEFINED, opacity=Component.UNDEFINED, ff=Component.UNDEFINED, fz=Component.UNDEFINED, fw=Component.UNDEFINED, lts=Component.UNDEFINED, ta=Component.UNDEFINED, lh=Component.UNDEFINED, fs=Component.UNDEFINED, tt=Component.UNDEFINED, td=Component.UNDEFINED, w=Component.UNDEFINED, miw=Component.UNDEFINED, maw=Component.UNDEFINED, h=Component.UNDEFINED, mih=Component.UNDEFINED, mah=Component.UNDEFINED, bgsz=Component.UNDEFINED, bgp=Component.UNDEFINED, bgr=Component.UNDEFINED, bga=Component.UNDEFINED, pos=Component.UNDEFINED, top=Component.UNDEFINED, left=Component.UNDEFINED, bottom=Component.UNDEFINED, right=Component.UNDEFINED, inset=Component.UNDEFINED, display=Component.UNDEFINED, flex=Component.UNDEFINED, classNames=Component.UNDEFINED, styles=Component.UNDEFINED, unstyled=Component.UNDEFINED, variant=Component.UNDEFINED, id=Component.UNDEFINED, tabIndex=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'allowRangeSelection', 'aria-*', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'checkOnSpace', 'checkboxes', 'checked', 'className', 'classNames', 'clearSelectionOnOutsideClick', 'collapsedIcon', 'darkHidden', 'data', 'data-*', 'display', 'expandOnClick', 'expandOnSpace', 'expanded', 'expandedIcon', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'iconSide', 'inset', 'left', 'levelOffset', 'lh', 'lightHidden', 'loading_state', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'opacity', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'right', 'selectOnClick', 'selected', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'unstyled', 'variant', 'visibleFrom', 'w']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['id', 'allowRangeSelection', 'aria-*', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'checkOnSpace', 'checkboxes', 'checked', 'className', 'classNames', 'clearSelectionOnOutsideClick', 'collapsedIcon', 'darkHidden', 'data', 'data-*', 'display', 'expandOnClick', 'expandOnSpace', 'expanded', 'expandedIcon', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'iconSide', 'inset', 'left', 'levelOffset', 'lh', 'lightHidden', 'loading_state', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'opacity', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'right', 'selectOnClick', 'selected', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'unstyled', 'variant', 'visibleFrom', 'w']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Tree, self).__init__(**args)
