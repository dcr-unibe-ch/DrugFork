import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np
from matplotlib.ticker import FixedLocator, ScalarFormatter
import math
import os

from burden_mapping.burden_utils import extract_canonical_classes

# Global variables - must be set from the notebook before using the functions
Overall = None
SAVE_DIR = None
DATASET_FILTER = ""


def generate_distinct_colors(n, cmap_name='nipy_spectral'):
    cmap = cm.get_cmap(cmap_name, n)
    return [mcolors.rgb2hex(cmap(i)) for i in range(n)]

def format_year_ticks(ax, year_range=None, interval=5):
    """
    Format x-axis to show year ticks at regular intervals (e.g., 1995, 2000, 2005, etc.)
    to reduce overcrowding.
    
    **ONLY FOR LINE PLOTS** where years are actual numeric values on x-axis.
    For bar plots, use format_year_ticks_for_bars() instead.
    
    Parameters:
    -----------
    ax : matplotlib axis
        The axis to format
    year_range : tuple or None
        Optional (min_year, max_year) to set boundaries. If None, uses current axis limits.
    interval : int
        Interval between tick marks (default: 5 for 5-year intervals)
    """
    if year_range is None:
        # Get current x-axis limits
        xlim = ax.get_xlim()
        min_year = int(np.ceil(xlim[0]))
        max_year = int(np.floor(xlim[1]))
    else:
        min_year, max_year = year_range
    
    # Find first year that's a multiple of interval
    first_tick = min_year + (interval - min_year % interval) % interval
    
    # Generate tick positions
    ticks = list(range(first_tick, max_year + 1, interval))
    
    # If the range is very small, fall back to showing all years
    if len(ticks) < 2:
        ticks = list(range(min_year, max_year + 1))
    
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(int(t)) for t in ticks])
    
    return ax

def format_year_ticks_for_bars(ax, year_index, interval=5):
    """
    Format x-axis ticks for bar plots to show years at regular intervals.
    
    For bar plots, the x positions are sequential integers (0, 1, 2, ...),
    so we need to map year values to their position in the index.
    
    Parameters:
    -----------
    ax : matplotlib axis
        The axis to format
    year_index : pandas Index or array-like
        The actual year values from the DataFrame index
    interval : int
        Interval between tick marks (default: 5 for 5-year intervals)
    """
    years = year_index.astype(int)
    min_year, max_year = years.min(), years.max()
    
    # Find first year that's a multiple of interval
    first_tick_year = min_year + (interval - min_year % interval) % interval
    
    # Generate years to display
    tick_years = list(range(first_tick_year, max_year + 1, interval))
    
    # Map years to their position in the index
    tick_positions = []
    tick_labels = []
    for year in tick_years:
        if year in years:
            # Find position of this year in the index
            pos = list(years).index(year)
            tick_positions.append(pos)
            tick_labels.append(str(year))
    
    # If too few ticks, show all years
    if len(tick_positions) < 2:
        tick_positions = list(range(len(years)))
        tick_labels = [str(int(y)) for y in years]
    
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    
    return ax

def get_agency_data(agency_name):
    """Get data for a specific agency from the full Overall dataset"""
    return Overall[Overall['Dataset'] == agency_name].copy()

# Helper function to create custom DATASETS dict with specific agencies
def create_datasets_dict(agencies):
    """
    Create a DATASETS dictionary for specific agencies.
    The 'Overall' entry will only include data from the specified agencies.
    
    Args:
        agencies: list of agency names (e.g., ['FDA', 'EMA', 'PMDA', 'Overall'])
    
    Returns:
        dict mapping agency names to filtered dataframes
    """
    datasets = {}
    actual_agencies = [a for a in agencies if a != 'Overall']
    
    for agency in agencies:
        if agency == 'Overall':
            # Filter Overall to only include the agencies in the list
            if actual_agencies:
                datasets[agency] = Overall[Overall['Dataset'].isin(actual_agencies)].copy()
            else:
                datasets[agency] = Overall.copy()
        else:
            datasets[agency] = get_agency_data(agency)
            if len(datasets[agency]) == 0:
                print(f"Warning: No data found for agency '{agency}'")
    return datasets

def generate_distinct_colors(n, cmap_name='tab20'):
    cmap = cm.get_cmap(cmap_name, n)
    return [mcolors.rgb2hex(cmap(i)) for i in range(n)]

def format_year_ticks(ax, year_range=None, interval=5):
    """
    Format x-axis to show year ticks at regular intervals (e.g., 1995, 2000, 2005, etc.)
    to reduce overcrowding.
    
    Parameters:
    -----------
    ax : matplotlib axis
        The axis to format
    year_range : tuple or None
        Optional (min_year, max_year) to set boundaries. If None, uses current axis limits.
    interval : int
        Interval between tick marks (default: 5 for 5-year intervals)
    """
    if year_range is None:
        # Get current x-axis limits
        xlim = ax.get_xlim()
        min_year = int(np.ceil(xlim[0]))
        max_year = int(np.floor(xlim[1]))
    else:
        min_year, max_year = year_range
    
    # Find first year that's a multiple of interval
    first_tick = min_year + (interval - min_year % interval) % interval
    
    # Generate tick positions
    ticks = list(range(first_tick, max_year + 1, interval))
    
    # If the range is very small, fall back to showing all years
    if len(ticks) < 2:
        ticks = list(range(min_year, max_year + 1))
    
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(int(t)) for t in ticks])
    
    return ax

def date_to_int(df, col_name):
    df = df.copy()
    original_len = len(df)

    numeric_years = pd.to_numeric(df[col_name], errors='coerce')
    numeric_years = numeric_years.where(numeric_years.between(1800, 2100))
    dt_years = pd.to_datetime(df[col_name], errors='coerce', infer_datetime_format=True).dt.year
    df[col_name] = numeric_years.fillna(dt_years).astype('Int64')
    df = df.dropna(subset=[col_name])
    df[col_name] = df[col_name].astype(int)

    final_len = len(df)
    print(f"Original length: {original_len}, Final length after cleaning: {final_len}, "
        f"Percentage kept: {final_len/original_len*100:.2f}%")
    return df

def plot_timeline(df, col_name, dataset_name=None):
    original_count = len(df)
    df = date_to_int(df, col_name)  # Ensure column is integer (e.g., year)
    
    if len(df) == 0:
        print(f"{dataset_name}: All {original_count} rows dropped after date_to_int for {col_name} (all values invalid/null), skipping plot.")
        return
    
    unique_vals = sorted(df[col_name].unique())
    
    # Check if there's any data after filtering
    if len(unique_vals) == 0:
        print(f"{dataset_name}: No unique values for {col_name}, skipping plot.")
        return
    
    bins = np.append(unique_vals, unique_vals[-1] + 1)
    plt.figure(figsize=(8, 4))
    ax = plt.gca()
    counts, edges, patches = plt.hist(df[col_name], bins=bins, color="seagreen", edgecolor='black', align='left', alpha=0.7)
    ax.set_xticks(unique_vals)
    ax.set_xticklabels([str(int(x)) for x in unique_vals], rotation=45, ha='center')
    plt.xlabel(col_name)
    plt.ylabel('Frequency')
    plt.title(dataset_name)
    plt.grid(axis='y', linestyle='--', alpha=0.7, color='silver')
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}/timeline_{col_name}_{dataset_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_drug_class_per_decision_year_absolute(df, year_col='Decision_year', drug_class_colormap=None, dataset_name=None):
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=['Drug_class', year_col])
    df = df[~df['Drug_class'].astype(str).str.contains('error: pycryptodome', case=False, na=False)]

    df = date_to_int(df, year_col)
    df.rename(columns={year_col: 'Year'}, inplace=True)

    count_df = (
        df.groupby(['Year', 'Drug_class'])
          .size()
          .unstack(fill_value=0)
          .sort_index()
    )

    if drug_class_colormap is None:
        colors = generate_distinct_colors(len(count_df.columns), cmap_name='nipy_spectral')
    else:
        colors = [drug_class_colormap.get(cls, '#333333') for cls in count_df.columns]

    # Plot
    ax = count_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        figsize=(8, 5),
        color=colors,
        edgecolor='black'
    )

    ax.set_ylabel(f'$N$ approvals', fontsize=14)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_title(dataset_name, fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=12)
    # ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    
    # Get legend handles and labels
    handles, labels = ax.get_legend_handles_labels()
    
    # Remove legend from main plot
    ax.get_legend().remove()
    
    plt.tight_layout()

    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/drug_class_per_decision_year_absolute_{dataset_name}.png",
                    dpi=300, bbox_inches='tight')
    
    # Save legend as separate file
    if dataset_name:
        fig_legend = plt.figure(figsize=(3, len(labels) * 0.25))
        fig_legend.legend(handles[::-1], labels[::-1], title='Drug Class', loc='center', fontsize=10, title_fontsize=12)
        fig_legend.savefig(f"{SAVE_DIR}/drug_class_per_decision_year_absolute_{dataset_name}_legend_{DATASET_FILTER}.png", dpi=300, bbox_inches='tight')
        plt.close(fig_legend)

