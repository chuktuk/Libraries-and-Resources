-- comparing two tables
-- rank scores
-- rank returned keys when score ties

with v5 as (
    select distinct
        session.quoteback as quoteback,
        r.entitykey as entitykey,
        rank() over(partition by session.quoteback order by r.score desc) as cand_rank,
        rank() over(partition by session.quoteback order by r.entitykey) as entity_sorted
    from kib_v5_output o,
        unnest(resolved_entities) r
),
v5b as (
    select distinct
        session.quoteback as quoteback,
        r.entitykey as entitykey,
        rank() over(partition by session.quoteback order by r.score desc) as cand_rank,
        rank() over(partition by session.quoteback order by r.entitykey) as entity_sorted
    from kib_v5b_output o,
        unnest(resolved_entities) r
)
select
    v5.quoteback,
    v5.entitykey,
    v5.score,
    v5b.entitykey,
    v5b.score
from v5
    full outer join v5b
        on v5.quoteback = v5b.quoteback
        and v5.candidate_rank = v5b.candidate_rank
        and v5.entity_sorted = v5b.entity_sorted
where v5.entitykey != v5b.entitykey  -- look for differences, no results, they all match
order by v5.quoteback, v5.score desc, v5.entitykey
;
