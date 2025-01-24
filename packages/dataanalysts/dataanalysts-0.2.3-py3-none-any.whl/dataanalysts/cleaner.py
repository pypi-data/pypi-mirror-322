
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

def clean(df, strategy='mean', handle_outliers=False, drop_threshold=0.5, convert_to_numeric=False):
    """
    Advanced cleaning of the dataset: missing values, outliers, duplicates, inconsistent data, encoding, scaling, and optional string-to-numeric conversion.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        strategy (str): Cleaning operation ('mean', 'median', 'mode', 'remove_duplicates', 'fill_unknown', 'convert_to_numeric', 'impute_by_group', 'drop_low_variance').
        handle_outliers (bool): If True, handles outliers in numeric columns using the IQR method.
        drop_threshold (float): Proportion of missing values in a column to drop it (0 to 1).
        convert_to_numeric (bool): If True, convert applicable string columns to numeric values.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    try:
        # 1. Drop columns with high missing value proportion
        initial_columns = df.shape[1]
        df = df.loc[:, df.isnull().mean() < drop_threshold]
        dropped_columns = initial_columns - df.shape[1]
        if dropped_columns > 0:
            print(f"Dropped {dropped_columns} columns with more than {drop_threshold * 100}% missing values.")

        # Handle strategy-specific operations
        if strategy == 'remove_duplicates':
            initial_rows = len(df)
            df.drop_duplicates(inplace=True)
            removed_rows = initial_rows - len(df)
            if removed_rows > 0:
                print(f"Removed {removed_rows} duplicate rows.")
        elif strategy == 'fill_unknown':
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].fillna('Unknown')
                elif pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(0)
            print("Filled unknown values for categorical and numeric columns.")
        elif strategy in ['mean', 'median', 'mode']:
            numeric_columns = df.select_dtypes(include=['number']).columns
            non_numeric_columns = df.select_dtypes(exclude=['number']).columns

            for col in numeric_columns:
                if strategy == 'mean':
                    df[col].fillna(df[col].mean(), inplace=True)
                elif strategy == 'median':
                    df[col].fillna(df[col].median(), inplace=True)
                elif strategy == 'mode' and not df[col].mode().empty:
                    df[col].fillna(df[col].mode()[0], inplace=True)

            for col in non_numeric_columns:
                if df[col].isnull().any():
                    if not df[col].mode().empty:
                        df[col] = df[col].fillna(df[col].mode()[0])
        elif strategy == 'convert_to_numeric' or convert_to_numeric:
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            print("Converted applicable numeric columns to numeric values where possible.")
        elif strategy == 'impute_by_group':
            group_column = input("Enter the column to group by: ").strip()
            if group_column in df.columns:
                for col in df.columns:
                    if df[col].isnull().any():
                        if pd.api.types.is_numeric_dtype(df[col]):
                            df[col] = df.groupby(group_column)[col].transform(lambda x: x.fillna(x.mean()))
                        else:
                            df[col] = df.groupby(group_column)[col].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 'Unknown'))
                print(f"Imputed missing values by group based on column: {group_column}")
        elif strategy == 'drop_low_variance':
            threshold = float(input("Enter variance threshold to drop columns: ").strip())
            low_variance_cols = [col for col in df.select_dtypes(include=['number']).columns if df[col].var() < threshold]
            df.drop(columns=low_variance_cols, inplace=True)
            print(f"Dropped columns with variance below {threshold}: {low_variance_cols}")

        # 2. Handle outliers using the IQR method
        if handle_outliers:
            numeric_columns = df.select_dtypes(include=['number']).columns
            for col in numeric_columns:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
                df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

        # 3. Standardize column names
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

        # 4. Encode categorical variables
        non_numeric_columns = df.select_dtypes(include=['object']).columns
        for col in non_numeric_columns:
            if df[col].dtype.name == 'object':
                df[col] = pd.Categorical(df[col]).codes

        # 5. Feature scaling (Normalization)
        numeric_columns = df.select_dtypes(include=['number']).columns
        for col in numeric_columns:
            df[col] = (df[col] - df[col].mean()) / df[col].std()

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
    Interactive cleaning process for datasets with user-defined options.

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
            print("7. Fill Unknown Values")
            print("8. Convert Strings to Numeric")
            print("9. Impute Missing Values by Group")
            print("10. Drop Low Variance Columns")
            print("11. Scale Features")
            print("12. Exit")

            option = input("Choose an option (1-12): ").strip()

            if option == '1':
                strategy = input("Enter strategy (mean/median/mode): ").strip()
                drop_threshold = float(input("Enter drop threshold for missing values (0-1): ").strip())
                df = clean(df, strategy, drop_threshold=drop_threshold)
            elif option == '2':
                df = clean(df, strategy='remove_duplicates')
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
                non_numeric_columns = df.select_dtypes(include=['object']).columns
                for col in non_numeric_columns:
                    df[col] = pd.Categorical(df[col]).codes
                print("Categorical variables encoded.")
            elif option == '7':
                df = clean(df, strategy='fill_unknown')
            elif option == '8':
                df = clean(df, strategy='convert_to_numeric', convert_to_numeric=True)
            elif option == '9':
                df = clean(df, strategy='impute_by_group')
            elif option == '10':
                df = clean(df, strategy='drop_low_variance')
            elif option == '11':
                print("Scaling numeric features.")
                numeric_columns = df.select_dtypes(include=['number']).columns
                for col in numeric_columns:
                    df[col] = (df[col] - df[col].mean()) / df[col].std()
                print("Features scaled.")
            elif option == '12':
                print("Exiting Interactive Cleaning.")
                break
            else:
                print("Invalid option. Please try again.")

        logging.info("Interactive cleaning completed successfully.")
        return df

    except Exception as e:
        logging.error("Interactive Cleaning Error: %s", str(e))
        raise DataCleaningError(f"Interactive Cleaning Error: {str(e)}")
