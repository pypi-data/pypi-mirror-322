# timber_nds 
A Python package for structural timber design according to the NDS (National Design Specification). 

## Installation
`pip install timber_nds`

## Python Version Compatibility
This package is compatible with Python versions 3.7 and above.

## Connections
**Important Note:** This package does not include connection design. The user is responsible for ensuring correct connection design outside of this package.

## Limitations
This package has several limitations that users should be aware of:

* **Member Geometry:** The package is currently limited to the analysis of rectangular timber members only.

* **Compression :** The package does not perform a check on the net compression stresses in members subjected to combined bending and tension.

* **Geometric Modifications:** The package assumes solid members without any holes, notches, or other geometric modifications, except for incisions (if applicable). It is the user's responsibility to consider the effects of any such modifications.

* **Bearing Check:** The package does not explicitly check for bearing stresses from horizontal forces. Instead, the shear force is assumed to be representative of the support reaction. Users should ensure that this is a reasonable assumption for their specific loading and support conditions and apply necessary corrections.

* **Second-Order Effects:** The package does not consider second-order effects in compression-bending calculations.

* **Buckling:** will be included by the user with the corresponding adjustment factor

* **Units:**  Input and output values use centimeters (cm) for length and kilograms-force (kgf) for force.

## Important Considerations
* **Local Axes:** `x` is longitudinal, `y` is horizontal within the cross-section, and `z` is vertical within the cross-section.

* **Global Axes:** `x` and `y` are horizontal, and `z` is vertical.

* **User Responsibility:** Due to the mentioned limitations, users must ensure they understand the assumptions made by this package and verify any output for suitability within the context of their structural design.

* **Future Development:** These limitations represent areas that will be improved in future development of this package.

## Usage
There are two available tutorials in the repository:

* **Example for one combination of inputs** 
* **Example for n combinations of inputs**

But there is a lot more that you can do with this library.
  
## License
This package is licensed under the [MIT License].
