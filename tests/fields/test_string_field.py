#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preggy import expect

from motorengine import StringField
from tests import AsyncTestCase


class TestStringField(AsyncTestCase):
    def test_create_string_field(self):
        field = StringField(db_field="test", max_length=200)

        expect(field.db_field).to_equal("test")
        expect(field.max_length).to_equal(200)

    def test_validate_enforces_strings(self):
        field = StringField(max_length=5)

        expect(field.validate(1)).to_be_false()

    def test_validate_enforces_maxlength(self):
        field = StringField(max_length=5)

        expect(field.validate("-----")).to_be_true()
        expect(field.validate("-----" * 2)).to_be_false()

    def test_validate_enforces_minlength(self):
        field = StringField(min_length=5)

        expect(field.validate("------")).to_be_true()
        expect(field.validate("----")).to_be_false()

    def test_is_empty(self):
        field = StringField()

        expect(field.is_empty(None)).to_be_true()
        expect(field.is_empty("")).to_be_true()
        expect(field.is_empty("123")).to_be_false()

    def test_validate_only_if_not_none(self):
        field = StringField(required=False)

        expect(field.validate(None)).to_be_true()

    def test_choice(self):
        field = StringField(choices=["one", "two", "three"])

        expect(field.validate("one")).to_be_true()
        expect(field.validate("four")).to_be_false()

    def test_invalid_choice_type(self):
        try:
            StringField(choices=1).validate("a")
        except ValueError as err:
            expect(err).to_have_an_error_message_of("'choices' must be an iterable")
        else:
            expect.not_to_be_here()

    def test_empty(self):
        field = StringField(required=True)

        expect(field.validate(None)).to_be_true()

    def test_valid_regex(self):
        field = StringField(regex="[a-z0-9]+")

        expect(field.validate("test1")).to_be_true()
        expect(field.validate("Test1")).to_be_false()

    def test_invalid_regex(self):
        try:
            StringField(regex='][').validate('a')
        except ValueError as err:
            expect(err).to_have_an_error_message_of("Invalid regex: unexpected end of regular expression")
        else:
            expect.not_to_be_here()

