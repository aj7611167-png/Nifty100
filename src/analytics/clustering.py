import sqlite3
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score
)
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# =====================================================
# DATABASE
# =====================================================

DB_PATH = "db/nifty100.db"

# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():
    """
    Create SQLite database connection.
    """
    return sqlite3.connect(DB_PATH)

# =====================================================
# LOAD DATA
# =====================================================

def load_data():
    """
    Load financial ratios and sector data.
    """

    conn = get_connection()

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    sectors = pd.read_sql(
        "SELECT company_id, broad_sector FROM sectors",
        conn
    )

    conn.close()

    return ratios, sectors

# =====================================================
# FCF CAGR
# =====================================================

def calculate_fcf_cagr(series):
    """
    Calculate 5-year CAGR for Free Cash Flow.
    """

    values = series.to_numpy()

    cagr = [np.nan] * len(values)

    for i in range(5, len(values)):

        start = values[i - 5]
        end = values[i]

        if (
            pd.isna(start)
            or pd.isna(end)
            or start <= 0
            or end <= 0
        ):
            cagr[i] = np.nan

        else:

            cagr[i] = (
                ((end / start) ** (1 / 5) - 1)
                * 100
            )

    return cagr

# =====================================================
# PREPARE DATA
# =====================================================

def prepare_dataset():

    ratios, sectors = load_data()

    ratios = ratios.sort_values(
        ["company_id", "year"]
    )

    ratios["fcf_cagr_5yr"] = (
        ratios.groupby("company_id")["free_cash_flow_cr"]
        .transform(calculate_fcf_cagr)
    )

    latest = (
        ratios
        .sort_values(["company_id", "year"])
        .groupby("company_id", as_index=False)
        .last()
    )

    latest = latest.merge(
        sectors,
        on="company_id",
        how="left"
    )

    return latest

# =====================================================
# IMPUTE MISSING VALUES
# =====================================================

def impute_missing_values(df):
    """
    Fill missing feature values using sector median.
    """

    features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct"
    ]

    for feature in features:

        sector_median = (
            df.groupby("broad_sector")[feature]
            .transform("median")
        )

        df[feature] = df[feature].fillna(
            sector_median
        )

        overall_median = df[feature].median()

        df[feature] = df[feature].fillna(
            overall_median
        )

    return df

# =====================================================
# FEATURE SCALING
# =====================================================

def scale_features(df):
    """
    Scale clustering features using StandardScaler.
    """

    features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct"
    ]

    scaler = StandardScaler()

    scaled_array = scaler.fit_transform(
        df[features]
    )

    scaled_df = pd.DataFrame(
        scaled_array,
        columns=features,
        index=df.index
    )

    return scaled_df, scaler

# =====================================================
# KMEANS CLUSTERING
# =====================================================

def run_kmeans(scaled_df):
    """
    Run KMeans clustering with 5 clusters.
    """

    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    cluster_ids = model.fit_predict(
        scaled_df
    )

    distances = model.transform(
        scaled_df
    )

    distance_from_centroid = (
        distances.min(axis=1)
    )

    return (
        cluster_ids,
        distance_from_centroid,
        model
    )

# =====================================================
# CLUSTER EVALUATION
# =====================================================

def evaluate_clusters(
    scaled_df,
    cluster_ids
):
    """
    Evaluate clustering quality.
    """

    silhouette = silhouette_score(
        scaled_df,
        cluster_ids
    )

    davies = davies_bouldin_score(
        scaled_df,
        cluster_ids
    )

    calinski = calinski_harabasz_score(
        scaled_df,
        cluster_ids
    )

    print()

    print("=" * 50)
    print("CLUSTER EVALUATION")
    print("=" * 50)

    print(f"Silhouette Score       : {silhouette:.4f}")
    print(f"Davies-Bouldin Index   : {davies:.4f}")
    print(f"Calinski-Harabasz Score: {calinski:.2f}")

    return (
        silhouette,
        davies,
        calinski
    )
