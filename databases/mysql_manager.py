import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
import time 

class MysqlManager:
    
    dbconfig = {
        "database": "douyin",
        "user":     "root",
        "password": "password",
        "host":     "localhost"
    }

    TABLES = {}
    TABLES['urls'] = (
        "CREATE TABLE `urls` ("
        "  `index` int(11) NOT NULL AUTO_INCREMENT,"
        "  `url` varchar(512) NOT NULL,"
        "  `status` char(20) NOT NULL DEFAULT 'new',"
        "  `queue_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        "  `done_time` timestamp NOT NULL DEFAULT '1970-01-02 00:00:00',"
        "  PRIMARY KEY (`index`),"
        "  UNIQUE (`url`)"
        ") ENGINE=InnoDB")

    def __init__(self, max_num_thread):
        try:
            cnx = mysql.connector.connect(host=self.dbconfig['host'], user=self.dbconfig['user'], password=self.dbconfig['password'])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print('Create Error ' + err.msg)
            exit(1)

        cursor = cnx.cursor()

        try:
            cnx.database = self.dbconfig['database']
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(cursor)
                cnx.database = self.dbconfig['database']
                self.create_tables(cursor)
            else:
                print(err)
                exit(1)
        finally:
            cursor.close()
            cnx.close()

        self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                          pool_size = max_num_thread,
                                                          **self.dbconfig)


    def create_database(self, cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.dbconfig['database']))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def create_tables(self, cursor):
        for name, ddl in self.TABLES.items():
            try:
                cursor.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('create tables error ALREADY EXISTS')
                else:
                    print('create tables error ' + err.msg)
            else:
                print('Tables created')


    def enqueueUrl(self, url):
        con = self.cnxpool.get_connection()
        cursor = con.cursor()
        try:
            sql = "INSERT INTO urls(url) VALUES ('{}')".format(url)
            print(sql)
            cursor.execute((sql))
            con.commit()
        except mysql.connector.Error as err:
            print('enqueueUrl() ' + err.msg)
            return
        finally:
            cursor.close()
            con.close()


    def dequeueUrl(self):
        con = self.cnxpool.get_connection()
        cursor = con.cursor(dictionary=True)
        try:
            const_id = "%.9f" % time.time()
            update_query = ("UPDATE urls SET status='{}' WHERE status='new' LIMIT 1".format(const_id))
            cursor.execute(update_query)
            con.commit()

            query = ("SELECT `index`, `url` FROM urls WHERE status='{}'".format(const_id))
            cursor.execute(query)
            row = cursor.fetchone()
            if row is None:
                return None
            return row
        except mysql.connector.Error as err:
            print('dequeueUrl() ' + err.msg)
            return None
        finally:
            cursor.close()
            con.close()

    def finishUrl(self, index):
        con = self.cnxpool.get_connection()
        cursor = con.cursor()
        try:
            # we don't need to update done_time using time.strftime('%Y-%m-%d %H:%M:%S') as it's auto updated
            update_query = ("UPDATE urls SET `status`='done', `done_time`=%s WHERE `index`=%d") % (time.strftime('%Y-%m-%d %H:%M:%S'), index)
            cursor.execute(update_query)
            con.commit()
        except mysql.connector.Error as err:
            # print('finishUrl() ' + err.msg)
            return
        finally:
            cursor.close()
            con.close()

if __name__ == "__main__":
    mysql_mgr = MysqlManager(8)
    # for i in range(0, 100):
    #     mysql_mgr.enqueueUrl('https://www.douyin.com/all-{}'.format(i))
    print(mysql_mgr.dequeueUrl())