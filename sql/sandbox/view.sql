DROP VIEW Relatives
;
CREATE VIEW Relatives AS (
	SELECT p.*, r.relative, r.relation 
	FROM Person p, Relation r
	WHERE p.id = r.person
)
;
select * from Relatives
;