def plot_drug_class_per_year(df, date_col=None, drug_class_colormap=None, dataset_name=None):
    # Vorverarbeitung
    df = df.copy()
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=['Drug_class', date_col])
    df = df[~df['Drug_class'].astype(str).str.contains('error: pycryptodome', case=False, na=False)]

    df = date_to_int(df, date_col)
    df = df.rename(columns={date_col: 'Year'})

    # Gruppieren
    count_df = (
        df.groupby(['Year', 'Drug_class'])
          .size()
          .unstack(fill_value=0)
          .sort_index()
    )

    # Auf 100% normalisieren (Zeilenweise)
    denom = count_df.sum(axis=1).replace(0, np.nan)
    percent_df = (count_df.T / denom).T.fillna(0) * 100

    # Farben
    if drug_class_colormap is None:
        colors = generate_distinct_colors(len(percent_df.columns), cmap_name='nipy_spectral')
    else:
        colors = [drug_class_colormap.get(cls, '#333333') for cls in percent_df.columns]

    # Plot
    ax = percent_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        figsize=(6, 5),
        color=colors,
        edgecolor='black'
    )
    ax.set_ylabel('Approvals, normalized (%)', fontsize=14)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_title(dataset_name.replace('_', ' '), fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=12)

    # Get legend handles and labels
    handles, labels = ax.get_legend_handles_labels()
    
    # Remove legend from main plot
    ax.get_legend().remove()

    # X-Achse: show ticks at 5-year intervals to reduce overcrowding
    years = percent_df.index.astype(int)
    if len(years) > 10:  # Only apply filtering if many years
        format_year_ticks_for_bars(ax, years, interval=5)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    else:
        ax.set_xticks(range(len(years)))
        ax.set_xticklabels([str(int(y)) for y in years], rotation=45, ha='right')

    plt.tight_layout()
    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/drug_class_per_year_stacked_{date_col}_{dataset_name}.png", dpi=300, bbox_inches='tight')
    
    # Save legend as separate file
    if dataset_name:
        fig_legend = plt.figure(figsize=(3, len(labels) * 0.25))
        fig_legend.legend(handles[::-1], labels[::-1], title='Drug Class', loc='center', fontsize=10, title_fontsize=12)
        fig_legend.savefig(f"{SAVE_DIR}/drug_class_per_year_stacked_{date_col}_{dataset_name}_legend_{DATASET_FILTER}.png", dpi=300, bbox_inches='tight')
        plt.close(fig_legend)

def plot_drug_class_distribution_pie(df, drug_class_colormap=None, dataset_name=None):
    df = df.copy()
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=['Drug_class'])
    df = df[~df['Drug_class'].astype(str).str.contains('error: pycryptodome', case=False, na=False)]

    class_counts = df['Drug_class'].value_counts()
    labels = class_counts.index
    sizes = class_counts.values

    # Ensure colormap is complete
    if drug_class_colormap is None:
        drug_class_colormap = {}
    cmap = plt.get_cmap('tab20')
    for i, label in enumerate(labels):
        if label not in drug_class_colormap:
            drug_class_colormap[label] = cmap(i % cmap.N)

    colors = [drug_class_colormap[label] for label in labels]
    total = sizes.sum()

    plt.figure(figsize=(5, 5))
    wedges, _ = plt.pie(
        sizes,
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.3, edgecolor='w'),
    )
    legend_labels = [f"{label} ({size / total * 100:.1f}%)" for label, size in zip(labels, sizes)]

    plt.title(dataset_name)

    plt.legend(
        wedges,
        legend_labels,
        title='Drug Class',
        loc='center left',
        bbox_to_anchor=(1, 0.7),
        fontsize=9
    )
    plt.title(dataset_name.replace('_', ' '))
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}/drug_class_distribution_pie_{dataset_name}.png", dpi=300, bbox_inches='tight')

def plot_drug_class_by_administration_route(df, dataset_name=None):
    df = df.copy()
    
    # Preprocessing
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=['Drug_class', 'Administration_route'])
    df = df[~df['Drug_class'].astype(str).str.contains('error: pycryptodome', case=False, na=False)]

    # split administration routes and clean whitespace
    df['Administration_route'] = df['Administration_route'].str.replace('„|“|”', '"')
    df['Administration_route'] = df['Administration_route'].str.split(';')
    df = df.explode('Administration_route')
    df['Administration_route'] = df['Administration_route'].str.strip()

    # Count occurrences of drug classes by administration route
    class_counts = df.groupby(['Drug_class', 'Administration_route']).size().unstack(fill_value=0)
    class_counts = class_counts.loc[class_counts.sum(axis=1).sort_values(ascending=False).index]

    # Farben generieren mit generate_distinct_colors
    colors = generate_distinct_colors(len(class_counts.index), cmap_name='nipy_spectral')

    # Plot
    class_counts.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        color=colors,
        edgecolor='black',
        figsize=(8, 5)
    )

    plt.xlabel('Drug Class')
    plt.ylabel(f'$N$ approvals')
    plt.legend(title='Administration Route', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.xticks(rotation=45, ha='right')
    # plt.grid(axis='y', linestyle='--', alpha=0.7, color='silver')
    plt.tight_layout()

    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/drug_class_by_administration_route_{dataset_name}.png", dpi=300, bbox_inches='tight')

def plot_administration_route_per_year(df, agency_name, date_col='Application_date', admin_route_colormap=None, dataset_name=None):
    df = df.copy()
    
    # preprocessing
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=['Administration_route', date_col])
    # df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    df = df.dropna(subset=[date_col])
    # df['Year'] = df[date_col].dt.year.astype(int)

    # if multiple administration routes are separated by ';'
    df['Administration_route'] = df['Administration_route'].str.replace('„|“|”', '"')  # typografische Anführungszeichen entfernen
    df['Administration_route'] = df['Administration_route'].str.split(';')
    df = df.explode('Administration_route')
    df['Administration_route'] = df['Administration_route'].str.strip()

    # Get top 10 most frequent administration routes
    top10 = df['Administration_route'].value_counts().nlargest(10).index.tolist()
    df = df[df['Administration_route'].isin(top10)]

    # Group and normalize
    count_df = df.groupby(['Decision_year', 'Administration_route']).size().unstack(fill_value=0)
    percent_df = count_df.div(count_df.sum(axis=1), axis=0) * 100  # auf 100% normieren

    # Use global colormap if provided
    if admin_route_colormap is not None:
        colors = [admin_route_colormap.get(route, '#CCCCCC') for route in percent_df.columns]
    else:
        cmap = plt.get_cmap('tab20', len(percent_df.columns))
        colors = [cmap(i) for i in range(len(percent_df.columns))]

    # Plot
    percent_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        figsize=(8, 5),
        color=colors,
        edgecolor='black'
    )
    plt.title(agency_name)
    plt.xlabel('Year')
    plt.ylabel('normalized (%)')
    handels, labels = plt.gca().get_legend_handles_labels()
    plt.gca().legend(handels[::-1], labels[::-1], title='Administration Route\n(top 10 by frequency)', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    
    # Format x-axis ticks for better readability
    ax = plt.gca()
    if len(percent_df.index) > 10:
        format_year_ticks_for_bars(ax, percent_df.index, interval=5)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    else:
        plt.xticks(rotation=45, ha='right')
    
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/administration_route_per_year_{dataset_name}.png", dpi=300, bbox_inches='tight')

def plot_drug_class_by_pharmaceutical_form(df, pharma_form_colormap=None, dataset_name=None):
    df = df.copy()
    
    # Preprocessing
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=['Drug_class', 'Pharmaceutical_form'])

    # Split pharmaceutical forms and clean whitespace
    df['Pharmaceutical_form'] = df['Pharmaceutical_form'].str.replace('„|"|"', '"')  # typografische Anführungszeichen entfernen
    df['Pharmaceutical_form'] = df['Pharmaceutical_form'].str.split(';')
    df = df.explode('Pharmaceutical_form')
    df['Pharmaceutical_form'] = df['Pharmaceutical_form'].str.strip()

    ##################################
    top10 = (df['Pharmaceutical_form'].str.split(';').explode().str.strip()
            .value_counts().nlargest(10).index.tolist())
    # Get top 10 most frequent pharmaceutical forms
    top10 = df['Pharmaceutical_form'].value_counts().nlargest(10).index.tolist()
    df = df[df['Pharmaceutical_form'].isin(top10)]

    # Count occurrences of drug classes by pharmaceutical form
    class_counts = df.groupby(['Drug_class', 'Pharmaceutical_form']).size().unstack(fill_value=0)
    class_counts = class_counts.loc[class_counts.sum(axis=1).sort_values(ascending=False).index]
    # normalize to 100%
    percent_df = class_counts.div(class_counts.sum(axis=1), axis=0) * 100  # auf 100% normieren

    # Use global colormap if provided
    if pharma_form_colormap is not None:
        colors = [pharma_form_colormap.get(form, '#CCCCCC') for form in class_counts.columns]
    else:
        colors = generate_distinct_colors(len(class_counts.columns))

    # Plot
    percent_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        color=colors,
        edgecolor='black',
        figsize=(6, 5)
    )

    plt.xlabel('Drug Class')
    plt.ylabel('Approvals, normalized (%)')
    plt.title(dataset_name)
    handels, labels = plt.gca().get_legend_handles_labels()
    plt.gca().legend(handels[::-1], labels[::-1], title='Pharmaceutical Form', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    # plt.legend(title='Pharmaceutical Form', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.xticks(rotation=45, ha='right')
    # plt.grid(axis='y', linestyle='--', alpha=0.7, color='silver')
    plt.tight_layout()

    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/drug_class_by_pharmaceutical_form_{dataset_name}.png", dpi=300, bbox_inches='tight')

def plot_pharmaceutical_form_per_year(df, agency_name, date_col=None, pharma_form_colormap=None, dataset_name=None):
    df = df.copy()

    # preprocessing
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=['Pharmaceutical_form', date_col])
    # df = date_to_int(df, date_col)
    # df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    # df['Year'] = df[date_col].dt.year.astype(int)

    # if multiple pharmaceutical forms are separated by ';'
    df['Pharmaceutical_form'] = df['Pharmaceutical_form'].str.replace('„|"|"', '"')  # typografische Anführungszeichen entfernen
    df['Pharmaceutical_form'] = df['Pharmaceutical_form'].str.split(';')
    df = df.explode('Pharmaceutical_form')
    df['Pharmaceutical_form'] = df['Pharmaceutical_form'].str.strip()

    ##################################
    top10 = (df['Pharmaceutical_form'].str.split(';').explode().str.strip()
            .value_counts().nlargest(10).index.tolist())
    df_exploded = df.assign(Pharmaceutical_form=df['Pharmaceutical_form'].str.split(';')).explode('Pharmaceutical_form')
    df = df_exploded[df_exploded['Pharmaceutical_form'].str.strip().isin(top10)]
    ######################################

    # group and normalize
    count_df = df.groupby(['Decision_year', 'Pharmaceutical_form']).size().unstack(fill_value=0)
    percent_df = count_df.div(count_df.sum(axis=1), axis=0) * 100  # auf 100% normieren

    # Use global colormap if provided
    if pharma_form_colormap is not None:
        colors = [pharma_form_colormap.get(form, '#CCCCCC') for form in percent_df.columns]
    else:
        colors = generate_distinct_colors(len(percent_df.columns), cmap_name='tab20')

    # Plot
    percent_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        figsize=(8, 5),
        color=colors,
        edgecolor='black'
    )
    plt.title(agency_name)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Approvals, normalized (%)', fontsize=12)
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(handles[::-1], labels[::-1], title='Pharmaceutical Form', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    
    # Format x-axis ticks for better readability
    ax = plt.gca()
    if len(percent_df.index) > 10:
        format_year_ticks_for_bars(ax, percent_df.index, interval=5)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    else:
        plt.xticks(rotation=45, ha='right')
    plt.yticks(fontsize=11)
    plt.xticks(fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/pharmaceutical_form_per_year_{date_col}_{dataset_name}.png", dpi=300, bbox_inches='tight')

def plot_disease_class_per_decision_year_absolute(
    df, year_col=None, disease_class_colormap=None, dataset_name=None
):
    disease_col = 'Disease_class(es)'
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=[disease_col, year_col])
    df = df[~df[disease_col].astype(str).str.contains('error: pycryptodome', case=False, na=False)]

    # df = date_to_int(df, year_col)
    df.rename(columns={year_col: 'Year'}, inplace=True)

    df[disease_col] = df[disease_col].astype(str).str.split(';')
    df = df.explode(disease_col)
    df[disease_col] = df[disease_col].str.strip()
    df = df[df[disease_col] != '']

    top_classes = df[disease_col].value_counts().head(2)
    print("\nTop 2 Disease Classes (absolute Häufigkeit):")
    for cls, count in top_classes.items():
        print(f"{cls}: {count}")

    count_df = (
        df.groupby(['Year', disease_col])
          .size()
          .unstack(fill_value=0)
          .sort_index()
    )

    if disease_class_colormap is None:
        colors = generate_distinct_colors(len(count_df.columns))
    else:
        colors = [disease_class_colormap.get(cls, '#333333') for cls in count_df.columns]

    # Plot
    ax = count_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        figsize=(6, 5),
        color=colors,
        edgecolor='black'
    )

    ax.set_ylabel(f'$N$ approvals', fontsize=12)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_title(dataset_name)
    handles, labels = plt.gca().get_legend_handles_labels()
    
    # Remove legend from main plot
    if ax.get_legend():
        ax.get_legend().remove()
    
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.yticks(fontsize=10)
    
    # Format x-axis ticks for better readability
    if len(count_df.index) > 10:
        format_year_ticks_for_bars(ax, count_df.index, interval=5)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=10)
    else:
        plt.xticks(rotation=45, ha='right', fontsize=10)
    
    plt.tight_layout()

    if dataset_name:
        # Save main plot without legend
        plt.savefig(f"{SAVE_DIR}/disease_class_per_decision_year_absolute_{dataset_name}.png",
                    dpi=300, bbox_inches='tight')
        
        # Save legend separately
        fig_legend = plt.figure(figsize=(3, len(handles) * 0.3))
        fig_legend.legend(handles[::-1], labels[::-1], title='Disease Class', loc='center', fontsize=8)
        fig_legend.savefig(f"{SAVE_DIR}/disease_class_per_decision_year_absolute_{dataset_name}_legend_{DATASET_FILTER}.png",
                          dpi=300, bbox_inches='tight')
        plt.close(fig_legend)

