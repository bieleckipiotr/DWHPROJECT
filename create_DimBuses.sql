USE [DWH]
GO

/****** Object:  Table [dbo].[DimBuses]    Script Date: 10.06.2023 00:46:16 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimBuses](
	[bus_id] [varchar](50) NOT NULL,
	[linia] [varchar](50) NOT NULL,
	[brygada] [varchar](50) NOT NULL,
	PRIMARY KEY(bus_id)
) ON [PRIMARY]
GO

