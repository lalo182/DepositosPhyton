USE DepositoVehicular_DB
GO

CREATE TABLE [dbo].[Usuario](
	[Idusuario] [int] IDENTITY(1,1) NOT NULL,
	[Correo] [nvarchar](80) NOT NULL,
	[Clave] [nvarchar](512) NOT NULL,
	[Nombre] [nvarchar](80) NOT NULL,
	[Paterno] [nvarchar](80),
	[Materno] [nvarchar](80),
	[Numgafete] [nvarchar](80),
	[Numpatrulla] [nvarchar](80),
	[FechaExpedicionGafete] [datetime],
	[FechaVencimientoGafete] [datetime],
	[IdRol] [int]
PRIMARY KEY CLUSTERED 
(
	[Idusuario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
FOREIGN KEY([IdRol]) REFERENCES [Rol](IdRol)
) ON [PRIMARY]

GO