def plot_marketing_holder_distribution_pie(df, data_col=None, holder_colormap=None, dataset_name=None):
    df = df.copy()
    
    # Vorverarbeitung
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=[data_col])
    df = df[~df[data_col].astype(str).str.contains('error: pycryptodome', case=False, na=False)]

    holder_counts = df[data_col].str.strip().str.lower().value_counts()

    if len(holder_counts) > 20:
        top_counts = holder_counts.nlargest(20)
        others_labels = holder_counts.iloc[20:].index.tolist()
        others_count = len(others_labels)

        # Append 'Other' category
        top_counts['Other'] = others_count
        holder_counts = top_counts

    labels = holder_counts.index
    sizes = holder_counts.values

    # Ensure colormap is complete
    if holder_colormap is None:
        holder_colormap = {}
    cmap = plt.get_cmap('tab20')
    for i, label in enumerate(labels):
        if label not in holder_colormap:
            holder_colormap[label] = cmap(i % cmap.N)

    colors = [holder_colormap[label] for label in labels]
    total = sizes.sum()

    plt.figure(figsize=(10, 5))
    wedges, _ = plt.pie(
        sizes,
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.3, edgecolor='w'),
    )

    legend_labels = []
    for label, size in zip(labels, sizes):
        if label == 'Other':
            legend_labels.append(f"Other ({size} unique holders, {size / total * 100:.1f}%)")
        else:
            legend_labels.append(f"{label} ({size / total * 100:.1f}%)")

    plt.legend(
        wedges,
        legend_labels,
        title='Marketing Authorisation Holder',
        loc='center left',
        bbox_to_anchor=(1, 0.7),
        fontsize=9
    )
    plt.title(dataset_name.replace('_', ' '))
    plt.title(dataset_name)
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}/marketing_holder_distribution_pie_{dataset_name}.png", dpi=300, bbox_inches='tight')

def plot_review_duration_by_agency(agency_dfs: dict, submission_col='Application_date', decision_col='Decision_date', dataset_name=None):
   
    combined_list = []

    # calculate review duration for each agency
    for agency, df in agency_dfs.items(): 
        if "Application_date" in df.columns and "Decision_date" in df.columns:
            df = df.copy()
            df[submission_col] = pd.to_datetime(df[submission_col], errors='coerce', dayfirst=True)
            df[decision_col] = pd.to_datetime(df[decision_col], errors='coerce', dayfirst=True)
            
            # Calculate duration
            df['Review_duration_days'] = (df[decision_col] - df[submission_col]).dt.days
            
            # Keep only valid positive durations
            valid = df[(df['Review_duration_days'] > 0) & (~df['Review_duration_days'].isna())]
            
            # Check if Nonclinical_abridged column exists and has valid data
            if 'Nonclinical_abridged' in valid.columns:
                valid['Nonclinical_abridged'] = valid['Nonclinical_abridged'].str.lower().str.strip()
                # Create separate entries for abridged and non-abridged
                abridged = valid[valid['Nonclinical_abridged'] == 'yes'].copy()
                non_abridged = valid[valid['Nonclinical_abridged'] == 'no'].copy()
                
                if len(abridged) > 0:
                    abridged['Agency'] = f"{agency} (Abridged)"
                    combined_list.append(abridged[['Review_duration_days', 'Agency']])
                
                if len(non_abridged) > 0:
                    non_abridged['Agency'] = f"{agency} (Non-Abridged)"
                    combined_list.append(non_abridged[['Review_duration_days', 'Agency']])
            else:
                # No abridged column, use all data
                valid['Agency'] = agency
                combined_list.append(valid[['Review_duration_days', 'Agency']])
        else:
            print(f"{agency}: Missing required columns for review duration calculation.")

    # Check if we have any valid data
    if len(combined_list) == 0:
        print(f"No agencies have valid review duration data (Application_date and Decision_date columns). Skipping plot.")
        return

    combined_df = pd.concat(combined_list, ignore_index=True)

    # add overall data (with abridged breakdown if available)
    has_abridged = any('Abridged' in agency for agency in combined_df['Agency'].unique())
    if has_abridged:
        # Overall abridged
        overall_abridged = combined_df[combined_df['Agency'].str.contains('Abridged')].copy()
        if len(overall_abridged) > 0:
            overall_abridged['Agency'] = 'Overall (Abridged)'
            combined_df = pd.concat([combined_df, overall_abridged], ignore_index=True)
        
        # Overall non-abridged
        overall_non_abridged = combined_df[combined_df['Agency'].str.contains('Non-Abridged')].copy()
        if len(overall_non_abridged) > 0:
            overall_non_abridged['Agency'] = 'Overall (Non-Abridged)'
            combined_df = pd.concat([combined_df, overall_non_abridged], ignore_index=True)
    else:
        # Simple overall for all data
        overall_df = combined_df.copy()
        overall_df['Agency'] = 'Overall'
        combined_df = pd.concat([combined_df, overall_df], ignore_index=True)

    # Plot
    plt.figure(figsize=(8, 5))
    ax = sns.boxplot(data=combined_df, y='Agency', x='Review_duration_days', palette='tab20', orient='h')
    ax.set_xlabel('Review Duration (days, log scale)')
    ax.set_ylabel('Agency')
    ax.set_xscale("symlog", linthresh=500)
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.xaxis.set_minor_formatter(ScalarFormatter())
    ax.set_xticks([50, 100, 200, 300, 400, 500, 600, 800, 1000, 1250, 1500, 2000])
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/review_duration_by_agency_{dataset_name}.png", dpi=300, bbox_inches='tight')

