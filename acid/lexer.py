#!/usr/bin/env python3.4
# coding: utf-8

import re
from enum import Enum

from acid.types import SourcePos
from acid.exception import ParseError


class TokenType(Enum):
	def __init__(self, pattern):
		self.regex = re.compile(pattern)

	LAMBDA = r'lambda'
	LPAREN, RPAREN = r'\(', r'\)'
	FLOAT_LITERAL = r'\d+\.\d+'
	INT_LITERAL = r'\d+'
	ATOM = r"[\w+\-'*/:,$<>=~#&|@ç^_%!?.]+"
	WHITESPACE = r'\s+'


class Token:
	def __init__(self, type, value, pos):
		self.type = type
		self.value = value
		self.pos = pos

	def __repr__(self):
		fmt = 'Token(type={tok.type}, value={tok.value!r}, pos={tok.pos!s})'
		return fmt.format(tok=self)


def tokenize(code):
	remaining = code
	cursor = SourcePos(line=1, column=1)

	while remaining:
		for token_type in TokenType:
			match = token_type.regex.match(remaining)

			if match is not None:
				remaining = remaining[match.end():]

				if token_type is not TokenType.WHITESPACE:
					value = match.group(0)
					cursor.feed(value)
					pos = cursor.copy()
					yield Token(token_type, value, pos)

				break
		else:
			raise ParseError(pos, "Failed to tokenize code")
