USE DepositoVehicular_DB
GO

CREATE TABLE [dbo].[Incidentes](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[TipoIncidente] [int] NOT NULL,
	[FolioIncidente] [nvarchar](15) NOT NULL,
	[FechaIncidente] [datetime] NOT NULL,
	[MunicipioId] [int] NOT NULL,
	[RegionId] [int] NULL,
	[DepositoVehicular] [int] NOT NULL,
	[VialidadIncidente] [nvarchar](64) NULL,
	[ColoniaIncidente] [nvarchar](64) NULL,
	[ReferenciaUbicacionIncidente] [nvarchar](150) NULL,
	[LatitudUbicacionIncidente] [decimal](18, 7) NULL,
	[LongitudUbicacionIncidente] [decimal](18, 7) NULL,
	[UbicacionIncidente] [nvarchar](64) NULL,
	[RespondienteId] [int] NULL,
	[NotasRespondiente] [nvarchar](max) NULL,
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