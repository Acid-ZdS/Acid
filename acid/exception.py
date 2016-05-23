#!/usr/bin/env python3.4
# coding: utf-8


class ParseError(ValueError):
	"""
	Raised when the parser fails to parse the code.
	"""

	def __init__(self, pos, msg):
		self.pos = pos
		self.msg = msg

	def __str__(self):
		return """\
Parser failed to parse the code at {err.pos}:
{err.msg}
""".format(err=self)
