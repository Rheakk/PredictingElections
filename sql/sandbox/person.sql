DROP TABLE Person
;

CREATE TABLE Person (
	id text unique, name text, sex char, height int,
	PRIMARY KEY (id)
)
;

INSERT INTO Person (id, name, sex, height) VALUES
	('sanjay', 'Sanjay Kothari', 'M', 168),	
	('soo', 'Soo Kothari', 'F', 154),
	('rhea', 'Rhea Kothari', 'F', 160),
	('krsna', 'Krsna Kothari', 'F', 162)
;

select * from Person;


