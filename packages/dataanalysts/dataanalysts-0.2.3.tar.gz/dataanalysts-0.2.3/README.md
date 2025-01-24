# DataAnalysts Package

**DataAnalysts** is a robust and versatile Python library meticulously designed to simplify and enhance the data analysis process. It caters to users across diverse domains, including students, professional data analysts, researchers, and enthusiasts. The library integrates powerful modules for data cleaning, transformation, and visualization, enabling seamless handling of datasets with minimal coding effort.

Whether you're dealing with messy datasets or preparing sophisticated visualizations, DataAnalysts offers an intuitive and interactive interface to perform your tasks with precision and efficiency.
---

## 🚀 **Key Features**

### **Data Cleaning:**

- **Handle Missing Values:**

  - Supports mean, median, and mode strategies for numeric columns.
  - Automatically fills missing categorical data using mode.

- **Remove Duplicates:**

  - Eliminates duplicate rows to ensure data integrity.

- **Fill Unknown Values:**

  - Replaces missing categorical data with 'Unknown' and numeric data with `0`.

- **Convert Strings to Numeric:**

  - Converts applicable string columns to numeric where possible.

- **Impute Missing Values by Group:**

  - Fills missing values within groups defined by another column (e.g., by city or category).

- **Drop Low Variance Columns:**

  - Removes columns with variance below a user-specified threshold.

- **Handle Outliers:**

  - Detects and caps outliers in numeric columns using the IQR method.

- **Standardize Column Names:**

  - Renames columns to lowercase, replaces spaces with underscores, and removes extra spaces.

- **Encode Categorical Variables:**

  - Converts categorical columns to numeric codes.

- **Feature Scaling (Normalization):**

  - Scales numeric columns to have a mean of 0 and a standard deviation of 1.

---

### **Interactive Cleaning:**

- **Customizable Options:**

  - Perform cleaning tasks step-by-step through a user-friendly menu interface.

- **Menu Options:**

  - Handle missing values, remove duplicates, drop columns, rename columns, handle outliers, encode categorical variables, fill unknown values, convert strings to numeric, impute missing values by group, drop low variance columns, and scale features.

---

### **Data Transformation:**

- **Scaling:**

  - Standard, Min-Max, and Robust scaling strategies for numeric columns.

- **Encoding:**

  - Label encoding for categorical columns.

- **Dimensionality Reduction:**

  - Principal Component Analysis (PCA) to reduce dataset dimensions.

- **Duplicate Removal:**

  - Automatically remove duplicate rows.

- **Low-Variance Feature Removal:**

  - Remove features with variance below a defined threshold.

- **Interactive Transformation:**

  - Choose transformation steps interactively.

---

### **Data Visualization:**

- **Histogram:**

  - Plot a histogram with advanced customization for bins, labels, and title.

- **Bar Chart:**

  - Generate bar charts with customizable sizes, labels, and colors.

- **Line Plot:**

  - Create line plots with options for markers, colors, and labels.

- **Scatter Plot:**

  - Generate scatter plots with hue-based grouping for better insights.

- **Heatmap:**

  - Visualize correlation matrices using customizable heatmaps.

- **Pair Plot:**

  - Plot pairwise relationships between numeric columns.

- **Box Plot:**

  - Create box plots to visualize data distribution and outliers.

- **Violin Plot:**

  - Generate violin plots to show data distribution with additional density insights.

---

### **Interactive Visualization:**

- **Customizable Options:**

  - Perform visualizations interactively through a user-friendly menu interface.

- **Menu Options:**

  - Choose from histograms, bar charts, line plots, scatter plots, heatmaps, pair plots, box plots, and violin plots.

---

### **Data Loading:**

- **CSV Files:**

  - Easily load datasets from CSV files with automatic logging.

- **Excel Files:**

  - Load data from Excel sheets with customizable sheet selection.

---

### **Error Handling:**

- **Robust Exception Handling:**

  - Provides clear error messages for debugging and ensures smooth execution.

---

### **Interactive Tools:**

- **Data Cleaning:**

  - Step-by-step interactive data cleaning options.

- **Data Transformation:**

  - Hands-on transformation with flexible menu options.

- **Data Visualization:**

  - Interactive plotting with multiple customization options.



---

## 🛠️ **Installation Steps**

### **1. Install the Package from PyPI**
To use the library in Google Colab or your local environment, install it directly from PyPI:

```bash
pip install dataanalysts
!pip install dataanalysts
```

---

## 💡 **Usage Examples**

### **1. Import the Library**
```python
import dataanalysts as da
import pandas as pd
```

### **2. Load Data**
```python
df = da.csv('data.csv')
df_excel = da.excel('data.xlsx', sheet_name='Sheet1')
```

