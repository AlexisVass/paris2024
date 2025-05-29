SELECT equipe AS pays,
       SUM(CASE WHEN id_medaille = 'O' THEN 1 ELSE 0 END) AS "Or",
       SUM(CASE WHEN id_medaille = 'A' THEN 1 ELSE 0 END) AS "Argent",
       SUM(CASE WHEN id_medaille = 'B' THEN 1 ELSE 0 END) AS "Bronze",
       COUNT(id_medaille) AS total 
FROM resultat
WHERE id_medaille IS NOT NULL
GROUP BY equipe 
ORDER BY "Or" DESC, "Argent" DESC, "Bronze" DESC;