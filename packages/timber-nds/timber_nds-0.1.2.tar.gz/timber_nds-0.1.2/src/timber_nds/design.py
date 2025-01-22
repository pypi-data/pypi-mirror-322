from typing import Union, List, Dict, Literal
from tqdm import tqdm
import pandas as pd
import os
import operator

import numpy as np
from timber_nds.settings import (
    TensionAdjustmentFactors,
    BendingAdjustmentFactors,
    ShearAdjustmentFactors,
    CompressionAdjustmentFactors,
    PerpendicularAdjustmentFactors,
    ElasticModulusAdjustmentFactors,
    RectangularSection,
    MemberDefinition,
    WoodMaterial,
    Forces,
)

from timber_nds.calculation import RectangularSectionProperties


class WoodElementCalculator:
    def __init__(
            self,
            tension_factors: TensionAdjustmentFactors,
            bending_factors_yy: BendingAdjustmentFactors,
            bending_factors_zz: BendingAdjustmentFactors,
            shear_factors: ShearAdjustmentFactors,
            compression_factors_yy: CompressionAdjustmentFactors,
            compression_factors_zz: CompressionAdjustmentFactors,
            compression_perp_factors: PerpendicularAdjustmentFactors,
            elastic_modulus_factors: ElasticModulusAdjustmentFactors,
            material_properties: WoodMaterial,
            section_properties: RectangularSectionProperties,
    ):

        self.tension_factors = tension_factors
        self.bending_factors_yy = bending_factors_yy
        self.bending_factors_zz = bending_factors_zz
        self.shear_factors = shear_factors
        self.compression_factors_yy = compression_factors_yy
        self.compression_factors_zz = compression_factors_zz
        self.compression_perp_factors = compression_perp_factors
        self.elastic_modulus_factors = elastic_modulus_factors
        self.material_properties = material_properties
        self.section_properties = section_properties

    def calculate_combined_factors(self) -> dict:
        try:
            tension_combined = np.prod(list(self.tension_factors.__dict__.values()))
            bending_combined_yy = np.prod(list(self.bending_factors_yy.__dict__.values()))
            bending_combined_zz = np.prod(list(self.bending_factors_zz.__dict__.values()))
            shear_combined = np.prod(list(self.shear_factors.__dict__.values()))
            compression_combined_yy = np.prod(list(self.compression_factors_yy.__dict__.values()))
            compression_combined_zz = np.prod(list(self.compression_factors_zz.__dict__.values()))
            compression_perp_combined = np.prod(list(self.compression_perp_factors.__dict__.values()))
            elastic_modulus_combined = np.prod(list(self.elastic_modulus_factors.__dict__.values()))
        except TypeError as e:
            raise TypeError(f"All factor values must be numeric: {e}") from e

        return {
            "tension": tension_combined,
            "bending_yy": bending_combined_yy,
            "bending_zz": bending_combined_zz,
            "shear": shear_combined,
            "compression_yy": compression_combined_yy,
            "compression_zz": compression_combined_zz,
            "compression_perp": compression_perp_combined,
            "elastic_modulus": elastic_modulus_combined,
        }

    def tension_strength(self) -> float:
        return (
            self.material_properties.tension_strength
            * self.section_properties.area()
            * self.calculate_combined_factors()["tension"]
        )

    def bending_strength(self, direction: str) -> float:
        if direction == "yy":
            return (
                    self.material_properties.bending_strength
                    * self.section_properties.elastic_section_modulus(direction)
                    * self.calculate_combined_factors()["bending_yy"]
            )
        elif direction == "zz":
            return (
                    self.material_properties.bending_strength
                    * self.section_properties.elastic_section_modulus(direction)
                    * self.calculate_combined_factors()["bending_zz"]
            )
        else:
            raise ValueError("Invalid direction. Use 'yy' or 'zz'.")

    def shear_strength(self) -> float:
        return (
            2/3
            * self.material_properties.shear_strength
            * self.section_properties.area()
            * self.calculate_combined_factors()["shear"]
        )

    def compression_strength(self, direction: str) -> float:
        if direction == "yy":
            return (
                self.material_properties.compression_parallel_strength
                * self.section_properties.area()
                * self.calculate_combined_factors()["compression_yy"]
            )
        elif direction == "zz":
            return (
                self.material_properties.compression_parallel_strength
                * self.section_properties.area()
                * self.calculate_combined_factors()["compression_zz"]
            )
        else:
            raise ValueError("Invalid direction. Use 'yy' or 'zz'.")

    def compression_perp_strength(self, support_area: float = 1.0) -> float:
        return (
            self.material_properties.compression_perpendicular_strength
            * support_area
            * self.calculate_combined_factors()["compression_perp"]
        )


