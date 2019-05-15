# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class SpacetimegisException(Exception):
    status = 500


class SpacetimegisTimeoutException(SpacetimegisException):
    pass


class SpacetimegisSecurityException(SpacetimegisException):
    pass


class MetricPermException(SpacetimegisException):
    pass


class NoDataException(SpacetimegisException):
    status = 400


class NullValueException(SpacetimegisException):
    status = 400


class SpacetimegisTemplateException(SpacetimegisException):
    pass


class SpatialException(SpacetimegisException):
    pass
