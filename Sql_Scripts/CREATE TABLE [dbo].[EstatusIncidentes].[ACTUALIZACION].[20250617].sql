USE [DepositoVehicular_DB]
GO

/****** Object:  Table [dbo].[EstatusIncidentes]    Script Date: 17/06/2025 10:19:07 a. m. ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[EstatusIncidentes]') AND type in (N'U'))
DROP TABLE [dbo].[EstatusIncidentes]
GO

/****** Object:  Table [dbo].[EstatusIncidentes]    Script Date: 17/06/2025 10:19:07 a. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[EstatusIncidentes](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IncidenteId] [int] NOT NULL,
	[DepositoVehicularId] [int] NOT NULL,
	[EstatusId] [int] NOT NULL,
	[FechaMovimiento] [datetime] NOT NULL,
	[CreadoPor] [int] NOT NULL,
	[Activo] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


