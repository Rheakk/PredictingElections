select a.* from Relatives a
INNER JOIN (
	select relation, max (height) maxheight from Relatives
	where relation = 'daughter'
	group by relation
) b
on a.relation = b.relation and a.height = b.maxheight
;

