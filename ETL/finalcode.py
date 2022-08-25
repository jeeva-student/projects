import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import mysql.connector
from sklearn import preprocessing
# from textblob import Word
import xml.etree.ElementTree as ET
from dateutil.parser import parse

# Getting input from xml file
dbdoc = ET.parse('dbandpath.xml')
for d in dbdoc.iterfind('DBbody'):
    db_username = d.findtext('db_username')
    db_pwd = d.findtext('password')
    db_host = d.findtext('host')
    db_database = d.findtext('db_database')
    path = d.findtext('file_path')
    table1 = d.findtext('db_table1')
    table2 = d.findtext('db_table2')

# declaration of global dataframe
df = pd.DataFrame()


def transfrom(df):
    print("1. Basic Function (NULL values to -1) and Droping the duplicates and  \n"
          "2. replacing the miss addressed values in the dataset \n"
          "3. Encoding - Label Encoding and One hot encoding \n"
          "4. Transform - convert rows or columns and columns into rows \n")

    def transform_pose(df):
        df.transpose()
        return df

    def encoding(df):
        global feature

        def label_encode(df):
            global feature
            feature = []
            le = preprocessing.LabelEncoder()
            for i in df.columns:
                if df[i].dtypes == "object":
                    feature.append(i)
            print(feature)
            b = [str(x) for x in input("enter the column name : ").split()]
            for i in b:
                df[i] = le.fit_transform(df[i])
                print("the label encoding is done...")
                print(df[i].unique())

        def one_hotencode(df):
            feature = []
            for i in df.columns:
                if df[i].dtypes == "object":
                    feature.append(i)
            print(feature)
            b = [str(x) for x in input("enter the column name : ").split()]
            for i in b:
                df = pd.get_dummies(df, columns=[i])
                df.drop(df[i], axis=0)
            print(df)

        print("enter 1. for label encoding \n enter 2. for one hot encoding \n enter 3. for exit")
        a = int(input("enter your option : "))
        if a == 3:
            transfrom(df)
        elif a == 1:
            label_encode(df)
        elif a == 2:
            one_hotencode(df)

    #removes columns with max null valuesmy
    def valid(df):
        feature = df.columns
        df.replace(np.NAN, -1, inplace=True)
        a = []
        for i in range(len(feature) - 1):
            a.append(df.columns[i])
        b = a[0:2]
        for i in range(len(b)):
            df = df.drop(index=df[df[[a[i]][0]] == -1.0].index)
            print("done")

    def convert_time_to_std(df):
        feature = []
        temptime = []
        col_name = input('Enter the column name containing timestamp: ')
        for i in df[col_name]:
            feature.append(i)
        for ch in feature:
            try:
                temptime.append(parse(ch))
            except:
                print('Unable to convert the string into std time format')
        return temptime

    # Mergeing two tables if there exists a primary key colm in both the tables
    # to merge two different dataframes
    def merge(df):
        print(
            "1. Enter 1 for CSV \n 2. Enter 2 for TSV \n 3. Enter 3 for XLSX \n 4. Enter 4 for JSON \n 5. Enter 5 to exit")
        a = int(input("Enter the number : "))
        if a == 5:
            exit()
        elif a == 1:
            df1 = pd.read_csv(input("Enter the file : "))
        elif a == 2:
            df1 = pd.read_csv(input("Enter the file : "))
        elif a == 3:
            df1 = pd.read_excel(input("Enter the file : "))
        elif a == 4:
            df1 = pd.read_json(input("Enter the file : "))

        # print(df1.head(5))
        c = []
        b = []
        for i in df.columns:
            b.append(i)
        for i in df1.columns:
            c.append(i)

        d = []
        for i in b:
            if i in c:
                d.append(i)
        print("The matching columns are: ", d)

        print("if you want to merge these columns \n 1. Enter YES to countinue \n 2. Enter NO to back")
        e = str(input("Enter YES or NO here : "))
        if e == "NO":
            transfrom()
        elif e == "YES":
            result = pd.merge(df, df1, on=[d[0]])
        print(result)

    def basic(df):
        print(df.isnull().sum())
        print(df.info())
        df.replace(np.NAN, -1, inplace=True)
        features = df.columns
        for i in features:
            if df[i].dtypes == "object":
                print(df[i].name)
        print("these are the catogorical columns")
        for i in features:
            if df[i].dtypes != "object":
                df.drop_duplicates(i, inplace=True)
            print(np.unique(df[i]))
            print("----------------------------------------")

    print("1. Enter 1 to basic transform \n 2. Enter 2 to merge function \n 3. Enter 3 to encoding \n "
          "4. Enter 4 to transform \n 5. Enter 5 to drop rows if the first two columns has null values \n"
          "6. Enter 6 to date time function \n7. Enter 7 to exit")
    while (True):
        a = int(input("Enter the number : "))
        if a == 7:
            get_input()
        elif a == 1:
            basic(df)
        elif a == 2:
            merge(df)
        elif a == 3:
            encoding(df)
        elif a == 4:
            transform_pose(df)
        elif a == 5:
            valid(df)
        elif a == 6:
            convert_time_to_std(df)


def get_input():
    for ch in path:
        if ch == '.':
            ext = path[path.index(ch) + 1:]
            print(ext)

    if ext == 'csv':
        try:
            df = pd.read_csv(path)
            print('csv file read successfully')
            return df
        except:
            print('Error while reading csv file ')
    elif ext == 'tsv':
        try:
            df = pd.read_csv(path, sep='\t')
            print('tsv file sucessfully ')
            return df
        except:
            print('Error while reading tsv file')

    elif ext == 'xlsx':
        try:
            df = pd.read_excel(path)
            print("Excel file read sucessfully")
            return df
        except:
            print('Error while reading excel file ')

    elif ext == 'json':
        try:
            df = pd.read_json(path)
            print("Json file read successfully")
            return df
        except:
            print("Error while reading Json file")
    elif ext == 'txt':
        f = path
        df = np.loadtxt(f, delimiter=',', skiprows=1, dtype=str)
        return df
    # Function needs to be changed for db
    else:
        ch = input('Do you want to import from database(Y/N): ')
        if ch == 'Y' or ch == 'y':
            try:
                print(db_host)
                mydb = mysql.connector.connect(
                    host=db_host,
                    database=db_database,
                    password=db_pwd
                )
                print("Sucessfully connected to database")
            except:
                print("Unable to connect to database")

            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM " + table1)
            sq_data = mycursor.fetchall()
            df = pd.DataFrames(sq_data)
            return df
        else:
            print('Unbable to determine the file type')


df = get_input()