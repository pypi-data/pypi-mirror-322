
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
from dataanalysts.exceptions import DataVisualizationError

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    filename='visualizer.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Histogram
def histogram(df, column, bins=30, kde=True):
    """
    Plot a histogram for a specified column.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name for plotting.
        bins (int): Number of bins for the histogram.
        kde (bool): Whether to show Kernel Density Estimate.
    """
    try:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[column], bins=bins, kde=kde, color='skyblue')
        plt.title(f'Histogram of {column}', fontsize=14)
        plt.xlabel(column, fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()
        logging.info(f"Histogram plotted for column: {column}")
    except Exception as e:
        logging.error(f"Histogram Error: {str(e)}")
        raise DataVisualizationError(f"Histogram Error: {str(e)}")

# Bar Chart
def barchart(df, x_col, y_col):
    """
    Plot a bar chart for two specified columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        x_col (str): Column for x-axis.
        y_col (str): Column for y-axis.
    """
    try:
        plt.figure(figsize=(12, 7))
        sns.barplot(x=x_col, y=y_col, data=df, palette='viridis')
        plt.title(f'Bar Chart: {x_col} vs {y_col}', fontsize=14)
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.show()
        logging.info(f"Bar Chart plotted for columns: {x_col} vs {y_col}")
    except Exception as e:
        logging.error(f"Bar Chart Error: {str(e)}")
        raise DataVisualizationError(f"Bar Chart Error: {str(e)}")

# Line Plot
def linechart(df, x_col, y_col):
    """
    Plot a line chart for two specified columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        x_col (str): Column for x-axis.
        y_col (str): Column for y-axis.
    """
    try:
        plt.figure(figsize=(12, 7))
        sns.lineplot(x=x_col, y=y_col, data=df, marker='o', color='blue')
        plt.title(f'Line Plot: {x_col} vs {y_col}', fontsize=14)
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()
        logging.info(f"Line Plot plotted for columns: {x_col} vs {y_col}")
    except Exception as e:
        logging.error(f"Line Plot Error: {str(e)}")
        raise DataVisualizationError(f"Line Plot Error: {str(e)}")

# Scatter Plot
def scatter(df, x_col, y_col, hue=None):
    """
    Plot a scatter plot for two specified columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        x_col (str): Column for x-axis.
        y_col (str): Column for y-axis.
        hue (str): Column for color encoding.
    """
    try:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=x_col, y=y_col, data=df, hue=hue, palette='viridis')
        plt.title(f'Scatter Plot: {x_col} vs {y_col}', fontsize=14)
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.show()
        logging.info(f"Scatter Plot plotted for columns: {x_col} vs {y_col}")
    except Exception as e:
        logging.error(f"Scatter Plot Error: {str(e)}")
        raise DataVisualizationError(f"Scatter Plot Error: {str(e)}")

# Heatmap
def heatmap(df, annot=True, cmap='coolwarm'):
    """
    Plot a heatmap showing the correlation between numeric columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        annot (bool): Whether to annotate the heatmap with correlation values.
        cmap (str): Colormap for the heatmap.
    """
    try:
        plt.figure(figsize=(12, 8))
        sns.heatmap(df.corr(), annot=annot, cmap=cmap, fmt='.2f')
        plt.title('Heatmap of Correlation Matrix', fontsize=14)
        plt.show()
        logging.info("Heatmap plotted successfully.")
    except Exception as e:
        logging.error(f"Heatmap Error: {str(e)}")
        raise DataVisualizationError(f"Heatmap Error: {str(e)}")

# Pair Plot
def pairplot(df, hue=None):
    """
    Plot a pairplot for all numeric columns in the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        hue (str): Column for color encoding.
    """
    try:
        sns.pairplot(df, hue=hue, palette='coolwarm')
        plt.show()
        logging.info("Pairplot plotted successfully.")
    except Exception as e:
        logging.error(f"Pairplot Error: {str(e)}")
        raise DataVisualizationError(f"Pairplot Error: {str(e)}")

# Box Plot
def boxplot(df, x_col, y_col):
    """
    Plot a box plot for specified columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        x_col (str): Column for x-axis.
        y_col (str): Column for y-axis.
    """
    try:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=x_col, y=y_col, data=df, palette='Set2')
        plt.title(f'Box Plot: {x_col} vs {y_col}', fontsize=14)
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()
        logging.info(f"Box Plot plotted for columns: {x_col} vs {y_col}")
    except Exception as e:
        logging.error(f"Box Plot Error: {str(e)}")
        raise DataVisualizationError(f"Box Plot Error: {str(e)}")

# Violin Plot
def violinplot(df, x_col, y_col):
    """
    Plot a violin plot for specified columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        x_col (str): Column for x-axis.
        y_col (str): Column for y-axis.
    """
    try:
        plt.figure(figsize=(10, 6))
        sns.violinplot(x=x_col, y=y_col, data=df, palette='muted')
        plt.title(f'Violin Plot: {x_col} vs {y_col}', fontsize=14)
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()
        logging.info(f"Violin Plot plotted for columns: {x_col} vs {y_col}")
    except Exception as e:
        logging.error(f"Violin Plot Error: {str(e)}")
        raise DataVisualizationError(f"Violin Plot Error: {str(e)}")

# Interactive Visualization
def interactive_plot(df):
    """
    Interactive function for selecting visualization types.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
    """
    try:
        while True:
            print("\nInteractive Data Visualization Options:")
            print("1. Histogram")
            print("2. Bar Chart")
            print("3. Line Plot")
            print("4. Scatter Plot")
            print("5. Heatmap")
            print("6. Pair Plot")
            print("7. Box Plot")
            print("8. Violin Plot")
            print("9. Exit Visualization")

            option = input("Enter your choice (1-9): ").strip()

            if option == '1':
                column = input("Enter column for Histogram: ").strip()
                bins = int(input("Enter number of bins: ").strip())
                kde = input("Show KDE? (yes/no): ").strip().lower() == 'yes'
                histogram(df, column, bins=bins, kde=kde)
            elif option == '2':
                x_col = input("Enter X-axis column: ").strip()
                y_col = input("Enter Y-axis column: ").strip()
                barchart(df, x_col, y_col)
            elif option == '3':
                x_col = input("Enter X-axis column: ").strip()
                y_col = input("Enter Y-axis column: ").strip()
                linechart(df, x_col, y_col)
            elif option == '4':
                x_col = input("Enter X-axis column: ").strip()
                y_col = input("Enter Y-axis column: ").strip()
                hue = input("Enter column for color encoding (optional): ").strip()
                scatter(df, x_col, y_col, hue=hue if hue else None)
            elif option == '5':
                heatmap(df)
            elif option == '6':
                hue = input("Enter column for color encoding (optional): ").strip()
                pairplot(df, hue=hue if hue else None)
            elif option == '7':
                x_col = input("Enter X-axis column: ").strip()
                y_col = input("Enter Y-axis column: ").strip()
                boxplot(df, x_col, y_col)
            elif option == '8':
                x_col = input("Enter X-axis column: ").strip()
                y_col = input("Enter Y-axis column: ").strip()
                violinplot(df, x_col, y_col)
            elif option == '9':
                print("Exiting Visualization.")
                break
            else:
                print("Invalid option. Please try again.")

        logging.info("Interactive visualization session completed successfully.")
    except Exception as e:
        logging.error(f"Interactive Visualization Error: {str(e)}")
        raise DataVisualizationError(f"Interactive Visualization Error: {str(e)}")
