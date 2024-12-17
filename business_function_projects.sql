-- SELECT
--     l.value AS label_value,
--     ARRAY_AGG(DISTINCT CONCAT("projects/", project.number)) p_list
--   FROM
--   -- Detailed billing export table ID
--     `terraform-375010.detailed_billing_dataset.gcp_billing_export_resource_v1_0125FB_E96DD4_B48BC7`,
--     UNNEST(labels) AS l
--   WHERE
--     -- business function label key
--     l.key = "goog-resource-type"
--     AND DATE(_PARTITIONTIME) = DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY)
--     AND DATE(usage_start_time) = DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY)
--   GROUP BY 1



SELECT
    -- Extract the Business function vlaue, and the associated project ID's list
    l.value AS label_value,
    ARRAY_AGG(DISTINCT CONCAT("projects/", project.number)) p_list
  FROM
    `Detailed_Billing_Export_Table_ID` ,
    UNNEST(labels) AS l
  WHERE
    -- Business Function label key
    l.key = "business_function"
    -- Filter data from two days ago
    AND DATE(_PARTITIONTIME) = DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY)
    AND DATE(usage_start_time) = DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY)
  GROUP BY 1




  