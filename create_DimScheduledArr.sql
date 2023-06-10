USE [DWH]
GO

/****** Object:  Table [dbo].[DimScheduledArr]    Script Date: 10.06.2023 00:40:52 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimScheduledArr](
	[scheduled_arr_id] [varchar](255) NOT NULL,
	[time_scheduled_id] [int] NOT NULL,
	[kod_trasy] [varchar](50) NOT NULL,
	zespol_id varchar(50) NOT NULL,
	slupek_id varchar(50) NOT NULL,
	linia varchar(50) NOT NULL,
	brygada varchar(50) NOT NULL,
	StopOnRoute int NOT NULL,
	TypeName varchar(50),
	PRIMARY KEY(scheduled_arr_id)
) ON [PRIMARY]
GO


use HDiSBI_projekt
go
select count(*) from routes