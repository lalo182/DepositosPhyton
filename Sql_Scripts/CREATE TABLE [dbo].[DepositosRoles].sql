USE DepositoVehicular_DB
GO

CREATE TABLE [dbo].[DepositosRoles](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[DepositoVehicularId] [int] NOT NULL,
	[Anio] [int] NOT NULL,
	[Mes] [int] NOT NULL,
	[Dias] [nvarchar](128) NOT NULL,
	[CreadoPor] [int] NOT NULL,
	[FechaCreacion] [datetime] NOT NULL,
	[ActualizadoPor] [int] NULL,
	[FechaActualizacion] [datetime] NULL,
	[Activo] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO