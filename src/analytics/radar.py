import os
import numpy as np
import matplotlib.pyplot as plt

from src.analytics.comparison import (
    load_peer_percentiles,
    get_peer_group
)

OUTPUT_DIR = "reports/radar_charts"


def load_company_percentiles(company_id):

    peer_group = get_peer_group(company_id)

    if peer_group is None:
        return None, None

    df = load_peer_percentiles()

    df = df[df["peer_group_name"] == peer_group]

    return peer_group, df


def create_radar_chart(company_id):

    peer_group, df = load_company_percentiles(company_id)

    if df is None:
        print("No peer group assigned.")
        return

    company = df[df["company_id"] == company_id]

    peer_average = (
        df.groupby("metric")["percentile_rank"]
        .mean()
        .reset_index()
    )

    company = company.sort_values("metric")
    peer_average = peer_average.sort_values("metric")

    labels = company["metric"].tolist()

    company_values = company["percentile_rank"].tolist()
    average_values = peer_average["percentile_rank"].tolist()

    company_values += company_values[:1]
    average_values += average_values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig, ax = plt.subplots(
        figsize=(8, 8),
        subplot_kw=dict(polar=True)
    )

    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company_id
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )

    ax.plot(
        angles,
        average_values,
        linestyle="--",
        linewidth=2,
        label="Peer Average"
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)

    ax.set_ylim(0, 100)

    ax.set_title(
        f"{company_id} Radar Chart",
        pad=20
    )

    ax.legend(loc="upper right")

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    plt.savefig(
        f"{OUTPUT_DIR}/{company_id}_radar.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {OUTPUT_DIR}/{company_id}_radar.png")


if __name__ == "__main__":

    df = load_peer_percentiles()

    companies = sorted(df["company_id"].unique())

    print(f"Generating radar charts for {len(companies)} companies...\n")

    for company in companies:
        create_radar_chart(company)

    print("\nAll radar charts generated successfully.")