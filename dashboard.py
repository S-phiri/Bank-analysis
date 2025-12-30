"""
Bank Customer Analytics Dashboard
Streamlit web application for visualizing bank customer data
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Bank Customer Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection
DB_FILE = 'bank.db'

@st.cache_data
def load_view(view_name):
    """Load data from a SQL view with caching."""
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query(f"SELECT * FROM {view_name}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading {view_name}: {str(e)}")
        return pd.DataFrame()

# Title and header
st.title("🏦 Bank Customer Analytics Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("📊 Filters & Options")

# Check if database exists
try:
    # Load overall KPIs
    kpis_df = load_view('overall_kpis')
    
    if kpis_df.empty:
        st.error("⚠️ No data found. Please ensure views are created in the database.")
        st.stop()
    
    # Main KPI metrics
    st.header("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = int(kpis_df['total_customers'].iloc[0])
        st.metric(
            label="Total Customers",
            value=f"{total_customers:,}",
            delta=None
        )
    
    with col2:
        churn_rate = kpis_df['overall_churn_rate_pct'].iloc[0]
        st.metric(
            label="Overall Churn Rate",
            value=f"{churn_rate:.1f}%",
            delta=None
        )
    
    with col3:
        avg_balance = kpis_df['avg_balance'].iloc[0]
        st.metric(
            label="Average Balance",
            value=f"${avg_balance:,.2f}",
            delta=None
        )
    
    with col4:
        total_balance = kpis_df['total_balance'].iloc[0]
        st.metric(
            label="Total Balance",
            value=f"${total_balance:,.0f}",
            delta=None
        )
    
    st.markdown("---")
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔴 Churn Analysis",
        "💰 Balance Analysis",
        "👥 Customer Segmentation",
        "🏢 Branch Performance",
        "📋 Data Tables"
    ])
    
    # TAB 1: Churn Analysis
    with tab1:
        st.header("Customer Churn Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Churn Rate by Branch")
            churn_branch = load_view('churn_by_branch')
            if not churn_branch.empty:
                fig = px.bar(
                    churn_branch,
                    x='branch',
                    y='churn_rate_pct',
                    color='churn_rate_pct',
                    color_continuous_scale='Reds',
                    labels={'churn_rate_pct': 'Churn Rate (%)', 'branch': 'Branch'},
                    title="Churn Rate by Branch"
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Churn Rate by Account Type")
            churn_account = load_view('churn_by_account_type')
            if not churn_account.empty:
                fig = px.pie(
                    churn_account,
                    values='churn_rate_pct',
                    names='account_type',
                    title="Churn Rate Distribution by Account Type",
                    color_discrete_sequence=px.colors.sequential.Reds
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Churn by Income Band")
        income_churn = load_view('income_band_churn')
        if not income_churn.empty:
            fig = px.bar(
                income_churn,
                x='income_band',
                y='churn_rate_pct',
                color='churn_rate_pct',
                color_continuous_scale='Reds',
                labels={'churn_rate_pct': 'Churn Rate (%)', 'income_band': 'Income Band'},
                title="Churn Rate by Income Band",
                text='churn_rate_pct'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: Balance Analysis
    with tab2:
        st.header("Balance & Financial Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Average Balance by Branch")
            balance_branch = load_view('avg_balance_by_branch')
            if not balance_branch.empty:
                fig = px.bar(
                    balance_branch,
                    x='branch',
                    y='avg_balance',
                    color='avg_balance',
                    color_continuous_scale='Greens',
                    labels={'avg_balance': 'Average Balance ($)', 'branch': 'Branch'},
                    title="Average Balance by Branch"
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Average Balance by Account Type")
            balance_account = load_view('avg_balance_by_account_type')
            if not balance_account.empty:
                fig = px.bar(
                    balance_account,
                    x='account_type',
                    y='avg_balance',
                    color='avg_balance',
                    color_continuous_scale='Blues',
                    labels={'avg_balance': 'Average Balance ($)', 'account_type': 'Account Type'},
                    title="Average Balance by Account Type"
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Balance by Customer Tenure")
        balance_tenure = load_view('balance_by_tenure')
        if not balance_tenure.empty:
            fig = px.line(
                balance_tenure,
                x='tenure_group',
                y='avg_balance',
                markers=True,
                labels={'avg_balance': 'Average Balance ($)', 'tenure_group': 'Tenure Group'},
                title="Average Balance by Customer Tenure"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3: Customer Segmentation
    with tab3:
        st.header("Customer Segmentation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Account Type Distribution")
            account_dist = load_view('account_type_distribution')
            if not account_dist.empty:
                fig = px.pie(
                    account_dist,
                    values='num_customers',
                    names='account_type',
                    title="Customer Distribution by Account Type",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Branch Distribution")
            branch_dist = load_view('branch_distribution')
            if not branch_dist.empty:
                fig = px.pie(
                    branch_dist,
                    values='num_customers',
                    names='branch',
                    title="Customer Distribution by Branch",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("High-Value Customers")
        high_value = load_view('high_value_customers')
        if not high_value.empty:
            st.dataframe(
                high_value[['customer_id', 'branch', 'account_type', 'balance', 'income', 'tenure_years']],
                use_container_width=True,
                hide_index=True
            )
    
    # TAB 4: Branch Performance
    with tab4:
        st.header("Branch Performance Overview")
        
        branch_perf = load_view('branch_performance')
        if not branch_perf.empty:
            # Combined metrics chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=branch_perf['branch'],
                y=branch_perf['churn_rate_pct'],
                name='Churn Rate (%)',
                marker_color='lightcoral',
                yaxis='y'
            ))
            
            fig.add_trace(go.Scatter(
                x=branch_perf['branch'],
                y=branch_perf['avg_balance'],
                name='Avg Balance ($)',
                mode='lines+markers',
                line=dict(color='green', width=3),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="Branch Performance: Churn Rate vs Average Balance",
                xaxis_title="Branch",
                yaxis=dict(title="Churn Rate (%)", side="left"),
                yaxis2=dict(title="Average Balance ($)", overlaying="y", side="right"),
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance table
            st.subheader("Branch Performance Metrics")
            st.dataframe(
                branch_perf,
                use_container_width=True,
                hide_index=True
            )
    
    # TAB 5: Data Tables
    with tab5:
        st.header("Data Tables")
        
        view_options = {
            "Churn by Branch": "churn_by_branch",
            "Churn by Account Type": "churn_by_account_type",
            "Income Band Churn": "income_band_churn",
            "Average Balance by Branch": "avg_balance_by_branch",
            "Average Balance by Account Type": "avg_balance_by_account_type",
            "Balance by Tenure": "balance_by_tenure",
            "Account Type Distribution": "account_type_distribution",
            "Branch Distribution": "branch_distribution",
            "High Value Customers": "high_value_customers",
            "Overall KPIs": "overall_kpis",
            "Branch Performance": "branch_performance"
        }
        
        selected_view = st.selectbox("Select a view to display:", list(view_options.keys()))
        
        if selected_view:
            df = load_view(view_options[selected_view])
            if not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"{view_options[selected_view]}.csv",
                    mime="text/csv"
                )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Bank Customer Analytics Dashboard | Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

except sqlite3.OperationalError as e:
    st.error(f"⚠️ Database error: {str(e)}")
    st.info("💡 Make sure you've created the views by running views.sql first!")
except FileNotFoundError:
    st.error("⚠️ Database file 'bank.db' not found!")
    st.info("💡 Please ensure bank.db exists in the current directory.")
except Exception as e:
    st.error(f"⚠️ An error occurred: {str(e)}")

