USE DepositoVehicular_DB
GO

CREATE TABLE [dbo].[Respondientes](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[TipoRespondiente] [int] NOT NULL,
	[IdentificacionRespondiente] [nvarchar](64) NULL,
	[NombresRespondiente] [nvarchar](64) NULL,
	[ApellidosRespondiente] [nvarchar](64) NULL,
	[TelefonoRespondiente] [nvarchar](50) NULL,
	[FechaCreacion] [datetime] NOT NULL,
	[FechaActualizacion] [datetime] NULL,
	[Activo] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO