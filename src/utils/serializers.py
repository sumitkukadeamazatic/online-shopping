"""
Common serializers' definitions
"""

from rest_framework import serializers


class IntegerListField(serializers.ListField):
    """
    Common class created for array field for integer. No need to write child if this class used.
    """
    child = serializers.IntegerField()
