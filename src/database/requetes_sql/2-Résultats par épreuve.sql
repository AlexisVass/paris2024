SELECT 
    s.nom_sport,
    e.nom_epreuve,  
    r.classement,
    m.nom_medaille,
    participant,
    p.nom_pays,
    r.resultats,
    r.note
FROM resultat r
LEFT OUTER JOIN medaille m ON r.id_medaille = m.id_medaille
JOIN pays p ON r.equipe = p.id_pays
JOIN epreuve e ON r.id_epreuve = e.id_epreuve
JOIN sport s ON e.id_sport = s.id_sport
WHERE LOWER(s.nom_sport || e.nom_epreuve) LIKE '%' || LOWER(:epreuve) || '%'
ORDER BY s.nom_sport, e.nom_epreuve, r.classement+ 0;