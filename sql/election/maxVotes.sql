select a.year, a.state, a.candidate, a.candidatevotes from state_senate a
INNER JOIN (
	select state, max (candidatevotes) maxvotes from state_senate
	where year = 2018
	group by state
) b
on a.state = b.state and a.candidatevotes = b.maxVotes
where a.year = 2018
order by state asc
;

