select nom_sport, count(id_epreuve)
from sport s
join epreuve e on s.id_sport = e.id_sport
group by nom_sport
order by count(id_epreuve) desc;