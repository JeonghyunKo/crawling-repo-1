from db import login_mysql
mydb, cursor = login_mysql.login()

def brief_sub():
    qry = """
    SELECT 
        c.Brand
        , c.Timestamp
        , c.Subscribe
        , c.Prev_Sub
        , c.Subscribe - c.Prev_Sub as diff_Sub
    FROM
        (SELECT
            b.Brand
            , date(a.Timestamp) as Timestamp
            , CAST(REPLACE(a.Subscrib_counts, 'hidden', 0) AS signed integer) as Subscribe
            , LAG(CAST(REPLACE(a.Subscrib_counts, 'hidden', 0) AS signed integer)) 
            OVER(ORDER BY b.brand, a.Timestamp ASC) as Prev_Sub
        FROM Fact_channelResponse a
        LEFT JOIN dim_ch b
        ON a.Channel_Id = b.Channel_Id
        WHERE 
            Channel_genre = 'Influencer') c
    WHERE c.Timestamp = (select Timestamp from Fact_channelResponse order by Timestamp DESC limit 1)
    ORDER BY diff_Sub DESC;
    """
    cursor.execute(qry)
    result = cursor.fetchall()
    return result

def brief_video():
    qry = """
    SELECT 
        c.Brand
        , c.Timestamp
        , c.Video_cnt
        , c.Prev_Vcnt
        , c.Video_cnt - c.Prev_Vcnt as diff_Video
    FROM
        (SELECT
            b.Brand
            , date(a.Timestamp) as Timestamp
            , CAST(a.Video_counts AS signed integer) as Video_cnt
            , LAG(CAST(a.Video_counts AS signed integer)) 
            OVER(ORDER BY b.brand, a.Timestamp ASC) as Prev_Vcnt
        FROM Fact_channelResponse a
        LEFT JOIN dim_ch b
        ON a.Channel_Id = b.Channel_Id
        WHERE 
            Channel_genre = 'Influencer') c
    WHERE c.Timestamp = (select Timestamp from Fact_channelResponse order by Timestamp DESC limit 1)
    ORDER BY diff_Video DESC;
    """
    cursor.execute(qry)
    result = cursor.fetchall()
    return result

def brief_view():
    qry = """
    SELECT 
        c.Brand
        , c.Timestamp
        , c.View
        , c.Prev_View
        , c.View - c.Prev_View as diff_View
    FROM
        (SELECT
            b.Brand
            , date(a.Timestamp) as Timestamp
            , CAST(a.View_counts AS signed integer) as View
            , LAG(CAST(a.View_counts AS signed integer)) 
            OVER(ORDER BY b.brand, a.Timestamp ASC) as Prev_View
        FROM Fact_channelResponse a
        LEFT JOIN dim_ch b
        ON a.Channel_Id = b.Channel_Id
        WHERE 
            Channel_genre = 'Influencer') c
    WHERE c.Timestamp = (select Timestamp from Fact_channelResponse order by Timestamp DESC limit 1)
    ORDER BY diff_View DESC;
    """
    cursor.execute(qry)
    result = cursor.fetchall()
    return result




result = brief_sub()
print(result[1]["Brand"], result[1]["diff_Sub"])

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

