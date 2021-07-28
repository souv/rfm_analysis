--rfm modeling 
SELECT 
  member_id,
  COUNT(distinct date(main_order_day)) as frequency,
  (MAX(main_order_day)::date)- (MIN(main_order_day)::date) as recency,
  AVG(real_item_amount) as avg_monetary_value,
  SUM(real_item_amount) as sum_monetary_value,
  (('2021-04-19'::date) - MIN(main_order_day)::date) as T,
  (('2021-04-19'::date) - MAX(main_order_day)::date) as last_buy_interval
into temp table RFM_data
FROM public.ec2_order_item_detail_all
GROUP BY member_id

select * from RFM_data

--rfm分組
select *,case when last_buy_interval < 30 then 'less_30'
         when last_buy_interval >= 30 and last_buy_interval <= 60 then '30-60'
		 when last_buy_interval >= 61 and last_buy_interval <= 90 then '61-90'
		 when last_buy_interval >= 91 and last_buy_interval <= 120 then '91-120'
		 when last_buy_interval > 120 then 'over_120'
		 end as last_buy_interval_group,
		 
		 case when frequency = 1 then 'once'
         when frequency >= 2 and frequency <= 5 then '2-5'
		 when frequency >= 6 and frequency <= 10 then '6-10'
		 when frequency >= 11 and frequency <= 15 then '11-15'
		 when frequency > 15 then 'over15'
		 end as frequency_group
into trpt_member_rfm
from RFM_data

select * from trpt_member_rfm

