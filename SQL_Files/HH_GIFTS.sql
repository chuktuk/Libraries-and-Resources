

  If exists
	(select * from [SIUF_390_Src].INFORMATION_SCHEMA.TABLES
	WHERE TABLE_NAME = 'zBB_GIFT_HH')
  BEGIN
    DROP TABLE [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  END

  
  If not exists
	(select * from [SIUF_390_Src].INFORMATION_SCHEMA.TABLES
	WHERE TABLE_NAME = 'zBB_GIFT_HH')
  BEGIN
	CREATE TABLE [SIUF_390_Src].[Src].[zBB_GIFT_HH]
	(
	[RECEIPT_NUMBER] nvarchar(20),
	[DONOR_ID] nvarchar(20),
	[GIFT_ASSOCIATED_CODE] nvarchar(10),
	[ORIG_GIFT_AMT] money,
	[HH] nvarchar(10),
	[GIFT_AMT] money,
	[SC_AMT] money,
	[MEM] money
	)

	INSERT INTO [SIUF_390_Src].[Src].[zBB_GIFT_HH]
	([RECEIPT_NUMBER], [DONOR_ID], [GIFT_ASSOCIATED_CODE], [ORIG_GIFT_AMT])
  
  select 
  [GIFT_RECEIPT_NUMBER]
  , [GIFT_DONOR_ID]
  , [GIFT_ASSOCIATED_CODE]
  , [GIFT_ASSOCIATED_AMOUNT]
  FROM [SIUF_390_Src].[Src].[GIFT] g1
  WHERE 'P' IN (SELECT [GIFT_ASSOCIATED_CODE] FROM [SIUF_390_Src].[Src].[GIFT] g2
				WHERE g1.[GIFT_RECEIPT_NUMBER] = g2.[GIFT_RECEIPT_NUMBER])
		and 'J' IN (SELECT [GIFT_ASSOCIATED_CODE] FROM [SIUF_390_Src].[Src].[GIFT] g2
				WHERE g1.[GIFT_RECEIPT_NUMBER] = g2.[GIFT_RECEIPT_NUMBER])
	order by [GIFT_RECEIPT_NUMBER], [GIFT_ASSOCIATED_CODE] desc

  UPDATE [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  SET [HH] = 'Y'
  -- select [ID_NUMBER], [PRIMARY_SPOUSE_ENTITY_IND]
  FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  WHERE [DONOR_ID] IN (SELECT [ID_NUMBER] FROM [SIUF_390_Src].[Src].[ENTITY]
					   WHERE [PRIMARY_SPOUSE_ENTITY_IND] = 'Y')

  UPDATE [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  SET [HH] = 'Y'
  -- select *
  FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  WHERE RECEIPT_NUMBER NOT IN (SELECT [RECEIPT_NUMBER] 
							   FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH]
							   WHERE [HH] = 'Y')
  AND [GIFT_ASSOCIATED_CODE] = 'P'

  UPDATE [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  SET [GIFT_AMT] = (SELECT tmp.totes FROM (SELECT RECEIPT_NUMBER, SUM([ORIG_GIFT_AMT]) as totes
				    FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH] 
				    GROUP BY RECEIPT_NUMBER) tmp
					WHERE g.RECEIPT_NUMBER = tmp.RECEIPT_NUMBER) 
  FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH] g
  WHERE [HH] = 'Y' --AND [GIFT_ASSOCIATED_CODE] NOT IN ('H', 'M')

  UPDATE [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  SET [SC_AMT] = (SELECT MAX([GIFT_AMT]) FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH] tmp
				  WHERE g.RECEIPT_NUMBER = tmp.RECEIPT_NUMBER
				  AND tmp.HH = 'Y')
  FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH] g
  WHERE [HH] IS NULL --AND [GIFT_ASSOCIATED_CODE] NOT IN ('H', 'M')

  -- test this
  UPDATE [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  SET [GIFT_AMT] = (SELECT MAX([GIFT_AMT]) FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH] tmp
				  WHERE g.RECEIPT_NUMBER = tmp.RECEIPT_NUMBER
				  AND tmp.HH = 'Y')
  FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH] g
  WHERE [GIFT_ASSOCIATED_CODE] = 'P' AND EXISTS (SELECT * FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH] g2
												 WHERE g2.[GIFT_ASSOCIATED_CODE] = 'H' AND g2.[HH] = 'Y'
												 AND g.[RECEIPT_NUMBER] = g2.[RECEIPT_NUMBER])

  UPDATE [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  SET [GIFT_AMT] = NULL, [SC_AMT] = NULL
  WHERE [GIFT_ASSOCIATED_CODE] IN ('H', 'M')

  UPDATE [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  SET [SC_AMT] = NULL
  WHERE [GIFT_AMT] IS NOT NULL

  UPDATE [SIUF_390_Src].[Src].[zBB_GIFT_HH]
  SET [MEM] = (SELECT MAX([GIFT_AMT]) FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH] tmp
				  WHERE g.RECEIPT_NUMBER = tmp.RECEIPT_NUMBER)
				  --AND tmp.HH = 'Y')
  FROM [SIUF_390_Src].[Src].[zBB_GIFT_HH] g
  WHERE [GIFT_ASSOCIATED_CODE] IN ('H', 'M')

  -- select * from [SIUF_390_Src].[Src].[zBB_GIFT_HH] where gift_associated_code not IN ('H', 'M') AND ([gift_amt] is null and [sc_amt] is null)     receipt_number = '0000366106'

  -- select * from [SIUF_390_Src].[Src].[zBB_GIFT_HH] where receipt_number = '0000625036'

END

