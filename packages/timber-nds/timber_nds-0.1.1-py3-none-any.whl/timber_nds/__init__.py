"""
Timber NDS package initialization.
"""

__version__ = "0.3.2"

from . import settings
from . import calculation
from . import design

from .settings import (
    WoodMaterial,
    RectangularSection,
    MemberDefinition,
    TensionAdjustmentFactors,
    BendingAdjustmentFactors,
    ShearAdjustmentFactors,
    CompressionAdjustmentFactors,
    PerpendicularAdjustmentFactors,
    ElasticModulusAdjustmentFactors,
)
from .calculation import (
    WeightCalculator,
    effective_length,
    radius_of_gyration,
    polar_moment_of_inertia,
    RectangularSectionProperties,
)
from .design import (
    WoodElementCalculator,
)

__all__ = [
    "settings",
    "calculation",
    "design",
    "WoodMaterial",
    "RectangularSection",
    "MemberDefinition",
    "TensionAdjustmentFactors",
    "BendingAdjustmentFactors",
    "ShearAdjustmentFactors",
    "CompressionAdjustmentFactors",
    "PerpendicularAdjustmentFactors",
    "ElasticModulusAdjustmentFactors",
    "WeightCalculator",
    "effective_length",
    "radius_of_gyration",
    "polar_moment_of_inertia",
    "RectangularSectionProperties",
    "WoodElementCalculator",
]
