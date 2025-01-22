import unittest
import pytest

from timber_nds import (
    effective_length,
    radius_of_gyration,
    polar_moment_of_inertia,
    RectangularSectionProperties,
    WeightCalculator
)


class MockWoodMaterial:
    def __init__(self, specific_gravity, fibre_saturation_point):
        self.specific_gravity = specific_gravity
        self.fibre_saturation_point = fibre_saturation_point


class MockRectangularSection:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth


class MockMemberDefinition:
    def __init__(self, length):
        self.length = length


@pytest.fixture
def sample_material():
    return MockWoodMaterial(specific_gravity=0.5, fibre_saturation_point=30)


@pytest.fixture
def sample_section():
    return MockRectangularSection(width=100, depth=200)


@pytest.fixture
def sample_element():
    return MockMemberDefinition(length=3000)


@pytest.fixture
def weight_calculator(sample_material, sample_section, sample_element):
    return WeightCalculator(sample_material, sample_section, sample_element)


class TestWeightCalculator:

    def test_calculate_density_at_moisture_content(self, weight_calculator):

        density = weight_calculator.calculate_density_at_moisture_content(15)
        assert isinstance(density, float)
        assert density > 0

        density = weight_calculator.calculate_density_at_moisture_content(30)
        assert isinstance(density, float)
        assert density > 0

        # Test with moisture content above fibre saturation point
        density = weight_calculator.calculate_density_at_moisture_content(40)
        assert isinstance(density, float)
        assert density > 0

    def test_calculate_weight_at_moisture_content(self, weight_calculator):
        weight = weight_calculator.calculate_weight_at_moisture_content(15)
        assert isinstance(weight, float)
        assert weight > 0


class TestStructuralFunctions(unittest.TestCase):
    def test_effective_length(self):
        self.assertEqual(effective_length(2.0, 5.0), 10.0)
        self.assertEqual(effective_length(1.0, 10.0), 10.0)
        self.assertEqual(effective_length(0.5, 20.0), 10.0)

    def test_radius_of_gyration(self):
        self.assertEqual(radius_of_gyration(4.0, 4.0), 1.0)
        self.assertEqual(radius_of_gyration(16.0, 4.0), 2.0)

        with self.assertRaises(ValueError):
            radius_of_gyration(1.0, 0.0)

    def test_polar_moment_of_inertia(self):
        self.assertEqual(polar_moment_of_inertia(4.0, 6.0), 10.0)
        self.assertEqual(polar_moment_of_inertia(10.0, 0.0), 10.0)

    def test_rectangular_section_properties(self):
        section = RectangularSectionProperties(width=2.0, depth=3.0)
        self.assertEqual(section.area(), 6.0)
        self.assertEqual(section.moment_of_inertia("yy"), 4.5)
        self.assertEqual(section.moment_of_inertia("zz"), 2.0)
        self.assertEqual(section.elastic_section_modulus("yy"), 3.0)
        self.assertEqual(section.elastic_section_modulus("zz"), 2.0)
        self.assertEqual(section.plastic_section_modulus("yy"), 4.5)
        self.assertEqual(section.plastic_section_modulus("zz"), 3.0)
        self.assertEqual(section.polar_moment_of_inertia(), 6.5)
        self.assertAlmostEqual(section.radius_of_gyration("yy"), 0.8660254,
                               places=6)  # Using assertAlmostEqual for float comparison
        self.assertAlmostEqual(section.radius_of_gyration("zz"), 0.57735,
                               places=6)  # Using assertAlmostEqual for float comparison


if __name__ == "__main__":
    unittest.main()
