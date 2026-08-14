import pymysql
from pymysql.cursors import DictCursor

class MySqlHelper:
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self):
        #报错：AI提示为中文兼容问题#
        self.conn = pymysql.connect(**self.config)

    def execute_query(self, sql, params=None):
        """执行查询操作，返回结果列表"""
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()

    def execute_update(self, sql, params=None):
        """执行增删改操作，返回影响行数"""
        if not self.conn:
            self.connect()
        try:
            with self.conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, params or ())
                self.conn.commit()
                return affected_rows
        except pymysql.Error as e:
            self.conn.rollback()
            raise e

    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
            self.conn = None

# 使用示例
if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "你的密码",
        "database": "你的库名",
        "port": 3306,
        "charset": "utf8mb4",
        "cursorclass": DictCursor
    }
    db = MySqlHelper(db_config)
    # 查询
    data = db.execute_query("SELECT * FROM students")
    print(data)
    # 插入
    db.execute_update("INSERT INTO students (学号,姓名,身高) VALUES (%s,%s,%s)", ("2026003","李四",172))
    db.close()
