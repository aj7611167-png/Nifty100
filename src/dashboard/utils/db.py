import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


# =====================================================
# COMPANIES
# =====================================================

@st.cache_data(ttl=600)
def get_companies():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    conn.close()

    return df


# =====================================================
# FINANCIAL RATIOS
# =====================================================

@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    conn = get_connection()

    if year is not None:

        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        AND year = ?
        """

        df = pd.read_sql(
            query,
            conn,
            params=(ticker, year)
        )

    else:

        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        """

        df = pd.read_sql(
            query,
            conn,
            params=(ticker,)
        )

    conn.close()

    return df


# =====================================================
# PROFIT & LOSS
# =====================================================

@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=(ticker,)
    )

    conn.close()

    return df


# =====================================================
# BALANCE SHEET
# =====================================================

@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        """,
        conn,
        params=(ticker,)
    )

    conn.close()

    return df


# =====================================================
# CASH FLOW
# =====================================================

@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        """,
        conn,
        params=(ticker,)
    )

    conn.close()

    return df


# =====================================================
# SECTORS
# =====================================================

@st.cache_data(ttl=600)
def get_sectors():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM sectors
        """,
        conn
    )

    conn.close()

    return df


# =====================================================
# PEER GROUPS
# =====================================================

@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM peer_groups
        WHERE peer_group_name = ?
        """,
        conn,
        params=(group_name,)
    )

    conn.close()

    return df


# =====================================================
# VALUATION
# =====================================================

@st.cache_data(ttl=600)
def get_valuation(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM market_cap
        WHERE company_id = ?
        """,
        conn,
        params=(ticker,)
    )

    conn.close()

    return df

# =====================================================
# MASTER DASHBOARD DATA
# =====================================================

@st.cache_data(ttl=600)
def get_dashboard_data():

    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        c.roe_percentage,
        c.roce_percentage,

        s.broad_sector,
        s.sub_sector,

        r.year,
        r.composite_quality_score,
        r.debt_to_equity,
        r.free_cash_flow_cr,
        r.revenue_cagr_5yr,
        r.return_on_equity_pct

    FROM companies c

    LEFT JOIN financial_ratios r
        ON c.id = r.company_id

    LEFT JOIN sectors s
        ON c.id = s.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_pros_cons(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM prosandcons
        WHERE company_id=?
        """,
        conn,
        params=(ticker,)
    )

    conn.close()

    return df

# =====================================================
# MARKET CAP
# =====================================================

@st.cache_data(ttl=600)
def get_market_cap():
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM market_cap
        """,
        conn
    )

    conn.close()

    return df
