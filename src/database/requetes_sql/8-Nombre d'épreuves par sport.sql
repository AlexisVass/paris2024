SELECT nom_sport AS 'Sport', count(id_epreuve) as 'Nb d''épreuves'
FROM sport s
JOIN epreuve e ON s.id_sport = e.id_sport
GROUP BY nom_sport
ORDER BY count(id_epreuve) desc;