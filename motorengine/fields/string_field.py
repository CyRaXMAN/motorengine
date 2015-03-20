#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import six
import collections

from motorengine.fields.base_field import BaseField


class StringField(BaseField):
    '''
    Field responsible for storing text.

    Usage:

    .. testcode:: modeling_fields

        name = StringField(required=True, max_length=255, min_length=1)

    Available arguments (apart from those in `BaseField`):

    * `max_length` - Raises a validation error if the string has amount of characters more than specified
    * `min_length` - Raises a validation error if the string has amount of characters less than specified
    * `choices` - Raises a validation error if the string not in specified choices
    * `regex` - Raises a validation error if the string does not match specified regex
    '''

    def __init__(self, max_length=None, min_length=None, choices=None, regex=None, *args, **kw):
        super(StringField, self).__init__(*args, **kw)
        self.max_length = max_length
        self.min_length = min_length
        self.choices = choices
        self.regex = regex

    def validate(self, value):
        if value is None:
            return True

        if not isinstance(value, six.string_types):
            return False

        if self.max_length is not None and len(value) > self.max_length:
            return False

        if self.min_length is not None and len(value) < self.min_length:
            return False

        if self.regex is not None:
            try:
                regex = re.compile(self.regex)
                if not regex.match(value):
                    return False
            except re.error as err:
                raise ValueError("Invalid regex: %s" % err)

        if self.choices is not None:
            if not isinstance(self.choices, collections.Iterable):
                raise ValueError("'choices' must be an iterable")
            if value not in self.choices:
                return False

        return True

    def is_empty(self, value):
        return value is None or value == ""
