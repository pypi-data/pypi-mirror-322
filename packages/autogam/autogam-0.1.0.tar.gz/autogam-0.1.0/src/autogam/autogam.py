import numpy as np
import pandas as pd
from statsmodels.gam.api import GLMGam, BSplines

class AutoGAM:
    def __init__(self, data, y_col, **kwargs):
        """
        Automate the creation of a Generalized Additive Model (GAM).

        Parameters:
        - data: pandas.DataFrame containing the dataset.
        - y_col: str, name of the outcome column.
        - kwargs: Additional arguments passed to statsmodels.GLMGam.
        """
        self.data = data
        self.y_col = y_col
        self.params = kwargs
        self.perf = {}

        """Fit the GAM model."""
        gam_fmla = gam_formula(data, y_col)
        bs = BSplines(
            data[gam_fmla[1][0]], 
            gam_fmla[1][1],
            gam_fmla[1][2]
        )

        self.model = GLMGam.from_formula(gam_fmla[0], data=data, smoother=bs).fit()

        """Calculate performance metrics."""
        y_true = data[y_col].values
        y_pred = self.model.fittedvalues
        self.perf['mae']  = np.mean(np.abs(y_true - y_pred))
        self.perf['mad']  = np.mean(np.abs(y_true - np.mean(y_true)))
        self.perf['rmse'] = np.sqrt(np.mean((y_true - y_pred) ** 2))
        self.perf['sd']   = np.std(y_true)

    def summary(self):
        """Print a summary of the GAM model."""
        print(self.model.summary())
        print(self)

    def print(self):
        print(self.model)

        """Print the performance metrics."""
        print("Performance Metrics:")
        for metric, value in self.perf.items():
            print(f"{metric}: {value:.3f}")



def gam_formula(
    data: pd.DataFrame,
    y_col: str
) -> tuple:
    """
    Create a formula string that places y_col on the left-hand side and
    all other columns on the right-hand side. Numeric columns are wrapped
    in a smooth function if they have more than 4 unique values. Non-numeric
    columns are listed explicitly.

    Parameters
    ----------
    data : pd.DataFrame
        Data containing all variables. Exclude columns you do not want
        in the formula beforehand.
    y_col : str
        Name of the outcome variable.
    smooth_fun : str
        The smooth function name to wrap numeric columns in, default 's'.

    Returns
    -------
    str
        A formula string of the form "y_col ~ x1 + s(x2) + ...",
        with columnns processed in the order they appear in data.
    """
    default_df = 10  # mgcv default k
    default_degree = 3  # default from example in https://www.statsmodels.org/stable/gam.html

    col_names = data.columns.tolist()

    # Ensure y_col is a column in data
    if y_col not in col_names:
        raise ValueError("y_col not found in data")

    # Prepare a list of formula terms in the same order as columns appear
    param_terms  = []
    smooth_terms = []
    smooth_df = []
    smooth_degree = []

    for col in col_names:
        if col == y_col:
            # Skip the outcome column for the right-hand side
            continue

        # Check if column is numeric
        if pd.api.types.is_numeric_dtype(data[col]):
            # Determine number of unique values
            num_unique = data[col].nunique()

            if num_unique <= 4:
                # Use the column as-is (no smoothing)
                param_terms.append(col)
            else:
                smooth_terms.append(col)
                smooth_degree.append(default_degree) 

                if 5 <= num_unique <= 19:
                    # Use half the unique count (floored) for df
                    smooth_df.append(num_unique // 2) 
                else:
                    # Let the GAM function decide the knots
                    smooth_df.append(default_df) 
        else:
            # Non-numeric column: add to parametric formula
            param_terms.append(col)

    # Join terms for the parametric formula string
    # bkpt()
    # If param_terms is empty [] then set it to 1 (intercept)
    param_terms = param_terms or ['1']  # [] is False, so non-[] remains as param_terms
    param_string = y_col + ' ~ ' + '+'.join(param_terms)
   
    # Return elements for spline
    splines = [smooth_terms, smooth_df, smooth_degree]

    return param_string, splines