### **3. Data Cleaning**

 These features are designed to provide a one-stop solution for advanced data cleaning tasks, including handling missing values, removing duplicates, imputing missing values, and more.

---

## **1. Handle Missing Values (mean, median, mode)**
- **Explanation**: Fills missing numeric values with either the mean, median, or mode of the column. For categorical columns, the mode is used.
- **Syntax**:
```python
import dataanalysts as da

# Fill missing values using mean strategy
df = da.clean(df, strategy='mean')

# Fill missing values using median strategy
df = da.clean(df, strategy='median')

# Fill missing values using mode strategy
df = da.clean(df, strategy='mode')
```

---

## **2. Remove Duplicates**
- **Explanation**: Removes duplicate rows from the DataFrame.
- **Syntax**:
```python
# Remove duplicate rows
df = da.clean(df, strategy='remove_duplicates')
```

---

## **3. Fill Unknown Values**
- **Explanation**: Fills missing values in categorical columns with `'Unknown'` and numeric columns with `0`.
- **Syntax**:
```python
# Fill unknown values
df = da.clean(df, strategy='fill_unknown')
```

---

## **4. Convert Strings to Numeric**
- **Explanation**: Converts applicable string columns to numeric values where possible. Any invalid conversions are left as-is.
- **Syntax**:
```python
# Convert applicable string columns to numeric
df = da.clean(df, strategy='convert_to_numeric')
```

---

## **5. Impute Missing Values by Group**
- **Explanation**: Groups the data by a specified column and imputes missing values in each group using the mean (for numeric columns) or mode (for categorical columns).
- **Syntax**:
```python
# Impute missing values by group
df = da.clean(df, strategy='impute_by_group')
```
> **Note**: The function will prompt you to enter the column to group by during execution.

---

## **6. Drop Low Variance Columns**
- **Explanation**: Identifies columns with variance below a specified threshold and removes them.
- **Syntax**:
```python
# Drop columns with low variance
df = da.clean(df, strategy='drop_low_variance')
```
> **Note**: You will be prompted to enter the variance threshold during execution.

---

## **7. Handle Outliers**
- **Explanation**: Caps outliers in numeric columns using the IQR (Interquartile Range) method.
- **Syntax**:
```python
# Handle outliers in numeric columns
df = da.clean(df, handle_outliers=True)
```

---

## **8. Standardize Column Names**
- **Explanation**: Renames columns to lowercase, replaces spaces with underscores, and strips extra spaces.
- **Syntax**:
```python
# Standardize column names (part of default cleaning process)
df = da.clean(df)
```

---

## **9. Encode Categorical Variables**
- **Explanation**: Converts categorical columns to numeric codes using pandas' categorical encoding.
- **Syntax**:
```python
# Encode categorical variables (part of default cleaning process)
df = da.clean(df)
```

---

## **10. Feature Scaling (Normalization)**
- **Explanation**: Normalizes numeric columns to have a mean of 0 and a standard deviation of 1.
- **Syntax**:
```python
# Normalize numeric columns
df = da.clean(df)
```

---

## **11. Interactive Cleaning**
- **Explanation**: Provides an interactive interface where the user can choose different cleaning options one at a time.
- **Syntax**:
```python
# Perform interactive cleaning
df = da.interactive_clean(df)
```
> **Example Interactive Menu Options**:
```
Interactive Cleaning Options:
1. Handle Missing Values (mean/median/mode)
2. Remove Duplicates
3. Drop Columns
4. Rename Columns
5. Handle Outliers
6. Encode Categorical Variables
7. Fill Unknown Values
8. Convert Strings to Numeric
9. Impute Missing Values by Group
10. Drop Low Variance Columns
11. Scale Features
12. Exit
```

---

## Comprehensive Example

Here’s how you can use the `clean` function for multiple steps in one go:

```python
import dataanalysts as da
import pandas as pd

# Example dataset
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", None],
    "Age": [25, "30", None, 22, "unknown"],
    "Income": [50000, 60000, None, 45000, "NA"],
    "Gender": ["Female", "Male", None, "Male", "Unknown"],
    "City": ["New York", "Los Angeles", None, "Chicago", "Unknown"]
}

df = pd.DataFrame(data)

# 1. Handle missing values with mean
df = da.clean(df, strategy='mean')

# 2. Fill unknown values
df = da.clean(df, strategy='fill_unknown')

# 3. Remove duplicates
df = da.clean(df, strategy='remove_duplicates')

# 4. Impute missing values by grouping on 'City'
df = da.clean(df, strategy='impute_by_group')

# 5. Drop columns with low variance
df = da.clean(df, strategy='drop_low_variance')

# Print cleaned DataFrame
print(df)
```

This provides you with a one-stop solution for cleaning your dataset comprehensively. Let me know if you need more customizations!


### **4. Data Transformation**

