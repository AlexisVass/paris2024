SELECT s.nom_sport,e.nom_epreuve,m.nom_medaille, r.participant, r.equipe, r.note
FROM resultat r
JOIN epreuve e ON r.id_epreuve = e.id_epreuve
JOIN sport s ON e.id_sport = s.id_sport
JOIN medaille m ON r.id_medaille = m.id_medaille
WHERE LOWER(e.nom_epreuve) LIKE '%' || LOWER(:epreuve) || '%'
AND r.id_medaille IS NOT NULL
ORDER BY e.nom_epreuve,m.order_medaille;