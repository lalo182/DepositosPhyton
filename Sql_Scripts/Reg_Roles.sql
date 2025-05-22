USE [DepositoVehicular_DB]
GO

CREATE VIEW Reg_Roles AS

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