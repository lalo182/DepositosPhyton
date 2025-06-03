USE [DepositoVehicular_DB]
GO

/****** Object:  Table [dbo].[Incidentes]    Script Date: 03/06/2025 05:30:18 p. m. ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Incidentes]') AND type in (N'U'))
DROP TABLE [dbo].[Incidentes]
GO

/****** Object:  Table [dbo].[Incidentes]    Script Date: 03/06/2025 05:30:18 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Incidentes](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[TipoIncidente] [int] NOT NULL,
	[FolioIncidente] [nvarchar](15) NOT NULL,
	[FechaIncidente] [datetime] NOT NULL,
	[VialidadIncidente] [nvarchar](64) NULL,
	[ColoniaIncidente] [nvarchar](64) NULL,
	[ReferenciaUbicacionIncidente] [nvarchar](150) NULL,
	[LatitudUbicacionIncidente] [decimal](18, 7) NULL,
	[LongitudUbicacionIncidente] [decimal](18, 7) NULL,
	[UbicacionIncidente] [nvarchar](64) NULL,
	[MunicipioId] [int] NOT NULL,
	[RegionId] [int] NULL,
	[DepositoVehicularId] [int] NOT NULL,
	[RespondienteNombreCompleto]  [nvarchar](64) NULL,
	[RespondienteIdentificacion]  [nvarchar](64) NULL,
	[RespondienteNotas] [nvarchar](max) NULL,
	[Folio911] [nvarchar](50) NULL,
	[EstatusIncidente] [tinyint] NOT NULL,
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
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
