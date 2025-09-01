-- Model for table: mesh_headings
-- Source: seed 'adme.csv'
-- Database: chemistry_pubchem

SELECT
    "Compound_CID" AS compound_cid,
    "MeSH_Headings" AS heading
FROM {{ ref("adme") }}