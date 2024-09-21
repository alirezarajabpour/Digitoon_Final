def aggregate_data():
    #import sys
    #sys.path.append("/opt/airflow/include/my_package/src")

    import pandas as pd
    from sqlalchemy import create_engine

    # Define the MySQL connection URL
    mysql_url = 'mysql+mysqlconnector://root:root@mysql:3306/transactions'

    # Create an SQLAlchemy engine
    engine = create_engine(mysql_url)

    # Query your desired data (replace 'your_table_name' with the actual table name)
    query = 'SELECT * FROM clean_store_transactions'

    # Read data into a pandas DataFrame
    clean_store_transactions = pd.read_sql(query, con=engine)

    # Now you can work with the 'df' DataFrame as needed
    print(clean_store_transactions.head())  # Display the first few rows

    # Assuming you have a DataFrame called 'clean_store_transactions' with relevant columns (DATE, STORE_LOCATION, STORE_ID, SP, CP)

    # Location-wise profit
    location_wise_profit = (
        clean_store_transactions.groupby(['DATE', 'STORE_LOCATION'])
        .agg(lc_sp=pd.NamedAgg(column='SP', aggfunc='sum'),
            lc_cp=pd.NamedAgg(column='CP', aggfunc='sum'))
        .reset_index()
    )
    location_wise_profit['lc_profit'] = location_wise_profit['lc_sp'] - location_wise_profit['lc_cp']

    # Store-wise profit
    store_wise_profit = (
        clean_store_transactions.groupby(['DATE', 'STORE_ID'])
        .agg(st_sp=pd.NamedAgg(column='SP', aggfunc='sum'),
            st_cp=pd.NamedAgg(column='CP', aggfunc='sum'))
        .reset_index()
    )
    store_wise_profit['st_profit'] = store_wise_profit['st_sp'] - store_wise_profit['st_cp']

    print(location_wise_profit.head())
    print(store_wise_profit.head())

    # Save to CSV files
    location_wise_profit.to_csv('/usr/local/airflow/store_files_airflow/location_wise_profit.csv', index=False)
    store_wise_profit.to_csv('/usr/local/airflow/store_files_airflow/store_wise_profit.csv', index=False)
    
    return "Aggregation completed successfully"