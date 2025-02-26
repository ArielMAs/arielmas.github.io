import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from pandas import json_normalize
from sqlalchemy import create_engine
import sys
import json
import argparse

def sub_object_json_extractor(df,json_col,columns_to_keep):
    loce_df = df[['PositionID',json_col]].explode(json_col)#this wil be moved to its own table

    # Flatten the nested dictionary in the 'PositionLocation' column
    location_df = pd.json_normalize(loce_df[json_col])
    # Merge back into the original dataframe
    locations = loce_df.join(location_df[columns_to_keep]).drop(json_col,axis=1)
    return locations




def rumenation_extractor(df):
    # Flatten the nested dictionary in the 'PositionLocation' column
    remuneration_df_explode = df.explode('PositionRemuneration')
    remuneration_df = pd.json_normalize(remuneration_df_explode['PositionRemuneration'])

    # Select only the required columns
    columns_to_keep = ['MinimumRange', 'MaximumRange','RateIntervalCode']

    # Merge back into the original dataframe
    df = df.join(remuneration_df[columns_to_keep])

    df['MinimumRange'] = pd.to_numeric(df['MinimumRange'])
    df['MaximumRange'] = pd.to_numeric(df['MaximumRange'])
    #feature generating
    #Yearly Salary=Hourly Wage×40×52
    def normalized_salary(row,col_name):
        s = row[col_name]
        rateCode = row['RateIntervalCode']
        if rateCode=='PH':
            return 40*52*s
        elif rateCode=='PA':
            return s

    df['NormalizedMinSalary'] = df.apply(lambda row: normalized_salary(row, 'MinimumRange'), axis=1)
    df['NormalizedMaxSalary'] = df.apply(lambda row: normalized_salary(row, 'MaximumRange'), axis=1)
    df['mean_salary'] = df[["NormalizedMinSalary", "NormalizedMaxSalary"]].mean(axis=1)
    return df


def write_to_postgres(schema_name,jobs,duties,locations,job_category):
    load_dotenv("secrets.env")
        
    postgresPassword = os.getenv("POSTGRES_PASSWORD")
    postgresUserName = os.getenv("POSTGRES_USER_NAME")
    postgresPort = os.getenv("POSTGRES_PORT")

    conn = psycopg2.connect(host='localhost',dbname='jobs_us', user=postgresUserName, password=postgresPassword,port=postgresPort)

    cur = conn.cursor()
    

    create_schema_q = f'''
    CREATE SCHEMA IF NOT EXISTS {schema_name};
                '''
    cur.execute(create_schema_q)
    conn.commit()


    engine = create_engine(f'postgresql+psycopg2://postgres:machal2010@localhost:5432/jobs_us')

    jobs.to_sql('jobs', engine, if_exists='replace', index=False,schema = schema_name)

    duties.to_sql('duties', engine, if_exists='replace', index=False,schema = schema_name)

    locations.to_sql('locations', engine, if_exists='replace', index=False,schema = schema_name)

    job_category.to_sql('job_category', engine, if_exists='replace', index=False,schema = schema_name)

    conn.close()

def main(path,schema_name):
    df_clean = pd.read_json(path)
    userArea = pd.json_normalize(df_clean['UserArea'],sep='_')
    df_clean = df_clean.join(userArea)
    locations = sub_object_json_extractor(df=df_clean,json_col='PositionLocation',columns_to_keep=['LocationName', 'CountryCode', 'CountrySubDivisionCode', 'CityName', 'Longitude', 'Latitude'])
    job_category = sub_object_json_extractor(df=df_clean,json_col='JobCategory',columns_to_keep=['Name', 'Code'])
    df_clean = rumenation_extractor(df=df_clean)
    df_clean['date_col'] = pd.to_datetime(df_clean['PublicationStartDate']).dt.date
    duties = df_clean[['PositionID','Details_MajorDuties']].explode('Details_MajorDuties')
    jobs = df_clean.drop(['UserArea','PositionLocation','JobCategory','Details_MajorDuties','MinimumRange','MaximumRange','RateIntervalCode','PublicationStartDate','PositionRemuneration'],axis=1)
    write_to_postgres(schema_name=schema_name,jobs=jobs,duties=duties,locations=locations,job_category=job_category)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process job market data and store in PostgreSQL.")
    parser.add_argument("path", type=str, help="Path to the JSON file")
    parser.add_argument("schema_name", type=str, help="Schema name for the database")
    
    args = parser.parse_args()
    main(args.path, args.schema_name)
