import os
import sqlite3
import threading
import concurrent.futures


class Query:
    tag_table = "CREATE TABLE IF NOT EXISTS tag(tag_name VARCHAR(30) UNIQUE, tag_path VARCHAR(100) UNIQUE)"

    project_table = "CREATE TABLE IF NOT EXISTS project(id integer primary key, datetime DATETIME , " \
                    "tag_name VARCHAR(30), tag_img_path VARCHAR(100), project_text VARCHAR(2000))"

    goal_table = "CREATE TABLE IF NOT EXISTS goal(id integer primary key, datetime DATETIME , tag_name VARCHAR(30), " \
                 "tag_img_path VARCHAR(100), goal_text VARCHAR(2000))"

    todo_table = "CREATE TABLE IF NOT EXISTS todo(id integer primary key, datetime DATETIME , tag_name VARCHAR(30), " \
                 "tag_img_path VARCHAR(100), todo_text VARCHAR(2000))"

    insert_to_tag = "INSERT INTO tag(tag_name, tag_path) VALUES(?, ?)"
    insert_to_project = "INSERT INTO project(datetime, tag_name, tag_img_path, project_text) VALUES(?, ?, ?, ?)"
    insert_to_goal = "INSERT INTO goal(datetime, tag_name, tag_img_path, goal_text) VALUES(?, ?, ?, ?)"
    insert_to_todo = "INSERT INTO todo(datetime, tag_name, tag_img_path, todo_text) VALUES(?, ?, ?, ?)"

    get_all_tags = "SELECT * FROM tag ORDER BY tag_name COLLATE NOCASE ASC"
    get_all_projects = "SELECT * FROM project ORDER BY datetime ASC"
    get_all_goals = "SELECT * FROM goal ORDER BY datetime ASC"
    get_all_todo = "SELECT * FROM todo ORDER BY datetime ASC"

    get_tag_where = "SELECT * FROM tag WHERE tag_name = (?)"
    get_project_where_tag = "SELECT * FROM project WHERE tag_name = (?)"
    get_goal_where_tag = "SELECT * FROM goal WHERE tag_name = (?)"
    get_todo_where_tag = "SELECT * FROM todo WHERE tag_name = (?)"

    delete_tag = "DELETE FROM tag WHERE tag_name = (?) AND tag_path = (?)"
    delete_project_where_tag = "DELETE FROM project WHERE tag_name = (?)"
    delete_goal_where_tag = "DELETE FROM goal WHERE tag_name = (?)"
    delete_todo_where_tag = "DELETE FROM todo WHERE tag_name = (?)"

    delete_project_where_id = "DELETE FROM project WHERE id = (?)"
    delete_goal_where_id = "DELETE FROM goal WHERE id = (?)"
    delete_todo_where_id = "DELETE FROM todo WHERE id = (?)"

    update_project_where_id = "UPDATE project SET datetime=(?), tag_name=(?), tag_img_path=(?)," \
                              " project_text=(?) WHERE id=(?)"
    update_goal_where_id = "UPDATE goal SET datetime=(?), tag_name=(?), tag_img_path=(?)," \
                           " goal_text=(?) WHERE id=(?)"
    update_todo_where_id = "UPDATE todo SET datetime=(?), tag_name=(?), tag_img_path=(?)," \
                           " todo_text=(?) WHERE id=(?)"

    get_all_tables_by_date = "SELECT * FROM (SELECT 'Goal', * FROM goal UNION ALL SELECT 'Todo', * FROM todo) ORDER " \
                             "BY datetime ASC "


class DBHandler:
    _sql_file = r"UserResources/userTodo.db"
    registered_classes = {}  # stores the class instances that needs to be notified of the change in database

    user_resources = r"UserResources"
    img_folder = r"UserResources/tag_images"

    @classmethod
    def initialize_files(cls):  # creates the folder if it doesn't exist

        if not os.path.isdir(
                cls.user_resources):  # check if the UserResources folder exists if it doesn't exits create it
            os.mkdir(cls.user_resources)

        if not os.path.isdir(cls.img_folder):
            os.mkdir(cls.img_folder)  # creates image folder

        table_lst = [Query.tag_table, Query.project_table, Query.goal_table, Query.todo_table]

        for table in table_lst:
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
        with sqlite3.connect(cls._sql_file, check_same_thread=False) as conn:
            conn.execute(sql_query)
            conn.commit()

    @classmethod
    def create_table(cls, sql_query: Query):  # calls _add_table from thread
        thread = threading.Thread(target=cls._add_table_db, args=(sql_query,))
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
            cls.notify("settings")

    @classmethod
    def _get_data_from_db(cls, query: Query, *values):  # gets value from db
        with sqlite3.connect(cls._sql_file) as conn:
            curr = conn.cursor()
            curr.execute(query, *values)
            items = curr.fetchall()
            conn.commit()

        return items

    @classmethod
    def get_data(cls, query: Query, *values):  # starts _get_data from another thread and returns the result
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
        thread.start()
        thread.join()

    @classmethod
    def _update_date_from_db(cls, query, *args):  # updates value in database
        with sqlite3.connect(cls._sql_file) as conn:
            conn.execute(query, *args)

    @classmethod
    def update_data(cls, query, *args):
        thread = threading.Thread(target=cls._update_date_from_db, args=(query, args))
        thread.start()

    @classmethod
    def get_notify_classes(cls):  # returns dict of all the classes registered
        return cls.registered_classes

    @classmethod
    def register(cls, key: str, instance):  # adds the instances to the notify set
        if key not in cls.registered_classes.keys():
            cls.registered_classes[key] = instance

        else:
            raise Exception(f"{key} Key already exists")

    @classmethod
    def unregister(cls, key: str):  # removes the instances from the notify set
        cls.registered_classes.pop(key)

    @classmethod
    def notify(cls, key=None):  # call's the db_changed method in all the registered classes
        # if key provided notifies only particular class

        if key:

            try:
                cls.registered_classes[key].db_changed()

            except NameError:
                raise NotImplementedError

            except KeyError:
                print("No such key")

            except Exception as e:
                print(f"EXCEPTION: {e}")

        else:
            for instances in cls.registered_classes.values():
                try:
                    instances.db_changed()

                except NameError:
                    raise NotImplementedError


#  Note: This class could be simplified by just having one method to execute all the queries.
#  But, for the sake of readability and ease of use its not done.
