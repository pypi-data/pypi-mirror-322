
from uuid import uuid4
from datetime import datetime
import sqlite3
import bcrypt
import html
import pandas as pd
from difflib import SequenceMatcher
from random import randint

def sanitize_data(data):
    clean_data = {}
    for k in data:
        value = data[k]
        if isinstance(value, str):
            sanitized_value = html.escape(value)
            clean_data[k] = sanitized_value
        elif isinstance(value, int):
            clean_data[k] = value
        else:
            # Handle other data types as needed
            clean_data[k] = value

    return clean_data
        



class Table:
    def __init__(self, table_name, 
                 db: sqlite3.Connection, 
                 cursor : sqlite3.Cursor, make_uuid = True, created_at = True):
        self.table_name = table_name
        self.db = db
        self.cursor = cursor
        self.make_uuid = make_uuid
        self.created_at = created_at
        self.types = {
            "<class 'str'>": 'TEXT',
            "<class 'int'>": 'INTEGER',
            "<class 'float'>": 'REAL',
            "<class 'bool'>": 'BOOL',
            "<class 'bytes'>": 'BLOB',
            "<class 'decimal.Decimal'>": 'NUMERIC',
            "INDEX": 'INTEGER PRIMARY KEY'
        }
        
        self.allowed_filters = ['between', 'larger_than', 'less_than', 'less_or_equal', 'larger_or_equal', 'not', 'equal']
    

    def table_exists(self) -> bool:
        """Check if the table exists in the database."""
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.cursor.execute(query, (self.table_name,)).fetchone()
        return result is not None
    

    def ensure_table(self, schema: dict = None):
        """Ensure the table exists; create it if it doesn't."""
        if not self.table_exists():
            schema = schema or self.default_schema
            schema_columns = self.get_types(schema)
            query = f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    _index {self.types['INDEX']}, {schema_columns}
                )
            '''
            self.cursor.execute(query)
            self.db.commit()
        
    
    def get_types(self, data):

        if self.make_uuid:
            data['uuid'] = str(uuid4())
        
        if self.created_at:
            data['created_at'] = str(datetime.now())

        cols = []
        for k in data:
            cols.append(f'{k} {self.types[str(type(data[k]))]}')

        return ', '.join(cols)
    
    def get_column_names(self):
        column_names = self.cursor.execute(f'''SELECT * FROM 
        {self.table_name} LIMIT 1''').description

        return [description[0] for description in column_names]

    def Insert(self, data : dict):

        data = sanitize_data(data)

        q = f'''
            CREATE TABLE IF NOT EXISTS
            {self.table_name}

            (_index {self.types['INDEX']}, {self.get_types(data)})
        '''

        #print(q)

        self.cursor.execute(q)

        q = f'''
         INSERT INTO {self.table_name} ({','.join(data.keys())})
         VALUES ({','.join(['?' for _ in range(len(data.keys()))])})
        '''

        #print(q)

        self.cursor.execute(q, tuple([v for v in data.values()]))
        self.db.commit()

        

        return self.GetBy(**data)
    

    @classmethod
    def is_number_in_range(self, number, a, b):
        if number >= a and number <= b:
            return True
        else:
            return False


    
    def hash_password(self, password: str):
        return bcrypt.hashpw(
            password = password.encode(), salt = bcrypt.gensalt()
        )
    
    def check_password(self, password, hashed_password):
        password = password.encode()

        return bcrypt.checkpw(password, hashed_password)
   
    def show_results(self, results) -> list:
        rows = []

        for result in results:
            rows.append({k:v for k, v in zip(self.get_column_names(), result)})

        return rows
    

    def InsertMany(self, data_list : list) -> list:
        for data in data_list:
            self.Insert(data = data)
        
        return self.GetALL()
    

    def Register(self, data, password_hash = True):

        # check if user is not exists by email
        try:
            if self.GetBy(email = data['email']):
                return False
        except sqlite3.OperationalError:
            pass
        
        if 'password' in data:
            if password_hash:
                data['password'] = self.hash_password(data['password'])
            
            data['password'] = data['password']
        
        
        self.Insert(data = data)
        return self.GetBy(email = data['email'])
    
    def LogIn(self, data):

        data = sanitize_data(data)
        #self.ensure_table(schema=data)

        # find the user by email
        user = self.FindOne(email = data['email'])
        if user:
            # get the hashed password of this user
            user_password = user['password']

            if isinstance(user_password, str):
                if data['password'] == user_password:
                    return user
                
                return

            if self.check_password(data['password'], user_password):
                return user
            
    def Slice(self, a, b):
        recordes = self.GetALL()
        if recordes:
            return recordes[a:b]
        
    def Limit(self, limit : int):
        recordes = self.GetALL()
        if recordes:
            return recordes[:limit]
    
    def GenerateLikeThis(self, schema : dict, faker, n : int = 1):
        try:
            _funcs_names = dir(faker)
            _funcs = {}
            samples = []

            for func in _funcs_names:
                _funcs[func] = f'faker.{func}()'
                
            for i in range(n):
                out_data = {}
                for k in schema:
                    value = schema[k]
                    if isinstance(value, int):
                        out_data[k] = randint(0, value)
                    elif k not in _funcs_names:
                        indexs = []
                        for fname in _funcs_names:
                            r = SequenceMatcher(a = k, b = fname).ratio()
                            indexs.append(r)

                        large_num = max(indexs)
                        index = indexs.index(large_num)
                        
                        out_data[k] = eval(_funcs[_funcs_names[index]])
                             
                    else:
                        out_data[k] = eval(_funcs[k])
                
                samples.append(out_data)
                    
            return samples
        except Exception as e:
            print(e)

   
    def GetALL(self) -> list:
        try:
            results = self.cursor.execute(f'SELECT * FROM {self.table_name}').fetchall()
            return self.show_results(results)
        except sqlite3.OperationalError:
            return
    

    def GetByID(self, uuid : str) -> dict:
        try:
                    
            q = f'''
            SELECT * FROM {self.table_name} WHERE uuid = "{uuid}"
            '''
            result = self.cursor.execute(q).fetchone()
            self.db.commit()

            return {k:v for k, v in zip(self.get_column_names(), result)}
        except sqlite3.OperationalError:
            return
    
    def GetBy(self, **args) -> list:
        filter_key_vals = ''
        
        for k, v in args.items():
            filter_key_vals += f'AND {k} = "{v}" '

        # Remove the first and in text
        filter_key_vals = filter_key_vals[3:].strip()
        #print(filter_key_vals)

        q = f'''
        SELECT * FROM {self.table_name} WHERE {filter_key_vals}
         '''.strip()
        
        try:
            results = self.cursor.execute(q).fetchall()

            self.db.commit()
            return self.show_results(results)
        except sqlite3.OperationalError:
            return
    

    def NotEqual(self, **args) -> list:
        filter_key_vals = ''
        
        for k, v in args.items():
            filter_key_vals += f'AND {k} != "{v}" '

        # Remove the first and in text
        filter_key_vals = filter_key_vals[3:].strip()
        #print(filter_key_vals)

        q = f'''
        SELECT * FROM {self.table_name} WHERE {filter_key_vals}
         '''.strip()
        
        try:
            results = self.cursor.execute(q).fetchall()
            self.db.commit()
            return self.show_results(results)
        except sqlite3.OperationalError:
            return
    
    def FindBy(self, **args) -> list:
        return self.GetBy(**args)
    
    def FindOne(self, **args) -> dict:
        records = self.FindBy(**args)
        if records:
            return records[0]
    
    def FilterBy(self, **args) -> list:
        return self.GetBy(**args)
    
    def Filter(self, filter_keys: dict) -> dict:
        filtred_records = []
        # get column names
        for col in filter_keys.keys():
            # get filter keys and values
            key_filters = list(filter_keys[col])
            for k in key_filters:
                if k in self.allowed_filters:
                    value = filter_keys[col][k]
                    # Build the query based on the filter key
                    if k == 'between':
                        q = f'''
                            SELECT * FROM {self.table_name} 
                            WHERE {col} BETWEEN {value[0]} AND {value[1]}'''
                    
                    elif k == 'larger_than':
                        q = f'''
                            SELECT * FROM {self.table_name} 
                            WHERE {col} > {value}'''
                    
                    elif k == 'larger_or_equal':  # Added filter
                        q = f'''
                            SELECT * FROM {self.table_name} 
                            WHERE {col} >= {value}'''
                    
                    elif k == 'less_than':
                        q = f'''
                            SELECT * FROM {self.table_name} 
                            WHERE {col} < {value}'''
                    
                    elif k == 'less_or_equal':  # Previously added filter
                        q = f'''
                            SELECT * FROM {self.table_name} 
                            WHERE {col} <= {value}'''
                    
                    elif k == 'not':
                        q = f'''
                            SELECT * FROM {self.table_name} 
                            WHERE {col} != {value}'''
                    
                    elif k == 'equal':
                        q = f'''
                            SELECT * FROM {self.table_name} 
                            WHERE {col} = {value}'''
                    
                    # Execute the query and collect results
                    try:
                        filtred_records.append(
                            dict(
                                key=col,
                                records=self.show_results(
                                    self.cursor.execute(q).fetchall()
                                ),
                            )
                        )
                    except Exception as e:
                        print(f"Error executing query: {q}, Error: {str(e)}")
                        return

        return filtred_records

    

    def Update(self, uuid, data: dict) -> dict:

        data = sanitize_data(data)
        

        filter_keys = ''

        for k in data:
            filter_keys += f'{k} = ? , '

        # remove the last , in 
        filter_keys = filter_keys[:-2]
        #print(filter_keys)

        q = f'''UPDATE {self.table_name} SET {filter_keys} 
        WHERE uuid = "{uuid}"  '''.strip()

        #print(q)

        try:
            self.cursor.execute(q, tuple([v for v in data.values()]))
            self.db.commit()

            return self.GetByID(uuid = uuid)
        except sqlite3.OperationalError:
            return
        

    def UpdateMany(self, data : dict, **args) -> list:
        records = self.GetBy(**args)
        for record in records:
            self.Update(uuid = record['uuid'], data = data)

        return self.FilterBy(**data)

    def Delete(self, uuid) -> bool:
        try:
            q = f'DELETE FROM {self.table_name} WHERE uuid = ?'
            self.cursor.execute(q, (uuid,))
            self.db.commit()
            return True
        except sqlite3.OperationalError:
            return
    

    def DeleteMany(self, **args) -> bool:
        records = self.GetBy(**args)
        for record in records:
            self.Delete(uuid = record['uuid'])

        return True
    

    def convert(self):
        try:
            records = {k:[] for k in self.get_column_names()}
            all_records = self.GetALL()
            for i, r in enumerate(all_records):
                record = all_records[i]
                for k in r:
                    records[k].append(record[k])
            
            return pd.DataFrame(data=records)
        except sqlite3.OperationalError:
            return
        



class SmileyDB3:
    def __init__(self, database, **args):
        self.database = database
        self.conn = sqlite3.connect(self.database, **args)
        self.cursor = self.conn.cursor()

    def table(self, table_name, make_uuid = True, created_at = True) -> Table:
        return Table(table_name, self.conn, self.cursor, make_uuid, created_at)

