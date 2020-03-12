if coalesce(OBJECT_ID('mbucolumn'), 0) > 0 

 

begin 

 

drop table dbo.mbucolumns

 

end 

 

create table dbo.mbucolumns (tablename varchar(1000), column_name varchar(1000), tschema varchar(1000), id int identity)
insert into dbo.mbucolumns
select distinct TABLE_NAME, COLUMN_NAME, TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS 

 

declare @startid int
declare @endid int
declare @SQL varchar(4000)

 

declare @tablename varchar(1000)
declare @columnname varchar(1000)
declare @tschema varchar(1000)
declare @newcolumnname varchar(1000)
set @startid = (select min(id) from dbo.mbucolumns)
set @endid = (select MAX(id) from dbo.mbucolumns)

 


while @startid<=@endid
begin
    set @tablename = (select tablename from dbo.mbucolumns where id = @startid)
    set @columnname = (select column_name from dbo.mbucolumns where id = @startid)
    set @tschema = (select tschema from dbo.mbucolumns where id = @startid)
    set @newcolumnname = REPLACE(@columnname,' ','_')
    
--set @SQL = 'exec sp_rename '''+'['+@tschema+ '].'+@tablename+'.'+'['+@columnname+']'', '+ @newcolumnname+ ',''Column'''
			

            set @sql = 'update Src.[' + @tableName + '] 
            set [' + @columnname + '] = replace([' + @columnname + '], ''NULL'', NULL) 
            where charIndex(''NULL'', [' + @columnname + ']) > 0 '
print @sql

 

exec(@sql)

 

set @startid= @startid+1
end