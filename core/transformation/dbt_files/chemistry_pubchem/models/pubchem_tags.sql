-- Model for table: pubchem_tags
-- Source: seed 'adme.csv'
-- Database: chemistry_pubchem

SELECT
    "Compound_CID" AS compound_cid,
    "Tagged_by_PubChem" AS tag
FROM {{ ref("adme") }}