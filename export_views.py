"""
export_views.py
Exports all SQL views from bank.db to CSV files in the results/ folder.
"""

import sqlite3
import pandas as pd
import os
from pathlib import Path

# Database and output settings
DB_FILE = 'bank.db'
RESULTS_DIR = 'results'

# List of all views to export
VIEWS = [
    'churn_by_branch',
    'churn_by_account_type',
    'income_band_churn',
    'avg_balance_by_branch',
    'avg_balance_by_account_type',
    'balance_by_tenure',
    'account_type_distribution',
    'branch_distribution',
    'high_value_customers',
    'overall_kpis',
    'branch_performance'
]


def create_results_folder():
    """Create results directory if it doesn't exist."""
    Path(RESULTS_DIR).mkdir(exist_ok=True)
    print(f"[OK] Results folder '{RESULTS_DIR}' ready")


def export_view_to_csv(conn, view_name):
    """
    Export a single view to CSV.
    
    Args:
        conn: SQLite database connection
        view_name: Name of the view to export
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Query the view
        query = f"SELECT * FROM {view_name}"
        df = pd.read_sql_query(query, conn)
        
        # Export to CSV
        csv_path = os.path.join(RESULTS_DIR, f"{view_name}.csv")
        df.to_csv(csv_path, index=False)
        
        # Print success message
        num_rows = len(df)
        print(f"  [OK] Exported {view_name:30s} -> {num_rows:3d} rows -> {csv_path}")
        
        return True
        
    except sqlite3.OperationalError as e:
        print(f"  [ERROR] Error exporting {view_name}: View does not exist")
        print(f"    Hint: Make sure you've run views.sql first")
        return False
    except Exception as e:
        print(f"  [ERROR] Error exporting {view_name}: {str(e)}")
        return False


def main():
    """Main function to export all views."""
    print("=" * 70)
    print("Bank Customer Analytics - View Exporter")
    print("=" * 70)
    print()
    
    # Check if database exists
    if not os.path.exists(DB_FILE):
        print(f"[ERROR] Database file '{DB_FILE}' not found!")
        print("  Make sure bank.db exists in the current directory.")
        return
    
    # Create results folder
    create_results_folder()
    print()
    
    # Connect to database
    try:
        conn = sqlite3.connect(DB_FILE)
        print(f"[OK] Connected to {DB_FILE}")
        print()
        print("Exporting views to CSV...")
        print("-" * 70)
        
        # Export each view
        success_count = 0
        for view in VIEWS:
            if export_view_to_csv(conn, view):
                success_count += 1
        
        # Close connection
        conn.close()
        
        # Summary
        print("-" * 70)
        print(f"\nSummary: {success_count}/{len(VIEWS)} views exported successfully")
        print(f"CSV files saved to: {os.path.abspath(RESULTS_DIR)}/")
        print("=" * 70)
        
    except Exception as e:
        print(f"[ERROR] Error connecting to database: {str(e)}")


if __name__ == "__main__":
    main()

