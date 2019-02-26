import json

from functools import reduce

INDENT = '  '

def is_scalar(value):
    return not is_list(value) and not is_dict(value)


def is_list(value):
    return isinstance(value, list) or isinstance(value, tuple)


def is_dict(value):
    return isinstance(value, dict)


def dump_scalar(obj):
    return json.dumps(obj)


def dump_list(obj, current_indent=''):
    entries = [dump_obj(value, current_indent + INDENT) for value in obj]

    if len(entries) == 0:
        return '[]'

    values_format = '{indent}{value}'
    output_format = '[\n{values}\n{indent}]'

    output = output_format.format(
        indent=current_indent,
        values=',\n'.join([values_format.format(
            value=entry,
            indent=current_indent + INDENT
        ) for entry in entries])
    )

    return output


def dump_dict(obj, current_indent='', sub_width=None):
    entries = {}

    key_width = None
    if sub_width is not None:
        sub_width = (sub_width[0]-1, sub_width[1])
        if sub_width[0] == 0:
            key_width = sub_width[1]

    for key, value in obj.items():
        if key == ':playthrough':
            sub_keys = [location for sphere_nr, sphere in value.items() for location in sphere]
            sub_width = (2, reduce(lambda acc, entry: max(acc, len(entry)), sub_keys, 0))
        
        entries[dump_scalar(str(key))] = dump_obj(value, current_indent + INDENT, sub_width)

    if key_width is None:
        key_width = reduce(lambda acc, entry: max(acc, len(entry)), entries, 0)

    if len(entries) == 0:
        return '{}'

    if 'item' in obj or 'gossip' in obj:
        values_format = '{key} {value}'
        output_format = '{{{values}}}'
        join_format   = ', '
    else:
        values_format = '{indent}{key:{padding}}{value}'
        output_format = '{{\n{values}\n{indent}}}'
        join_format   = ',\n'

    output = output_format.format(
        indent=current_indent,
        values=join_format.join([values_format.format(
            key='{key}:'.format(key=key), 
            value=value,
            indent=current_indent + INDENT,
            padding=key_width + 2,
        ) for key, value in entries.items()])
    )

    return output


def dump_obj(obj, current_indent='', sub_width=None):
    if is_list(obj):
        return dump_list(obj, current_indent)
    elif is_dict(obj):
        return dump_dict(obj, current_indent, sub_width)
    else:
        return dump_scalar(obj)
