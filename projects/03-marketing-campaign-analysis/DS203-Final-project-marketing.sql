--Create table
CREATE TABLE marketing (
	CampaignID VARCHAR(50),
	StartDate DATE,
	EndDate DATE,
	Channel VARCHAR(50),
	Impressions INT,
	Clicks INT,
	Leads INT,
	Conversions INT,
	Cost_USD FLOAT,
	Revenue_USD FLOAT,
	ROI FLOAT
);

--Import .csv file
COPY marketing(CampaignID, StartDate, EndDate, Channel, Impressions, Clicks, Leads, Conversions, Cost_USD, Revenue_USD, ROI)
FROM 'D:\marketing_campaign_performance_10000.csv'
DELIMITER ','
CSV HEADER;

--Check
SELECT * FROM marketing;

--View--

--channel ROI View--
CREATE OR REPLACE VIEW channel_roi_v AS
SELECT Channel, ROUND(AVG(ROI)::numeric, 3) as avg_roi
FROM Marketing
GROUP BY Channel;

SELECT * FROM channel_roi_v

--channel COST View--
CREATE OR REPLACE VIEW channel_cost_v AS
SELECT Channel, ROUND(SUM(Cost_USD)::numeric, 3) as sum_cost
FROM Marketing
GROUP BY Channel;

SELECT * FROM channel_cost_v

--channel REVENUE View--
CREATE OR REPLACE VIEW channel_revenue_v AS
SELECT Channel, ROUND(SUM(Revenue_USD)::numeric, 3) as sum_revenue
FROM Marketing
GROUP BY Channel;

SELECT * FROM channel_revenue_v

--channel CONVERSIONS View--
CREATE OR REPLACE VIEW channel_convers_v AS
SELECT Channel, SUM(Conversions) as sum_convers
FROM Marketing
GROUP BY Channel;

SELECT * FROM channel_convers_v

----Function---

CREATE OR REPLACE FUNCTION marketing_cost_f (name_channel TEXT)
RETURNS TABLE(
	channel_name VARCHAR(50), 
	avg_roi NUMERIC, 
	sum_cost NUMERIC, 
	sum_revenue NUMERIC, 
	sum_convers FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
	RETURN QUERY
	SELECT 
		Channel, 
		ROUND(AVG(ROI)::numeric, 3) as avg_roi, 
		ROUND(SUM(Cost_USD)::numeric, 3) as sum_cost, 
		ROUND(SUM(Revenue_USD)::numeric, 3) as sum_revenue, 
		SUM(Conversions) :: double precision as sum_convers
	FROM marketing
	WHERE Channel = name_channel
	GROUP BY Channel;

END; $$;

SELECT * FROM marketing_cost_f('Social');


SELECT 
	Channel, 
	ROUND(AVG(ROI)::numeric, 3) as avg_roi,  
	ROUND(SUM(Cost_USD)::numeric, 3) as sum_cost, 
	ROUND(SUM(Revenue_USD)::numeric, 3) as sum_revenue, 
	SUM(Conversions) :: double precision as sum_convers
FROM Marketing
WHERE StartDate BETWEEN '2025-04-01' AND '2025-04-30'
GROUP BY Channel;




