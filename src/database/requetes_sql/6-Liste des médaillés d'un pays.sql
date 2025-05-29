SELECT
    p.nom_pays AS pays,
    m.nom_medaille AS medaille,
    r.participant,
    s.nom_sport,
    e.nom_epreuve,
    r.resultats,
    r.note
FROM resultat r
JOIN epreuve e ON r.id_epreuve = e.id_epreuve
JOIN medaille m ON r.id_medaille = m.id_medaille
JOIN pays p ON r.equipe = p.id_pays
JOIN sport s ON s.id_sport = e.id_sport
WHERE LOWER(p.id_pays || p.nom_pays) LIKE '%' || LOWER(:pays) || '%'
ORDER BY pays, m.order_medaille, r.participant;