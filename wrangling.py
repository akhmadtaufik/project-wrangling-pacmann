import pandas as pd
import seaborn as sns
import numpy as np
import sqlite3
import matplotlib.pyplot as plt


def mapping_translation():
    """_summary_

    Returns:
        _type_: _description_
    """

    querry = """
    SELECT * FROM product_category_name_translation
    """

    product_category_name_translation = pd.read_sql(
        querry, sqlite3.connect("dataset/olist.db")
    )

    mapping = {}

    for i in range(len(product_category_name_translation)):
        original = product_category_name_translation.iloc[i][1]
        english = product_category_name_translation.iloc[i][2]
        mapping[original] = english

    return mapping


def kde_multiple_plot(data: str, n_row: int, fig_size: tuple = tuple()):
    """_summary_

    Args:
        data (str): _description_
        n_row (int): _description_
        fig_size (tuple, optional): _description_. Defaults to tuple().
    """

    # create subplots with 11x3 grids and size 12x30
    fig, ax = plt.subplots(n_row, 3, figsize=fig_size)

    try:

        # counter to select colnames
        cnt = 0

        # loop through the grids
        for i in range(n_row):
            if cnt >= n_row * 3:
                break

            for j in range(3):
                if cnt >= n_row * 3:
                    break

                # we use boxplot from pyplot
                x = data.columns[cnt]
                sns.kdeplot(data=data, x=x, ax=ax[i, j])

                # draw vertical line to describe the mean value
                ax[i, j].axvline(
                    x=data[x].mean(), color="b", linestyle="--", label="mean"
                )
                # draw vertical line to describe the median value
                ax[i, j].axvline(
                    x=data[x].median(),
                    color="g",
                    linestyle="-.",
                    label="median",
                )

                # increment counter
                cnt = cnt + 1

        # make sure layout is not overlapping
        fig.tight_layout()

        # show the legend
        ax[0, 2].legend(loc="upper right")

        # show the graphs
        plt.show()

    except IndexError:
        # make sure layout is not overlapping
        fig.tight_layout()
        # show the legend
        ax[0, 2].legend(loc="upper right")
        # show the graphs
        plt.show()


def boxplot_multiple_plot(data: str, n_row: int, fig_size=tuple()):
    """_summary_

    Args:
        data (str): _description_
        n_row (int): _description_
        fig_size (tuple, optional): _description_. Defaults to tuple().
    """

    # create subplots with 11x3 grids and size 12x30
    fig, ax = plt.subplots(n_row, 3, figsize=fig_size)

    try:

        # counter to select colnames
        cnt = 0

        # loop through the grids
        for i in range(n_row):
            if cnt >= n_row * 3:
                break

            for j in range(3):
                if cnt >= n_row * 3:
                    break

                # we use boxplot from pyplot
                x = data.columns[cnt]
                sns.boxplot(data=data, x=x, ax=ax[i, j])

                # increment counter
                cnt = cnt + 1

        # make sure layout is not overlapping
        fig.tight_layout()

        # show the graphs
        plt.show()

    except IndexError:
        # make sure layout is not overlapping
        fig.tight_layout()

        # show the graphs
        plt.show()


def subplots_dayname_timeday(
    data: pd.DataFrame,
    column_name_1: str,
    column_name_2: str,
    title: str,
    parse_by: str = "order_id",
):
    """_summary_

    Args:
        data (pd.DataFrame): _description_
        column_name_1 (str): _description_
        column_name_2 (str): _description_
        title (str): Judul Figure
        parse_by (str, optional): _description_. Defaults to 'order_id'.
    """

    fig, ax = plt.subplots(1, 2, figsize=(16, 8))

    sns.countplot(data=data, x=column_name_1, ax=ax[0], palette="YlGnBu")

    # Create Absolute Value for labels
    abs_values = data.groupby(column_name_1)[parse_by].count().to_list()

    # Create Relative Value for labels
    rel_values = [val / np.sum(abs_values) for val in abs_values]

    # Labels Formatting
    lbls = [f"{p[0]}\n({p[1]:.2%})" for p in zip(abs_values, rel_values)]

    # Assign label into plot
    ax[0].bar_label(container=ax[0].containers[0], labels=lbls, padding=5)

    # Create weekday label in order
    weekday_label = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Assign weekday label using xticklabels
    ax[0].set_xticklabels(weekday_label)

    sns.countplot(data=data, x=column_name_2, ax=ax[1], palette="coolwarm_r")

    # Create Absolute Value for labels
    abs_values = data.groupby(column_name_2)[parse_by].count().to_list()

    # Create Relative Value for labels
    rel_values = [val / np.sum(abs_values) for val in abs_values]

    # Labels Formatting
    lbls = [f"{p[0]}\n({p[1]:.2%})" for p in zip(abs_values, rel_values)]

    # Assign label into plot
    ax[1].bar_label(container=ax[1].containers[0], labels=lbls, padding=5)

    fig.suptitle(f"{title}\n")
    fig.tight_layout()
    plt.show()


def check_missing_value(data: pd.DataFrame):
    """Function to check missing value in dataframe

    Args:
        data (pd.DataFrame): dataframe to be checked

    Returns:
        DataFrame: dataframe that contains missing values in percentage
    """
    # sum all missing value in dataset and
    # keep only columns with missing value > 0
    missing = data.isnull().sum()[data.isnull().sum() > 0]

    # construct a dataframe consists of NaN count and
    # NaN percentage from the dataset
    missing_df = pd.DataFrame(
        {"NaN_count": missing, "NaN_percentage": missing / len(data)}
    ).sort_values(by="NaN_percentage", ascending=False)

    return missing_df
