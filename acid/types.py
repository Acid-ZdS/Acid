#!/usr/bin/env python3.4
# coding: utf-8

"""
Defines some types that are used by several modules in the package.
"""


class SourcePos:
	"""
	Represents a position in a file.
	"""

	def __init__(self, line, column):
		self.line, self.column = line, column

	def __repr__(self):
		return 'SourcePos(line={pos.line}, col={pos.column})'.format(pos=self)

	def __str__(self):
		return 'line {pos.line}, column {pos.column}'.format(pos=self)

	def feed(self, string):
		for char in string:
			if char == '\n':
				self.line += 1
				self.column = 1
			else:
				self.column += 1

	def copy(self):
		return SourcePos(line=self.line, column=self.column)
