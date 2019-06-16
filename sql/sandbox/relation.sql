DROP TABLE Relation
;

CREATE TABLE Relation (
	person text, relative text, relation text,
	PRIMARY KEY (person, relative)
)
;

INSERT INTO Relation (person, relative, relation) VALUES
	('sanjay', 'soo', 'husband'),
	('sanjay', 'rhea', 'father'),
	('sanjay', 'krsna', 'father'),

	('rhea', 'soo', 'daughter'),
	('rhea', 'sanjay', 'daughter'),
	('krsna', 'sanjay', 'daughter'),
	('krsna', 'soo', 'daughter'),

	('soo', 'sanjay', 'wife'),
	('soo', 'krsna', 'mother'),
	('soo', 'rhea', 'mother'),

	('rhea', 'krsna', 'sister'),
	('krsna', 'rhea', 'sister')

;

select * from Relation;