def plot_review_duration_by_disease_class(df, submission_col=None, decision_col=None, dataset_name=None, disease_class_colormap=None, abridged=None):
   
    df = df.copy()
    
    # Filter by abridged status FIRST (before date conversion)
    if abridged is not None and 'Nonclinical_abridged' in df.columns:
        df['Nonclinical_abridged'] = df['Nonclinical_abridged'].str.lower().str.strip()
        if abridged == True:
            df = df[df['Nonclinical_abridged'] == 'yes']
        elif abridged == False:
            df = df[df['Nonclinical_abridged'] == 'no']
    
    df[submission_col] = pd.to_datetime(df[submission_col], errors='coerce', dayfirst=True)
    df[decision_col] = pd.to_datetime(df[decision_col], errors='coerce', dayfirst=True)
    df['Review_duration_days'] = (df[decision_col] - df[submission_col]).dt.days

    # Filter out invalid durations and disease classes
    df = df.dropna(subset=['Review_duration_days', 'Disease_class(es)'])
    df = df[df['Review_duration_days'] > 0]

    # Check if we have any valid data
    if len(df) == 0:
        print(f"{dataset_name}: No valid review duration data (empty after filtering). Skipping plot.")
        return

    # Split disease classes and clean whitespace
    df['Disease_class(es)'] = df['Disease_class(es)'].str.split(';')
    df = df.explode('Disease_class(es)')
    df['Disease_class(es)'] = df['Disease_class(es)'].str.strip()  # clean whitespace

    # After exploding, check again if we have data
    if len(df) == 0:
        print(f"{dataset_name}: No valid disease classes found. Skipping plot.")
        return

    # Order disease classes by mean review duration (ascending)
    mean_durations = df.groupby('Disease_class(es)')['Review_duration_days'].median().sort_values()
    ordered_diseases = mean_durations.index.tolist()
    
    # Map colors using the global colormap (in the sorted order)
    if disease_class_colormap is not None:
        palette = [disease_class_colormap.get(disease, '#CCCCCC') for disease in ordered_diseases]
    else:
        # Fallback to tab20 if no colormap provided
        palette = 'tab20'

    # Determine title suffix based on abridged filter
    title_suffix = ""
    filename_suffix = ""
    if abridged is True:
        title_suffix = " (Abridged)"
        filename_suffix = "_abridged"
    elif abridged is False:
        title_suffix = " (Non-Abridged)"
        filename_suffix = "_nonabridged"

    # Plot
    plt.figure(figsize=(10, 7))
    ax = sns.boxplot(data=df, y='Disease_class(es)', x='Review_duration_days', 
                     palette=palette, orient='h', order=ordered_diseases)
    ax.set_xscale("symlog", linthresh=500)
    ax.set_xlabel('Review Duration (days)')
    ax.set_ylabel('Disease Class')
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.xaxis.set_minor_formatter(ScalarFormatter())
    ax.set_xticks([50, 100, 200, 300, 400, 500, 600, 800, 1000, 1250, 1500, 2000])
    plt.xticks(rotation=45, ha='right')
    plt.title(f"{dataset_name}{title_suffix}")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save the plot
    if dataset_name:
        filename = f"review_duration_by_disease_class_{dataset_name}{filename_suffix}.png"
        plt.savefig(os.path.join(SAVE_DIR, filename), dpi=300, bbox_inches='tight')

def plot_decision_distribution_by_agency(agency_dfs: dict, dataset_name=None):
  
    # Prepare data for plotting
    all_counts = []

    for agency, df in agency_dfs.items():
        df = df.copy()
        if 'Decision' not in df.columns:
            continue
        decision_counts = df['Decision'].str.lower().value_counts(normalize=True) * 100

        for decision, percent in decision_counts.items():
            all_counts.append({'Agency': agency, 'Decision': decision, 'Percent': percent})

    plot_df = pd.DataFrame(all_counts)

    # Pivot the DataFrame for plotting
    pivot_df = plot_df.pivot(index='Agency', columns='Decision', values='Percent').fillna(0)
    pivot_df = pivot_df.loc[sorted(pivot_df.index)]  

    # Plot
    pivot_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        colormap='tab20',
        edgecolor='black',
        figsize=(8, 5)
    )

    plt.ylabel('Decisions, normalized (%)')
    plt.xlabel('Agency')
    plt.ylim(0, 100)
    # plt.title('Decision Distribution per Agency (100% stacked)')
    plt.legend(title='Decision', bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/decision_distribution_by_agency_{dataset_name}.png", dpi=300, bbox_inches='tight')

def plot_decision_breakdown_per_disease_class(df, dataset_name=None, date_col='Decision_date'):
    df = df.copy()

    # preprocessing
    df['Decision'] = df['Decision'].astype(str).str.lower()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)
    df['Year'] = df[date_col].dt.year
    df = df.dropna(subset=['Year', 'Decision', 'Disease_class(es)'])
    df['Year'] = df['Year'].astype(int)

    if "Disease_class(es)" in df.columns:
        count_disease = df.groupby(['Disease_class(es)', 'Decision']).size().unstack(fill_value=0)
        top_classes = count_disease.sum(axis=1).nlargest(10).index
        count_disease = count_disease.loc[top_classes]

        count_disease.plot(kind='bar', width=1.0, stacked=True, figsize=(12, 6), edgecolor='black')
        plt.title(dataset_name)
        plt.xlabel('Disease Class')
        plt.ylabel('Number of Decisions')
        plt.xticks(rotation=45, ha='right')
        # plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        if dataset_name:
            plt.savefig(f"{SAVE_DIR}/decision_distribution_by_disease_class_{dataset_name}.png",
                        dpi=300, bbox_inches='tight')
    else:
        print(f"{dataset_name}: 'Disease_class(es)' column not found for decision breakdown by disease class.")

def plot_decision_breakdown_per_agency_per_year(df, dataset_name=None, date_col='Decision_date'):
    df = df.copy()

    # preprocessing
    df['Decision'] = df['Decision'].astype(str).str.lower()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)
    df['Year'] = df[date_col].dt.year
    df = df.dropna(subset=['Year', 'Decision'])
    df['Year'] = df['Year'].astype(int)

    count_year = df.groupby(['Year', 'Decision']).size().unstack(fill_value=0).sort_index()
    ax = count_year.plot(kind='bar', width=1.0,stacked=True, figsize=(10, 5), edgecolor='black')
    plt.title(dataset_name)
    plt.xlabel('Year')
    plt.ylabel('Number of Decisions')
    
    # Format x-axis ticks for better readability
    if len(count_year.index) > 10:
        format_year_ticks_for_bars(ax, count_year.index, interval=5)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    else:
        plt.xticks(rotation=45, ha='right')
    
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/decision_distribution_by_year_{dataset_name}.png",
                    dpi=300, bbox_inches='tight')

