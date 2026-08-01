from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"


def load_data() -> pd.DataFrame:
    clean_path = DATA / "clean_lgfv_credit_data.csv"
    sample_path = DATA / "sample_lgfv_credit_data.csv"
    path = clean_path if clean_path.exists() else sample_path
    df = pd.read_csv(path)
    df["period"] = pd.to_datetime(df["period"])
    return df


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["credit_spread"] = df["weighted_yield"] - df["benchmark_yield"]
    df["land_revenue_share"] = df["land_transfer_revenue"] / df["fiscal_revenue"]
    df["net_financing_ratio"] = df["net_financing"] / df["fiscal_revenue"]
    return df


def save_summary(df: pd.DataFrame) -> None:
    summary = (
        df.groupby("region", as_index=False)
        .agg(
            fiscal_revenue=("fiscal_revenue", "mean"),
            land_transfer_revenue=("land_transfer_revenue", "mean"),
            bond_issuance=("bond_issuance", "sum"),
            repayment=("repayment", "sum"),
            net_financing=("net_financing", "sum"),
            credit_spread=("credit_spread", "mean"),
            remaining_maturity=("remaining_maturity", "mean"),
            turnover=("turnover", "mean"),
        )
        .sort_values("credit_spread", ascending=False)
    )
    summary.to_csv(OUT / "summary_by_region.csv", index=False)


def _svg_bar_chart(path: Path, title: str, labels: list[str], values: list[float], y_label: str) -> None:
    width, height = 820, 460
    margin_left, margin_right, margin_top, margin_bottom = 90, 30, 70, 90
    chart_w = width - margin_left - margin_right
    chart_h = height - margin_top - margin_bottom
    min_v = min(0, min(values))
    max_v = max(values)
    span = max(max_v - min_v, 1)
    bar_gap = 24
    bar_w = (chart_w - bar_gap * (len(values) + 1)) / len(values)

    def y(v: float) -> float:
        return margin_top + chart_h - ((v - min_v) / span) * chart_h

    zero_y = y(0)
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="35" text-anchor="middle" font-family="Arial" font-size="22" font-weight="700">{title}</text>',
        f'<text x="22" y="{height/2}" transform="rotate(-90 22 {height/2})" text-anchor="middle" font-family="Arial" font-size="13">{y_label}</text>',
        f'<line x1="{margin_left}" y1="{zero_y:.1f}" x2="{width-margin_right}" y2="{zero_y:.1f}" stroke="#222" stroke-width="1"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height-margin_bottom}" stroke="#222" stroke-width="1"/>',
    ]

    for i, (label, value) in enumerate(zip(labels, values)):
        x = margin_left + bar_gap + i * (bar_w + bar_gap)
        bar_y = min(y(value), zero_y)
        bar_h = abs(y(value) - zero_y)
        parts.append(f'<rect x="{x:.1f}" y="{bar_y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" fill="{colors[i % len(colors)]}"/>')
        parts.append(f'<text x="{x + bar_w/2:.1f}" y="{bar_y - 8:.1f}" text-anchor="middle" font-family="Arial" font-size="12">{value:.2f}</text>')
        parts.append(f'<text x="{x + bar_w/2:.1f}" y="{height - 55}" text-anchor="middle" font-family="Arial" font-size="12">{label}</text>')

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def _svg_line_chart(path: Path, title: str, df: pd.DataFrame, x_col: str, y_col: str, group_col: str, y_label: str) -> None:
    width, height = 900, 500
    margin_left, margin_right, margin_top, margin_bottom = 90, 40, 70, 80
    chart_w = width - margin_left - margin_right
    chart_h = height - margin_top - margin_bottom
    periods = sorted(df[x_col].unique())
    min_v = float(df[y_col].min())
    max_v = float(df[y_col].max())
    span = max(max_v - min_v, 1)

    def x(period) -> float:
        idx = periods.index(period)
        return margin_left + (idx / max(len(periods) - 1, 1)) * chart_w

    def y(value: float) -> float:
        return margin_top + chart_h - ((value - min_v) / span) * chart_h

    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="35" text-anchor="middle" font-family="Arial" font-size="22" font-weight="700">{title}</text>',
        f'<text x="24" y="{height/2}" transform="rotate(-90 24 {height/2})" text-anchor="middle" font-family="Arial" font-size="13">{y_label}</text>',
        f'<line x1="{margin_left}" y1="{height-margin_bottom}" x2="{width-margin_right}" y2="{height-margin_bottom}" stroke="#222"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height-margin_bottom}" stroke="#222"/>',
    ]

    for i, period in enumerate(periods):
        label = pd.to_datetime(period).strftime("%Y-%m")
        parts.append(f'<text x="{x(period):.1f}" y="{height - 45}" text-anchor="middle" font-family="Arial" font-size="11">{label}</text>')

    for i, (group, sub) in enumerate(df.groupby(group_col)):
        sub = sub.sort_values(x_col)
        points = " ".join(f'{x(row[x_col]):.1f},{y(float(row[y_col])):.1f}' for _, row in sub.iterrows())
        color = colors[i % len(colors)]
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3"/>')
        for _, row in sub.iterrows():
            parts.append(f'<circle cx="{x(row[x_col]):.1f}" cy="{y(float(row[y_col])):.1f}" r="4" fill="{color}"/>')
        legend_x = width - margin_right - 145
        legend_y = margin_top + i * 24
        parts.append(f'<rect x="{legend_x}" y="{legend_y - 10}" width="14" height="14" fill="{color}"/>')
        parts.append(f'<text x="{legend_x + 20}" y="{legend_y + 2}" font-family="Arial" font-size="12">{group}</text>')

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def plot_credit_spread(df: pd.DataFrame) -> None:
    _svg_line_chart(
        OUT / "credit_spread_by_region.svg",
        "Credit Spread by Region",
        df,
        "period",
        "credit_spread",
        "region",
        "Weighted yield minus benchmark yield",
    )


def plot_net_financing(df: pd.DataFrame) -> None:
    summary = df.groupby("region", as_index=False)["net_financing"].sum()
    _svg_bar_chart(
        OUT / "net_financing_by_region.svg",
        "Net Financing by Region",
        summary["region"].astype(str).tolist(),
        summary["net_financing"].astype(float).tolist(),
        "Issuance minus repayment",
    )


def plot_fiscal_land_revenue(df: pd.DataFrame) -> None:
    summary = (
        df.groupby("region", as_index=False)[["fiscal_revenue", "land_transfer_revenue"]]
        .mean()
        .sort_values("fiscal_revenue", ascending=False)
    )
    summary["land_revenue_share_percent"] = (
        summary["land_transfer_revenue"] / summary["fiscal_revenue"] * 100
    )
    _svg_bar_chart(
        OUT / "land_revenue_share.svg",
        "Land-Transfer Revenue Share of Fiscal Revenue",
        summary["region"].astype(str).tolist(),
        summary["land_revenue_share_percent"].astype(float).tolist(),
        "Percent",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = prepare(load_data())
    save_summary(df)
    plot_credit_spread(df)
    plot_net_financing(df)
    plot_fiscal_land_revenue(df)
    print(f"Generated outputs in {OUT}")


if __name__ == "__main__":
    main()
