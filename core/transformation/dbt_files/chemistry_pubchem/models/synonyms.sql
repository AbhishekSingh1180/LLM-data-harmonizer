-- Model for table: synonyms
-- Source: seed 'adme.csv'
-- Database: chemistry_pubchem

SELECT
    "Compound_CID" AS compound_cid,
    "Synonyms" AS synonym
FROM {{ ref("adme") }}