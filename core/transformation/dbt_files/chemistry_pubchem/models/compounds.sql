-- Model for table: compounds
-- Source: seed 'adme.csv'
-- Database: chemistry_pubchem

SELECT
    "Compound_CID" AS compound_cid,
    "Name" AS name,
    "IUPAC_Name" AS iupac_name,
    "SMILES" AS smiles,
    "InChI" AS inchi,
    "InChIKey" AS inchikey,
    "Molecular_Weight" AS molecular_weight,
    "Molecular_Formula" AS molecular_formula,
    "Polar_Area" AS polar_area,
    "Complexity" AS complexity,
    "XLogP" AS xlogp,
    "Heavy_Atom_Count" AS heavy_atom_count,
    "H-Bond_Donor_Count" AS hbond_donor_count,
    "H-Bond_Acceptor_Count" AS hbond_acceptor_count,
    "Rotatable_Bond_Count" AS rotatable_bond_count,
    "Exact_Mass" AS exact_mass,
    "Monoisotopic_Mass" AS monoisotopic_mass,
    "Charge" AS charge,
    "Covalent_Unit_Count" AS covalent_unit_count,
    "Isotopic_Atom_Count" AS isotopic_atom_count,
    "Total_Atom_Stereo_Count" AS total_atom_stereo_count,
    "Defined_Atom_Stereo_Count" AS defined_atom_stereo_count,
    "Undefined_Atom_Stereo_Count" AS undefined_atom_stereo_count,
    "Total_Bond_Stereo_Count" AS total_bond_stereo_count,
    "Defined_Bond_Stereo_Count" AS defined_bond_stereo_count,
    "Undefined_Bond_Stereo_Count" AS undefined_bond_stereo_count,
    "Create_Date" AS create_date,
    "Data_Source" AS data_source,
    "Data_Source_Category" AS data_source_category
FROM {{ ref("adme") }}