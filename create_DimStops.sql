USE [DWH]
GO

/****** Object:  Table [dbo].[DimStops]    Script Date: 10.06.2023 00:46:58 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimStops](
	[stop_id] [varchar](50) NOT NULL,
	[zespol_id] [varchar](50) NOT NULL,
	[slupek_id] [varchar](50) NOT NULL,
	[nazwa_zespolu] [varchar](50) NULL,
	[lat] [float] NOT NULL,
	[lon] [float] NOT NULL,
	PRIMARY KEY(stop_id)
) ON [PRIMARY]
GO