def plot_nonclinical_abridged_distribution(agency_dfs: dict, dataset_name=None):
    all_data = []

    # prepare data for plotting
    for agency, df in agency_dfs.items():
        df = df.copy()
        if 'Nonclinical_abridged' not in df.columns:
            continue
        df['Nonclinical_abridged'] = df['Nonclinical_abridged'].str.lower().str.strip()
        counts = df['Nonclinical_abridged'].value_counts(normalize=True) * 100
        for status in ['yes', 'no']:
            all_data.append({
                'Agency': agency,
                'Status': status,
                'Percent': counts.get(status, 0.0)
            })

    plot_df = pd.DataFrame(all_data)

    # Pivot the DataFrame for plotting
    pivot_df = plot_df.pivot(index='Agency', columns='Status', values='Percent').fillna(0)
    if 'yes' not in pivot_df.columns:
        pivot_df['yes'] = 0.0
    if 'no' not in pivot_df.columns:
        pivot_df['no'] = 0.0
    pivot_df = pivot_df[['yes', 'no']] 

    # Plot
    pivot_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        color=['#377eb8', '#f781bf'],
        edgecolor='black',
        figsize=(5, 3)
    )

    plt.ylabel('Approvals, normalized (%)')
    plt.xlabel('Agency')
    plt.ylim(0, 100)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(title='Nonclinical Abridged', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/nonclinical_abridged_distribution_{dataset_name}.png", dpi=300, bbox_inches='tight')

def plot_orphan_drug_status_distribution(agency_dfs: dict, dataset_name=None):
    all_data = []

    # prepare data for plotting
    for agency, df in agency_dfs.items():
        df = df.copy()
        if 'Orphan_drug_status' not in df.columns:
            continue
        df['Orphan_drug_status'] = df['Orphan_drug_status'].str.lower().str.strip()
        counts = df['Orphan_drug_status'].value_counts(normalize=True) * 100
        for status in ['yes', 'no']:
            all_data.append({
                'Agency': agency,
                'Status': status,
                'Percent': counts.get(status, 0.0)
            })

    plot_df = pd.DataFrame(all_data)

    # Pivot the DataFrame for plotting
    pivot_df = plot_df.pivot(index='Agency', columns='Status', values='Percent').fillna(0)
    for status in ['yes', 'no']:
        if status not in pivot_df.columns:
            pivot_df[status] = 0.0
    pivot_df = pivot_df[['yes', 'no']] 

    # Plot
    pivot_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        color=['#377eb8', '#f781bf'], 
        edgecolor='black',
        figsize=(5, 3)
    )

    plt.ylabel('Approvals, normalized (%)')
    plt.xlabel('Agency')
    plt.ylim(0, 100)
    plt.legend(title='Orphan Drug Status', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    if dataset_name:
        plt.savefig(f"{SAVE_DIR}/orphan_drug_status_distribution_{dataset_name}.png", dpi=300, bbox_inches='tight')

def plot_some_class_per_year_panel(datasets_dict, bbox_to_anchor_val=None, date_col=None, info_col=None, drug_class_colormap=None, nrows=None, ncols=None, figsize_per_subplot=(5, 4)):
    # Auto-calculate grid dimensions if not provided
    n_datasets = len(datasets_dict)
    if nrows is None or ncols is None:
        ncols = min(3, n_datasets)  # Max 3 columns
        nrows = int(np.ceil(n_datasets / ncols))
    
    # Calculate total figure size
    total_width = figsize_per_subplot[0] * ncols
    total_height = figsize_per_subplot[1] * nrows
    
    # Create subplots
    fig, axes = plt.subplots(nrows, ncols, figsize=(total_width, total_height))
    
    # Flatten axes for easy iteration
    if nrows == 1 and ncols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    # Plot each dataset
    for i, (dataset_name, df) in enumerate(datasets_dict.items()):
        if info_col not in df.columns:
            continue

        if i >= len(axes):
            break
            
        ax = axes[i]
        df = df.copy()
        ncols = min(3, n_datasets)  # Max 3 columns
        # Preprocessing
        df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
        df = df.dropna(subset=[info_col, date_col])
        
        if df.empty:
            ax.text(0.5, 0.5, f'{dataset_name}\n(No data)', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            continue
        
        # Extract year - handle both datetime strings and year integers
        if df[date_col].dtype in ['int64', 'float64']:
            # If column is already numeric (likely years), use it directly
            df['Year'] = df[date_col].astype(int)
        else:
            # If column contains dates, extract year
            df['Year'] = pd.to_datetime(df[date_col], errors='coerce').dt.year
        df = df.dropna(subset=['Year'])

        # Split semicolon-separated values if present (for Disease_class(es), Administration_route, etc.)
        if df[info_col].astype(str).str.contains(';').any():
            df[info_col] = df[info_col].astype(str).str.split(';')
            df = df.explode(info_col)
            df[info_col] = df[info_col].str.strip()  # Remove whitespace
            df = df[df[info_col] != '']  # Remove empty values
        
        # Count per year and class
        grouped = df.groupby(['Year', info_col]).size().reset_index(name='Count')
        pivot_df = grouped.pivot(index='Year', columns=info_col, values='Count').fillna(0)
        
        # Normalize to percentages
        percent_df = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100
        
        # Set up colors
        if drug_class_colormap is None:
            colors = generate_distinct_colors(len(percent_df.columns), cmap_name='tab20')
        else:
            colors = [drug_class_colormap.get(cls, '#333333') for cls in percent_df.columns]
        
        # Plot on this subplot
        percent_df.plot(
            kind='bar',
            width=1.0,
            stacked=True,
            ax=ax,
            color=colors,
            edgecolor='black',
            legend=False  # We'll add a shared legend later
        )
        
        ax.set_ylabel('Approvals, normalized (%)', fontsize=12)
        ax.set_xlabel('Year', fontsize=12)
        ax.set_title(
                    dataset_name.replace('_', ' '), 
                    fontsize=16, 
                    # fontweight='bold'
                    )
        # ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Format x-axis ticks for better readability
        if len(percent_df.index) > 10:
            format_year_ticks_for_bars(ax, percent_df.index, interval=5)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=10)
        else:
            ax.set_xticklabels([str(int(y)) for y in percent_df.index], rotation=45, ha='right', fontsize=10)
        ax.tick_params(axis='y', labelsize=12)
    
    # Hide unused subplots
    for i in range(len(datasets_dict), len(axes)):
        axes[i].set_visible(False)
    
    # Create a shared legend
    if drug_class_colormap is not None:
        # Get all unique drug classes across all datasets
        all_classes = set()
        for df in datasets_dict.values():
            if info_col in df.columns:
                # Split semicolon-separated values to match what we plotted
                values = df[info_col].dropna().astype(str)
                if values.str.contains(';').any():
                    # Split and explode to get individual items
                    split_values = values.str.split(';').explode().str.strip()
                    split_values = split_values[split_values != '']
                    all_classes.update(split_values.unique())
                else:
                    all_classes.update(values.unique())
        
        # Create legend patches
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=drug_class_colormap.get(cls, '#333333'), 
                                edgecolor='black', label=cls) 
                          for cls in sorted(all_classes) if cls in drug_class_colormap]
        
        # Add legend below the plots
        legend_name = ""
        if info_col == "Drug_class":
            legend_name = "Drug classes"
        elif info_col == "Pharmaceutical_form":
            legend_name = "Pharmaceutical form"
        elif info_col == "Administration_route":
            legend_name = "Administration route"
        elif info_col == "Disease_class(es)":
            legend_name = "Disease classes"
        else:
            legend_name = "NAME MISSING"
        legend_elements = legend_elements[::-1]
        
        # Save legend as separate file
        fig_legend = plt.figure(figsize=(3, len(legend_elements) * 0.25))
        fig_legend.legend(legend_elements, [elem.get_label() for elem in legend_elements], 
                         title=legend_name, loc='center', fontsize=10, title_fontsize=12)
        fig_legend.savefig(f"{SAVE_DIR}/panel_some_class_per_year_stacked_{date_col}_{info_col}_legend_{DATASET_FILTER}.png", dpi=300, bbox_inches='tight')
        plt.close(fig_legend)
    
    plt.tight_layout()

    # Save
    plt.savefig(f"{SAVE_DIR}/panel_some_class_per_year_stacked_{date_col}_{info_col}.png", dpi=300, bbox_inches='tight')
    plt.show()

def plot_some_class_per_year_single(df, dataset_name, date_col=None, info_col=None, drug_class_colormap=None, bbox_to_anchor_val=(0.6, 0.2)):
    """
    Create a single normalized stacked bar chart for one dataset.
    This is the individual version of plot_some_class_per_year_panel.
    """
    df = df.copy()
    
    # Preprocessing
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=[info_col, date_col])
    df = df[~df[info_col].astype(str).str.contains('error: pycryptodome', case=False, na=False)]
    
    # Clean the date column
    df = date_to_int(df, date_col)
    df.rename(columns={date_col: 'Year'}, inplace=True)
    
    # Handle semicolon-separated values (e.g., for disease classes)
    if df[info_col].astype(str).str.contains(';').any():
        # Split and explode
        df[info_col] = df[info_col].astype(str).str.split(';')
        df = df.explode(info_col)
        df[info_col] = df[info_col].str.strip()
        df = df[df[info_col] != '']
    
    # Group and normalize
    count_df = (
        df.groupby(['Year', info_col])
          .size()
          .unstack(fill_value=0)
          .sort_index()
    )
    
    # Normalize to percentages
    denom = count_df.sum(axis=1).replace(0, np.nan)
    percent_df = (count_df.T / denom).T.fillna(0) * 100
    
    # Get colors
    if drug_class_colormap is not None:
        colors = [drug_class_colormap.get(cls, '#333333') for cls in percent_df.columns]
    else:
        colors = generate_distinct_colors(len(percent_df.columns), cmap_name='nipy_spectral')
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))
    percent_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        ax=ax,
        color=colors,
        edgecolor='black',
        legend=False  # We'll add it manually with reversed order
    )
    
    ax.set_ylabel('Approvals, normalized (%)', fontsize=12)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_title(dataset_name.replace("_", " ").replace("(es)", ""), fontsize=14)
    
    # Format x-axis ticks for better readability
    if len(percent_df.index) > 10:
        format_year_ticks_for_bars(ax, percent_df.index, interval=5)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    else:
        ax.set_xticklabels([str(int(y)) for y in percent_df.index], rotation=45, ha='right')
    
    # Don't add legend to main plot - we'll save it separately
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, edgecolor='black', label=label) 
                      for label, color in zip(percent_df.columns, colors)]
    
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}/some_class_per_year_stacked_{date_col}_{info_col}_{dataset_name}.png", dpi=300, bbox_inches='tight')
    
    # Save legend as separate file
    fig_legend = plt.figure(figsize=(3, len(legend_elements) * 0.25))
    fig_legend.legend(handles=legend_elements[::-1], title=info_col.replace('_', ' '), loc='center', fontsize=10, title_fontsize=12)
    fig_legend.savefig(f"{SAVE_DIR}/some_class_per_year_stacked_{date_col}_{info_col}_{dataset_name}_legend_{DATASET_FILTER}.png", dpi=300, bbox_inches='tight')
    plt.close(fig_legend)
    plt.close()

