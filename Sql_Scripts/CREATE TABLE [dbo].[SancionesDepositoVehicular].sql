USE DepositoVehicular_DB
GO

CREATE TABLE [dbo].[SancionesDepositoVehicular](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[DepositoVehicularId] [int] NOT NULL,
	[Observaciones] [nvarchar](128) NULL,
	[TipoPenalizacion] [nvarchar](128) NULL,
	[PeriodoPenalizacion] [nvarchar](128) NULL,
	[CreadoPorAdminId] [int] NOT NULL,
	[FechaCreacion] [datetime] NOT NULL,
	[Activo] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO