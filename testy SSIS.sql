use DWH
go
--Create Model

--lookup TimeID
select * from HDiSBI_projekt.dbo.schedules s
join DimTime t on t.hour_val = SUBSTRING(s.czas, 1,2)%24 and t.minute_val = SUBSTRING(s.czas, 4,2) 

--lookup stop Info
select * from HDiSBI_projekt.dbo.schedules s
join HDiSBI_projekt.dbo.Routes r 
on r.linia = s.linia and
r.kod = s.trasa and
r.nr_zespolu = s.zespol and
r.nr_przystanku = s.slupek

-- update metrics

-- lookup TimeID and DateID
select * from HDiSBI_projekt.dbo.CurrentPosition c
join DimDate d on d.Date = SUBSTRING(c.Time,1,10)
join DimTime t on t.hour_val = (SUBSTRING(c.Time,12,2)) and t.minute_val = (SUBSTRING(Time,15,2))

-- BusID lookup

select * from HDiSBI_projekt.dbo.CurrentPosition c
join DimBuses b on b.linia = c.linia and b.brygada = c.Brigade