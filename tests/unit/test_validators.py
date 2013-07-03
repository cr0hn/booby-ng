# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from doublex import Mimic, Stub
from nose.tools import assert_raises, assert_raises_regexp

from booby import validators, fields, models, errors


class TestRequired(object):
    def test_when_value_is_none_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'is required'):
            self.validator.validate(None)

    def test_when_value_is_not_none_then_does_not_raise(self):
        self.validator.validate('foo')

    def setup(self):
        self.validator = validators.Required()


class TestIn(object):
    def test_when_value_is_not_in_choices_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, "should be in \[u?'foo', u?'bar'\]"):
            self.validator.validate('baz')

    def test_when_value_is_in_choices_then_does_not_raise(self):
        self.validator.validate('bar')

    def setup(self):
        self.validator = validators.In(['foo', 'bar'])


class StringMixin(object):
    def test_when_value_is_not_string_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be a string'):
            self.validator.validate(1)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator.validate(None)


class TestString(StringMixin):
    def test_when_value_is_a_string_then_does_not_raise(self):
        self.validator.validate('foo')

    def test_when_value_is_unicode_then_does_not_raise(self):
        self.validator.validate('foo')

    def setup(self):
        self.validator = validators.String()


class TestInteger(object):
    def test_when_value_is_not_an_integer_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be an integer'):
            self.validator.validate('foo')

    def test_when_value_is_an_integer_then_does_not_raise(self):
        self.validator.validate(1)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator.validate(None)

    def setup(self):
        self.validator = validators.Integer()


class TestFloat(object):
    def test_when_value_is_not_a_float_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be a float'):
            self.validator.validate('foo')

    def test_when_value_is_a_float_then_does_not_raise(self):
        self.validator.validate(1.0)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator.validate(None)

    def setup(self):
        self.validator = validators.Float()


class TestBoolean(object):
    def test_when_value_is_not_a_boolean_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be a boolean'):
            self.validator.validate('foo')

    def test_when_value_is_a_boolean_then_does_not_raises(self):
        self.validator.validate(False)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator.validate(None)

    def setup(self):
        self.validator = validators.Boolean()


class TestModel(object):
    def test_when_value_is_not_instance_of_model_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, "should be an instance of 'User'"):
            self.validator.validate(object())

    def test_when_model_validate_raises_validation_error_then_raises_validation_error(self):
        with Mimic(Stub, User()) as user:
            user.validate().raises(errors.ValidationError())

        with assert_raises(errors.ValidationError):
            self.validator.validate(user)

    def test_when_model_validate_does_not_raise_then_does_not_raise(self):
        self.validator.validate(User())

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator.validate(None)

    def setup(self):
        self.validator = validators.Model(User)


class TestList(object):
    def test_when_value_is_not_a_list_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be a list'):
            self.validator.validate(object())

    def test_when_value_is_none_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be a list'):
            self.validator.validate(None)

    def test_when_value_is_a_list_then_does_not_raise(self):
        self.validator.validate(['foo', 'bar'])

    def test_when_inner_validator_raises_validation_error_then_raises_validation_error(self):
        with Stub() as inner:
            inner.validate('bar').raises(errors.ValidationError('invalid'))

        self.validator = validators.List(Stub(), inner)

        with assert_raises_regexp(errors.ValidationError, 'invalid'):
            self.validator.validate(['foo', 'bar'])

    def setup(self):
        self.validator = validators.List()


class TestEmail(StringMixin):
    def test_when_value_doesnt_match_email_pattern_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be a valid email'):
            self.validator.validate('foo@example')

    def test_when_value_doesnt_have_at_sign_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be a valid email'):
            self.validator.validate('foo%example.com')

    def test_when_value_is_a_valid_email_then_does_not_raise(self):
        self.validator.validate('foo2bar@example.com')

    def setup(self):
        self.validator = validators.Email()


class User(models.Model):
    name = fields.String()