The **Data Transformation Module** enables comprehensive data preprocessing and transformation for datasets, including scaling, dimensionality reduction, encoding, and more. The module supports both direct and interactive transformation methods.

---

### **Key Features**

- **Scaling**: Standard, Min-Max, and Robust scaling strategies for numeric columns.
- **Encoding**: Label encoding for categorical columns.
- **Dimensionality Reduction**: Principal Component Analysis (PCA) to reduce dataset dimensions.
- **Duplicate Removal**: Automatically remove duplicate rows.
- **Low-Variance Feature Removal**: Remove features with variance below a defined threshold.
- **Interactive Transformation**: Choose transformation steps interactively.

---

### **Syntax and Examples**

#### **1. Scaling**

Scales numeric columns based on the selected strategy:

- **Standard Scaling**: Centers data around mean (0) with standard deviation (1).
- **Min-Max Scaling**: Scales data to a range of [0, 1].
- **Robust Scaling**: Handles outliers by scaling data based on the interquartile range (IQR).

**Syntax**:
```python
import dataanalysts as da

# Standard Scaling
df_transformed = da.transform(df, strategy='standard')

# Min-Max Scaling
df_transformed = da.transform(df, strategy='minmax')

# Robust Scaling
df_transformed = da.transform(df, strategy='robust')
```

---

#### **2. Encoding**

Encodes categorical columns into numeric values using label encoding. This is particularly useful for machine learning models that require numeric data.

**Syntax**:
```python
# Encode categorical columns
df_transformed = da.transform(df, encode_categorical=True)
```

---

#### **3. Duplicate Removal**

Automatically removes duplicate rows from the dataset.

**Syntax**:
```python
# Remove duplicate rows
df_transformed = da.transform(df, remove_duplicates=True)
```

---

#### **4. Low-Variance Feature Removal**

Removes features with variance below a specified threshold to reduce noise in the data.

**Syntax**:
```python
# Remove features with variance below 0.01
df_transformed = da.transform(df, remove_low_variance=True, variance_threshold=0.01)
```

---

#### **5. Dimensionality Reduction (PCA)**

Uses Principal Component Analysis to reduce the number of features while retaining most of the variance in the dataset.

**Syntax**:
```python
# Apply PCA to retain 3 components
df_pca = da.transform(df_transformed, reduce_dimensionality=True, n_components=3)
```

---

#### **6. Interactive Transformation**

Provides an interactive menu for selecting transformation steps one at a time.

**Menu Options**:

1. Apply Standard Scaling  
2. Apply Min-Max Scaling  
3. Apply Robust Scaling  
4. Encode Categorical Columns  
5. Remove Duplicates  
6. Remove Low-Variance Features  
7. Apply PCA for Dimensionality Reduction  
8. Exit Transformation

**Syntax**:
```python
# Perform interactive transformation
df_interactive_transform = da.interactive_transform(df)
```

---

### **Comprehensive Example**

Here’s an end-to-end example combining multiple transformations:

```python
import dataanalysts as da
import pandas as pd

# Sample dataset
data = {
    'Age': [25, 30, 35, 40, 45],
    'Salary': [50000, 60000, 70000, 80000, 90000],
    'Department': ['HR', 'IT', 'Finance', 'IT', 'HR']
}
df = pd.DataFrame(data)

# Step 1: Apply standard scaling
df_transformed = da.transform(df, strategy='standard')

# Step 2: Apply PCA to reduce dimensions to 2 components
df_pca = da.transform(df_transformed, reduce_dimensionality=True, n_components=2)

# Step 3: Perform additional transformations interactively
df_final = da.interactive_transform(df_pca)

print(df_final)
```

---

### **Logging**

- Logs are stored in the `transformer.log` file.
- Each transformation step is logged with details about the operation and parameters used.
- Errors during transformations are also logged for debugging purposes.


### **5. Data Visualization**
### **Data Visualization**

The **Data Visualization Module** provides advanced tools for creating insightful and customized visual representations of your dataset. With this module, you can generate a variety of plots, including histograms, scatter plots, heatmaps, and more, with customization options for size, titles, and styles.

---

### **Key Features**

- **Histogram**: Visualize the distribution of a single numeric column.
- **Bar Chart**: Compare values across categories.
- **Line Chart**: Display trends over time or sequential data.
- **Scatter Plot**: Show relationships between two numeric columns.
- **Heatmap**: Visualize correlations between numeric columns.
- **Pair Plot**: Display pairwise relationships in a dataset.
- **Box Plot**: Compare distributions of a numeric column across categories.
- **Violin Plot**: Combine box plot and density plot for richer insights.
- **Interactive Visualization**: Select and generate plots interactively.

---

### **Syntax and Examples**

#### **1. Histogram**
Visualize the distribution of a single numeric column.

