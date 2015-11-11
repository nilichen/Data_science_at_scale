create view corpus as
	SELECT * FROM frequency
	UNION
	SELECT 'q' as docid, 'washington' as term, 1 as count 
	UNION
	SELECT 'q' as docid, 'taxes' as term, 1 as count
	UNION 
	SELECT 'q' as docid, 'treasury' as term, 1 as count;

select max(score) from (
SELECT A.docid, B.docid, SUM(A.count * B.count) as score
FROM corpus as A join corpus as B on A.term = B.term
WHERE A.docid = 'q' and B.docid != 'q'
group by B.docid);
