SELECT 
    m.nom_medaille,
    participant AS athlete,
    p.nom_pays,
    s.nom_sport,
    e.nom_epreuve,  
    r.resultats,
    r.note
FROM resultat r
JOIN medaille m ON r.id_medaille = m.id_medaille
JOIN pays p ON r.equipe = p.id_pays
JOIN epreuve e ON r.id_epreuve = e.id_epreuve
JOIN sport s ON s.id_sport = e.id_sport
WHERE LOWER(participant) LIKE '%' || LOWER(:participant) || '%'
GROUP BY participant, e.nom_epreuve 
ORDER BY m.order_medaille;