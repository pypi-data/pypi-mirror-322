# -*- coding: utf-8 -*-
import typing
from typing import Optional

# this is an interface file for python tooling. values are declared here and defined in `src/python/mod.rs`.

__version__ = ...

class VFGException(Exception):
    ...

@typing.final
class FileManipulationError(VFGException):
    ...

@typing.final
class RkyvDeserializationError(VFGException):
    ...

@typing.final
class JsonSerializationError(VFGException):
    ...

@typing.final
class ValidationError(VFGException):
    ...

@typing.final
class InvalidGraphVersionError(VFGException):
    ...

@typing.final
class ProbabilityDistribution:
    """
    Probability distribution.
    """

    Categorical: int = 0
    CategoricalConditional: int = 1

    def __richcmp__(self, other: ProbabilityDistribution, op) -> bool: ...
    def __int__(self) -> int: ...

@typing.final
class VariableRole:
    """
    VariableRole can be one of three values: NoRole, ControlState, or Latent.
    """
    NoRole: int = 0
    ControlState: int = 1
    Latent: int = 2

    def __richcmp__(self, other: VariableRole, op) -> bool: ...
    def __int__(self) -> int: ...

@typing.final
class DiscreteVariableNamedElements:
    """
    DiscreteVariableNamedElements represents a discrete variable with named elements.
    """

    elements: list[str]
    role: VariableRole

    def __init__(self, elements: list[str], role: typing.Optional[VariableRole] = None) -> None: ...

@typing.final
class DiscreteVariableAnonymousElements:
    """
    DiscreteVariableAnonymousElements represents a discrete variable with anonymous elements.
    """

    cardinality: int
    role: VariableRole

    def __init__(self, cardinality: int, role: typing.Optional[VariableRole] = None) -> None: ...

@typing.final
class FactorRole:
    """
    FactorRole is optional can can be one of 3 values: "transition", "preference" or "likelihood".
    There is no default value, only if specified on the factor will it exist
    None is used for the default value in the event that it exists and the numeric value doesn't match the enum
    """
    NoRole: int = 0
    Transition: int = 1
    Preference: int = 2
    Likelihood: int = 3
    InitialStatePrior: int = 4

    def __richcmp__(self, other: FactorRole, op) -> bool: ...
    def __int__(self) -> int: ...

@typing.final
class Factor:
    """
    A Factor represents a single factor extraction of the factor graph.
    It contains variables, values, and a type.
    """

    variables: list[str]
    distribution: ProbabilityDistribution
    """ values is a numpy array """
    values: list[typing.Any]
    role: FactorRole

    @staticmethod
    def default() -> Factor: ...

    def __init__(self, variables: list[str], distribution: typing.Union[ProbabilityDistribution, int], role: typing.Optional[FactorRole] = None) -> None: ...\

@typing.final
class Metadata:
    model_type: Optional[ModelType]
    model_version: Optional[str]
    description: Optional[str]

@typing.final
class ModelType:
    """
    ModelType is optional but can contain one of the four given model types
    """
    BayesianNetwork: int = 0
    MarkovRandomField: int = 1,
    Pomdp: int = 2,
    FactorGraph: int = 3

    def __richcmp__(self, other: FactorRole, op) -> bool: ...
    def __int__(self) -> int: ...

@typing.final
class VFG:
    """
    Represents the entire VFG.

    :param version: The version of the VFG schema used
    :param factors: The factors, represented by Factors
    :param variables: The variables in the VFG, as a dictionary of names to DiscreteVariableNamedElements or DiscreteVariableAnonymousElements
    :param metadata: Metadata, which includeds graph version, graph description, and model type
    :param visualization_metadata: Metadata for visualization. Should be treated as opaque.
    """

    version: str
    factors: list[Factor]
    variables: dict[str, typing.Union[DiscreteVariableNamedElements, DiscreteVariableAnonymousElements]]
    metadata: Optional[Metadata]
    visualization_metadata: Optional[str]

    @staticmethod
    def default() -> VFG: ...

    def __init__(self, factors: list[Factor], variables: dict[str, typing.Union[DiscreteVariableNamedElements, DiscreteVariableAnonymousElements]]) -> None: ...

def get_graph() -> VFG:
    """
    Get the global VFG.
    """
    ...

def set_graph(new_graph: VFG) -> None:
    """
    Set the global VFG.

    :param new_graph: The graph to set
    """
    ...

def validate_graph(graph: VFG) -> None:
    """
    Validates VFG.

    :param graph: The graph to validate
    """
    ...

def get_subgraph_from(variable_name: list[str]) -> VFG:
    """
    Retrieve subgraph.

    :param variable_name:
    """
    ...

def vfg_to_json(vfg: VFG) -> str:
    """
    Serialize a VFG to a JSON string.

    :param vfg:
    """
    ...

def vfg_from_json(json: str) -> VFG:
    """
    Deserialize a JSON string to VFG.

    :param json:
    """
    ...
