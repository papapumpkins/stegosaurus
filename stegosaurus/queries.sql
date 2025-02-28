-- Tyrannosaurus Risk
with live_offers as (select cb.workspace_id as workspace_id,
                            ch.is_ucc_filing_required,
                            ch.credit_limit,
                            case
                                when personal_guarantee is null and personal_guarantee_percent is not null
                                    then credit_limit * personal_guarantee_percent / 100
                                when personal_guarantee is not null then personal_guarantee
                                else 0 end  as pg_amount,
                            cb.created_at   as created_at,
                            cb.updated_at   as updated_at
                     from airbyte.credit_underwriting_offer_history ch
                              join airbyte.credit_underwriting_offer as co on ch.offer_id = co.id
                              join airbyte.credit_underwriting_offer_bundle_offers as cbo on cbo.offer_id = co.id
                              join airbyte.credit_underwriting_offer_bundle as cb on cbo.bundle_id = cb.id
                     where cbo.is_main is true
                       and cb.status = 'LIVE'
                       and ch.is_current = true)
        ,
     pg_ucc_now as (select lo.workspace_id
                         , lo.is_ucc_filing_required
                         , lo.pg_amount
                         , lo.credit_limit       as initial_offer_credit_limit
                         , cva.creditlimit / 100 as current_limit
                         , lo.updated_at         as off_out_at
                    from live_offers lo
                             join airbyte.creditvirtualaccount cva on lo.workspace_id = cva.workspaceid
                    where lo.pg_amount != 0
                       or lo.is_ucc_filing_required is true
     ),daca as (select workspace_id
                   , current_balance
              from analytics.bank_account
              where subtype = 'SECURITY'),
     deposit_account as (select distinct workspace_id
                         from airbyte.treasury_prime_account
                         where status = 'open')
select current_date::date as execution_date
     , ws.id                                                                      as workspace_id
     , ws.name                                                                    as workspace_name
     , wst.name                                                                   as latest_state
     , case when da.workspace_id is not null then true else false end             as has_deposit_product
     , ft.credit_limit
     , case when ft.bank_revenue_l30d is not null then true else false end        as is_bank_connected
     , case when ft.sp_sum_sales_last_30days is not null then true else false end as is_sp_connected
     , case when monthly_accounting_revenue is not null then true else false end  as is_accounting_connected
     , coalesce(pg_amount, 0)                                                     as pg_amount
     , coalesce(is_ucc_filing_required, false)                                    as ucc
     , coalesce(d.current_balance, 0)                                             as daca_balance
     , scf.avg_monthly_revenue_ratio_l3m_to_l12m
     , scf.revenue_l3m_ratio_yoy
     , scf.revenue_l12m_best
     , scf.operating_margin_l3m_2m_ago
     , scf.net_margin_l3m_2m_ago
     , scf.current_ratio_2m_ago
     , scf.quick_ratio_2m_ago
     , scf.avg_available_cash_l12m
     , scf.limit_to_cash_ratio_l3m
     , scf.avg_available_cash_l3m
     , scf.quick_ratio_l1m_ratio_yoy_2m_ago
     , scf.available_cash_l3m_ratio_yoy
     , scf.current_ratio_ratio_2m_ago_to_5m_ago
     , scf.liabilities_2m_ago_to_monthly_revenue_l3m_2m_ago_ratio
     , scf.liabilities_2m_ago_to_avg_available_cash_l3m_ratio
     , scf.monthly_debt_repayment_2m_ago_to_monthly_revenue_l12m_2m_ago_ratio
     , scr.data_quality
     , scf.min_available_cash_l12m
     , scf.gross_margin_l3m_2m_ago
     , scf.revenue_l3m_best
     , scf.was_dq10_in_l3m
     , scf.ltv90d_2m_ago_ratio_yoy
from airbyte.workspace ws
         inner join analytics.workspace_processing_state_most_recent wst on ws.id = wst.workspace_id
         inner join analytics.fact_table ft on ws.id = ft.workspace_id and ft.ref_date = current_date - interval '1 day'
         left join analytics.scorecard_v3_features_daily scf
                   on ws.id = scf.workspace_id and scf.ref_date = current_date - interval '1 day'
         left join analytics.scorecard_v3_rating_daily scr
                   on ws.id = scr.workspace_id and scr.ref_date = current_date - interval '1 day'
         left join pg_ucc_now pu on pu.workspace_id = ws.id
         left join daca d on ws.id = d.workspace_id
         left join deposit_account da on ws.id = da.workspace_id
where ws.id = '<workspace_id>' 