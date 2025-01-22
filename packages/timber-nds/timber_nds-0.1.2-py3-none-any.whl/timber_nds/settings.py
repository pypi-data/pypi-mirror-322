from dataclasses import dataclass


@dataclass
class WoodMaterial:
    name: str = "Default Wood"
    specific_gravity: float = 0.58
    fibre_saturation_point: float = 0.30
    tension_strength: float = 84.0
    bending_strength: float = 212.0
    shear_strength: float = 94.9
    compression_perpendicular_strength: float = 8.54
    compression_parallel_strength: float = 81.4
    elastic_modulus: float = 127000
    color: str = "Brown"


@dataclass
class RectangularSection:
    name: str = "Default Section"
    depth: float = 8.9
    width: float = 3.8


@dataclass
class MemberDefinition:
    name: str = "Default Member"
    length: float = 300.
    effective_length_factor_yy: float = 1.0
    effective_length_factor_zz: float = 1.0


@dataclass
class TensionAdjustmentFactors:
    due_moisture: float = 1.0
    due_temperature: float = 1.0
    due_size: float = 1.0
    due_incising: float = 1.0
    due_format_conversion: float = 2.70
    due_resistance_reduction: float = 0.80
    due_time_effect: float = 1.0


@dataclass
class BendingAdjustmentFactors:
    due_moisture: float = 1.0
    due_temperature: float = 1.0
    due_beam_stability: float = 1.0
    due_size: float = 1.0
    due_flat_use: float = 1.0
    due_incising: float = 1.0
    due_repetitive_member: float = 1.0
    due_format_conversion: float = 2.54
    due_resistance_reduction: float = 0.85
    due_time_effect: float = 1.0


@dataclass
class ShearAdjustmentFactors:
    due_moisture: float = 1.0
    due_temperature: float = 1.0
    due_incising: float = 1.0
    due_format_conversion: float = 2.88
    due_resistance_reduction: float = 0.75
    due_time_effect: float = 1.0


@dataclass
class CompressionAdjustmentFactors:
    due_moisture: float = 1.0
    due_temperature: float = 1.0
    due_size: float = 1.0
    due_incising: float = 1.0
    due_column_stability: float = 1.0
    due_format_conversion: float = 2.40
    due_resistance_reduction: float = 0.90
    due_time_effect: float = 1.0


@dataclass
class PerpendicularAdjustmentFactors:
    due_moisture: float = 1.0
    due_temperature: float = 1.0
    due_incising: float = 1.0
    due_bearing_area: float = 1.0
    due_format_conversion: float = 1.67
    due_resistance_reduction: float = 0.90
    due_time_effect: float = 1.0


@dataclass
class ElasticModulusAdjustmentFactors:
    due_moisture: float = 1.0
    due_temperature: float = 1.0
    due_incising: float = 1.0
    due_format_conversion: float = 1.76
    due_resistance_reduction: float = 0.85


@dataclass
class Forces:
    name: str = "default force"
    axial: float = 0.0
    shear_y: float = 0.0
    shear_z: float = 0.0
    moment_xx: float = 0.0
    moment_yy: float = 0.0
    moment_zz: float = 0.0
