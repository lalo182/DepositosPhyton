USE [master]
GO
/****** Object:  Database [DepositoVehicular_DB]    Script Date: 22/05/2025 05:26:47 p. m. ******/
CREATE DATABASE [DepositoVehicular_DB]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'DepositoVehicular_DB', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\DepositoVehicular.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'DepositoVehicular_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\DepositoVehicular_log.ldf' , SIZE = 73728KB , MAXSIZE = 524288KB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [DepositoVehicular_DB] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [DepositoVehicular_DB].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [DepositoVehicular_DB] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET ARITHABORT OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [DepositoVehicular_DB] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [DepositoVehicular_DB] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET  DISABLE_BROKER 
GO
ALTER DATABASE [DepositoVehicular_DB] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [DepositoVehicular_DB] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET RECOVERY FULL 
GO
ALTER DATABASE [DepositoVehicular_DB] SET  MULTI_USER 
GO
ALTER DATABASE [DepositoVehicular_DB] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [DepositoVehicular_DB] SET DB_CHAINING OFF 
GO
ALTER DATABASE [DepositoVehicular_DB] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [DepositoVehicular_DB] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [DepositoVehicular_DB] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [DepositoVehicular_DB] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'DepositoVehicular_DB', N'ON'
GO
ALTER DATABASE [DepositoVehicular_DB] SET QUERY_STORE = ON
GO
ALTER DATABASE [DepositoVehicular_DB] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [DepositoVehicular_DB]
GO
/****** Object:  Table [dbo].[CatRegion]    Script Date: 22/05/2025 05:26:47 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CatRegion](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[NombreRegion] [nvarchar](80) NOT NULL,
	[Activo] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DepositosRoles]    Script Date: 22/05/2025 05:26:47 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
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
/****** Object:  Table [dbo].[CatDepositoVehicular]    Script Date: 22/05/2025 05:26:47 p. m. ******/
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
/****** Object:  View [dbo].[Reg_Roles]    Script Date: 22/05/2025 05:26:47 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[Reg_Roles] AS

SELECT Dep, Nombre, Listadia, act, anio, mes, regid
FROM
(SELECT Id as Dep, RazonSocial as Nombre, RegionId as Regid, T1.Listadia, T1.act, t1.anio, t1.mes
FROM Dbo.CatDepositoVehicular 
INNER JOIN (SELECT Dias AS Listadia, DepositoVehicularId as Iddep, Activo as act, anio, mes FROM Dbo.DepositosRoles) AS T1
ON Id=iddep) as t2
INNER JOIN
Dbo.CatRegion
ON Id=RegID

GO
/****** Object:  Table [dbo].[CatMunicipio]    Script Date: 22/05/2025 05:26:47 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CatMunicipio](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Municipio] [nvarchar](80) NOT NULL,
	[RegionId] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SancionesDepositoVehicular]    Script Date: 22/05/2025 05:26:47 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
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
USE [master]
GO
ALTER DATABASE [DepositoVehicular_DB] SET  READ_WRITE 
GO
