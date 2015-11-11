SELECT count(distinct term)
FROM frequency
where docid in ('10398_txt_earn' ,'925_txt_trade') and count = 1;