# =====================================================
# CLUSTER NAMES
# =====================================================

def assign_cluster_names(df):
    """
    Assign descriptive names to KMeans clusters.
    """

    cluster_summary = (
        df.groupby("cluster_id")[
            [
                "return_on_equity_pct",
                "debt_to_equity",
                "revenue_cagr_5yr",
                "fcf_cagr_5yr",
                "operating_profit_margin_pct"
            ]
        ]
        .mean()
    )

    print()

    print("=" * 50)
    print("CLUSTER PROFILE")
    print("=" * 50)

    print(cluster_summary.round(2))

    return cluster_summary

# =====================================================
# EXPORT CLUSTER PROFILE
# =====================================================

def export_cluster_profile(cluster_profile):
    """
    Export cluster summary statistics.
    """

    cluster_profile.round(2).to_csv(
        "reports/cluster_profile.csv"
    )

    print()
    print("=" * 50)
    print("CLUSTER PROFILE EXPORTED")
    print("=" * 50)
    print("Saved to reports/cluster_profile.csv")

# =====================================================
# CLUSTER NAME MAPPING
# =====================================================

def add_cluster_names(df):
    """
    Assign descriptive names to each cluster.
    """

    cluster_names = {
        0: "Emerging Growth",
        1: "High-Quality Compounders",
        2: "Stable Performers",
        3: "Financial Leaders",
        4: "Distressed / Turnaround"
    }

    df["cluster_name"] = (
        df["cluster_id"]
        .map(cluster_names)
    )

    return df

# =====================================================
# EXPORT CLUSTER LABELS
# =====================================================

def export_cluster_labels(df):
    """
    Export cluster labels to CSV.
    """

    output = df[
        [
            "company_id",
            "cluster_id",
            "cluster_name",
            "distance_from_centroid"
        ]
    ].copy()

    output = output.sort_values(
        by="company_id"
    )

    output.to_csv(
        "output/cluster_labels.csv",
        index=False
    )

    print()

    print("=" * 50)
    print("CLUSTER LABELS EXPORTED")
    print("=" * 50)

    print(
        "Saved to output/cluster_labels.csv"
    )

    print()

    print(output.head())

# =====================================================
# EXPORT CLUSTERED COMPANIES
# =====================================================

def export_clustered_companies(df):
    """
    Export all companies with their assigned clusters.
    """

    output = df[
        [
            "company_id",
            "cluster_id",
            "cluster_name",
            "broad_sector",
            "distance_from_centroid"
        ]
    ].copy()

    output = output.sort_values(
        ["cluster_id", "company_id"]
    )

    output.to_csv(
        "output/clustered_companies.csv",
        index=False
    )

    print()
    print("=" * 50)
    print("CLUSTERED COMPANIES EXPORTED")
    print("=" * 50)
    print("Saved to output/clustered_companies.csv")

# =====================================================
# EXPORT CLUSTER METRICS
# =====================================================

def export_cluster_metrics(
    silhouette,
    dbi,
    ch_score
):
    """
    Export clustering evaluation metrics to CSV.
    """

    metrics = pd.DataFrame(
        {
            "Metric": [
                "Silhouette Score",
                "Davies-Bouldin Index",
                "Calinski-Harabasz Score"
            ],
            "Value": [
                round(silhouette, 4),
                round(dbi, 4),
                round(ch_score, 4)
            ]
        }
    )

    metrics.to_csv(
        "output/cluster_metrics.csv",
        index=False
    )

    print()

    print("=" * 50)
    print("CLUSTER METRICS EXPORTED")
    print("=" * 50)

    print(
        "Saved to output/cluster_metrics.csv"
    )

    print()

    print(metrics)


# =====================================================
# ELBOW PLOT
# =====================================================

