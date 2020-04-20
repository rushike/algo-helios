CREATE OR REPLACE FUNCTION get_calls_for_today (portfolio_id INT)
RETURNS TABLE(
	callid INT,
	algoid INT,
	calltime timestamp with time zone,
	side VARCHAR,
	callprice NUMERIC,
	targetprice NUMERIC,
	stoploss NUMERIC,
	callstatus VARCHAR,
	exitprice NUMERIC,
	exittime timestamp with time zone,
	activeflag INT,
	instrumentname VARCHAR,
	instrumenttoken INT,
	tradestrategy VARCHAR,
	algocategory VARCHAR,
	pids INT[]
)
AS $$
BEGIN
	RETURN QUERY SELECT 
			C.*, 
			I.InstrumentName, I.InstrumentToken, 
			T.TradeStrategy, T.AlgoCategory, 
			Q.PIds 
		FROM 
			( 
				SELECT 
					C.AlgoId AS AId, 
					ARRAY_AGG(DISTINCT PM.PortfolioId) AS PIds 
				FROM 
					Calls C, 
					PortfolioMap PM 
					WHERE C.AlgoId=PM.AlgoId 
					GROUP BY C.AlgoId
			) AS Q, 
			Calls C, 
			Algos A, 
			Instruments I, 
			TradeStrategies T, 
			PortfolioMap PM 
			WHERE C.AlgoId=Q.AId 
					AND 
				C.AlgoId=A.AlgoId 
					AND 
				A.InstrumentId=I.InstrumentId 
					AND 
				A.TradeStrategyId=T.TradeStrategyId 
					AND 
				PM.AlgoId=A.AlgoId 
					AND 
				(
					C.ActiveFlag=1 
						OR 
					(
						C.ActiveFlag=0 
							AND 
						C.ExitTime > NOW()::date
					)
				)
					AND
				PM.PortfolioId=portfolio_id;
END;
$$
LANGUAGE 'plpgsql';

GRANT EXECUTE ON FUNCTION  get_calls_for_today(INT) TO sysadmin;