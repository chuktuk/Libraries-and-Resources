
/*
Using update statement combined with subquery to set ORIsprimary.
Same technique would work for ESRPrimAlum.

This assumes that a constituent has multiple org relat.
We are setting primary to the one with the max sequence_nbr, 
which is supplied with the data.

The ORImpID has been set as the ConsID + Sequence_Nbr,
so the max sequence_nbr and the max ORImpID are the same
record for that constituent.
*/

  -- this works, but the one down lower works better
  UPDATE [TRAINING_RIC_Trg].[dbo].[Organization_Relationship]
Set [ORIsPrimary] = 'True'
 -- SELECT DISTINCT [ImportID], [ORImpID], [ORIsprimary]
  FROM [TRAINING_RIC_Trg].[dbo].[Organization_Relationship] ORG
INNER JOIN [TRAINING_RIC_Src].[Src].[WORK] W
ON ORG.[ImportID] = W.[EMPLID]
AND ORG.[NOTES] = 
	(SELECT [temp1].[NUM] FROM (SELECT [EMPLID], MAX([SEQUENCE_NBR]) AS [NUM]
		FROM [TRAINING_RIC_Src].[Src].[WORK] W
		GROUP BY [EMPLID])
		AS [temp1]
		WHERE [temp1].[EMPLID] = W.[EMPLID])
ORDER BY [ORImpID]
;

select count(*)
from [TRAINING_RIC_Trg].[dbo].[Organization_Relationship]
where [ORIsprimary] = 'False'



-- This one works the best
UPDATE [TRAINING_RIC_Trg].[dbo].[Organization_Relationship]
SET [ORIsprimary] = 'True'
-- SELECT [temp1].[ImportID], [temp1].[ORImpID], org.[ORIsprimary]
FROM (SELECT [ImportID], MAX([ORImpID]) AS [ORImpID]
		FROM [TRAINING_RIC_Trg].[dbo].[Organization_Relationship]
		GROUP BY [ImportID]) AS [temp1]
INNER JOIN [TRAINING_RIC_Trg].[dbo].[Organization_Relationship] org
	ON [temp1].[ORImpID] = org.[ORImpID]

-- or could use if stored SEQUENCE_NBR in notes,
-- but didn't append SEQUENCE_NBR to the ORImpID
UPDATE [TRAINING_RIC_Trg].[dbo].[Organization_Relationship]
SET [ORIsprimary] = 'True'
-- SELECT [temp1].[ImportID], [temp1].[SEQUENCE_NBR], org.[ORImpID], org.[ORIsprimary]
FROM (SELECT [ImportID], MAX([NOTES]) AS [SEQUENCE_NBR]
		FROM [TRAINING_RIC_Trg].[dbo].[Organization_Relationship]
		GROUP BY [ImportID]) AS [temp1]
INNER JOIN [TRAINING_RIC_Trg].[dbo].[Organization_Relationship] org
	ON [temp1].[ImportID] = org.[ImportID]
	AND [temp1].[SEQUENCE_NBR] = org.[NOTES]
