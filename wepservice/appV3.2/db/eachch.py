from db import login_mysql
import pandas as pd
mydb, cursor = login_mysql.login()


def ch_info(channelname):
    chname = "%" + channelname + "%"
    qry = """
    SELECT *
    FROM dim_ch 
    RIGHT JOIN Fact_channelResponse
    ON dim_ch.Channel_Id = Fact_channelResponse.Channel_Id
    WHERE (timestamp = (select distinct Timestamp from Fact_channelResponse
	ORDER BY Timestamp DESC limit 1)) and 
    (Chnnel_Title like %s);
    """
    cursor.execute(qry, chname)
    #result = cursor.fetchall()
    result = cursor.fetchall()
    
    return result

def ch_video(chid):
    qry1 = """
    select Video_ID, View_counts, Timestamp from Fact_VideoResponse
    WHERE Timestamp >=subdate(curdate(),7) and Timestamp<(curdate());
    """
    cursor.execute(qry1)
    viewcount = cursor.fetchall()
    viewcount = pd.DataFrame(viewcount)

    qry2 = """
    select DISTINCT Video_Id, Channel_Id, Brand, Video_title, Pub_date
    from Dimension_Video3
    WHERE (Channel_Id = %s);
    """
    cursor.execute(qry2, chid)
    chlist = cursor.fetchall()
    chlist = pd.DataFrame(chlist)

    dates = viewcount.Timestamp.unique()
    lastday = viewcount[viewcount["Timestamp"] == dates[0]]
    recent = viewcount[viewcount["Timestamp"] == dates[-1]]
    total = pd.merge(left = recent, right = lastday, on = "Video_ID")
    total["increase"] = total["View_counts_x"] - total["View_counts_y"]
    total = total.sort_values(by="increase", ascending=False)
    total_df = pd.merge(left = total, right = chlist, 
        left_on ="Video_ID", right_on="Video_Id")
    
    
    total_df.reset_index(drop=True, inplace = True)
    
    return total_df


def ch_detail(chid):
    qry = """
    SELECT 
        c.Brand
        , c.Timestamp
        , c.View
        , c.Prev_View
        , c.View - c.Prev_View as diff_View
        , c.Subscribe
        , c.Prev_Sub
        , c.Subscribe - c.Prev_Sub as diff_Sub
        , c.Video_cnt
        , c.Prev_cnt
        , c.Video_cnt - c.Prev_cnt as diff_Video
    FROM
        (SELECT
            b.Brand
            , date(a.Timestamp) as Timestamp
            , CAST(a.View_counts AS signed integer) as View
            , LAG(CAST(a.View_counts AS signed integer)) 
            OVER(ORDER BY b.brand, a.Timestamp ASC) as Prev_View
            , CAST(a.Video_counts AS signed integer) as Video_cnt
            , LAG(CAST(a.Video_counts AS signed integer)) 
            OVER(ORDER BY b.brand, a.Timestamp ASC) as Prev_cnt
            , CAST(REPLACE(a.Subscrib_counts, 'hidden', 0) AS signed integer) as Subscribe
            , LAG(CAST(REPLACE(a.Subscrib_counts, 'hidden', 0) AS signed integer)) 
            OVER(ORDER BY b.brand, a.Timestamp ASC) as Prev_Sub
        FROM Fact_channelResponse a
        LEFT JOIN dim_ch b
        ON a.Channel_Id = b.Channel_Id
        WHERE 
            a.Channel_Id = %s) c
    WHERE c.Timestamp = (select Timestamp from Fact_channelResponse order by Timestamp DESC limit 1)
    ORDER BY diff_View DESC;
    """
    cursor.execute(qry, chid)
    result = cursor.fetchall()   
    result[0]["viewper"] = round(result[0]["diff_View"] / result[0]["Prev_View"], 4)*100
    result[0]["subper"] = round(result[0]["diff_Sub"] / result[0]["Prev_Sub"], 4)*100
    result[0]["vdper"] = round(result[0]["diff_Video"] / result[0]["Prev_cnt"], 4)*100
    return result 

def ch_recent(chid):
    
    qry2 = """
    select DISTINCT Video_Id, Channel_Id, Video_title, Pub_date
    from Dimension_Video3
    WHERE Channel_Id = %s
    ORDER BY Pub_date DESC limit 5;
    """
    cursor.execute(qry2, chid)
    newlist = cursor.fetchall()
    return newlist 
