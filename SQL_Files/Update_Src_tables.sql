


/*
Training Note:
Looking for skewed records & query row in the tables

*/


--select *
  --FROM [RIC_Src_ARG].[Src].[Constituents]

Delete
--select *
  FROM [RIC_Src_ARG].[Src].[ADDRESSES]
where IsNumeric([CNST_TYPE]) = 0

Delete
--select *
  FROM [RIC_Src_ARG].[Src].[SEASONAL_ADDRESSES]
where IsNumeric([EMPLID]) = 0

--select *
  --FROM [RIC_Src_ARG].[Src].[Phones]

Delete
--select *
  FROM [RIC_Src_ARG].[Src].[ETHNIC_GROUPS]
where IsNumeric([CNST_TYPE]) = 0

--select *
  --FROM [RIC_Src_ARG].[Src].[Involvements]

Delete
--select *
  FROM [RIC_Src_ARG].[Src].[Service_indicators]
where IsNumeric([EMPLID]) = 0

Delete
--select *
  FROM [RIC_Src_ARG].[Src].[NAME_HISTORY]
where IsNumeric([CNST_TYPE]) = 0

--select *
  --FROM [RIC_Src_ARG].[Src].[DEGREES]

--select *
  --FROM [RIC_Src_ARG].[Src].[Legacy_degrees]

Delete
--select *
  FROM [RIC_Src_ARG].[Src].[Relationships]
where IsNumeric([EMPLID]) = 0

--select *
  --FROM [RIC_Src_ARG].[Src].[WORK]

Delete
--select *
  FROM [RIC_Src_ARG].[Src].[Designation_codes]
where IsNumeric([DESIGNATION]) = 0

--select *
  --FROM [RIC_Src_ARG].[Src].[GIFT_DETAIL]






------ Populate the new name fields added to [Relationships]
/*
Select *
FROM <Src>.[Src].[Relationships]
*/


UPDATE <Src>.[Src].[Relationships]
Set [first] = LTrim(Right([Name], Len([Name])-CharIndex(',', [Name])))
-- Select [Name], LTrim(Right([Name], Len([Name])-CharIndex(',', [Name])))
FROM <Src>.[Src].[Relationships]
Where IsNull([Name],'')<>''  -- value in [Name]
AND IsNull([EMPLID_RELATED],'')='' -- [EMPLID_RELATED] is blank
;


UPDATE <Src>.[Src].[Relationships]
Set [last] = RTrim(Left([Name], CharIndex(',', [Name])-1))
-- Select [Name], RTrim(Left([Name], CharIndex(',', [Name])-1))
FROM <Src>.[Src].[Relationships]
Where IsNull([Name],'')<>''  -- value in [Name]
AND IsNull([EMPLID_RELATED],'')='' -- [EMPLID_RELATED] is blank
;


---- pull suffixes out of [first] field & update [first]
UPDATE <Src>.[Src].[Relationships]
Set [Suffix] = ', ' + RTrim(Left([First], CharIndex(',', [First])-1))
, [first] = LTrim(Right([First], Len([First])-CharIndex(',', [First])))
-- Select [First], ', ' + RTrim(Left([First], CharIndex(',', [First])-1)), LTrim(Right([First], Len([First])-CharIndex(',', [First])))
FROM <Src>.[Src].[Relationships]
Where IsNull([First],'')<>''  -- value in [First]
AND CharIndex(',', [First])>0
;

/*  testing the parsing
Select [Name],[first], [last], [suffix]
FROM <Src>.[Src].[Relationships]
Where IsNull([EMPLID_RELATED],'')='' -- [EMPLID_RELATED] is blank
*/








-------- Removing "NULL" from [Legacy_degrees]
UPDATE <Src>.[Src].[Legacy_degrees]
Set [AV_CLASS_YR] = NULL
-- select [AV_CLASS_YR]
from <Src>.[Src].[Legacy_degrees]
where [AV_CLASS_YR] = 'NULL'
;
------------------
UPDATE <Src>.[Src].[Legacy_degrees]
Set [GVT_DESCR70] = NULL
-- select [GVT_DESCR70]
from <Src>.[Src].[Legacy_degrees]
where [GVT_DESCR70] = 'NULL'
;









