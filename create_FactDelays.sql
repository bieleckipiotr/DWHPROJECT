USE [DWH]
GO

/****** Object:  Table [dbo].[FactDelays]    Script Date: 10.06.2023 21:42:44 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[FactDelays](
	[bus_id] [varchar](50) NOT NULL,
	[stop_id] [varchar](50) NOT NULL,
	[scheduled_arr_id] [varchar](50) NOT NULL,
	[Time_id] [int] NOT NULL,
	[Date_id] [int] NOT NULL,
	[lat] [float] NOT NULL,
	[lon] [float] NOT NULL,
	[delay] [int],
	[distance] [int],
	[time_estimated_id] [int]
) ON [PRIMARY]
GO

