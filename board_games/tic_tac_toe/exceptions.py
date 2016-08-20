"""
Module for All Exception Errors
"""

class InvalidMoveError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