def calculate_dcr_for_wood_elements(
    section: RectangularSection,
    element: MemberDefinition,
    forces: Forces,
    material: WoodMaterial,
    tension_factors: TensionAdjustmentFactors,
    bending_factors_yy: BendingAdjustmentFactors,
    bending_factors_zz: BendingAdjustmentFactors,
    shear_factors: ShearAdjustmentFactors,
    compression_factors_yy: CompressionAdjustmentFactors,
    compression_factors_zz: CompressionAdjustmentFactors,
    compression_perp_factors: PerpendicularAdjustmentFactors,
    elastic_modulus_factors: ElasticModulusAdjustmentFactors,
    support_area: float
) -> dict:
    if not isinstance(section, RectangularSection):
        raise TypeError("'section' must be a RectangularSection instance.")
    if not isinstance(element, MemberDefinition):
        raise TypeError("'element' must be a MemberDefinition instance.")
    if not isinstance(forces, Forces):
        raise TypeError("'force' must be a Forces instance.")
    if not isinstance(material, WoodMaterial):
        raise TypeError("'material' must be a WoodMaterial instance.")

    section_properties = RectangularSectionProperties(
        width=section.width, depth=section.depth
    )

    wood_calculator = WoodElementCalculator(
        tension_factors=tension_factors,
        bending_factors_yy=bending_factors_yy,
        bending_factors_zz=bending_factors_zz,
        shear_factors=shear_factors,
        compression_factors_yy=compression_factors_yy,
        compression_factors_zz=compression_factors_zz,
        compression_perp_factors=compression_perp_factors,
        elastic_modulus_factors=elastic_modulus_factors,
        material_properties=material,
        section_properties=section_properties,
    )

    dcr_results = {}

    tension_capacity = wood_calculator.tension_strength()
    axial_tension_load = (-1 * forces.axial) if forces.axial <= 0 else 0
    dcr_results["axial tension"] = axial_tension_load
    dcr_results["tension (dcr)"] = float(axial_tension_load / tension_capacity) if tension_capacity != 0 else 0

    compression_capacity_yy = wood_calculator.compression_strength("yy")
    compression_capacity_zz = wood_calculator.compression_strength("zz")
    compression_capacity = max(compression_capacity_yy, compression_capacity_zz)
    axial_compression_load = forces.axial if forces.axial > 0 else 0
    dcr_results["axial compression"] = axial_compression_load
    dcr_results["compression (dcr)"] = (
        float(abs(axial_compression_load) / compression_capacity)
        if compression_capacity != 0
        else 0
    )

    bending_capacity_yy = wood_calculator.bending_strength("yy")
    bending_capacity_zz = wood_calculator.bending_strength("zz")
    dcr_results["moment yy"] = abs(forces.moment_yy)
    dcr_results["moment zz"] = abs(forces.moment_zz)
    dcr_results["biaxial bending (dcr)"] = (
        float(abs(forces.moment_yy) / bending_capacity_yy) + float(abs(forces.moment_zz) / bending_capacity_zz)
        if bending_capacity_yy or bending_capacity_zz != 0
        else 0
    )

    shear_capacity_y = wood_calculator.shear_strength()
    dcr_results["shear y"] = abs(forces.shear_y)
    shear_capacity_z = wood_calculator.shear_strength()
    dcr_results["shear z"] = abs(forces.shear_z)
    dcr_results["shear y (dcr)"] = (
        float(abs(forces.shear_y) / shear_capacity_y) if shear_capacity_y != 0 else 0
    )
    dcr_results["shear z (dcr)"] = (
        float(abs(forces.shear_z) / shear_capacity_z) if shear_capacity_z != 0 else 0
    )

    dcr_results["bending and tension (dcr)"] = dcr_results["tension (dcr)"] + dcr_results["biaxial bending (dcr)"]

    dcr_results["bending and compression (dcr)"] = dcr_results["compression (dcr)"]**2 + dcr_results["biaxial bending (dcr)"]

    compression_perpendicular_capacity = (
        wood_calculator.compression_perp_strength(support_area)
    )
    dcr_results["compression perpendicular"] = abs(forces.shear_z)
    dcr_results["compression perpendicular (dcr)"] = (
        float(max(abs(forces.shear_z), abs(forces.shear_z)) / compression_perpendicular_capacity)
        if compression_perpendicular_capacity != 0
        else 0
    )

    return dcr_results


