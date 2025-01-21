def desc(df):
    import pandas as pd
    import numpy as np
    from scipy.stats import anderson
    x = np.round(df.describe().T,2)
    x = x.iloc[:, [0,1,2,5,3,7]]
    x.rename(columns={'50%': 'median'}, inplace=True)
    mad_values = {}
    # computes the manual mad which is more robust to outliers and non-normal distributions
    for column in df.select_dtypes(include=[np.number]):
        median = np.median(df[column])
        abs_deviation = np.abs(df[column] - median)
        mad = np.median(abs_deviation)
        mad_values[column] = mad
    mad_df = pd.DataFrame(list(mad_values.items()), columns=['Variable', 'MAD'])
    mad_df.set_index('Variable', inplace=True)
    results = {}
    # Loop through each column to test only continuous variables (numeric columns)
    for column in df.select_dtypes(include=[np.number]):  # Only continuous variables
        result = anderson(df[column])
        statistic = result.statistic
        critical_values = result.critical_values
        # Only select the 5% and 1% significance levels
        selected_critical_values = {
            '5% crit_value': critical_values[2],  # 5% critical value
            '1% crit_value': critical_values[4]   # 1% critical value
        }
        # Store the results in a dictionary
        results[column] = {
            'AD_stat': statistic,
            **selected_critical_values  # Add critical values for 5% and 1% levels
        }
    # Convert the results dictionary into a DataFrame
    anderson_df = pd.DataFrame.from_dict(results, orient='index')
    
    xl = x.iloc[:, :4]
    xr = x.iloc[:, 4:]
    x_df = np.round(pd.concat([xl, mad_df, xr, anderson_df], axis=1),2)
    return x_df

def freqdist(df, column_name):
    import pandas as pd
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    if df[column_name].dtype not in ['object', 'category']:
        raise ValueError(f"Column '{column_name}' is not a categorical column.")
    
    freq_dist = df[column_name].value_counts().reset_index()
    freq_dist.columns = [column_name, 'Count']
    freq_dist['Percentage'] = (freq_dist['Count'] / len(df)) * 100
    return freq_dist