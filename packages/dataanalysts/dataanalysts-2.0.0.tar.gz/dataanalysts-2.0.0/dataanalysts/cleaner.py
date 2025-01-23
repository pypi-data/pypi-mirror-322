
import pandas as pd
import numpy as np
import logging
from dataanalysts.exceptions import DataCleaningError

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    filename='cleaner.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def clean(df, strategy='mean', handle_outliers=False, drop_threshold=0.5):
    """
    Clean the dataset by handling missing values, outliers, duplicates, inconsistent data, and scaling numeric features.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        strategy (str): Strategy for filling missing values ('mean', 'median', 'mode').
        handle_outliers (bool): If True, handles outliers in numeric columns using the IQR method.
        drop_threshold (float): Proportion of missing values in a column to drop it (0 to 1).

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    try:
        # Drop columns with high missing value proportion
        initial_columns = df.shape[1]
        df = df.loc[:, df.isnull().mean() < drop_threshold]
        dropped_columns = initial_columns - df.shape[1]
        if dropped_columns > 0:
            print(f"Dropped {dropped_columns} columns with more than {drop_threshold * 100}% missing values.")

        # Handling missing values
        numeric_columns = df.select_dtypes(include=['number']).columns
        non_numeric_columns = df.select_dtypes(exclude=['number']).columns

        if strategy == 'mean':
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
        elif strategy == 'median':
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
        elif strategy == 'mode':
            for col in df.columns:
                df[col] = df[col].fillna(df[col].mode()[0])
        else:
            raise ValueError("Invalid strategy: Choose 'mean', 'median', or 'mode'.")

        for col in non_numeric_columns:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].mode()[0])

        # Handle outliers if specified
        if handle_outliers:
            for col in numeric_columns:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
                df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

        # Renaming columns to standardized format
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

        # Encoding categorical variables
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = pd.Categorical(df[col]).codes

        # Feature scaling
        for col in numeric_columns:
            df[col] = (df[col] - df[col].mean()) / df[col].std()

        # Removing duplicates
        initial_rows = len(df)
        df.drop_duplicates(inplace=True)
        removed_rows = initial_rows - len(df)
        if removed_rows > 0:
            print(f"Removed {removed_rows} duplicate rows.")

        logging.info(
            "Data cleaned successfully with strategy: %s, outlier handling: %s, drop threshold: %s",
            strategy, handle_outliers, drop_threshold
        )
        print(f"Data cleaned successfully using strategy: {strategy}, outlier handling: {handle_outliers}, and drop threshold: {drop_threshold}")
        return df

    except Exception as e:
        logging.error("Data Cleaning Error: %s", str(e))
        raise DataCleaningError(f"Data Cleaning Error: {str(e)}")

def interactive_clean(df):
    """
    Interactive cleaning process for larger datasets with advanced options.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    try:
        while True:
            print("\nInteractive Cleaning Options:")
            print("1. Handle Missing Values (mean/median/mode)")
            print("2. Remove Duplicates")
            print("3. Drop Columns")
            print("4. Rename Columns")
            print("5. Handle Outliers")
            print("6. Encode Categorical Variables")
            print("7. Scale Features")
            print("8. Exit")

            option = input("Choose an option (1-8): ").strip()

            if option == '1':
                strategy = input("Enter strategy (mean/median/mode): ").strip()
                drop_threshold = float(input("Enter drop threshold for missing values (0-1): ").strip())
                df = clean(df, strategy, drop_threshold=drop_threshold)
            elif option == '2':
                df.drop_duplicates(inplace=True)
                print("Duplicates removed.")
            elif option == '3':
                cols = input("Enter columns to drop (comma-separated): ").split(',')
                df.drop(columns=cols, inplace=True, errors='ignore')
                print("Columns dropped successfully.")
            elif option == '4':
                print("Current columns:", list(df.columns))
                cols = input("Enter new column names (comma-separated, in order): ").split(',')
                if len(cols) != len(df.columns):
                    print("Number of new column names must match the existing columns.")
                else:
                    df.columns = cols
                    print("Columns renamed successfully.")
            elif option == '5':
                df = clean(df, handle_outliers=True)
            elif option == '6':
                print("Encoding categorical variables.")
                categorical_cols = df.select_dtypes(include=['object']).columns
                for col in categorical_cols:
                    df[col] = pd.Categorical(df[col]).codes
                print("Categorical variables encoded.")
            elif option == '7':
                print("Scaling numeric features.")
                numeric_columns = df.select_dtypes(include=['number']).columns
                for col in numeric_columns:
                    df[col] = (df[col] - df[col].mean()) / df[col].std()
                print("Features scaled.")
            elif option == '8':
                print("Exiting Interactive Cleaning.")
                break
            else:
                print("Invalid option. Please try again.")

        logging.info("Interactive cleaning completed successfully.")
        return df

    except Exception as e:
        logging.error("Interactive Cleaning Error: %s", str(e))
        raise DataCleaningError(f"Interactive Cleaning Error: {str(e)}")
