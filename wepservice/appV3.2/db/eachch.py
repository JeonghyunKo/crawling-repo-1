from db import login_mysql
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
    