import numpy as np
import pandas as pd
import timber_nds.settings as settings
from timber_nds.settings import Forces


class WeightCalculator:
    """
    Calculates the weight of a wood element considering moisture content.

    Args:
        material: Properties of the wood material (WoodMaterial).
        section: Properties of the structural section (RectangularSection).
        element: Properties of the structural element (MemberDefinition).

    Returns:
        None

    Assumptions:
        - The provided material, section and element objects are valid.
    """

    def __init__(
        self,
        material: settings.WoodMaterial,
        section: settings.RectangularSection,
        element: settings.MemberDefinition,
    ):
        self.material = material
        self.section = section
        self.element = element

    def calculate_density_at_moisture_content(self, moisture_content: float) -> float:
        """
        Calculates the density of the wood element at a given moisture content.

        Args:
            moisture_content: The moisture content of the wood, as a percentage.

        Returns:
            The density of the wood element in kg/m^3.

        Assumptions:
            - The moisture content is given as a percentage (e.g., 12.5 for 12.5%).
            - Density of water is 1000 kg/m^3.
        """
        if not isinstance(moisture_content, (int, float)):
            raise TypeError("Moisture content must be a number (int or float)")
        if moisture_content < 0:
            raise ValueError("Moisture content must be non-negative.")
        if self.material.fibre_saturation_point < 0:
            raise ValueError("Fibre saturation point must be non-negative.")

        if moisture_content <= self.material.fibre_saturation_point:
            density_at_moisture = (
                self.material.specific_gravity
                * 1000
                * ((moisture_content / 100) + 1)
                / (
                    (self.material.fibre_saturation_point / 100)
                    * self.material.specific_gravity
                    + 1
                )
            )
        else:
            density_at_moisture = (
                self.material.specific_gravity
                * 1000
                * (
                    (self.material.fibre_saturation_point / 100)
                    + 1
                )
                / (
                    (self.material.fibre_saturation_point / 100)
                    * self.material.specific_gravity
                    + 1
                )
            )
        return density_at_moisture

    def calculate_weight_at_moisture_content(self, moisture_content: float) -> float:
        """
        Calculates the weight of the wood element at a given moisture content.

        Args:
            moisture_content: The moisture content of the wood, as a percentage.

        Returns:
            The weight of the wood element in kg.

        Assumptions:
           - The provided dimensions are valid (positive).
        """

        if not isinstance(moisture_content, (int, float)):
            raise TypeError("Moisture content must be a number (int or float)")
        if moisture_content < 0:
            raise ValueError("Moisture content must be non-negative.")
        if self.section.width < 0 or self.section.depth < 0 or self.element.length < 0:
            raise ValueError("Element dimensions must be non-negative values.")

        density = self.calculate_density_at_moisture_content(moisture_content)

        return self.section.width / 100 * self.section.depth / 100 * self.element.length / 100 * density


def effective_length(k_factor: float, length: float) -> float:
    """
    Calculates the effective length of a member.

    Args:
        k_factor: Effective length factor (K).
        length: Length of the element.

    Returns:
        The effective length of the member.
    """
    return k_factor * length


def radius_of_gyration(moment_of_inertia: float, area: float) -> float:
    """
    Calculates the radius of gyration for any section.

    Args:
        moment_of_inertia: Second moment of area (I).
        area: Area of the section (A).

    Returns:
        The radius of gyration.

    Assumptions:
         - Area must be a non-zero value.
    """
    if area == 0:
        raise ValueError("Area cannot be zero.")
    return np.sqrt(moment_of_inertia / area)


def polar_moment_of_inertia(moment_of_inertia_yy: float, moment_of_inertia_zz: float) -> float:
    """
    Calculates the polar moment of inertia for any section.

    Args:
        moment_of_inertia_yy: Second moment of area about the yy axis (Ix).
        moment_of_inertia_zz: Second moment of area about the zz axis (Iy).

    Returns:
        The polar moment of inertia.
    """
    return moment_of_inertia_yy + moment_of_inertia_zz


