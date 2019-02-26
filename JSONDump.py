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


def dump_dict(obj, current_indent = ''):
    entries = {dump_scalar(str(key)): dump_obj(value, current_indent + INDENT) for key, value in obj.items()}
    only_scalars = reduce(lambda acc, is_scalar_entry: acc and is_scalar_entry, 
        [is_scalar(value) for value in obj.values()], True)
    key_width = reduce(lambda acc, entry: max(acc, len(entry)), entries, 0)

    if only_scalars: 
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


def dump_obj(obj, current_indent = ''):
    if is_list(obj):
        return dump_list(obj, current_indent)
    elif is_dict(obj):
        return dump_dict(obj, current_indent)
    else:
        return dump_scalar(obj)
