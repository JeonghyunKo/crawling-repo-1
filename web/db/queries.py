from db import login_mysql
mydb, cursor = login_mysql.login()
#import pandas as pd

def main_influencer():
    qry = """
    SELECT
	Fact_channelResponse.Channel_Id,
    Fact_channelResponse.Subscrib_counts, 
    dim_ch.Chnnel_Title, 
    dim_ch.Channel_Id,
    Fact_channelResponse.Timestamp
    FROM dim_ch 
    LEFT JOIN Fact_channelResponse
    ON Fact_channelResponse.Channel_Id = dim_ch.Channel_Id
    WHERE Channel_genre = "Influencer" 
        and  Timestamp = (select Timestamp from Fact_channelResponse
                                        order by Timestamp DESC limit 1)
    ORDER BY Subscrib_counts;
    """
    cursor.execute(qry)
    result = cursor.fetchall()
    
    return result

def main_brand():
    qry = """
    SELECT
	Fact_channelResponse.Channel_Id,
    Fact_channelResponse.Subscrib_counts, 
    dim_ch.Chnnel_Title, 
    dim_ch.Channel_Id,
    Fact_channelResponse.Timestamp
    FROM dim_ch 
    LEFT JOIN Fact_channelResponse
    ON Fact_channelResponse.Channel_Id = dim_ch.Channel_Id
    WHERE Channel_genre = "Brand" 
        and  Timestamp = (select Timestamp from Fact_channelResponse
                                        order by Timestamp DESC limit 1)
    ORDER BY Subscrib_counts;
    """
    
    cursor.execute(qry)
    result = cursor.fetchall()
    
    return result

