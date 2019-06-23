select a.year, a.state, a.candidate, a.candidatevotes from state_senate a
INNER JOIN (
	select year, state, max (candidatevotes) maxvotes from state_senate
	group by year, state
) b
on a.year = b.year and a.state = b.state and a.candidatevotes = b.maxVotes
where a.year = 2018
order by state asc
;

