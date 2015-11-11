SELECT SUM(A.count * B.count)
FROM frequency as A join frequency as B on A.term = B.term
WHERE 
A.docid = '10080_txt_crude'
and B.docid = '17035_txt_earn'
;
