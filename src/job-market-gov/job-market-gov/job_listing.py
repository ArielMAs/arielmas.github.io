import pandas as pd
import argparse
import os


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
    df['NormalizedMeanSalary'] = df[["NormalizedMinSalary", "NormalizedMaxSalary"]].mean(axis=1)
    df['NormalizedRangeSalary'] = df['NormalizedMaxSalary']-df['NormalizedMinSalary']
    return df


def write_to_parquet(jobs,duties,locations,job_category,first_run):
    os.makedirs('./job-market-gov/data/', exist_ok=True)
    # Path to the Parquet file
    files_dict = {'jobs':jobs,
                  'duties':duties,
                  'locations':locations,
                  'job_category':job_category}
    for df_name,df_current in files_dict.items():
        p_path = f'./job-market-gov/data/{df_name}.parquet'
        if first_run:
            # Write the DataFrame back to the Parquet file
            df_current.to_parquet(p_path, engine='pyarrow', index=False)
        else:
            try:
                # Try reading the existing Parquet file
                existing_df = pd.read_parquet(p_path)
                # Append the new data to the existing DataFrame
                combined_df = pd.concat([existing_df, df_current], ignore_index=True)
            except FileNotFoundError:
                # If the file doesn't exist, create a new DataFrame with the new data
                combined_df = df_current

            # Write the combined DataFrame back to the Parquet file
            combined_df.to_parquet(p_path, engine='pyarrow', index=False)


def main(path,first_run):
    print('starting')
    df_clean = pd.read_json(path)
    userArea = pd.json_normalize(df_clean['UserArea'],sep='_')
    df_clean = df_clean.join(userArea)
    locations = sub_object_json_extractor(df=df_clean,json_col='PositionLocation',columns_to_keep=['LocationName', 'CountryCode', 'CountrySubDivisionCode', 'CityName', 'Longitude', 'Latitude'])
    job_category = sub_object_json_extractor(df=df_clean,json_col='JobCategory',columns_to_keep=['Name', 'Code'])
    df_clean = rumenation_extractor(df=df_clean)
    df_clean['date_col'] = pd.to_datetime(df_clean['PublicationStartDate']).dt.date
    duties = df_clean[['PositionID','Details_MajorDuties']].explode('Details_MajorDuties')
    jobs = df_clean.drop(['UserArea','PositionLocation','JobCategory','Details_MajorDuties','MinimumRange','MaximumRange','RateIntervalCode','PublicationStartDate','PositionRemuneration'],axis=1)
    write_to_parquet(jobs,duties,locations,job_category,first_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process job market data and store in parquet files.")
    parser.add_argument("path", type=str, help="Path to the JSON file")
    parser.add_argument("--first_run",
                        type=bool,
                        default=False,  # Default value if not provided
                        help="Indicate if it's the first run or not (default is False)")
    
    args = parser.parse_args()
    # Access the value of first_run
    main(args.path,args.first_run)