def generate_elbow_plot(scaled_df):
    """
    Generate KMeans elbow plot.
    """

    inertias = []

    k_values = range(2, 11)

    for k in k_values:

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(scaled_df)

        inertias.append(
            model.inertia_
        )

    plt.figure(figsize=(8, 5))

    plt.plot(
        k_values,
        inertias,
        marker="o"
    )

    plt.title(
        "KMeans Elbow Curve"
    )

    plt.xlabel(
        "Number of Clusters (k)"
    )

    plt.ylabel(
        "Inertia"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "reports/elbow_plot.png",
        dpi=300
    )

    plt.close()

    return inertias

# =====================================================
# PCA CLUSTER VISUALIZATION
# =====================================================

def plot_clusters(
    scaled_df,
    cluster_ids
):
    """
    Plot KMeans clusters using PCA.
    """

    pca = PCA(
        n_components=2,
        random_state=42
    )

    components = pca.fit_transform(
        scaled_df
    )

    plt.figure(figsize=(8, 6))

    scatter = plt.scatter(
        components[:, 0],
        components[:, 1],
        c=cluster_ids
    )

    plt.title(
        "KMeans Clusters (PCA Projection)"
    )

    plt.xlabel(
        "Principal Component 1"
    )

    plt.ylabel(
        "Principal Component 2"
    )

    plt.colorbar(
        scatter,
        label="Cluster"
    )

    plt.tight_layout()

    plt.savefig(
        "reports/clusters_pca.png",
        dpi=300
    )

    plt.close()

# =====================================================
# CLUSTER SCATTER PLOT
# =====================================================

def plot_cluster_scatter(df):
    """
    Plot clusters using ROE vs Revenue CAGR.
    """

    plt.figure(figsize=(10, 7))

    scatter = plt.scatter(
        df["return_on_equity_pct"],
        df["revenue_cagr_5yr"],
        c=df["cluster_id"],
        s=70,
        alpha=0.8
    )

    plt.title(
        "Company Clusters (ROE vs Revenue CAGR)"
    )

    plt.xlabel(
        "Return on Equity (%)"
    )

    plt.ylabel(
        "Revenue CAGR 5 Year (%)"
    )

    plt.grid(True)

    plt.colorbar(
        scatter,
        label="Cluster"
    )

    plt.tight_layout()

    plt.savefig(
        "reports/cluster_scatter.png",
        dpi=300
    )

    plt.close()

# =====================================================
# CLEAN FEATURES
# =====================================================