def check_for_all_forces(
        section: RectangularSection,
        element: MemberDefinition,
        list_forces: Union[List[Forces], Forces],
        material: WoodMaterial,
        tension_factors: float,
        bending_factors_yy: float,
        bending_factors_zz: float,
        shear_factors: float,
        compression_factors_yy: float,
        compression_factors_zz: float,
        compression_perp_factors: float,
        elastic_modulus_factors: float,
        support_area: float
) -> pd.DataFrame:
    if not isinstance(list_forces, list):
        list_forces = [list_forces]

    if not list_forces:
        raise ValueError("The 'list_forces' is not a list.")

    all_results = []
    errors = []

    for force in tqdm(list_forces, desc="Checking for all forces"):
        print(f'Calculando para la fuerza: {force.name}')
        try:
            dcr = calculate_dcr_for_wood_elements(
                section=section, element=element, forces=force, material=material,
                tension_factors=tension_factors, bending_factors_yy=bending_factors_yy,
                bending_factors_zz=bending_factors_zz, shear_factors=shear_factors,
                compression_factors_yy=compression_factors_yy, compression_factors_zz=compression_factors_zz,
                compression_perp_factors=compression_perp_factors, elastic_modulus_factors=elastic_modulus_factors,
                support_area=support_area
            )

            try:
                section_name = section.name
                member_name = element.name
                force_name = force.name
            except AttributeError:
                raise AttributeError("Section, element, and force must have a 'name' attribute.")

            max_dcr = max(dcr.get(key, 0) for key in [
                "dcr_tension", "biaxial bending (dcr)",
                "shear y (dcr)", "shear z (dcr)",
                "compression (dcr)", "bending and compression (dcr)"
            ])

            result = {
                "member": member_name, "section": section_name, "force": force_name, "dcr_max": max_dcr
            }
            result.update(dcr)
            all_results.append(result)

        except Exception as e:
            error_msg = f"Error processing section '{section.name}', member '{element.name}', force '{force.name}': {e}"
            errors.append(error_msg)
            print(error_msg)

    all_results_df = pd.DataFrame(all_results)

    if errors:
        print("\nErrors encountered during processing:")
        for error in errors:
            print(error)

    return all_results_df


def check_for_all_sections(
        list_sections: Union[List[RectangularSection], RectangularSection],
        list_elements: Union[List[MemberDefinition], MemberDefinition],
        list_forces: Union[List[Forces], Forces],
        material: WoodMaterial,
        tension_factors: float,
        bending_factors_yy: float,
        bending_factors_zz: float,
        shear_factors: float,
        compression_factors_yy: float,
        compression_factors_zz: float,
        compression_perp_factors: float,
        elastic_modulus_factors: float,
        support_area
) -> pd.DataFrame:
    if not isinstance(list_sections, list):
        list_sections = [list_sections]

    if not list_sections:
        raise ValueError("The 'list_sections' cannot be empty.")

    all_results = []
    errors = []

    for section in tqdm(list_sections, desc="Checking for all sections"):
        print('..................................................')
        print(f'Calculando para la sección: {section.name}')
        print('..................................................')
        try:
            dcr_df = check_for_all_forces(
                section=section,
                element=list_elements,
                list_forces=list_forces,
                material=material,
                tension_factors=tension_factors,
                bending_factors_yy=bending_factors_yy,
                bending_factors_zz=bending_factors_zz,
                shear_factors=shear_factors,
                compression_factors_yy=compression_factors_yy,
                compression_factors_zz=compression_factors_zz,
                compression_perp_factors=compression_perp_factors,
                elastic_modulus_factors=elastic_modulus_factors,
                support_area=support_area
            )

            all_results.append(dcr_df)

        except Exception as e:
            error_msg = f"Error processing section '{section.name}': {e}"
            errors.append(error_msg)
            print(error_msg)

    if errors:
        print("\nErrors encountered during processing:")
        for error in errors:
            print(error)

    if all_results:
        return pd.concat(all_results, ignore_index=True)
    else:
        return pd.DataFrame()