def plot_burden_vs_approvals_combined(
    datasets_dict,
    burden_data,
    date_col=None,
    disease_col=None,
    measure=None,
    save_dir=None,
    ncols=4,
    figsize=(20, 14)
    ):
    import textwrap

    # Set default save_dir dynamically to respect current SAVE_DIR value
    if save_dir is None:
        save_dir = f"{SAVE_DIR}/burden/"
    
    os.makedirs(save_dir, exist_ok=True)
    
    # Dataset colors
    dataset_colors = {
        "EMA": "#e41a1c",
        "PMDA": "#df65dd",
        "Swissmedic": "#2AAA26",
        "TGA": "#f38e30",
        "FDA": "#391EB2",
        "HealthCanada": "#6EB5DC",
        "Overall": "#116A23",
    }
    
    # Burden color
    burden_color = "#0C0D0D"
    
    # Copy burden data to avoid modifying the input
    burden_agg = burden_data.copy()
    
    # Process each dataset
    print("Processing datasets...")
    all_approvals = {}
    
    for dataset_name, df_drugs in datasets_dict.items():
        print(f"  - {dataset_name}")
        df = df_drugs.copy()
        
        # Extract year
        if date_col in df.columns:
            ser = df[date_col].dropna()
            if len(ser) > 0 and pd.api.types.is_numeric_dtype(ser):
                df["Year"] = pd.to_numeric(df[date_col], errors="coerce").astype("Int64")
            # elif it is a string col which is actually year
            elif len(ser) > 0 and ser.astype(str).str.match(r"^\d{4}$").all():
                df["Year"] = pd.to_numeric(df[date_col], errors="coerce").astype("Int64")
            else:
                df["Year"] = pd.to_datetime(df[date_col], errors="coerce").dt.year
        else:
            print(f"    Warning: Column '{date_col}' not found in {dataset_name}")
            continue
        
        df = df.dropna(subset=["Year"])
        df["Year"] = df["Year"].astype(int)
        
        # Extract disease classes using the utility function
        if disease_col in df.columns:
            df["canonical_classes"] = df[disease_col].apply(extract_canonical_classes)
            df = df.explode("canonical_classes").dropna(subset=["canonical_classes"])
            df = df.rename(columns={"canonical_classes": "Disease_class"})
        else:
            print(f"    Warning: Column '{disease_col}' not found in {dataset_name}")
            continue
        
        # Count approvals
        approvals_agg = df.groupby(["Year", "Disease_class"]).size().reset_index(name="Approvals")
        all_approvals[dataset_name] = approvals_agg
    
    # Get year range (1995+)
    all_years_list = [burden_agg["Year"].min()]
    for approvals in all_approvals.values():
        if len(approvals) > 0:
            all_years_list.append(approvals["Year"].min())
            all_years_list.append(approvals["Year"].max())
    
    min_year = max(int(min(all_years_list)), 1995)
    max_year = int(max([burden_agg["Year"].max()] + [approvals["Year"].max() for approvals in all_approvals.values() if len(approvals) > 0]))
    all_years = list(range(min_year, max_year + 1))
    
    # Get all disease classes
    disease_classes = sorted(burden_agg["Disease_class"].unique())
    
    # EXCLUDE specific disease classes to make plots smaller/more informative
    EXCLUDE_CLASSES = [
        # "Certain infectious and parasitic diseases",
        # "Neoplasms",
        # "Diseases of the blood and blood-forming organs",
        # "Endocrine, nutritional and metabolic diseases",
        # "Mental and behavioural disorders",
        # "Diseases of the nervous system",
        # "Diseases of the eye and adnexa",
        "Diseases of the ear",
        # "Diseases of the circulatory system",
        # "Diseases of the respiratory system",
        # "Diseases of the digestive system",
        # "Diseases of the skin",
        # "Diseases of the musculoskeletal system and connective tissue",
        # "Diseases of the genitourinary system",
        # "Pregnancy and childbirth",
        # "Congenital malformations and chromosomal abnormalities",
        "Injury, poisoning and certain other consequences of external causes",
        "Other",
    ]
    disease_classes = [dc for dc in disease_classes if dc not in EXCLUDE_CLASSES]
    
    if len(disease_classes) == 0:
        print("No disease classes found!")
        return
    
    print(f"Found {len(disease_classes)} disease classes")
    print(f"Year range: {min_year} - {max_year}")
    
    # Create panel plot
    nrows = math.ceil(len(disease_classes) / ncols)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, sharex=False)
    axes = np.array(axes).reshape(-1) if nrows == 1 and ncols == 1 else np.array(axes).flatten()
    
    for idx, disease_class in enumerate(disease_classes):
        ax1 = axes[idx]
        
        # Get burden data for this disease class (don't fill with zeros - keep only actual data)
        burden_class = burden_agg[burden_agg["Disease_class"] == disease_class].copy()
        # Remove zeros to avoid plotting them (burden data ends in 2021)
        burden_class = burden_class[burden_class[measure] > 0]
        
        # Plot burden (left y-axis) - only where data exists
        if len(burden_class) > 0:
            ax1.plot(burden_class["Year"], burden_class[measure], 
                    marker="o", linewidth=1, markersize=4, alpha=0.5, color=burden_color, 
                    label=measure, zorder=5)
            
            # Add trend line for burden
            if len(burden_class) > 1:
                # Calculate linear regression for burden
                z_burden = np.polyfit(burden_class["Year"], burden_class[measure], 2)
                p_burden = np.poly1d(z_burden)
                
                # Plot burden trend line
                burden_trend_y = p_burden(burden_class["Year"])
                ax1.plot(burden_class["Year"], burden_trend_y,
                        linestyle="-", linewidth=1, color=burden_color, 
                        alpha=0.8, label=f"{measure} (trend)", zorder=6)
        
        # ax1.set_title(disease_class, fontsize=9)
        title = textwrap.fill(str(disease_class), width=22)  # tweak width
        ax1.set_title(title, fontsize=9)
        ax1.set_ylabel(f"{measure}", fontsize=8, color=burden_color)
        ax1.tick_params(axis='y', labelcolor=burden_color, labelsize=8)
        ax1.tick_params(axis='x', labelsize=8)
        ax1.grid(axis="both", linestyle="--", alpha=0.3)
        ax1.set_ylim(bottom=0)
        
        # Plot approvals for each dataset (right y-axis)
        ax2 = ax1.twinx()
        
        overall_approvals_for_fit = None
        for dataset_name, approvals_agg in all_approvals.items():
            # Get approvals for this disease class and dataset
            approvals_class = approvals_agg[approvals_agg["Disease_class"] == disease_class].copy()
            approvals_class = approvals_class.set_index("Year").reindex(all_years).fillna(0).reset_index()
            
            color = dataset_colors.get(dataset_name, "#999999")
            ax2.plot(approvals_class["Year"], approvals_class["Approvals"],
                    linestyle="--", marker="s", linewidth=1, markersize=3,
                    color=color, alpha=0.6, label=dataset_name, zorder=3)
            
            # Store Overall dataset for trend line
            if dataset_name == "Overall":
                overall_approvals_for_fit = approvals_class.copy()
        
        # Add trend line for Overall dataset
        if overall_approvals_for_fit is not None and len(overall_approvals_for_fit) > 1:
            # Filter out years with no data for better fit
            fit_data = overall_approvals_for_fit[overall_approvals_for_fit["Approvals"] > 0]
            if len(fit_data) > 1:
                # Calculate linear regression
                z = np.polyfit(fit_data["Year"], fit_data["Approvals"], 2)
                p = np.poly1d(z)
                
                # Plot trend line for all years
                trend_y = p(overall_approvals_for_fit["Year"])
                ax2.plot(overall_approvals_for_fit["Year"], trend_y,
                        linestyle="-", linewidth=1, color=dataset_colors["Overall"], 
                        alpha=0.8, label="Overall (trend)", zorder=4)
        
        ax2.set_ylabel("Approvals", fontsize=8)
        ax2.tick_params(axis='y', labelsize=8)
        ax2.set_ylim(bottom=0)
        
        # Format x-axis ticks for better readability (5-year intervals)
        format_year_ticks(ax1, year_range=(min_year, max_year), interval=5)
        ax1.tick_params(axis='x', labelsize=8, rotation=45)
    
    # Remove empty subplots
    for idx in range(len(disease_classes), len(axes)):
        fig.delaxes(axes[idx])
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=burden_color, linewidth=1, marker='o', alpha=0.4, markersize=3, label=measure),
        Line2D([0], [0], color=burden_color, linewidth=1, linestyle='-', alpha=0.8, label=f"{measure} (trend)")
    ]
    
    # Add dataset lines to legend
    for dataset_name in datasets_dict.keys():
        color = dataset_colors.get(dataset_name, "#999999")
        legend_elements.append(
            Line2D([0], [0], color=color, linewidth=1, linestyle='--', alpha=0.6, 
                   marker='s', markersize=3, label=dataset_name)
        )
    
    # Add Overall trend line to legend
    if "Overall" in all_approvals:
        legend_elements.append(
            Line2D([0], [0], color=dataset_colors["Overall"], linewidth=1, linestyle='-', alpha=0.8, 
                   label="Overall (trend)")
        )
    
    fig.legend(
            handles=legend_elements, 
            loc='upper center', 
            # bbox_to_anchor=(0.5, 0.98), 
            ncol=5, 
            fontsize=10, 
            frameon=True
            )
    
    # fig.suptitle(f"{measure} vs. $N$ Approvals", fontsize=14, y=0.996)
    
    # Set x-axis labels
    for ax in axes:
        if ax in fig.axes:
            ax.set_xlabel("Year", fontsize=9)
    
    fig.tight_layout(rect=[0.02, 0.02, 0.98, 0.97])
    
    # Save
    filename = f"{measure.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')}_vs_approvals_{date_col}.png"
    save_path = os.path.join(save_dir, filename)
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nSaved: {save_path}")
    
    plt.show()
    plt.close(fig)

