import os
import sqlite3
import threading
import concurrent.futures


class Query:

    tag_table = "CREATE TABLE IF NOT EXISTS tag(tag_name VARCHAR(30) UNIQUE, tag_path VARCHAR(100) UNIQUE)"

    goal_table = "CREATE TABLE IF NOT EXISTS goal(datetime DATETIME , tag_name VARCHAR(30), " \
                 "tag_img_path VARCHAR(100), goal_text VARCHAR(2000))"

    todo_table = "CREATE TABLE IF NOT EXISTS todo(datetime DATETIME , tag_name VARCHAR(30), " \
                 "tag_img_path VARCHAR(100), todo_text VARCHAR(2000))"

    insert_to_tag = "INSERT INTO tag(tag_name, tag_path) VALUES(?, ?)"
    insert_to_goal = "INSERT INTO goal VALUES(?, ?, ?, ?)"
    insert_to_todo = "INSERT INTO todo VALUES(?, ?, ?, ?)"

    get_all_tags = "SELECT * FROM tag ORDER BY tag_name COLLATE NOCASE ASC"
    get_all_goals = "SELECT * FROM goal ORDER BY datetime ASC"
    get_all_todo = "SELECT * FROM todo ORDER BY datetime ASC"

    get_tag_where = "SELECT * FROM tag WHERE tag_name = (?)"

    delete_tag = "DELETE FROM tag WHERE tag_name = (?) AND tag_path = (?)"


class DBHandler:
    _sql_file = r"UserResources/userTodo.db"
    notify_cls = set()  # stores the class instances that needs to be notified of the change in database

    user_resources = r"UserResources"
    img_folder = r"UserResources/tag_images"

    @classmethod
    def initialize_files(cls):  # creates the folder if it doesn't exist

        if not os.path.isdir(cls.user_resources):  # check if the UserResources folder exists if it doesn't exits create it
            os.mkdir(cls.user_resources)

        if not os.path.isdir(cls.img_folder):
            os.mkdir(cls.img_folder)  # creates image folder

        table_lst = [Query.tag_table, Query.goal_table, Query.todo_table]

        for table in table_lst:
            print(table)
            cls.create_table(table)

        cls.check()

    @classmethod
    def _check(cls):  # check if the image in the database exist in the folder and if it doesn't remove it
        tag_table = "SELECT * FROM tag"
        delete_tag = "DELETE FROM tag WHERE tag_name=(?)"

        with sqlite3.connect(cls._sql_file) as conn:

            curr = conn.cursor()
            curr.execute(tag_table)
            items = curr.fetchall()

            for tag_name, tag_img_path in items:

                if not os.path.isfile(tag_img_path):
                    conn.execute(delete_tag, (tag_name,))
                    conn.commit()

    @classmethod
    def check(cls):  # calls check method

        thread = threading.Thread(target=cls._check)
        thread.start()

    @classmethod
    def _add_table_db(cls, sql_query: Query):  # creates a new table if it doesn't exist
        print("Query: ", sql_query)
        with sqlite3.connect(cls._sql_file, check_same_thread=False) as conn:
            conn.execute(sql_query)
            conn.commit()

    @classmethod
    def create_table(cls, sql_query: Query):  # calls _add_table from thread
        thread = threading.Thread(target=cls._add_table_db, args=(sql_query, ))
        thread.start()
        thread.join()

    @classmethod
    def _insert_values(cls, insert_query: Query, *values):  # inserts into table
        with sqlite3.connect(cls._sql_file, check_same_thread=False) as conn:
            conn.execute(insert_query, *values)
            conn.commit()

    @classmethod
    def insert_to_table(cls, insert_query: Query, *values):
        thread = threading.Thread(target=cls._insert_values, args=(insert_query, values))
        thread.start()
        thread.join()

        if insert_query == Query.insert_to_tag:
            cls.notify()

    @classmethod
    def register(cls, instance):  # adds the instances to the notify set
        cls.notify_cls.add(instance)

    @classmethod
    def unregister(cls, instance):  # removes the instances from the notify set
        cls.notify_cls.remove(instance)

    @classmethod
    def notify(cls): # call's the db_changed method in all the registered classes
        for instances in cls.notify_cls:
            try:
                instances.db_changed()

            except NameError:
                raise NotImplementedError

    @classmethod
    def _get_data_from_db(cls, query: Query, *values):  # gets value from db
        print("QUERY: ", query, values)
        with sqlite3.connect(cls._sql_file) as conn:
            curr = conn.cursor()
            curr.execute(query, *values)
            items = curr.fetchall()
            print("Items Tag: ", items, curr.fetchone())
            conn.commit()

        return items

    @classmethod
    def get_data(cls, query: Query, *values):  # starts _get_data from another thread and returns the result
        print("Query: ", query, values)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(cls._get_data_from_db, query, values)
            result = future.result()

        return result

    @classmethod
    def _delete_data_from_db(cls, query: Query, *where_value):
        # deletes the data from database options : where_value is the condition where
        with sqlite3.connect(cls._sql_file) as conn:
            conn.execute(query, *where_value)

    @classmethod
    def delete_data(cls, query, *where_value):
        thread = threading.Thread(target=cls._delete_data_from_db, args=(query, where_value))
