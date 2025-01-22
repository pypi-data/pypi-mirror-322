import pytest

from timber_nds.design import (
    WoodElementCalculator,
    calculate_dcr_for_wood_elements,
)
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


@pytest.fixture
def sample_factors():
    tension_factors = TensionAdjustmentFactors(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    bending_factors_yy = BendingAdjustmentFactors(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    bending_factors_zz = BendingAdjustmentFactors(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    shear_factors = ShearAdjustmentFactors(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    compression_factors_yy = CompressionAdjustmentFactors(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    compression_factors_zz = CompressionAdjustmentFactors(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    compression_perp_factors = PerpendicularAdjustmentFactors(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    elastic_modulus_factors = ElasticModulusAdjustmentFactors(1.0, 1.0, 1.0, 1.0)
    return (
        tension_factors,
        bending_factors_yy,
        bending_factors_zz,
        shear_factors,
        compression_factors_yy,
        compression_factors_zz,
        compression_perp_factors,
        elastic_modulus_factors,
    )


@pytest.fixture
def sample_material():
    return WoodMaterial(
        name="Test Wood",
        specific_gravity=0.5,
        fibre_saturation_point=28.0,
        tension_strength=20.0,
        bending_strength=30.0,
        shear_strength=5.0,
        compression_perpendicular_strength=8.0,
        compression_parallel_strength=25.0,
        elastic_modulus=1000.0,
        color="brown",
    )


@pytest.fixture
def sample_section():
    return RectangularSection(name="Test Section", depth=20.0, width=10.0)


@pytest.fixture
def sample_element():
    return MemberDefinition(name="Test Element", length=300.0, effective_length_factor_yy=1.0, effective_length_factor_zz=1.0)


@pytest.fixture
def sample_forces():
    return Forces(
        name="Test Forces",
        axial=100.0,
        shear_y=50.0,
        shear_z=30.0,
        moment_xx=10.0,
        moment_yy=20.0,
        moment_zz=15.0,
    )


@pytest.fixture
def sample_forces_no_name():
    return Forces(
        axial=100.0,
        shear_y=50.0,
        shear_z=30.0,
        moment_xx=10.0,
        moment_yy=20.0,
        moment_zz=15.0,
    )


@pytest.fixture
def sample_rect_section_props(sample_section):
    return RectangularSectionProperties(width=sample_section.width, depth=sample_section.depth)


@pytest.fixture
def wood_element_calculator(sample_factors, sample_material, sample_rect_section_props):
    (
        tension_factors,
        bending_factors_yy,
        bending_factors_zz,
        shear_factors,
        compression_factors_yy,
        compression_factors_zz,
        compression_perp_factors,
        elastic_modulus_factors,
    ) = sample_factors
    return WoodElementCalculator(
        tension_factors=tension_factors,
        bending_factors_yy=bending_factors_yy,
        bending_factors_zz=bending_factors_zz,
        shear_factors=shear_factors,
        compression_factors_yy=compression_factors_yy,
        compression_factors_zz=compression_factors_zz,
        compression_perp_factors=compression_perp_factors,
        elastic_modulus_factors=elastic_modulus_factors,
        material_properties=sample_material,
        section_properties=sample_rect_section_props,
    )


class TestWoodElementCalculator:
    def test_calculate_combined_factors(self, wood_element_calculator):
        factors = wood_element_calculator.calculate_combined_factors()
        assert isinstance(factors, dict)
        assert all(isinstance(value, float) for value in factors.values())
        assert len(factors) == 8

    def test_tension_strength(self, wood_element_calculator):
        strength = wood_element_calculator.tension_strength()
        assert isinstance(strength, float)
        assert strength > 0

    def test_bending_strength(self, wood_element_calculator):
        strength_yy = wood_element_calculator.bending_strength("yy")
        assert isinstance(strength_yy, float)
        assert strength_yy > 0

        strength_zz = wood_element_calculator.bending_strength("zz")
        assert isinstance(strength_zz, float)
        assert strength_zz > 0

        with pytest.raises(ValueError, match="Invalid direction. Use 'yy' or 'zz'."):
            wood_element_calculator.bending_strength("invalid")

    def test_shear_strength(self, wood_element_calculator):
        strength = wood_element_calculator.shear_strength()
        assert isinstance(strength, float)
        assert strength > 0

    def test_compression_strength(self, wood_element_calculator):
        strength_yy = wood_element_calculator.compression_strength("yy")
        assert isinstance(strength_yy, float)
        assert strength_yy > 0

        strength_zz = wood_element_calculator.compression_strength("zz")
        assert isinstance(strength_zz, float)
        assert strength_zz > 0

        with pytest.raises(ValueError, match="Invalid direction. Use 'yy' or 'zz'."):
            wood_element_calculator.compression_strength("invalid")

    def test_compression_perp_strength(self, wood_element_calculator):
        strength = wood_element_calculator.compression_perp_strength()
        assert isinstance(strength, float)
        assert strength > 0


class TestCalculateDcrForWoodElements:
    def test_calculate_dcr_for_wood_elements(
        self, sample_section, sample_element, sample_forces, sample_material, sample_factors
    ):
        (
            tension_factors,
            bending_factors_yy,
            bending_factors_zz,
            shear_factors,
            compression_factors_yy,
            compression_factors_zz,
            compression_perp_factors,
            elastic_modulus_factors,

        ) = sample_factors
        dcr_results = calculate_dcr_for_wood_elements(
            section=sample_section,
            element=sample_element,
            forces=sample_forces,
            material=sample_material,
            tension_factors=tension_factors,
            bending_factors_yy=bending_factors_yy,
            bending_factors_zz=bending_factors_zz,
            shear_factors=shear_factors,
            compression_factors_yy=compression_factors_yy,
            compression_factors_zz=compression_factors_zz,
            compression_perp_factors=compression_perp_factors,
            elastic_modulus_factors=elastic_modulus_factors,
            support_area=1.0
        )

        assert isinstance(dcr_results, dict)
        assert all(isinstance(value, (int, float)) for value in dcr_results.values())
        assert len(dcr_results) == 15

        with pytest.raises(TypeError, match="'section' must be a RectangularSection instance."):
            calculate_dcr_for_wood_elements(
                section=123,
                element=sample_element,
                forces=sample_forces,
                material=sample_material,
                tension_factors=tension_factors,
                bending_factors_yy=bending_factors_yy,
                bending_factors_zz=bending_factors_zz,
                shear_factors=shear_factors,
                compression_factors_yy=compression_factors_yy,
                compression_factors_zz=compression_factors_zz,
                compression_perp_factors=compression_perp_factors,
                elastic_modulus_factors=elastic_modulus_factors,
                support_area=1.0
            )

        with pytest.raises(TypeError, match="'element' must be a MemberDefinition instance."):
            calculate_dcr_for_wood_elements(
                section=sample_section,
                element=123,
                forces=sample_forces,
                material=sample_material,
                tension_factors=tension_factors,
                bending_factors_yy=bending_factors_yy,
                bending_factors_zz=bending_factors_zz,
                shear_factors=shear_factors,
                compression_factors_yy=compression_factors_yy,
                compression_factors_zz=compression_factors_zz,
                compression_perp_factors=compression_perp_factors,
                elastic_modulus_factors=elastic_modulus_factors,
                support_area=1.0
            )

        with pytest.raises(TypeError, match="'force' must be a Forces instance."):
            calculate_dcr_for_wood_elements(
                section=sample_section,
                element=sample_element,
                forces=123,
                material=sample_material,
                tension_factors=tension_factors,
                bending_factors_yy=bending_factors_yy,
                bending_factors_zz=bending_factors_zz,
                shear_factors=shear_factors,
                compression_factors_yy=compression_factors_yy,
                compression_factors_zz=compression_factors_zz,
                compression_perp_factors=compression_perp_factors,
                elastic_modulus_factors=elastic_modulus_factors,
                support_area=1.0
            )
        with pytest.raises(TypeError, match="'material' must be a WoodMaterial instance."):
            calculate_dcr_for_wood_elements(
                section=sample_section,
                element=sample_element,
                forces=sample_forces,
                material=123,
                tension_factors=tension_factors,
                bending_factors_yy=bending_factors_yy,
                bending_factors_zz=bending_factors_zz,
                shear_factors=shear_factors,
                compression_factors_yy=compression_factors_yy,
                compression_factors_zz=compression_factors_zz,
                compression_perp_factors=compression_perp_factors,
                elastic_modulus_factors=elastic_modulus_factors,
                support_area=1.0
            )
