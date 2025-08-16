-- Canonicalized ATS event table
CREATE TABLE candidate_events (
  candidate_id INT,
  job_id INT,
  role TEXT,
  location TEXT,
  source TEXT,
  stage TEXT,
  stage_entered_at DATE,
  diversity_flag INT
);

-- Example: applied -> hired conversion by source
WITH last_stage AS (
  SELECT candidate_id, MAX(stage) AS last_stage
  FROM candidate_events
  GROUP BY candidate_id
)
SELECT source,
       COUNT(*) FILTER (WHERE last_stage IN ('Phone Screen','Hiring Manager','Onsite','Offer','Hired'))::float / COUNT(*) AS to_phone_screen,
       COUNT(*) FILTER (WHERE last_stage IN ('Onsite','Offer','Hired'))::float / COUNT(*) AS to_onsite,
       COUNT(*) FILTER (WHERE last_stage IN ('Offer','Hired'))::float / COUNT(*) AS to_offer,
       COUNT(*) FILTER (WHERE last_stage = 'Hired')::float / COUNT(*) AS to_hired
FROM candidate_events ce
JOIN last_stage ls USING (candidate_id)
GROUP BY source
ORDER BY to_hired DESC;
