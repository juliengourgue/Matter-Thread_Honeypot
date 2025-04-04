import mysql.connector
from mysql.connector import errorcode
from config import db_pswd
# SQL Query
auth_query = ("SELECT * FROM auth WHERE session=%s")
input_query = ("SELECT * FROM input WHERE session=%s")
session_query = ("SELECT * FROM sessions")
sql_insert_query = """
INSERT IGNORE INTO homeAssistant (ip, timestamp, nbr_packets)
VALUES (%s, %s, %s)
"""
ha_ip_query = ("SELECT * FROM homeAssistant WHERE ip=%s")
session_ip_query = ("SELECT ip FROM sessions WHERE id=%s")
packets_nbr_time_range_query = ("SELECT sum(nbr_packets) FROM homeAssistant WHERE timestamp>=%s AND timestamp<%s AND ip=%s")
packets_ip_time_range_query = ("SELECT DISTINCT ip FROM homeAssistant WHERE timestamp>=%s AND timestamp<%s")


class DB:
    cnx = None
    def __init__(self):
        self.connection()
        if self.cnx == None:
            raise Exception("Impossible to connect to the DB")
    
    def connection(self):
        try:
            self.cnx = mysql.connector.connect(user='cowrie', password=db_pswd,
                                        host='127.0.0.1',
                                        database='cowrie')
      
        except mysql.connector.Error as err:
            print(err)
        
    def disconnect(self):
        self.cnx.close() 
    
    def exec_query(self, query, args=None):
        cursor = self.cnx.cursor()
        if args == None :
            cursor.execute(query)
        
        else:
            cursor.execute(query, args)                       
        
        results = cursor.fetchall()
        cursor.close()
        return results
        
    def try_auth(self,sessionId):
        results = self.exec_query(auth_query, (sessionId,))
        if len(results) == 0:
            return False
        return True
        
    def get_auth_by_session(self, sessionId):
        results = self.exec_query(auth_query, (sessionId,))
        auths = []
        for id, session, success, username, password, timestamp in results:
            auth = {"username": username, "password":password, "success":bool(success), "timestamp":timestamp}
            auths.append(auth)
        auths = sorted(auths, key=lambda x: x['timestamp'])
        return auths
    
    def get_input_by_session(self, sessionId):
        results = self.exec_query(input_query, (sessionId,))
        inputs = []
        for id, session, timestamp, realm, success, input in results:
            input = {"input":input, "success":bool(success), "timestamp":timestamp}
            inputs.append(input)
        inputs = sorted(inputs, key=lambda x: x['timestamp'])        
        return inputs     
     
    def get_sessionId_in_ha(self, sessionId):
        #Get ip of the session
        results = self.exec_query(session_ip_query, (sessionId,))
        for value in results:
            ip = value[0]
            print(ip)
            #Is there this IP in HA
            results2 = self.exec_query(ha_ip_query, (ip,))
            if len(results2) == 0 : return (False, ip)
            return (True, ip)       
               
    def get_sessions(self):
        results = self.exec_query(session_query)        
        sessions = []
        # Print the results
        for sessionId, start, end, sensor, ip, termsize, client in results:
            session = {"sessionId":sessionId, "start":start, "end":end, "ip":ip}
            if self.try_auth(sessionId):
                sessions.append(session)
            else : continue
        sessions = sorted(sessions, key=lambda x: x['start'], reverse=True)    
        return sessions
                
    def put_haIp(self, ip, timestamp, nbr_packets):
        cursor = self.cnx.cursor()
        cursor.execute(sql_insert_query, (ip,timestamp,nbr_packets))
        self.cnx.commit()
        cursor.close()
    
    def get_ip_time_range(self, mn, mx):
        mint = mn.strftime('%Y-%m-%d %H:%M')
        maxt = mx.strftime('%Y-%m-%d %H:%M')
        ips = self.exec_query(packets_ip_time_range_query, (mint,maxt))
        result = []
        for ip in ips:
            result.append(ip[0]) 
        print(result)      
        return result
    
    def get_packets_nbr_time_range(self, mn, mx, ip):
        mint = mn.strftime('%Y-%m-%d %H:%M')
        maxt = mx.strftime('%Y-%m-%d %H:%M')
        results = self.exec_query(packets_nbr_time_range_query, (mint,maxt,ip))
        if results[0][0] == None : res = 0
        else : res = int(results[0][0])
        return res
    
if __name__ == '__main__':
    pass