def check_for_all_elements(
        list_sections: List[RectangularSection],
        list_elements: List[MemberDefinition],
        list_forces: List[Forces],
        material: WoodMaterial,
        tension_factors: TensionAdjustmentFactors,
        bending_factors_yy: BendingAdjustmentFactors,
        bending_factors_zz: BendingAdjustmentFactors,
        shear_factors: ShearAdjustmentFactors,
        compression_factors_yy: CompressionAdjustmentFactors,
        compression_factors_zz: CompressionAdjustmentFactors,
        compression_perp_factors: PerpendicularAdjustmentFactors,
        elastic_modulus_factors: ElasticModulusAdjustmentFactors,
        support_area_values: dict,
) -> pd.DataFrame :
    if not list_sections or not list_elements or not list_forces :
        return pd.DataFrame()

    results = []
    for section in list_sections :
        for element in list_elements :
            for forces in list_forces :

                section_properties = RectangularSectionProperties(width=section.width, depth=section.depth)
                wood_calculator = WoodElementCalculator(
                    tension_factors=tension_factors,
                    bending_factors_yy=bending_factors_yy,
                    bending_factors_zz=bending_factors_zz,
                    shear_factors=shear_factors,
                    compression_factors_yy=compression_factors_yy,
                    compression_factors_zz=compression_factors_zz,
                    compression_perp_factors=compression_perp_factors,
                    elastic_modulus_factors=elastic_modulus_factors,
                    material_properties=material,
                    section_properties=section_properties,
                )

                support_area = support_area_values.get(element.name, 1.0)

                try :
                    dcr_tension = abs(forces.axial) / wood_calculator.tension_strength() if forces.axial > 0 else 0
                except ZeroDivisionError :
                    dcr_tension = 0

                dcr_bending_yy = abs(forces.moment_yy) / wood_calculator.bending_strength(
                    "yy") if forces.moment_yy else 0
                dcr_bending_zz = abs(forces.moment_zz) / wood_calculator.bending_strength(
                    "zz") if forces.moment_zz else 0

                dcr_biaxial_bending = dcr_bending_yy + dcr_bending_zz

                try :
                    dcr_shear_y = abs(forces.shear_y) / wood_calculator.shear_strength() if forces.shear_y else 0
                except ZeroDivisionError :
                    dcr_shear_y = 0

                try :
                    dcr_shear_z = abs(forces.shear_z) / wood_calculator.shear_strength() if forces.shear_z else 0
                except ZeroDivisionError :
                    dcr_shear_z = 0

                try :
                    dcr_compression = abs(forces.axial) / wood_calculator.compression_strength(
                        "yy") if forces.axial < 0 else 0
                except ZeroDivisionError :
                    dcr_compression = 0

                try :
                    max_shear = max(abs(forces.shear_y), abs(forces.shear_z)) # Correct calculation of max_shear
                    dcr_compression_perp = max_shear / wood_calculator.compression_perp_strength(
                        support_area) if max_shear > 0 else 0 # Correct use of max_shear and add if condition
                except ZeroDivisionError :
                    dcr_compression_perp = 0

                dcr_bending_and_compression = dcr_compression + dcr_biaxial_bending

                results.append({
                    "member" : element.name,
                    "section" : section.name,
                    "force" : forces.name,
                    "tension (dcr)" : dcr_tension,
                    "biaxial bending (dcr)" : dcr_biaxial_bending,
                    "shear y (dcr)" : dcr_shear_y,
                    "shear z (dcr)" : dcr_shear_z,
                    "compression (dcr)" : dcr_compression,
                    "bending and compression (dcr)" : dcr_bending_and_compression,
                    "compression perpendicular (dcr)" : dcr_compression_perp

                })
    return pd.DataFrame(results)


