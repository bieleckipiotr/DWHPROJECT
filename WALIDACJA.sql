use DWH
go


-- MAPA
SELECT ds.nazwa_zespolu, AVG(f.delay) AS avg_delay
FROM FactDelays f
JOIN DimStops ds ON f.stop_id = ds.stop_id
WHERE f.delay > -10
GROUP BY ds.nazwa_zespolu
ORDER BY avg_delay DESC;


select f.stop_id, ds.nazwa_zespolu, ds.lon, ds.lat, f.delay
from FactDelays f
join DimStops ds on f.stop_id = ds.stop_id
where ds.nazwa_zespolu = 'Mandarynki'




-- OPOZNIENIA NA TRASIE
select dsa.kod_trasy, dsa.StopOnRoute, avg(f.delay) as avg_delay
from FactDelays f
join DimScheduledArr dsa on f.scheduled_arr_id = dsa.scheduled_arr_id
where f.delay > -10
group by dsa.kod_trasy, dsa.StopOnRoute
order by dsa.kod_trasy
-- TO-SAN

select dsa.kod_trasy, count(*) as cnt
from FactDelays f
join DimScheduledArr dsa on f.scheduled_arr_id = dsa.scheduled_arr_id
where f.delay > -10
group by dsa.kod_trasy
order by cnt desc


select d.linia, COUNT(*) as cnt
from FactDelays f
join DimBuses d on f.bus_id=d.bus_id
group by d.linia
order by cnt desc






-- ROZK£ADY (2)
select d3.nazwa_zespolu, d1.linia, d2.time_scheduled_id, f.time_estimated_id
from FactDelays f
join DimBuses d1 on f.bus_id=d1.bus_id
join DimScheduledArr d2 on f.scheduled_arr_id=d2.scheduled_arr_id
join DimStops d3 on f.stop_id=d3.stop_id
--where d3.nazwa_zespolu
order by d3.nazwa_zespolu asc


-- OPOZNIENIE VS CZAS


select bus_id, COUNT(*) as num
from FactDelays
group by bus_id
order by num desc

