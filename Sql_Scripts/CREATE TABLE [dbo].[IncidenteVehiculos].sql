USE DepositoVehicular_DB
GO

CREATE TABLE [dbo].[IncidenteVehiculos](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IncidenteId] [int] NOT NULL,
	[EstatusIncidente] [int] NOT NULL,
	[FolioVehiculo] [nvarchar](15) NOT NULL,
	[NumeroVehiculo] [tinyint] NOT NULL,
	[NumeroPlaca] [nvarchar](50) NOT NULL,
	[NumeroSerie] [nvarchar](50) NULL,
	[Marca] [int] NOT NULL,
	[TipoVehiculo] [int] NULL,
	[LineaVehiculo] [nvarchar](100) NULL,
	[ModeloVehiculo] [nvarchar](50) NULL,
	[NombresConductor] [nvarchar](64) NULL,
	[ApellidosConductor] [nvarchar](128) NULL,
	[ObservacionesVehiculo] [nvarchar](512) NULL,
	[PlacasEstado] [int] NULL,
	[PlacasExtrangeras] [bit] NOT NULL,
	[Observaciones] [nvarchar](512) NULL,
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