select count(*) from (
SELECT distinct docid
FROM frequency
where term = 'transaction'
intersect 
select distinct docid
from frequency
where term = 'world');