class RectangularSectionProperties:
    """
    Represents properties of a rectangular section.

    Args:
        width: Width of the section.
        depth: Depth of the section.

    Returns:
        None

    Assumptions:
         - Width and Depth must be positive values.
    """

    def __init__(self, width: float, depth: float):
        self.width = width
        self.depth = depth

    def area(self) -> float:
        """
        Calculates the area of the rectangular section.

        Returns:
            The area of the section.
        """
        return self.width * self.depth

    def moment_of_inertia(self, direction: str) -> float:
        """Calculates the moment of inertia.

        Args:
            direction: Axis direction ("yy" or "zz").

        Returns:
            Moment of inertia.
        """

        if direction not in ("yy", "zz"):
            raise ValueError("Invalid direction. Use 'yy' or 'zz'.")

        elif direction == "yy":
            inertia = (self.width * self.depth**3) / 12

        else:
            inertia = (self.depth * self.width ** 3) / 12

        return inertia

    def elastic_section_modulus(self, direction: str = None) -> float:
        """Calculates the elastic section modulus.

        Args:
            direction: Axis direction ("yy" or "zz").

        Returns:
            Elastic section modulus.
        """

        if direction == "yy":
            section_modulus = (self.width * self.depth**2) / 6

        elif direction == "zz":
            section_modulus = (self.depth * self.width**2) / 6

        else:

            raise ValueError("Invalid direction. Use 'yy' or 'zz'.")

        return section_modulus

    def plastic_section_modulus(self, direction: str) -> float:
        """Calculates the plastic section modulus.

        Args:
            direction: Axis direction ("yy" or "zz").

        Returns:
            Plastic section modulus.
        """

        if direction not in ("yy", "zz"):
            raise ValueError("Invalid direction. Use 'yy' or 'zz'.")

        if direction == "yy":
            return (self.width * self.depth**2) / 4
        else:  # direction == "zz"
            return (self.depth * self.width**2) / 4

    def polar_moment_of_inertia(self) -> float:
        """
        Calculates the polar moment of inertia.

        Returns:
            The polar moment of inertia.
        """
        return self.moment_of_inertia("yy") + self.moment_of_inertia("zz")

    def radius_of_gyration(self, direction: str) -> float:
        """
        Calculates the radius of gyration about the yy axis.

        Returns:
            The radius of gyration.
        """
        return radius_of_gyration(self.moment_of_inertia(direction), self.area())


def import_robot_bar_forces(filepath: str) -> pd.DataFrame:
    """
    Creates a Pandas DataFrame from Robot Structural Analysis force export.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A Pandas DataFrame with multi-indexed rows.

    Assumptions:
        - The CSV file follows the specified format.
    """

    df = pd.read_csv(filepath, sep=";", decimal=",", thousands=".", header=0)

    first_column_name = df.columns[0]
    df_split = df[first_column_name].str.split(expand=True)

    if len(df_split.columns) < 4:
        raise ValueError("The first column does not have enough parts to form Member, Node, Case, and Mode.")

    df_split.columns = ["Member", "Node", "Case", "Mode"] + [f"Extra_Part_{i}" for i in range(1, len(df_split.columns) - 3)]

    df_split = df_split.iloc[:, :4]

    df = pd.concat([df_split, df.drop(columns=[first_column_name])], axis=1)
    print(f'first_column_name {first_column_name}')

    df.rename(columns={
        "FX (kgf)": "axial",
        "FY (kgf)": "shear_y",
        "FZ (kgf)": "shear_z",
        "MX (kgfcm)": "torque",
        "MY (kgfcm)": "moment_yy",
        "MZ (kgfcm)": "moment_zz",
        "Length (m)": "length"
    }, inplace=True)

    df = df.set_index(["Member", "Node", "Case", "Mode"])
    return df


def create_robot_bar_forces_as_objects(df: pd.DataFrame) -> list[Forces]:
    """
    Creates a list of Forces objects from a Pandas DataFrame.

    Args:
        df: DataFrame containing force and moment data.
            Requires columns 'axial', 'shear_y', 'shear_z', 'torque', 'moment_yy', 'moment_zz'.
            The index levels are concatenated to create the 'name' attribute.

    Returns:
        A list of Forces objects.

    Assumptions:
        - The input DataFrame has the required columns.
        - All values in the DataFrame are numeric.
        - No missing data needs to be handled
    """

    forces_list = []
    for index, row in df.iterrows():
        name = "/".join(map(str, index))

        forces = Forces(
            name=name,
            axial=row['axial'],
            shear_y=row['shear_y'],
            shear_z=row['shear_z'],
            moment_xx=row['torque'],
            moment_yy=row['moment_yy'],
            moment_zz=row['moment_zz'],
        )
        forces_list.append(forces)
    return forces_list
