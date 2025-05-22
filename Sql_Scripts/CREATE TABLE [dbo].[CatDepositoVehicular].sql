USE [DepositoVehicular_DB]
GO

/****** Object:  Table [dbo].[CatDepositoVehicular]    Script Date: 22/05/2025 11:20:59 a. m. ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CatDepositoVehicular]') AND type in (N'U'))
DROP TABLE [dbo].[CatDepositoVehicular]
GO

/****** Object:  Table [dbo].[CatDepositoVehicular]    Script Date: 22/05/2025 11:20:59 a. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[CatDepositoVehicular](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[RazonSocial] [nvarchar](256) NOT NULL,
	[RepresentanteLegal] [nvarchar](128) NOT NULL,
	[CorreoElectronicoContacto] [nvarchar](64) NOT NULL,
	[NombreCompletoContactos] [nvarchar](256) NOT NULL,
	[Telefonos] [nvarchar](50) NOT NULL,
	[DireccionDeposito] [nvarchar](256) NOT NULL,
	[RegionId] [int] NOT NULL,
	[Ubicacion] [nvarchar](64) NULL,
	[Latitud] [nvarchar](50) NULL,
	[Longitud] [nvarchar](50) NULL,
	[CreadoPorAdminId] [int] NOT NULL,
	[FechaCreacion] [datetime] NOT NULL,
	[ActualizadoPorAdminId] [int] NULL,
	[FechaActualizacion] [datetime] NULL,
	[Activo] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


