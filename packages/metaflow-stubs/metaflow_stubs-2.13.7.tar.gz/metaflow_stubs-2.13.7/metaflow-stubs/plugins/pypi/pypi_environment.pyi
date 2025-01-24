######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.7                                                                                 #
# Generated on 2025-01-23T20:47:22.278882                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

