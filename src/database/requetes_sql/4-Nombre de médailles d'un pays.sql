SELECT 
    p.nom_pays AS pays,
    m.nom_medaille AS medaille,
    COUNT(*) AS nb
FROM resultat r
JOIN medaille m ON r.id_medaille = m.id_medaille
JOIN pays p ON r.equipe = p.id_pays
WHERE LOWER(p.id_pays ||' '|| p.nom_pays) LIKE '%' || LOWER(:pays) || '%'
GROUP BY p.nom_pays, m.nom_medaille
ORDER BY pays, m.order_medaille;