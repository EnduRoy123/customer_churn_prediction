create database churn;
use churn;
SHOW TABLES;
RENAME TABLE `customer-churn-analysis` TO `customer_churn_analysis`;
select*from customer_churn_analysis;
#SQL query 1: Total customers
select count(*) AS total_customers from customer_churn_analysis;
#SQL query 2: Customers who left
select churn,count(*) as total_churn from customer_churn_analysis group by churn;
#: Overall churn percentage who left the company
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customer_churn_analysis;

#SQL query 4: Churn by contract type
SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE
        WHEN Churn = 'Yes' THEN 1
        ELSE 0
    END) AS customers_lost,
    ROUND(
        100.0 * SUM(CASE
            WHEN Churn = 'Yes' THEN 1
            ELSE 0
        END) / COUNT(*),
        2
    ) AS churn_percentage
FROM customer_churn_analysis
GROUP BY Contract
ORDER BY churn_percentage DESC;

#SQL query 5: Churn by tenure group
SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 36 THEN '13-36 months'
        ELSE '37+ months'
    END AS tenure_group,
    COUNT(*) AS total_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customer_churn_analysis
# SQL query 6: Customers with high monthly charges
SELECT 
    customerID,
    tenure,
    Contract,
    MonthlyCharges,
    Churn
FROM customer_churn_analysis
WHERE MonthlyCharges > 80
ORDER BY MonthlyCharges DESC;