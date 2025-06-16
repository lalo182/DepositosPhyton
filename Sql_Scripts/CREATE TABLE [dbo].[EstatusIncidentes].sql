USE [DepositoVehicular_DB]
GO

CREATE TABLE [dbo].[EstatusIncidentes](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IncidenteId] [int] NOT NULL,
	[DepositoVehicularId] [int] NOT NULL,
	[Estatus] [nvarchar](32) NOT NULL,
	[FechaMovimiento] [datetime] NOT NULL,
	[CreadoPor] [int] NOT NULL,
	[Activo] [bit] NOT NULL,
PRIMARY KEY CLUSTERED
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


