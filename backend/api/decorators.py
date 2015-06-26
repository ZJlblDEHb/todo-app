# -*- encoding: utf-8 -*-


"""
Description.
"""


__author__ = 'ZJlblDEHb'


from httplib import BAD_REQUEST


QUERY_INPUT = 1
JSON_INPUT = 2


CAST_TABLE = {
    int: lambda x: int(x),
    str: lambda x: str(x),
    (tuple, list): lambda x: list(x)
}


class ValidateError(Exception):
    pass


class ValidateField(object):

    def __init__(self, name, field_type):
        self.name = name
        self.field_type = field_type
        self.cast_func = CAST_TABLE.get(self.field_type)
        if self.cast_func is None:
            raise ValidateError("Can't find type '%s' in CAST TABLE." % str(self.field_type))

    def cast_value(self, value):
        if not isinstance(value, self.field_type):
            try:
                return self.cast_func(value)

            except (ValueError, TypeError) as e:
                raise ValidateError("Can't cast value to '%s' type!" % str(self.field_type))

        else:
            return value


class ValidateDecorator(object):

    def __init__(self, request, mandatory=(), optional=(), source=QUERY_INPUT):
        if source not in (QUERY_INPUT, JSON_INPUT):
            raise ValidateError("Unknown source '%s'!" % str(source))

        self.request = request
        self.source = source

        self.fields = {field['name']: ValidateField(**field) for field in mandatory}
        for field in optional:
            self.fields[field['name']] = ValidateField(**field)

        self.mandatory_keys = set(field['name'] for field in mandatory)
        self.optional_keys = set(field['name'] for field in optional)
        self.summary_keys = self.mandatory_keys.union(self.optional_keys)

    def get_source_dict(self):
        if self.source == QUERY_INPUT:
            return self.request.args

        else:
            return self.request.json

    def __call__(self, func):

        def tmp(instance, *args, **kwargs):

            result = {}
            source_dict = self.get_source_dict()
            source_keys = set(source_dict.keys())

            for mandatory_key in self.mandatory_keys:
                if mandatory_key not in source_keys:
                    return "Mandatory key '%s' not found!" % mandatory_key, BAD_REQUEST

            for source_key, source_value in source_dict.iteritems():
                if source_key in self.summary_keys:
                    if source_value is not None:
                        try:
                            result[source_key] = self.fields[source_key].cast_value(source_value)

                        except ValidateError as e:
                            return "Key '%s' has non-convertible value to type '%s'" % (source_key, str(self.fields[source_key].field_type))

                    else:
                        result[source_key] = None

                else:
                    return "Unknown key '%s'!" % source_key, BAD_REQUEST

            return func(instance, result, *args, **kwargs)

        return tmp


def validate(request, mandatory=(), optional=(), source=QUERY_INPUT):
    return ValidateDecorator(request, mandatory, optional, source)