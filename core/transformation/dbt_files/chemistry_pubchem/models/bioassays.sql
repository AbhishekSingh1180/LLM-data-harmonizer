-- Model for table: bioassays
-- Source: seed 'adme.csv'
-- Database: chemistry_pubchem

SELECT
    "Compound_CID" AS compound_cid,
    "Linked_BioAssays" AS assay_identifier
FROM {{ ref("adme") }}