USE [DepositoVehicular_DB]
GO

/****** Object:  Table [dbo].[IncidenteVehiculos]    Script Date: 03/06/2025 05:36:30 p. m. ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[IncidenteVehiculos]') AND type in (N'U'))
DROP TABLE [dbo].[IncidenteVehiculos]
GO

/****** Object:  Table [dbo].[IncidenteVehiculos]    Script Date: 03/06/2025 05:36:30 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[IncidenteVehiculos](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IncidenteId] [int] NOT NULL,
	[NumeroVehiculo] [tinyint] NOT NULL,
	[TipoVehiculo] [int] NOT NULL,
	[SinPlacas] [bit] NOT NULL,
	[LugarOrigenPlacas] [int] NOT NULL,
	[NumeroPlaca] [nvarchar](50) NOT NULL,
	[NumeroSerie] [nvarchar](50) NULL,
	[MarcaId] [int] NOT NULL,
	[LineaVehiculo] [nvarchar](100) NULL,
	[ModeloVehiculo] [nvarchar](10) NULL,
	[Color] [nvarchar](20) NULL,
	[NombresConductor] [nvarchar](64) NULL,
	[ApellidosConductor] [nvarchar](128) NULL,
	[ObservacionesVehiculo] [nvarchar](512) NULL,
	[CreadoPor] [int] NOT NULL,
	[FechaCreacion] [datetime] NOT NULL,
	[ActualizadoPor] [int] NULL,
	[FechaActualizacion] [datetime] NULL,
	[EliminadoPor] [int] NULL,
	[FechaEliminacion] [datetime] NULL,
	[Activo] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


