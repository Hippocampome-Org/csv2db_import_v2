CREATE VIEW SynproErrPropConstants AS
SELECT 
    6.2 AS length_bouton, 
    1.09 AS length_spine,
    2 AS radius_int,
    (4/3)*PI()*(POW(2,3)) AS volume_int,
    (4/3)*PI()*(POW(2,3)) / (6.2 * 1.09) AS constant
FROM
    Article
WHERE
    id = 1;