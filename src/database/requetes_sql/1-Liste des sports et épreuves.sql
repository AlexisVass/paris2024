SELECT 
    s.nom_sport || ' > ' || e.nom_epreuve AS sport_et_epreuve
FROM resultat r
JOIN epreuve e ON r.id_epreuve = e.id_epreuve
JOIN sport s ON e.id_sport = s.id_sport
GROUP BY s.nom_sport, e.nom_epreuve
ORDER BY s.nom_sport, e.nom_epreuve;