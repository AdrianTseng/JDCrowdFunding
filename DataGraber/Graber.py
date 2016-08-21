import json
from .__init__ import DATABASE,HOST,USER,PASSWORD


class Graber:

    def __init__(self):
        self.sql = "SELECT result FROM \"JDCrowdFunding\" LIMIT 5000 OFFSET %d;"

    @staticmethod
    def decrypt(obj):
        return json.loads(bytes(obj[0]).decode('utf-8'))

    def grab(self):
        import psycopg2
        import pandas as pd

        offset = 0
        conn = psycopg2.connect(database=DATABASE,
                                host=HOST,
                                user=USER,
                                password=PASSWORD)
        cur = conn.cursor()

        data_frame = pd.DataFrame()

        try:
            while True:
                cur.execute(self.sql % offset)
                result = cur.fetchall()
                if not result:
                    break
                data_frame = data_frame.append(pd.DataFrame(data=list(map(self.decrypt, result))))
                offset += 5000
        except psycopg2.Error as e:
            print("Cannot fetch data from spider database due to: \n%s" % e.pgerror)
            import sys
            sys.exit(-1)
        finally:
            cur.close()
            conn.close()

        return data_frame