def plot_drug_class_distribution_pie_panel(datasets_dict, drug_class_colormap=None, nrows=None, ncols=None, figsize_per_subplot=(5, 5)):
    # Auto-calculate grid dimensions if not provided
    n_datasets = len(datasets_dict)
    if nrows is None or ncols is None:
        ncols = min(3, n_datasets)  # Max 3 columns
        nrows = int(np.ceil(n_datasets / ncols))

    # Calculate total figure size
    total_width = figsize_per_subplot[0] * ncols
    total_height = figsize_per_subplot[1] * nrows
    
    # Create subplots
    fig, axes = plt.subplots(nrows, ncols, figsize=(total_width, total_height))
    
    # Flatten axes for easy iteration
    if nrows == 1 and ncols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    # Prepare colormap
    if drug_class_colormap is None:
        drug_class_colormap = {}
        cmap = plt.get_cmap('tab20')
    
    # Plot each dataset
    for i, (dataset_name, df) in enumerate(datasets_dict.items()):
        if i >= len(axes):
            break
            
        ax = axes[i]
        df = df.copy()
        
        # Skip if Drug_class column missing
        if 'Drug_class' not in df.columns:
            ax.text(0.5, 0.5, f'{dataset_name.replace("_", " ")}\n(No Drug_class column)', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')
            continue
        
        # Preprocessing
        df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
        df = df.dropna(subset=['Drug_class'])
        df = df[~df['Drug_class'].astype(str).str.contains('error: pycryptodome', case=False, na=False)]
        
        if df.empty:
            ax.text(0.5, 0.5, f'{dataset_name.replace("_", " ")}\n(No data)', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')
            continue
        
        # Count drug classes
        class_counts = df['Drug_class'].value_counts()
        labels = class_counts.index
        sizes = class_counts.values
        
        # Ensure colormap is complete for this dataset
        for j, label in enumerate(labels):
            if label not in drug_class_colormap:
                if drug_class_colormap:
                    # Use a default color
                    drug_class_colormap[label] = plt.get_cmap('tab20')(j % 20)
                else:
                    drug_class_colormap[label] = cmap(j % cmap.N)
        
        colors = [drug_class_colormap[label] for label in labels]
        total = sizes.sum()
        
        # Create pie chart on this subplot
        wedges, texts = ax.pie(
            sizes,
            startangle=140,
            colors=colors,
            wedgeprops=dict(width=0.7, edgecolor='w')
        )
        
        # Add title
        ax.set_title(
                    dataset_name.replace('_', ' '), 
                    fontsize=16, 
                    # fontweight='bold', 
                    pad=1
                    )
        
        # Add percentage labels on the pie
        for j, (wedge, size) in enumerate(zip(wedges, sizes)):
            angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
            x = np.cos(np.radians(angle))
            y = np.sin(np.radians(angle))
            
            # Only show percentage if slice is large enough
            percentage = size / total * 100
            if percentage > 5:  # Only show if > 5%
                ax.annotate(f'{percentage:.0f}%',
                           xy=(x*0.8, y*0.8),
                           ha='center', va='center',
                           fontsize=12,
                        #    weight='bold',
                           color='black')
    
    # Hide unused subplots
    for i in range(len(datasets_dict), len(axes)):
        axes[i].set_visible(False)
        axes[i].axis('off')
    
    # Create a shared legend
    if drug_class_colormap:
        # Get all unique drug classes across all datasets
        all_classes = set()
        for df in datasets_dict.values():
            if 'Drug_class' in df.columns:
                classes = df['Drug_class'].dropna().unique()
                all_classes.update(classes)
        
        # Create legend patches
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=drug_class_colormap.get(cls, '#333333'), 
                                edgecolor='white', label=cls) 
                          for cls in sorted(all_classes) if cls in drug_class_colormap]
        
        # Save legend as separate file
        fig_legend = plt.figure(figsize=(3, len(legend_elements) * 0.25))
        fig_legend.legend(legend_elements, [elem.get_label() for elem in legend_elements], 
                         title='Drug Class', loc='center', fontsize=10, title_fontsize=12)
        fig_legend.savefig(f"{SAVE_DIR}/panel_drug_class_distribution_pie_legend_{DATASET_FILTER}.png", dpi=300, bbox_inches='tight')
        plt.close(fig_legend)
    
    plt.tight_layout()
    
    # Save
    plt.savefig(f"{SAVE_DIR}/panel_drug_class_distribution_pie.png", dpi=300, bbox_inches='tight')
    plt.show()

def plot_disease_class_per_drug_class_panel(datasets_dict, xcol=None, ycol=None, disease_class_colormap=None, nrows=None, ncols=None, figsize_per_subplot=(6, 5)):
    # Auto-calculate grid dimensions if not provided
    n_datasets = len(datasets_dict)
    if nrows is None or ncols is None:
        ncols = min(3, n_datasets)  # Max 3 columns
        nrows = int(np.ceil(n_datasets / ncols))

    # Calculate total figure size
    total_width = figsize_per_subplot[0] * ncols
    total_height = figsize_per_subplot[1] * nrows
    
    # Create subplots
    fig, axes = plt.subplots(nrows, ncols, figsize=(total_width, total_height))
    
    # Flatten axes for easy iteration
    if nrows == 1 and ncols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    # Plot each dataset
    for i, (dataset_name, df) in enumerate(datasets_dict.items()):
        if i >= len(axes):
            break
            
        ax = axes[i]
        df = df.copy()
        
        # Skip if required columns missing
        if ycol not in df.columns or xcol not in df.columns:
            ax.text(0.5, 0.5, f'{dataset_name}\n(Missing columns)', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')
            continue
        
        # Preprocessing
        df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
        df = df.dropna(subset=[ycol, xcol])

        if df.empty:
            ax.text(0.5, 0.5, f'{dataset_name.replace("_", " ")}\n(No data)', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')
            continue
        
        # Split semicolon-separated disease classes
        df[ycol] = df[ycol].astype(str).str.split(';')
        df = df.explode(ycol)
        df[ycol] = df[ycol].str.strip()
        df = df[df[ycol] != '']
        
        # Count occurrences of disease classes by drug class
        class_counts = df.groupby([xcol, ycol]).size().unstack(fill_value=0)
        class_counts = class_counts.loc[class_counts.sum(axis=1).sort_values(ascending=False).index]
        
        # Normalize to percentages
        percent_df = class_counts.div(class_counts.sum(axis=1), axis=0) * 100
        
        # Set up colors
        if disease_class_colormap is not None:
            colors = [disease_class_colormap.get(disease, '#CCCCCC') for disease in class_counts.columns]
        else:
            colors = generate_distinct_colors(len(class_counts.columns))
        
        # Plot on this subplot
        percent_df.plot(
            kind='bar',
            width=1.0,
            stacked=True,
            ax=ax,
            color=colors,
            edgecolor='black',
            legend=False  # We'll add a shared legend later
        )
        
        ax.set_ylabel('Approvals, normalized (%)', fontsize=12)
        ax.set_xlabel(xcol.replace('_', ' '), fontsize=12)
        ax.set_title(dataset_name.replace('_', ' '), fontsize=12)
        # ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Format x-axis
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
        ax.tick_params(axis='y', labelsize=10)
    
    # Hide unused subplots
    for i in range(len(datasets_dict), len(axes)):
        axes[i].set_visible(False)
        axes[i].axis('off')
    
    # Create a shared legend
    if disease_class_colormap:
        # Get all unique disease classes across all datasets
        all_diseases = set()
        for df in datasets_dict.values():
            if ycol in df.columns:
                # Split semicolon-separated values to match what we plotted
                values = df[ycol].dropna().astype(str)
                if values.str.contains(';').any():
                    split_values = values.str.split(';').explode().str.strip()
                    split_values = split_values[split_values != '']
                    all_diseases.update(split_values.unique())
                else:
                    all_diseases.update(values.unique())
        
        # Create legend patches
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=disease_class_colormap.get(disease, '#CCCCCC'), 
                                edgecolor='black', label=disease) 
                          for disease in sorted(all_diseases) if disease in disease_class_colormap]
        
        # Save legend as separate file
        legend_elements = legend_elements[::-1]
        fig_legend = plt.figure(figsize=(3, len(legend_elements) * 0.25))
        fig_legend.legend(legend_elements, [elem.get_label() for elem in legend_elements], 
                         title=ycol.replace('_', ' '), loc='center', fontsize=10, title_fontsize=12)
        fig_legend.savefig(f"{SAVE_DIR}/panel_{ycol}_per_{xcol}_legend_{DATASET_FILTER}.png", dpi=300, bbox_inches='tight')
        plt.close(fig_legend)
    
    plt.tight_layout()
    
    # Save
    plt.savefig(f"{SAVE_DIR}/panel_{ycol}_per_{xcol}.png", dpi=300, bbox_inches='tight')
    plt.show()

