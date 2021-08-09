from db import login_mysql
mydb, cursor = login_mysql.login()

def main_influencer():
    #console.log("D")
    qry = """
    SELECT 
    b.Brand
    , date(b.Published_Date) as Published
    , date(a.Timestamp) as Timestamp
    , CAST(a.View_Counts AS signed integer) as View
    , CAST(REPLACE(a.Subscribe_Counts, 'hidden', 0) AS signed integer) as Subscribe
    , CAST(a.Video_Counts AS signed integer) as Video_cnt
    , CAST(a.View_Counts AS signed integer) / CAST(REPLACE(a.Subscribe_Counts, 'hidden', 0) AS signed integer) as ViewperSub
    , CAST(a.View_Counts AS signed integer) / CAST(a.Video_Counts AS signed integer) as ViewperVideo
    FROM Fact_channelResponse a
    LEFT JOIN dim_ch b
    ON a.Channel_Id = b.Channel_Id
    WHERE 
        Channel_Genre = 'Influencer'
        and Timestamp = (select Timestamp from Fact_channelResponse order by Timestamp DESC limit 1)
    ORDER BY Subscribe DESC;
    """
    cursor.execute(qry)
    #result = cursor.fetchall()
    result = cursor.fetchall()
   
    return result

def main_brand():
    qry = """
    SELECT 
    b.Brand
    , date(b.Published_Date) as Published
    , date(a.Timestamp) as Timestamp
    , CAST(a.View_Counts AS signed integer) as View
    , CAST(REPLACE(a.Subscribe_Counts, 'hidden', 0) AS signed integer) as Subscribe
    , CAST(a.Video_Counts AS signed integer) as Video_cnt
    , CAST(a.View_Counts AS signed integer) / CAST(REPLACE(a.Subscribe_Counts, 'hidden', 0) AS signed integer) as ViewperSub
    , CAST(a.View_Counts AS signed integer) / CAST(a.Video_Counts AS signed integer) as ViewperVideo

    FROM Fact_channelResponse a
    LEFT JOIN dim_ch b
    ON a.Channel_Id = b.Channel_Id
    WHERE 
        Channel_Genre = 'Brand'
        and Timestamp = (select Timestamp from Fact_channelResponse order by Timestamp DESC limit 1)
    ORDER BY Subscribe DESC;
    """
    
    cursor.execute(qry)
    result = cursor.fetchall()
    return result


#import pandas as pd
#from pandas import DataFrame, Series

#import pymysql
# def login():
#     mydb = pymysql.connect(
#         user='root',
#         passwd='dss',
#         host='34.64.111.84',
#         db='crwdb_yt',
#         charset='utf8'
#     )
#     cursor = mydb.cursor(pymysql.cursors.DictCursor)
#     return mydb, cursor

# def main_influencer():
#     qry = """
#     SELECT
# 	Fact_channelResponse.Channel_Id,
#     Fact_channelResponse.Subscrib_counts, 
#     dim_ch.Chnnel_Title, 
#     dim_ch.Channel_Id,
#     Fact_channelResponse.Timestamp
#     FROM dim_ch 
#     LEFT JOIN Fact_channelResponse
#     ON Fact_channelResponse.Channel_Id = dim_ch.Channel_Id
#     WHERE Channel_genre = "Influencer" 
#         and  Timestamp = (select Timestamp from Fact_channelResponse
#                                         order by Timestamp DESC limit 1)
#     ORDER BY Subscrib_counts;
#     """
#     cursor.execute(qry)
#     result = cursor.fetchall()
    
#     return result

