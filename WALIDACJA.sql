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
select d.linia, COUNT(*) as cnt
from FactDelays f
join DimBuses d on f.bus_id=d.bus_id
group by d.linia
order by cnt desc

select d.linia, d2.StopOnRoute, avg(f.delay) as avg_delay, count(d.bus_id) as number_of_vehicles
from FactDelays f
join DimBuses d on f.bus_id= d.bus_id
join DimScheduledArr d2 on f.scheduled_arr_id=d2.scheduled_arr_id
where f.delay > -10
group by d.linia, d2.StopOnRoute
order by d.linia




-- ROZK£ADY
select d3.nazwa_zespolu, d1.linia, d4.TimeFull, d5.TimeFull
from FactDelays f
join DimBuses d1 on f.bus_id=d1.bus_id
join DimScheduledArr d2 on f.scheduled_arr_id=d2.scheduled_arr_id
join DimStops d3 on f.stop_id=d3.stop_id
join DimTime d4 on d2.time_scheduled_id=d4.TimeID
join DimTime d5 on f.time_estimated_id=d5.TimeID
order by d3.nazwa_zespolu asc, d1.linia asc, d4.TimeFull


-- OPOZNIENIE VS CZAS
select d.hour_val, avg(f.delay) as avg_delay, COUNT(f.bus_id) as number_of_vehicles
from FactDelays f
join DimTime d on f.Time_id=d.TimeID
where f.delay > -10
group by d.hour_val