**Syntax**:
```python
da.histogram(df, column='age', bins=30, kde=True)
```

**Customization Options**:
- `bins`: Number of bins for the histogram.
- `kde`: Whether to display the Kernel Density Estimate.
- `size`: Tuple specifying figure size.
- `title_fontsize`: Font size for the title.
- `axis_fontsize`: Font size for axis labels.
- `custom_title`: Custom title for the chart.

---

#### **2. Bar Chart**
Compare values across categories.

**Syntax**:
```python
da.barchart(df, x_col='city', y_col='population')
```

**Customization Options**:
- `size`: Tuple specifying figure size.
- `title_fontsize`: Font size for the title.
- `axis_fontsize`: Font size for axis labels.
- `custom_title`: Custom title for the chart.

---

#### **3. Line Chart**
Display trends over time or sequential data.

**Syntax**:
```python
da.linechart(df, x_col='date', y_col='sales')
```

**Customization Options**:
- `size`: Tuple specifying figure size.
- `title_fontsize`: Font size for the title.
- `axis_fontsize`: Font size for axis labels.
- `custom_title`: Custom title for the chart.

---

#### **4. Scatter Plot**
Show relationships between two numeric columns.

**Syntax**:
```python
da.scatter(df, x_col='height', y_col='weight', hue='gender')
```

**Customization Options**:
- `hue`: Column for color encoding.
- `size`: Tuple specifying figure size.
- `title_fontsize`: Font size for the title.
- `axis_fontsize`: Font size for axis labels.
- `custom_title`: Custom title for the chart.

---

#### **5. Heatmap**
Visualize correlations between numeric columns.

**Syntax**:
```python
da.heatmap(df)
```

**Customization Options**:
- `annot`: Whether to annotate the heatmap with correlation values.
- `cmap`: Colormap for the heatmap.
- `size`: Tuple specifying figure size.
- `title_fontsize`: Font size for the title.
- `custom_title`: Custom title for the chart.

---

#### **6. Pair Plot**
Display pairwise relationships in a dataset.

**Syntax**:
```python
da.pairplot(df, hue='category')
```

**Customization Options**:
- `hue`: Column for color encoding.
- `size`: Tuple specifying figure size for each subplot.
- `title_fontsize`: Font size for the title.
- `custom_title`: Custom title for the chart.

---

#### **7. Box Plot**
Compare distributions of a numeric column across categories.

**Syntax**:
```python
da.boxplot(df, x_col='region', y_col='sales')
```

**Customization Options**:
- `size`: Tuple specifying figure size.
- `title_fontsize`: Font size for the title.
- `axis_fontsize`: Font size for axis labels.
- `custom_title`: Custom title for the chart.

---

#### **8. Violin Plot**
Combine box plot and density plot for richer insights.

**Syntax**:
```python
da.violinplot(df, x_col='region', y_col='sales')
```

**Customization Options**:
- `size`: Tuple specifying figure size.
- `title_fontsize`: Font size for the title.
- `axis_fontsize`: Font size for axis labels.
- `custom_title`: Custom title for the chart.

---

#### **9. Interactive Visualization**

Provides an interactive menu for generating various plots one at a time.

**Menu Options**:
1. Histogram  
2. Bar Chart  
3. Line Plot  
4. Scatter Plot  
5. Heatmap  
6. Pair Plot  
7. Box Plot  
8. Violin Plot  
9. Exit Visualization

**Syntax**:
```python
# Perform interactive visualization
da.interactive_plot(df)
```

---

### **Comprehensive Example**

Here’s how you can use the `visualizer` functions to create multiple plots:

```python
import dataanalysts as da
import pandas as pd

# Sample dataset
data = {
    'age': [25, 30, 35, 40, 45],
    'salary': [50000, 60000, 70000, 80000, 90000],
    'city': ['NY', 'LA', 'SF', 'CHI', 'HOU'],
    'gender': ['M', 'F', 'F', 'M', 'M']
}
df = pd.DataFrame(data)

# Histogram
da.histogram(df, column='age', bins=20, kde=True)

# Bar Chart
da.barchart(df, x_col='city', y_col='salary')

# Scatter Plot
da.scatter(df, x_col='age', y_col='salary', hue='gender')

# Heatmap
da.heatmap(df)

# Interactive Visualization
da.interactive_plot(df)
```

---

### **Logging**

- Logs are stored in the `visualizer.log` file.
- Each visualization step is logged with details about the operation and parameters used.
- Errors during visualizations are also logged for debugging purposes.

---

This module provides highly customizable and interactive visualizations to gain insights from your data effectively.

---

## 🤝 **Contributing**
Contributions are welcome! Please submit a pull request via our GitHub Repository.

---

## 📜 **License**
This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🛠️ **Support**
If you encounter any issues, feel free to open an issue on our GitHub Issues page.