def filter_and_export_results(
    results_df: pd.DataFrame,
    filters: Dict[str, Union[str, List[str], Dict[str, Union[int, float, dict]]]],
    output_path: str = None,
    output_filename: str = "filtered_results.xlsx",
    sort_by: str = None,
    sort_order: Literal["asc", "desc"] = "asc",
) -> pd.DataFrame:
    if not isinstance(results_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    if not isinstance(filters, dict):
        raise TypeError("Filters must be a dictionary.")
    if not isinstance(output_filename, str):
        raise TypeError("output_filename must be a string.")
    if output_path is not None and not isinstance(output_path, str):
        raise TypeError("output_path must be a string.")
    if sort_by is not None and not isinstance(sort_by, str):
        raise TypeError("sort_by must be a string.")
    if sort_order not in ["asc", "desc"]:
        raise ValueError("sort_order must be 'asc' or 'desc'.")

    for column, condition in filters.items():
        if not isinstance(column, str):
            raise TypeError("Filter columns must be strings")
        if column not in results_df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")
        if isinstance(condition, dict):
            if "range" in condition:
                if "min" not in condition["range"] or "max" not in condition["range"]:
                    raise ValueError(f"Invalid filter format for numeric column '{column}'. Range filter must include 'min' and 'max' keys.")
                if not isinstance(condition["range"]["min"], (int, float)) or not isinstance(condition["range"]["max"], (int, float)):
                    raise TypeError(f"Range values for column '{column}' must be numeric (int or float)")
            elif "operator" not in condition or "threshold" not in condition:
                raise ValueError(f"Invalid filter format for numeric column '{column}'. Must include 'operator' and 'threshold' or 'range'.")
            elif not isinstance(condition["threshold"], (int, float)):
                raise TypeError(f"Threshold for column '{column}' must be numeric (int or float)")
            elif condition["operator"] not in ["eq", "gt", "lt", "ge", "le"]:
                raise ValueError(f"Invalid operator '{condition['operator']}' for column '{column}'. Use 'eq', 'gt', 'lt', 'ge', or 'le'.")
        elif not isinstance(condition, (str, list)):
            raise TypeError(f"Invalid filter format for column '{column}'. Must be a string or a list or a dictionary.")
        if isinstance(condition, list):
            for value in condition:
                if not isinstance(value, str):
                    raise TypeError(f"Invalid filter values in list for column '{column}'. Must be strings")

    filtered_df = results_df.copy()
    for column, condition in filters.items():
        if isinstance(condition, str):
            filtered_df = filtered_df[filtered_df[column] == condition]
        elif isinstance(condition, list):
            filtered_df = filtered_df[filtered_df[column].isin(condition)]
        elif isinstance(condition, dict):
            if "range" in condition:
                min_val = condition["range"]["min"]
                max_val = condition["range"]["max"]
                filtered_df = filtered_df[(filtered_df[column] >= min_val) & (filtered_df[column] <= max_val)]
            else:
                op_str = condition["operator"]
                threshold = condition["threshold"]
                op = {
                    "eq": operator.eq,
                    "gt": operator.gt,
                    "lt": operator.lt,
                    "ge": operator.ge,
                    "le": operator.le,
                }[op_str]
                filtered_df = filtered_df[op(filtered_df[column], threshold)]

    if sort_by:
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=(sort_order == "asc"))

    if output_path is None:
        output_path = os.path.join(os.getcwd(), output_filename)
    else:
        output_path = os.path.join(output_path, output_filename)

    filtered_df.to_excel(output_path, index=False)
    print(f"Filtered results exported to: {output_path}")
    return filtered_df
