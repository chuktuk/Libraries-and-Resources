


-- ========= there is a subquery method in Update_Highest_Nbr file ================


/*  Testing
select [EMPLID], Max([STDNT_DEGR])
FROM <Src>.[Src].[DEGREES]
Group by [EMPLID]

select * 
FROM <Src>.[Src].[DEGREES]
LEFT JOIN <Src>.[Src].[TERM_TBL]
ON [COMPLETION_TERM] = [STRM]
where [EMPLID] = '0237032'  -- this one has 5 rows
;
*/



------ Set [ESRPrimAlum] -- ANALYST NOTES: Set to True for the highest number for the constituent.

---- Drop table so it will pull in the most recent set of data
If exists  
	(Select * from <Src>.[Information_Schema].[Tables]
	Where Table_Name = 'zzSTDNT_DEGR')
BEGIN
	Drop Table <Src>.[Src].[zzSTDNT_DEGR];
END

----------- Create temp table to hold highest [STDNT_DEGR] value
If NOT exists  
	(Select * from <Src>.[Information_Schema].[Tables]
	Where Table_Name = 'zzSTDNT_DEGR')	
BEGIN

	Create table <Src>.[Src].[zzSTDNT_DEGR] (EMPLID nvarchar(max), STDNT_DEGR nvarchar(max))
	--select * from <Src>.[Src].[zzSTDNT_DEGR];

	-- populate table
	INSERT INTO <Src>.[Src].[zzSTDNT_DEGR]
	(
		[EMPLID]
		, [STDNT_DEGR]
	)

	SELECT
		[EMPLID] as [EMPLID]
		, Max([STDNT_DEGR]) as [STDNT_DEGR]
	FROM <Src>.[Src].[DEGREES]
	Group by [EMPLID]
	;
END

/*
test -- should be '05'
select * from <Src>.[Src].[zzSTDNT_DEGR]
where [EMPLID] = '0237032'
;
*/


------ Update [ESRPrimAlum], [STDNT_DEGR]
UPDATE <Trg>.[dbo].[Education_School_Relationship]
Set [ESRPrimAlum] = 'True'
-- Select [ESRImpID],ESR.[SourceRow],SD.[STDNT_DEGR]
from <Trg>.[dbo].[Education_School_Relationship] ESR
INNER JOIN <Src>.[Src].[zzSTDNT_DEGR] SD
ON ESR.[ImportID] = SD.[EMPLID]
AND ESR.[SourceRow] = SD.[STDNT_DEGR]
;

/*  testing
Select * from <Trg>.[dbo].[Education_School_Relationship]
where [ImportID] =  '0237032'
;
*/

---- Dropped table before creating it again above.
--Drop Table <Src>.[Src].[zzSTDNT_DEGR]

