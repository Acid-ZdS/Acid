#!/usr/bin/env python3.4
# coding: utf-8

from acid.parser import parse


def main(path):
	with open(path) as file:
		print(parse(file.read()))


if __name__ == '__main__':
	# todo: use argparse

	import sys

	path = sys.argv[1]
	main(path)
