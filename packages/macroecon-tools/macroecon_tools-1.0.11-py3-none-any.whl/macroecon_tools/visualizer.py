# Description: a visulization module for timeseries data

# Import visualization libraries
import matplotlib.pyplot as plt

# Add path to current directory
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import timeseries datastructures
from timeseries import Timeseries, TimeseriesTable

# Function to plot multiple timeseries in one graph 
def vis_multi_series(data: TimeseriesTable, save_path: str, variables: dict[str, str] = {}, start_date: str = "", end_date: str = "", is_percent: bool = False):
    """
    Creates a plot of multiple timeseries data in one graph with the data and variables provided.

    Parameters
    ----------
    data : TimeseriesTable
        The timeseries data to be plotted.
    save_path : str
        The path to save the plot, also indicates the type of file to save as (supports pdf, png, eps, etc.)
    variables : dict[str, str], optional
        A dictionary containing the variable name and the title of the plot. 
        Default: {} (indicates all variables in the TimeseriesTable will be plotted).
    start_date : str, optional
        The start date of the plot.
        Default: "" (indicates the start date of the data).
    end_date : str, optional
        The end date of the plot. 
        Default: "" (indicates the end date of the data).
    is_percent : bool, optional
        Indicates if the y-axis is in percentage format.
        Default: False (indicates the y-axis is not in percentage format).

    Notes
    -----
    The plot will be saved to the path specified in the save_path parameter.
    """
    # Check for variables
    if len(variables) == 0:
        for var in data:
            variables[var] = var
    # Map variables to list
    variables = [(var, variables[var]) for var in variables]
    # Create a figure and axis
    fig, axs = plt.subplots(len(variables), figsize=(6.5, 4))
    # Plot variables
    for idx, ax in enumerate(axs.flat):
        # plot data
        ax.plot(data.df[variables[idx][0]][start_date:end_date])
        # set title
        ax.set_title(variables[idx][1])
        # set y-axis format
        if is_percent:
            ax.yaxis.set_major_formatter('{x:.0f}%')
        else:
            ax.yaxis.set_major_formatter('{x:.0f}')
        # format graph
        ax.grid()
        ax.autoscale(tight=True)
        ax.label_outer()

    # Use tight layout
    plt.tight_layout()
    # Add 5% padding to each y-axis
    for idx, ax in enumerate(axs.flat):
        ax.margins(y=0.05)

    # Save plot
    plt.savefig(save_path)
    # Close plot
    plt.close()

# Function to plot two variables in one graph
def vis_two_vars(data: TimeseriesTable, x_var: str, y_var: str, save_path: str, title: str = "", start_date: str = "", end_date: str = "", x_is_percent: bool = False, y_is_percent: bool = False):
    """
    Plot two variables in one graph with the data and variables provided.

    Parameters
    ----------
    data : TimeseriesTable
        The timeseries data to be plotted.
    x_var : str
        The variable to be plotted on the x-axis.
    y_var : str
        The variable to be plotted on the y-axis.
    save_path : str
        The path to save the plot, also indicates the type of file to save as (supports pdf, png, eps, etc.)
    title : str, optional
        The title of the plot.
        Default: "" (indicates {x_var} vs {y_var}).
    start_date : str, optional
        The start date of the plot.
        Default: "" (indicates the start date of the data).
    end_date : str, optional
        The end date of the plot. 
        Default: "" (indicates the end date of the data).
    x_is_percent : bool, optional
        Indicates if the x-axis is in percentage format.
        Default: False (indicates the x-axis is not in percentage format).
    y_is_percent : bool, optional
        Indicates if the y-axis is in percentage format.
        Default: False (indicates the y-axis is not in percentage format).
    """
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(6.5, 4))
    # get start and end date
    if start_date == "":
        # get the start date of the two variables
        start_date = max(data.df[x_var].index[0], data.df[y_var].index[0])
    if end_date == "":
        # get the end date of the two variables
        end_date = min(data.df[x_var].index[-1], data.df[y_var].index[-1])
    # plot data
    ax.scatter(data.df[x_var][start_date:end_date], data.df[y_var][start_date:end_date])
    # set title
    if title == "":
        title = f"{x_var} vs {y_var}"
    ax.set_title(title if title != "" else f"{x_var} vs {y_var}")
    # set axis labels
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    # set x-axis format
    if x_is_percent:
        ax.xaxis.set_major_formatter('{x:.0f}%')
    else:
        ax.xaxis.set_major_formatter('{x:.0f}')
    # set y-axis format
    if y_is_percent:
        ax.yaxis.set_major_formatter('{x:.0f}%')
    else:
        ax.yaxis.set_major_formatter('{x:.0f}')
    # format graph
    ax.grid()
    ax.autoscale(tight=True)
    ax.label_outer()

    # Save plot
    plt.savefig(save_path)
    # Close plot
    plt.close()

# Visualize multiples variables in one graph
def vis_multi_lines(data: TimeseriesTable, vars: list[str], save_path: str, title: str, start_date: str = "", end_date: str = "", is_percent: bool = False):
    """
    Visualizes multiple variables in one graph with the data and variables provided.

    Parameters
    ----------
    data : TimeseriesTable
        The timeseries data to be plotted.
    vars : list[str]
        The list of variables to be plotted.
    save_path : str
        The path to save the plot, also indicates the type of file to save as (supports pdf, png, eps, etc.)
    title : str
        The title of the plot.
    start_date : str, optional
        The start date of the plot.
        Default: "" (indicates the start date of the data).
    end_date : str, optional
        The end date of the plot. 
        Default: "" (indicates the end date of the data).
    is_percent : bool, optional
        Indicates if the y-axis is in percentage format.
        Default: False (indicates the y-axis is not in percentage format).
    """
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(6.5, 4))

    # get start and end date
    if start_date == "":
        # get the start date of the two variables
        start_date = min([data.df[var].index[0] for var in vars])
    if end_date == "":
        # get the end date of the two variables
        end_date = max([data.df[var].index[-1] for var in vars])

    # define a list of color and line types to use
    line_types = [('red', '-'), ('blue', '--'), ('darkgreen', '-.'), ('black', ':')]

    # plot data, use different colors and line types if less than 4 variables
    if len(vars) <= len(line_types):
        for idx, var in enumerate(vars):
            ax.plot(data.df[var][start_date:end_date], color=line_types[idx][0], linestyle=line_types[idx][1], label=var)
    else:
        for idx, var in enumerate(vars):
            ax.plot(data.df[var][start_date:end_date], label=var)

    # set title
    ax.set_title(title)
    # set axis labels
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    # set y-axis format
    if is_percent:
        ax.yaxis.set_major_formatter('{x:.0f}%')
    else:
        ax.yaxis.set_major_formatter('{x:.0f}')
    # format graph
    ax.grid()
    ax.autoscale(tight=True)
    ax.label_outer()
    # add legend
    ax.legend()

    # Save plot
    plt.savefig(save_path)
    # Close plot
    plt.close()
