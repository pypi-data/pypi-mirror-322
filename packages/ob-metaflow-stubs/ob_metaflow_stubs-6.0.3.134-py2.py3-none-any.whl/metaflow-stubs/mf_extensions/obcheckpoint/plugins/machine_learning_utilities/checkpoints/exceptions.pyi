######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.7.1+obcheckpoint(0.1.6);ob(v1)                                                    #
# Generated on 2025-01-23T20:10:29.036473                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class CheckpointNotAvailableException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class CheckpointException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

