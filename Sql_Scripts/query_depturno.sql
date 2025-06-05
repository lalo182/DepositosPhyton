USE
DepositoVehicular_DB
GO
SELECT Dep, Nombre, Listadia FROM Reg_Roles 
WHERE act=1 AND mes=MONTH(GETDATE()) AND anio=YEAR(GETDATE()) AND regid=3 and SUBSTRING(Listadia, 1,3) LIKE '%1,%'
OR act=1 AND mes=MONTH(GETDATE()) AND anio=YEAR(GETDATE()) AND regid=3 and Listadia LIKE '%,1,%'