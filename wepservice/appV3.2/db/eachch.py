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
    WHERE (Timestamp = (select distinct Timestamp from Fact_channelResponse
	ORDER BY Timestamp DESC limit 1)) and 
    (Channel_Title like %s);
    """
    cursor.execute(qry, chname)
    #result = cursor.fetchall()
    result = cursor.fetchall()
    
    return result

def ch_video(chid):
    qry1 = """
    select Video_ID, View_Counts, Timestamp from Fact_VideoResponse
    WHERE Timestamp >=(20210710) and Timestamp<(20210715);
    """
    cursor.execute(qry1)
    viewcount = cursor.fetchall()
    viewcount = pd.DataFrame(viewcount)
    viewcount["Timestamp"] = viewcount["Timestamp"].astype("str")
    qry2 = """
    select DISTINCT Video_Id, Channel_Id, Brand, Video_Title, Published_Date
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
    total["increase"] = total["View_Counts_x"] - total["View_Counts_y"]
    total = total.sort_values(by="increase", ascending=False)
    total_df = pd.merge(left = total, right = chlist, 
        left_on ="Video_ID", right_on="Video_Id")
    
    
    total_df.reset_index(drop=True, inplace = True)
    
    bestvideo = list(total_df.iloc[:5]["Video_ID"])
    rank1, rank2, rank3, rank4, rank5 = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()    
    ranklist = [rank1, rank2, rank3, rank4, rank5]
    for num, i in enumerate(bestvideo):
        ranklist[num] = viewcount[viewcount["Video_ID"] == i].reset_index(drop=True).to_dict()
   
    graphvalues=[]
    for i in range(len(ranklist)):
        try:
            graphvalues.append(list(ranklist[i]["View_Counts"].values()))
        except:
            continue
    
    return total_df, ranklist, graphvalues


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
            , CAST(a.View_Counts AS signed integer) as View
            , LAG(CAST(a.View_Counts AS signed integer)) 
            OVER(ORDER BY b.Brand, a.Timestamp ASC) as Prev_View
            , CAST(a.Video_Counts AS signed integer) as Video_cnt
            , LAG(CAST(a.Video_Counts AS signed integer)) 
            OVER(ORDER BY b.Brand, a.Timestamp ASC) as Prev_cnt
            , CAST(REPLACE(a.Subscribe_Counts, 'hidden', 0) AS signed integer) as Subscribe
            , LAG(CAST(REPLACE(a.Subscribe_Counts, 'hidden', 0) AS signed integer)) 
            OVER(ORDER BY b.Brand, a.Timestamp ASC) as Prev_Sub
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
    try: 
        result[0]["viewper"] = round(result[0]["diff_View"] / result[0]["Prev_View"], 4)*100
    except: 
        result[0]["viewper"] = "(no increase)"
    try:
        result[0]["subper"] = round(result[0]["diff_Sub"] / result[0]["Prev_Sub"], 4)*100
    except:
        result[0]["subper"] = "(hidden)"
    try:
        result[0]["vdper"] = round(result[0]["diff_Video"] / result[0]["Prev_cnt"], 4)*100
    except:
        result[0]["vdper"] = "(no increase)"
    return result 

def ch_recent(chid):
    
    qry2 = """
    select DISTINCT Video_Id, Channel_Id, Video_Title, Published_date
    from Dimension_Video3
    WHERE Channel_Id = %s
    ORDER BY Published_Date DESC limit 5;
    """
    cursor.execute(qry2, chid)
    newlist = cursor.fetchall()
    return newlist 