def plot_disease_class_per_drug_class_single(df, dataset_name, xcol='Drug_class', ycol='Disease_class(es)', disease_class_colormap=None):
    """
    Create a single normalized stacked bar chart showing disease class distribution per drug class.
    Individual version of plot_disease_class_per_drug_class_panel.
    """
    df = df.copy()
    
    # Skip if required columns missing
    if ycol not in df.columns or xcol not in df.columns:
        print(f'{dataset_name}: Missing required columns ({xcol} or {ycol})')
        return
    
    # Preprocessing
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=[ycol, xcol])
    df = df[~df[ycol].astype(str).str.contains('error:', case=False, na=False)]
    df = df[~df[xcol].astype(str).str.contains('error:', case=False, na=False)]
    
    if df.empty:
        print(f'{dataset_name}: No data after filtering')
        return
    
    # Split semicolon-separated disease classes
    df[ycol] = df[ycol].astype(str).str.split(';')
    df = df.explode(ycol)
    df[ycol] = df[ycol].str.strip()
    df = df[df[ycol] != '']
    
    # Group and normalize
    count_df = (
        df.groupby([xcol, ycol])
          .size()
          .unstack(fill_value=0)
    )
    
    # Normalize to percentages
    denom = count_df.sum(axis=1).replace(0, np.nan)
    percent_df = (count_df.T / denom).T.fillna(0) * 100
    
    # Get colors
    if disease_class_colormap is not None:
        colors = [disease_class_colormap.get(disease, '#CCCCCC') for disease in percent_df.columns]
    else:
        colors = generate_distinct_colors(len(percent_df.columns), cmap_name='tab20')
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 7))
    percent_df.plot(
        kind='bar',
        width=1.0,
        stacked=True,
        ax=ax,
        color=colors,
        edgecolor='black',
        legend=True
    )
    
    ax.set_ylabel('Approvals, normalized (%)', fontsize=12)
    ax.set_xlabel(xcol.replace("_", " "), fontsize=12)
    ax.set_title(dataset_name, fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.legend(title=ycol, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}/{ycol}_per_{xcol}_{dataset_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_pie_disease_class_per_drug_class_panel(datasets_dict, xcol=None, ycol=None, disease_class_colormap=None, nrows=None, ncols=None, figsize_per_subplot=(6, 5)):
    """
    Create a panel plot showing disease class distribution per drug class for multiple datasets.
    
    Parameters:
    -----------
    datasets_dict : dict
        Dictionary with dataset names as keys and DataFrames as values
    disease_class_colormap : dict
        Mapping of disease classes to colors
    nrows : int
        Number of rows in the subplot grid (auto-calculated if None)
    ncols : int
        Number of columns in the subplot grid (auto-calculated if None)
    figsize_per_subplot : tuple
        Size of each individual subplot (width, height)
    """
    # Auto-calculate grid dimensions if not provided
    n_datasets = len(datasets_dict)
    if nrows is None or ncols is None:
        ncols = min(3, n_datasets)  # Max 3 columns
        nrows = int(np.ceil(n_datasets / ncols))
    
    # Calculate total figure size
    total_width = figsize_per_subplot[0] * ncols
    total_height = figsize_per_subplot[1] * nrows
    
    # Create subplots
    fig, axes = plt.subplots(nrows, ncols, figsize=(total_width, total_height))
    
    # Flatten axes for easy iteration
    if nrows == 1 and ncols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    # Plot each dataset
    for i, (dataset_name, df) in enumerate(datasets_dict.items()):
        if i >= len(axes):
            break
            
        ax = axes[i]
        df = df.copy()
        
        # Skip if required columns missing
        if ycol not in df.columns or xcol not in df.columns:
            ax.text(0.5, 0.5, f'{dataset_name}\n(Missing columns)', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')
            continue
        
        # Preprocessing
        df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
        df = df.dropna(subset=[ycol, xcol])
        df = df[~df[ycol].astype(str).str.contains('error:', case=False, na=False)]
        df = df[~df[xcol].astype(str).str.contains('error:', case=False, na=False)]

        if df.empty:
            ax.text(0.5, 0.5, f'{dataset_name}\n(No data)', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')
            continue
        
        # Split semicolon-separated disease classes
        df[ycol] = df[ycol].astype(str).str.split(';')
        df = df.explode(ycol)
        df[ycol] = df[ycol].str.strip()
        df = df[df[ycol] != '']
        
        # Count occurrences of disease classes by drug class
        class_counts = df.groupby([xcol, ycol]).size().unstack(fill_value=0)
        class_counts = class_counts.loc[class_counts.sum(axis=1).sort_values(ascending=False).index]
        
        # Get unique drug classes
        drug_classes = class_counts.index.tolist()
        num_drug_classes = len(drug_classes)
        
        if num_drug_classes == 0:
            ax.text(0.5, 0.5, f'{dataset_name}\n(No drug classes)', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.axis('off')
            continue
        
        # Create sub-axes for pie charts (one per drug class)
        ax.axis('off')  # Turn off main axis
        
        # Calculate grid for pie charts within this subplot
        n_cols_pies = min(3, num_drug_classes)  # Max 3 columns of pies
        n_rows_pies = int(np.ceil(num_drug_classes / n_cols_pies))
        
        # Add dataset title
        ax.text(0.5, 0.98, dataset_name.replace('_', ' '), ha='center', va='top', 
               transform=ax.transAxes, fontsize=10)
        
        # Create pie charts for each drug class
        for j, drug_class in enumerate(drug_classes):
            # Calculate position for this pie chart
            row = j // n_cols_pies
            col = j % n_cols_pies
            
            # Calculate subplot position (left, bottom, width, height)
            pie_width = 0.95 / n_cols_pies
            pie_height = 0.9 / n_rows_pies
            left = 0.05 + col * (0.9 / n_cols_pies)
            bottom = 0.08 + (n_rows_pies - row - 1) * (0.85 / n_rows_pies)
            
            # Create inset axes for this pie
            pie_ax = ax.inset_axes([left, bottom, pie_width, pie_height])
            
            # Get data for this drug class
            sizes = class_counts.loc[drug_class]
            sizes = sizes[sizes > 0]  # Remove zero values
            
            if sizes.empty:
                pie_ax.axis('off')
                continue
            
            # Set up colors for this pie
            if disease_class_colormap is not None:
                pie_colors = [disease_class_colormap.get(disease, '#CCCCCC') for disease in sizes.index]
            else:
                pie_colors = generate_distinct_colors(len(sizes))
            
            # Create pie chart
            wedges, texts = pie_ax.pie(
                sizes,
                colors=pie_colors,
                startangle=90,
                wedgeprops=dict(width=0.7, edgecolor='white', linewidth=0.5)  # Donut style
            )
            
            # Add drug class label below pie
            pie_ax.text(0.5, -0.15, drug_class, ha='center', va='bottom',
                       transform=pie_ax.transAxes, fontsize=8)
    
    # Hide unused subplots
    for i in range(len(datasets_dict), len(axes)):
        axes[i].set_visible(False)
        axes[i].axis('off')
    
    # Create a shared legend
    if disease_class_colormap:
        # Get all unique disease classes across all datasets
        all_diseases = set()
        for df in datasets_dict.values():
            if ycol in df.columns:
                # Split semicolon-separated values to match what we plotted
                values = df[ycol].dropna().astype(str)
                if values.str.contains(';').any():
                    split_values = values.str.split(';').explode().str.strip()
                    split_values = split_values[split_values != '']
                    all_diseases.update(split_values.unique())
                else:
                    all_diseases.update(values.unique())
        
        # Create legend patches
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=disease_class_colormap.get(disease, '#CCCCCC'), 
                                edgecolor='black', label=disease) 
                          for disease in sorted(all_diseases) if disease in disease_class_colormap]
        
        # Save legend as separate file
        fig_legend = plt.figure(figsize=(3, len(legend_elements) * 0.25))
        fig_legend.legend(legend_elements, [elem.get_label() for elem in legend_elements], 
                         title=ycol.replace('_', ' '), loc='center', fontsize=10, title_fontsize=12)
        fig_legend.savefig(f"{SAVE_DIR}/panel_pie_{ycol}_per_{xcol}_legend_{DATASET_FILTER}.png", dpi=300, bbox_inches='tight')
        plt.close(fig_legend)
    
    plt.tight_layout()
    
    # Save
    plt.savefig(f"{SAVE_DIR}/panel_pie_{ycol}_per_{xcol}.png", dpi=300, bbox_inches='tight')
    plt.show()

def plot_pie_disease_class_per_drug_class_single(df, dataset_name, xcol='Drug_class', ycol='Disease_class(es)', disease_class_colormap=None):
    """
    Create pie charts showing disease class distribution for each drug class.
    Individual version of plot_pie_disease_class_per_drug_class_panel.
    """
    df = df.copy()
    
    # Skip if required columns missing
    if ycol not in df.columns or xcol not in df.columns:
        print(f'{dataset_name}: Missing required columns ({xcol} or {ycol})')
        return
    
    # Preprocessing
    df = df.replace(["not reported", "Not reported", "", np.nan], np.nan)
    df = df.dropna(subset=[ycol, xcol])
    df = df[~df[ycol].astype(str).str.contains('error:', case=False, na=False)]
    df = df[~df[xcol].astype(str).str.contains('error:', case=False, na=False)]
    
    if df.empty:
        print(f'{dataset_name}: No data after filtering')
        return
    
    # Split semicolon-separated disease classes
    df[ycol] = df[ycol].astype(str).str.split(';')
    df = df.explode(ycol)
    df[ycol] = df[ycol].str.strip()
    df = df[df[ycol] != '']
    
    # Count occurrences
    class_counts = df.groupby([xcol, ycol]).size().unstack(fill_value=0)
    drug_classes = class_counts.index.tolist()
    
    if len(drug_classes) == 0:
        print(f'{dataset_name}: No drug classes found')
        return
    
    # Calculate grid layout
    n_drug_classes = len(drug_classes)
    n_cols = min(4, n_drug_classes)
    n_rows = (n_drug_classes + n_cols - 1) // n_cols
    
    # Create figure
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 4*n_rows))
    if n_rows == 1 and n_cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if n_rows > 1 or n_cols > 1 else [axes]
    
    # Plot each drug class
    for idx, drug_class in enumerate(drug_classes):
        ax = axes[idx]
        sizes = class_counts.loc[drug_class]
        sizes = sizes[sizes > 0]
        
        if sizes.empty:
            ax.axis('off')
            continue
        
        # Colors
        if disease_class_colormap is not None:
            colors = [disease_class_colormap.get(disease, '#CCCCCC') for disease in sizes.index]
        else:
            colors = generate_distinct_colors(len(sizes))
        
        # Pie chart
        wedges, texts, autotexts = ax.pie(
            sizes,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops=dict(edgecolor='white', linewidth=1)
        )
        ax.set_title(drug_class, fontsize=12, fontweight='bold')
    
    # Hide unused subplots
    for idx in range(len(drug_classes), len(axes)):
        axes[idx].axis('off')
    
    # Add legend
    if disease_class_colormap:
        all_diseases = set()
        for disease_list in class_counts.columns:
            all_diseases.add(disease_list)
        
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=disease_class_colormap.get(disease, '#CCCCCC'), 
                                edgecolor='white', label=disease) 
                          for disease in sorted(all_diseases) if disease in disease_class_colormap]
        
        fig.legend(handles=legend_elements, 
                  title=ycol,
                  loc='lower center', 
                  bbox_to_anchor=(0.5, -0.05),
                  ncol=min(3, len(legend_elements)),
                  fontsize=9)
    
    plt.suptitle(f'{dataset_name}: {ycol} per {xcol}', fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}/pie_{ycol}_per_{xcol}_{dataset_name}.png", dpi=300, bbox_inches='tight')
    plt.close()