def clean_features(df):
    """
    Clean unrealistic KPI values before clustering.
    """

    # ROE should generally be within ±100%
    df["return_on_equity_pct"] = (
        df["return_on_equity_pct"]
        .clip(-100, 100)
    )

    # Operating Margin should generally be within ±100%
    df["operating_profit_margin_pct"] = (
        df["operating_profit_margin_pct"]
        .clip(-100, 100)
    )

    # Debt to Equity cannot be negative
    df["debt_to_equity"] = (
        df["debt_to_equity"]
        .clip(lower=0)
    )

    return df

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    # -------------------------------------------------
    # Prepare Dataset
    # -------------------------------------------------

    df = prepare_dataset()

    df = clean_features(df)

    # -------------------------------------------------
    # Impute Missing Values
    # -------------------------------------------------

    df = impute_missing_values(df)

    # -------------------------------------------------
    # Scale Features
    # -------------------------------------------------

    scaled_df, scaler = scale_features(df)

    # -------------------------------------------------
    # Run KMeans
    # -------------------------------------------------

    cluster_ids, distances, model = run_kmeans(
        scaled_df
    )

    # -------------------------------------------------
    # Evaluate Clustering
    # -------------------------------------------------

    silhouette, dbi, ch_score = evaluate_clusters(
        scaled_df,
        cluster_ids
    )

    export_cluster_metrics(
        silhouette,
        dbi,
        ch_score
    )

    # -------------------------------------------------
    # Generate Elbow Plot
    # -------------------------------------------------

    inertias = generate_elbow_plot(
        scaled_df
    )

    # -------------------------------------------------
    # Add Cluster Results
    # -------------------------------------------------

    df["cluster_id"] = cluster_ids

    df["distance_from_centroid"] = (
        distances.round(4)
    )

    # -------------------------------------------------
    # Cluster Profiling
    # -------------------------------------------------

    cluster_profile = assign_cluster_names(df)

    export_cluster_profile(cluster_profile)

    # Add descriptive cluster names
    df = add_cluster_names(df)

    # Export clustered companies
    export_clustered_companies(df)

    # Export cluster labels
    export_cluster_labels(df)

    # -------------------------------------------------
    # PCA Cluster Visualization
    # -------------------------------------------------

    plot_clusters(
        scaled_df,
        cluster_ids
    )

    # -------------------------------------------------
    # Cluster Scatter Plot
    # -------------------------------------------------

    plot_cluster_scatter(df)

    # -------------------------------------------------
    # Dataset Preview
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("LATEST DATASET")
    print("=" * 50)

    print(df.head())

    print()

    print(df.columns.tolist())

    # -------------------------------------------------
    # Missing Values
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("MISSING VALUES")
    print("=" * 50)

    print(
        df[
            [
                "return_on_equity_pct",
                "debt_to_equity",
                "revenue_cagr_5yr",
                "fcf_cagr_5yr",
                "operating_profit_margin_pct"
            ]
        ].isna().sum()
    )

    # -------------------------------------------------
    # Scaled Features
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("SCALED FEATURES")
    print("=" * 50)

    print(scaled_df.head())

    # -------------------------------------------------
    # Scaling Verification
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("FEATURE MEANS")
    print("=" * 50)

    print(
        scaled_df.mean().round(4)
    )

    print()

    print("=" * 50)
    print("FEATURE STANDARD DEVIATIONS")
    print("=" * 50)

    print(
        scaled_df.std().round(4)
    )

    # -------------------------------------------------
    # Cluster Summary
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("CLUSTER SUMMARY")
    print("=" * 50)

    print(
        df["cluster_id"]
        .value_counts()
        .sort_index()
    )

    # -------------------------------------------------
    # First 10 Companies
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("FIRST 10 COMPANIES")
    print("=" * 50)

    print(
        df[
            [
                "company_id",
                "cluster_id",
                "distance_from_centroid"
            ]
        ].head(10)
    )

    # -------------------------------------------------
    # Feature Summary
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("FEATURE SUMMARY")
    print("=" * 50)

    print(
        df[
            [
                "return_on_equity_pct",
                "debt_to_equity",
                "revenue_cagr_5yr",
                "fcf_cagr_5yr",
                "operating_profit_margin_pct"
            ]
        ].describe()
    )

    # -------------------------------------------------
    # Highest ROE
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("EXTREME ROE")
    print("=" * 50)

    print(
        df[
            [
                "company_id",
                "return_on_equity_pct"
            ]
        ]
        .sort_values(
            by="return_on_equity_pct",
            ascending=False
        )
        .head(10)
    )

    # -------------------------------------------------
    # Highest Operating Profit Margin
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("EXTREME OPM")
    print("=" * 50)

    print(
        df[
            [
                "company_id",
                "operating_profit_margin_pct"
            ]
        ]
        .sort_values(
            by="operating_profit_margin_pct",
            ascending=False
        )
        .head(10)
    )

    # -------------------------------------------------
    # Lowest Operating Profit Margin
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("LOWEST OPM")
    print("=" * 50)

    print(
        df[
            [
                "company_id",
                "operating_profit_margin_pct"
            ]
        ]
        .sort_values(
            by="operating_profit_margin_pct",
            ascending=True
        )
        .head(10)
    )

    # -------------------------------------------------
    # Companies in Each Cluster
    # -------------------------------------------------

    print()

    print("=" * 50)
    print("COMPANIES PER CLUSTER")
    print("=" * 50)

    for cluster in sorted(df["cluster_id"].unique()):

        print()

        print(f"Cluster {cluster}")

        print(
            df.loc[
                df["cluster_id"] == cluster,
                "company_id"
            ].tolist()
        )