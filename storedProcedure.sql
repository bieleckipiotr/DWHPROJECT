use HDiSBI_projekt
go

CREATE PROCEDURE dbo.ConvertStringToFloat
    @inputString VARCHAR(255),
    @outputFloat FLOAT OUTPUT
AS
BEGIN
    SET @outputFloat = CAST(@inputString AS FLOAT);
END;


SELECT
    szer_geo AS OriginalSzerGeo,
    dlug_geo AS OriginalDlugGeo,
    c.ConvertedSzerGeo,
    c.ConvertedDlugGeo
FROM
    stops
CROSS APPLY (
    SELECT
        CONVERT(FLOAT, szer_geo) AS ConvertedSzerGeo,
        CONVERT(FLOAT, dlug_geo) AS ConvertedDlugGeo
) c;



