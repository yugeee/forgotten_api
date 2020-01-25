# -*- coding: utf-8 -*-

from pprint import pprint

from cerberus import Validator
from cerberus.errors import BasicErrorHandler

class CustomErrorHandler(BasicErrorHandler):
    """ BasicErrorHandler.message を上書きして日本語化 """
    def __init__(self, tree=None):
        super(CustomErrorHandler, self).__init__(tree)
        # 文言を適宜日本語化してください
        self.messages = {
            0x00: "{0}",
            0x01: "document is missing",
            0x02: "'{field}' 必須項目です。",
            0x03: "unknown field",
            0x04: "'{field}' は必須項目です。",
            0x05: "depends on these values: {constraint}",
            0x06: "{0} must not be present with '{field}'",
            0x21: "'{0}' is not a document, must be a dict",
            0x22: "'{field}' に空文字は無効です。",
            0x23: "null value not allowed",
            0x24: "must be of {constraint} type",
            0x25: "must be of dict type",
            0x26: "length of list should be {constraint}, it is {0}",
            0x27: "min length is {constraint}",
            0x28: "max length is {constraint}",
            0x41: "value does not match regex '{constraint}'",
            0x42: "min value is {constraint}",
            0x43: "max value is {constraint}",
            0x44: "unallowed value {value}",
            0x45: "unallowed values {0}",
            0x46: "unallowed value {value}",
            0x47: "unallowed values {0}",
            0x48: "missing members {0}",
            0x61: "field '{field}' cannot be coerced: {0}",
            0x62: "field '{field}' cannot be renamed: {0}",
            0x63: "field is read-only",
            0x64: "default value for '{field}' cannot be set: {0}",
            0x81: "mapping doesn't validate subschema: {0}",
            0x82: "one or more sequence-items don't validate: {0}",
            0x83: "one or more keys of a mapping  don't validate: {0}",
            0x84: "one or more values in a mapping don't validate: {0}",
            0x85: "one or more sequence-items don't validate: {0}",
            0x91: "one or more definitions validate",
            0x92: "none or more than one rule validate",
            0x93: "no definitions validate",
            0x94: "one or more definitions don't validate",
        }

def validate_post(post):
    schema = {
        'post' : {
            'type' : 'string',
            'required': True,
            'empty': False,
        },
    }
        
    # 拡張したBasicErrorHandlerを指定
    v = Validator(schema, error_handler=CustomErrorHandler())
    
    v.validate(post)

    return v.errors

