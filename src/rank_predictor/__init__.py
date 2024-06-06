from logging import NullHandler, getLogger

getLogger(__name__).addHandler(NullHandler())
