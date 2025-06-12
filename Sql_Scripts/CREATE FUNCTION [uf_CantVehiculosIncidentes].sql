USE DepositoVehicular_DB
GO

CREATE FUNCTION uf_CantVehiculosIncidentes(@IncidenteId INT)
	   RETURNS INT
	BEGIN
		DECLARE @total INT 
		SET @total = (SELECT COUNT(1) 
					    FROM IncidenteVehiculos 
					   WHERE IncidenteId = @IncidenteId)
		RETURN @total
	END