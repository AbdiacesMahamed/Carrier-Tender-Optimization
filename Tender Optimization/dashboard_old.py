"""
Carrier Tender Optimization Dashboard
Main application file that orchestrates all components
"""

# Import necessary libraries
import pandas as pd
import streamlit as st

# Import all dashboard components
from components import (
    # Configuration
    configure_page, apply_custom_css, show_header,
    
    # Data handling
    show_file_upload_section, load_data_files, process_performance_data,
    validate_and_process_gvt_data, validate_and_process_rate_data, 
    perform_lane_analysis, merge_all_data, create_comprehensive_data,
    
    # Filtering
    show_filter_interface, apply_filters_to_data, show_selection_summary,
    
    # Metrics
    calculate_enhanced_metrics, display_current_metrics, show_detailed_analysis_table,
    show_top_savings_opportunities, show_complete_data_export,
    
    # Tables and analysis
    show_summary_tables,
    
    # Optimization
    show_optimization_section, show_optimization_methodology,
    
    # Analytics and visualizations
    show_advanced_analytics, show_interactive_visualizations,
    
    # Utilities
    show_calculation_logic, show_debug_performance_merge, show_footer
)

# Import performance calculator for clean calculations
from components.performance_calculator import calculate_performance_optimization

def main():
    """Main dashboard application"""
    
    # Configure page and apply styling
    configure_page()
    apply_custom_css()
    show_header()
    
    # File upload and data loading
    gvt_file, rate_file, performance_file = show_file_upload_section()
    GVTdata, Ratedata, Performancedata, has_performance = load_data_files(gvt_file, rate_file, performance_file)
    
    # Process performance data
    performance_clean, has_performance = process_performance_data(Performancedata, has_performance)
    
    # Validate and process data
    GVTdata = validate_and_process_gvt_data(GVTdata)
    Ratedata = validate_and_process_rate_data(Ratedata)
    
    # Perform lane analysis
    cheapest_rates_by_lane = perform_lane_analysis(Ratedata)
    
    # Merge all data
    merged_data = merge_all_data(GVTdata, Ratedata, cheapest_rates_by_lane, performance_clean, has_performance)
    comprehensive_data = create_comprehensive_data(merged_data)
    
    # Show filters
    show_filter_interface(comprehensive_data)
    
    # Apply filters
    final_filtered_data, display_ports, display_fcs, display_weeks, display_scacs = apply_filters_to_data(comprehensive_data)
    
    # Show selection summary
    show_selection_summary(display_ports, display_fcs, display_weeks, display_scacs, final_filtered_data)
    
    # Calculate and display metrics
    metrics = calculate_enhanced_metrics(final_filtered_data)
    display_current_metrics(metrics)
    
    # Show detailed analysis if data exists
    if len(final_filtered_data) > 0:
        show_detailed_analysis_table(final_filtered_data)
        show_summary_tables(final_filtered_data)
        show_top_savings_opportunities(final_filtered_data)
        show_complete_data_export(final_filtered_data)
    
    # Show calculation logic
    show_calculation_logic()
    
    # Debug performance merge
    show_debug_performance_merge(merged_data, performance_clean, has_performance)
    
    # Show optimization section
    show_optimization_section(final_filtered_data)
    show_optimization_methodology()
    
    # Show advanced analytics
    show_advanced_analytics(final_filtered_data)
    
    # Show interactive visualizations
    show_interactive_visualizations(final_filtered_data)
    
    # Footer
    show_footer()

if __name__ == "__main__":
    main()

# File upload section
st.markdown('<div class="section-header">📁 Upload Your Data</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**GVT Data**")
    gvt_file = st.file_uploader(
        "Upload GVT Data Excel file", 
        type=['xlsx', 'xls'],
        key="gvt_upload"
    )

with col2:
    st.markdown("**Rate Data**")
    rate_file = st.file_uploader(
        "Upload Rate Data Excel file", 
        type=['xlsx', 'xls'],
        key="rate_upload"
    )

with col3:
    st.markdown("**Performance Data**")
    performance_file = st.file_uploader(
        "Upload Performance Data Excel file", 
        type=['xlsx', 'xls'],
        key="performance_upload"
    )

# Load data based on uploads or use default
if gvt_file is not None and rate_file is not None:
    # Use uploaded files
    GVTdata = pd.read_excel(gvt_file, sheet_name='GVT data')
    Ratedata = pd.read_excel(rate_file, sheet_name='Rate Sheet')
    
    # Performance data is optional
    if performance_file is not None:
        Performancedata = pd.read_excel(performance_file)
        has_performance = True
        st.markdown('<div class="success-box">✅ All files uploaded successfully!</div>', unsafe_allow_html=True)
    else:
        has_performance = False
        st.markdown('<div class="success-box">✅ GVT and Rate data uploaded successfully! Performance data is optional.</div>', unsafe_allow_html=True)
        
elif gvt_file is not None or rate_file is not None:
    st.warning("⚠️ Please upload both GVT Data and Rate Data files to proceed. Performance Data is optional.")
    st.stop()
else:
    # Use default files
    try:
        GVTdata = pd.read_excel("c:\\Users\\maabdiac\\Downloads\\gvt data 8-5.xlsx")
        Ratedata = pd.read_excel("c:\\Users\\maabdiac\\Downloads\\Linear Programming.xlsx", sheet_name='Rate Sheet')
        
        # Try to load performance data, but make it optional
        try:
            Performancedata = pd.read_excel("C:\\Users\\maabdiac\\Downloads\\carrier scorecard 8-5.xlsx")
            has_performance = True
            st.markdown('<div class="info-box">ℹ️ Using default data files including performance data. Upload new files above to replace them.</div>', unsafe_allow_html=True)
        except FileNotFoundError:
            has_performance = False
            st.markdown('<div class="info-box">ℹ️ Using default GVT and Rate data files. Performance data not found - running without performance metrics.</div>', unsafe_allow_html=True)
            
    except FileNotFoundError:
        st.error("❌ Default GVT or Rate data files not found. Please upload your Excel files above.")
        st.stop()

# Process Performance Data (only if available)
st.markdown('<div class="section-header">📊 Performance Data Processing</div>', unsafe_allow_html=True)

# Process performance data using the centralized data loader function
performance_clean, has_performance = process_performance_data(Performancedata, has_performance)

# Check if required columns exist and handle missing ones
required_gvt_columns = ['SSL ATA', 'Discharged Port', 'Dray SCAC(FL)', 'Facility']
missing_columns = [col for col in required_gvt_columns if col not in GVTdata.columns]

if missing_columns:
    st.error(f"❌ Missing required columns in GVT data: {missing_columns}")
    st.write("Available columns:", list(GVTdata.columns))
    st.stop()

# Calculate week number from SSL ATA date
GVTdata['SSL ATA'] = pd.to_datetime(GVTdata['SSL ATA'], errors='coerce')
GVTdata['Week Number'] = GVTdata['SSL ATA'].dt.isocalendar().week

# Remove rows where SSL ATA is null (couldn't be converted to date)
GVTdata = GVTdata.dropna(subset=['SSL ATA'])

# Process columns for lookup creation
# Add "US" prefix to Discharged Port
GVTdata['Port_Processed'] = 'US' + GVTdata['Discharged Port'].astype(str)

# Take first 4 characters of Facility
GVTdata['Facility_Processed'] = GVTdata['Facility'].astype(str).str[:4]

# Create lookup key in GVT data (SCAC + Port + FC)
GVTdata['Lookup'] = (GVTdata['Dray SCAC(FL)'].astype(str) + 
                     GVTdata['Port_Processed'].astype(str) + 
                     GVTdata['Facility_Processed'].astype(str))

# Check if Lookup already exists in Rate data
if 'Lookup' in Ratedata.columns:
    st.success("✅ Lookup column found in Rate data")
else:
    st.error("❌ Lookup column not found in Rate data. Please ensure your rate data has a 'Lookup' column.")
    st.write("Available rate data columns:", list(Ratedata.columns))
    st.stop()

# Create Lane column in Rate data (Port + FC concatenation)
# First, identify Port and FC columns in Rate data
port_col_rate = None
fc_col_rate = None

for col in Ratedata.columns:
    if 'PORT' in col.upper():
        port_col_rate = col
    if 'FC' in col.upper() or 'FACILITY' in col.upper():
        fc_col_rate = col

if port_col_rate and fc_col_rate:
    Ratedata['Lane'] = Ratedata[port_col_rate].astype(str) + Ratedata[fc_col_rate].astype(str)
    st.success(f"✅ Created Lane column using {port_col_rate} + {fc_col_rate}")
else:
    st.error("❌ Cannot create Lane column. Port or FC column not found in rate data.")
    st.write(f"Available rate data columns: {list(Ratedata.columns)}")
    st.stop()

# Create corresponding Lane column in GVT data
GVTdata['Lane'] = GVTdata['Port_Processed'].astype(str) + GVTdata['Facility_Processed'].astype(str)

# Check if Base Rate column exists
rate_col = None
for col in Ratedata.columns:
    if 'RATE' in col.upper() or 'COST' in col.upper():
        rate_col = col
        break

if rate_col is None:
    st.error("❌ Rate column not found in rate data. Available columns:")
    st.write(list(Ratedata.columns))
    st.stop()
else:
    st.success(f"✅ Using rate column: {rate_col}")
    if rate_col != 'Base Rate':
        Ratedata = Ratedata.rename(columns={rate_col: 'Base Rate'})

# Find cheapest rate per lane (instead of per port)
st.markdown('<div class="section-header">📊 Lane Analysis</div>', unsafe_allow_html=True)
lane_analysis = Ratedata.groupby('Lane').agg({
    'Base Rate': ['count', 'min', 'max', 'mean'],
    'Lookup': 'count'
}).round(2)
lane_analysis.columns = ['Rate_Count', 'Min_Rate', 'Max_Rate', 'Avg_Rate', 'Lookup_Count']
lane_analysis = lane_analysis.reset_index()

# Show lanes with multiple rates
duplicate_lanes = lane_analysis[lane_analysis['Rate_Count'] > 1]
if len(duplicate_lanes) > 0:
    st.write("🔍 **Lanes with multiple rates:**")
    st.dataframe(duplicate_lanes, use_container_width=True)
else:
    st.info("ℹ️ No duplicate lanes found")

# Get cheapest rate per lane
cheapest_rates_by_lane = Ratedata.groupby('Lane')['Base Rate'].min().reset_index()
cheapest_rates_by_lane = cheapest_rates_by_lane.rename(columns={'Base Rate': 'Cheapest Base Rate'})

# Update lane_count to include Lane column - MOVED BEFORE THE MERGE
lane_count = GVTdata.groupby(['Week Number', 'Discharged Port', 'Dray SCAC(FL)', 'Facility', 'Lane', 'Lookup']).size().reset_index(name='Container Count')

# Merge with rate data first
merged_data = pd.merge(lane_count, Ratedata, how='left', on='Lookup', suffixes=('', '_rate'))

# Handle potential Lane column conflicts
if 'Lane' not in merged_data.columns:
    if 'Lane_rate' in merged_data.columns:
        # Use the Lane from rate data if it exists
        merged_data['Lane'] = merged_data['Lane_rate']
    else:
        # Recreate Lane column from the original data
        merged_data['Lane'] = merged_data['Discharged Port'].apply(lambda x: 'US' + str(x)) + merged_data['Facility'].astype(str).str[:4]

# Now merge with cheapest rates by lane - Lane column should exist now
merged_data = pd.merge(merged_data, cheapest_rates_by_lane, how='left', on='Lane')

# Merge with performance data (only if available)
if has_performance and len(performance_clean) > 0:
    merged_data = pd.merge(
        merged_data, 
        performance_clean, 
        left_on=['Dray SCAC(FL)', 'Week Number'], 
        right_on=['Carrier', 'Week Number'], 
        how='left'
    )

# Remove rows where Base Rate is null (no matching rate found)
merged_data = merged_data.dropna(subset=['Base Rate'])

merged_data['Total Rate'] = merged_data['Base Rate'] * merged_data['Container Count']

# Calculate potential savings (now based on cheapest lane rate)
merged_data['Cheapest Total Rate'] = merged_data['Cheapest Base Rate'] * merged_data['Container Count']
merged_data['Potential Savings'] = merged_data['Total Rate'] - merged_data['Cheapest Total Rate']

# Create comprehensive table with all data
comprehensive_data = merged_data.copy()

# Add additional calculated columns
comprehensive_data['Rate Difference'] = comprehensive_data['Base Rate'] - comprehensive_data['Cheapest Base Rate']
comprehensive_data['Savings Percentage'] = (comprehensive_data['Potential Savings'] / comprehensive_data['Total Rate'] * 100).round(2)

# FILTERS SECTION
st.markdown('<div class="section-header">🔍 Filters</div>', unsafe_allow_html=True)

# Initialize session state for filters if not exists
if 'filter_ports' not in st.session_state:
    st.session_state.filter_ports = []
if 'filter_fcs' not in st.session_state:
    st.session_state.filter_fcs = []
if 'filter_weeks' not in st.session_state:
    st.session_state.filter_weeks = []
if 'filter_scacs' not in st.session_state:
    st.session_state.filter_scacs = []

# Add search functionality
st.markdown("**Search and Filter Options:**")
search_col1, search_col2 = st.columns([1, 3])

with search_col1:
    apply_filters = st.button("🔍 Apply Filters", type="primary", use_container_width=True)

with search_col2:
    st.write("*Select your filters below and click 'Apply Filters' to update the results*")

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Port filter with search
    st.markdown("**🚢 Ports:**")
    port_search = st.text_input("Search ports...", key="port_search", placeholder="Type to search ports")
    
    port_options = sorted(list(comprehensive_data['Discharged Port'].unique()))
    if port_search:
        port_options = [port for port in port_options if port_search.lower() in str(port).lower()]
    
    # Use session state as default without triggering rerun
    port_display_options = ['All'] + port_options
    
    # Get current selection without triggering rerun
    current_port_selection = st.multiselect(
        "Select Port(s)", 
        port_display_options, 
        default=['All'] if not st.session_state.filter_ports else st.session_state.filter_ports,
        key="port_multiselect",
        on_change=None  # Prevent auto-rerun
    )

with col2:
    # FC filter with search
    st.markdown("**🏭 Facilities:**")
    fc_search = st.text_input("Search facilities...", key="fc_search", placeholder="Type to search facilities")
    
    fc_options = sorted(list(comprehensive_data['Facility'].str[:4].unique()))
    if fc_search:
        fc_options = [fc for fc in fc_options if fc_search.lower() in str(fc).lower()]
    
    fc_display_options = ['All'] + fc_options
    
    current_fc_selection = st.multiselect(
        "Select FC (Facility)", 
        fc_display_options, 
        default=['All'] if not st.session_state.filter_fcs else st.session_state.filter_fcs,
        key="fc_multiselect",
        on_change=None
    )

with col3:
    # Week filter with search
    st.markdown("**📅 Week Numbers:**")
    week_search = st.text_input("Search weeks...", key="week_search", placeholder="Type to search weeks")
    
    week_options = sorted(list(comprehensive_data['Week Number'].unique()))
    if week_search:
        week_options = [week for week in week_options if week_search.lower() in str(week).lower()]
    
    week_display_options = ['All'] + [str(week) for week in week_options]
    
    current_week_selection = st.multiselect(
        "Select Week Number(s)", 
        week_display_options, 
        default=['All'] if not st.session_state.filter_weeks else [str(w) for w in st.session_state.filter_weeks],
        key="week_multiselect",
        on_change=None
    )

with col4:
    # SCAC filter with search
    st.markdown("**🚛 SCACs:**")
    scac_search = st.text_input("Search SCACs...", key="scac_search", placeholder="Type to search SCACs")
    
    scac_options = sorted(list(comprehensive_data['Dray SCAC(FL)'].unique()))
    if scac_search:
        scac_options = [scac for scac in scac_options if scac_search.lower() in str(scac).lower()]
    
    scac_display_options = ['All'] + scac_options
    
    current_scac_selection = st.multiselect(
        "Select Dray SCAC(FL)", 
        scac_display_options, 
        default=['All'] if not st.session_state.filter_scacs else st.session_state.filter_scacs,
        key="scac_multiselect",
        on_change=None
    )

# Clear filters button
if st.button("🗑️ Clear All Filters", use_container_width=True):
    st.session_state.filter_ports = []
    st.session_state.filter_fcs = []
    st.session_state.filter_weeks = []
    st.session_state.filter_scacs = []
    st.rerun()

# Apply filters when button is clicked
if apply_filters:
    # Update session state with current selections
    st.session_state.filter_ports = [p for p in current_port_selection if p != 'All']
    st.session_state.filter_fcs = [f for f in current_fc_selection if f != 'All']
    st.session_state.filter_weeks = [int(w) for w in current_week_selection if w != 'All']
    st.session_state.filter_scacs = [s for s in current_scac_selection if s != 'All']
    
    st.success("✅ Filters applied successfully!")
    st.rerun()

# Apply filters to data
filtered_data = comprehensive_data.copy()

# Apply port filter
if st.session_state.filter_ports:
    filtered_data = filtered_data[filtered_data['Discharged Port'].isin(st.session_state.filter_ports)]
    display_ports = st.session_state.filter_ports
else:
    display_ports = "All Ports"

# Apply FC filter
if st.session_state.filter_fcs:
    fc_mask = filtered_data['Facility'].str[:4].isin(st.session_state.filter_fcs)
    filtered_data = filtered_data[fc_mask]
    display_fcs = st.session_state.filter_fcs
else:
    display_fcs = "All FCs"

# Apply week filter
if st.session_state.filter_weeks:
    filtered_data = filtered_data[filtered_data['Week Number'].isin(st.session_state.filter_weeks)]
    display_weeks = st.session_state.filter_weeks
else:
    display_weeks = "All Weeks"

# Apply SCAC filter
if st.session_state.filter_scacs:
    filtered_data = filtered_data[filtered_data['Dray SCAC(FL)'].isin(st.session_state.filter_scacs)]
    display_scacs = st.session_state.filter_scacs
else:
    display_scacs = "All SCACs"

final_filtered_data = filtered_data

# Show summary for selected data
st.markdown('<div class="section-header">📋 Selection Summary</div>', unsafe_allow_html=True)
summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.write(f"**Ports:** {display_ports}")
    st.write(f"**FCs (Facilities):** {display_fcs}")

with summary_col2:
    st.write(f"**Week Numbers:** {display_weeks}")
    st.write(f"**SCACs:** {display_scacs}")

st.write(f"**Total Records:** {len(final_filtered_data):,}")

# Calculate enhanced metrics for filtered data
if len(final_filtered_data) > 0:
    # Current metrics
    total_cost = final_filtered_data['Total Rate'].sum()
    cheapest_total_cost = final_filtered_data['Cheapest Total Rate'].sum()
    total_potential_savings = final_filtered_data['Potential Savings'].sum()
    avg_rate = final_filtered_data['Base Rate'].mean()
    avg_cheapest_rate = final_filtered_data['Cheapest Base Rate'].mean()
    
    # NEW METRIC 1: Highest Performance Cost - Using performance calculator
    highest_perf_cost = 0
    if 'Performance_Score' in final_filtered_data.columns:
        highest_perf_cost, _ = calculate_performance_optimization(final_filtered_data)
    
    # NEW METRIC 2: Linear Programming Optimized Cost (placeholder calculation)
    # This would be calculated from the LP optimization results if available
    lp_optimized_cost = 0
    if 'Performance_Score' in final_filtered_data.columns:
        # Simplified LP cost calculation - using balanced approach (70% cost, 30% performance)
        lp_selections = []
        for (lane, week), group in final_filtered_data.groupby(['Lane', 'Week Number']):
            if len(group) > 1 and not group['Performance_Score'].isna().all():
                # Normalize cost and performance for this group
                group_copy = group.copy()
                max_rate = group_copy['Base Rate'].max()
                min_rate = group_copy['Base Rate'].min()
                max_perf = group_copy['Performance_Score'].max()
                min_perf = group_copy['Performance_Score'].min()
                
                if max_rate != min_rate and max_perf != min_perf:
                    group_copy['norm_cost'] = (group_copy['Base Rate'] - min_rate) / (max_rate - min_rate)
                    group_copy['norm_perf'] = (group_copy['Performance_Score'] - min_perf) / (max_perf - min_perf)
                    
                    # LP objective: minimize (0.7 * cost - 0.3 * performance)
                    group_copy['lp_score'] = 0.7 * group_copy['norm_cost'] - 0.3 * group_copy['norm_perf']
                    best_lp_idx = group_copy['lp_score'].idxmin()
                    best_lp_row = group_copy.loc[best_lp_idx]
                else:
                    # If no variation, pick cheapest
                    best_lp_row = group.loc[group['Base Rate'].idxmin()]
                
                lp_selections.append({
                    'Lane': lane,
                    'Week Number': week,
                    'Container Count': best_lp_row['Container Count'],
                    'Base Rate': best_lp_row['Base Rate']
                })
            else:
                # Single option or no performance data
                lp_selections.append({
                    'Lane': lane,
                    'Week Number': week,
                    'Container Count': group['Container Count'].iloc[0],
                    'Base Rate': group['Base Rate'].iloc[0]
                })
        
        if lp_selections:
            lp_df = pd.DataFrame(lp_selections)
            lp_optimized_cost = (lp_df['Base Rate'] * lp_df['Container Count']).sum()
    
    # Display enhanced metrics
    st.markdown('<div class="section-header">📈 Current Selection Metrics</div>', unsafe_allow_html=True)
    
    # First row of metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💰 Total Current Cost", f"${total_cost:,.2f}")
        st.metric("📊 Average Current Rate", f"${avg_rate:.2f}")
    
    with col2:
        st.metric("💵 Total Cheapest Cost", f"${cheapest_total_cost:,.2f}")
        st.metric("📉 Average Cheapest Rate", f"${avg_cheapest_rate:.2f}")
    
    with col3:
        st.metric("💡 Total Potential Savings", f"${total_potential_savings:,.2f}")
        savings_pct = (total_potential_savings/total_cost*100) if total_cost > 0 else 0
        st.metric("📊 Savings Percentage", f"{savings_pct:.1f}%")

    # Second row - NEW METRICS
    if highest_perf_cost > 0 or lp_optimized_cost > 0:
        st.markdown("**🎯 Alternative Optimization Strategies:**")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            if highest_perf_cost > 0:
                hp_diff = highest_perf_cost - total_cost
                hp_savings_pct = ((total_cost - highest_perf_cost) / total_cost * 100) if total_cost > 0 else 0
                st.metric(
                    "🏆 Highest Performance Cost", 
                    f"${highest_perf_cost:,.2f}",
                    f"{hp_savings_pct:+.1f}%" if hp_diff != 0 else "Same as current"
                )
            else:
                st.metric("🏆 Highest Performance Cost", "N/A", "No performance data")
        
        with col5:
            if lp_optimized_cost > 0:
                lp_diff = lp_optimized_cost - total_cost
                lp_savings_pct = ((total_cost - lp_optimized_cost) / total_cost * 100) if total_cost > 0 else 0
                st.metric(
                    "🧮 LP Optimized Cost", 
                    f"${lp_optimized_cost:,.2f}",
                    f"{lp_savings_pct:+.1f}%" if lp_diff != 0 else "Same as current"
                )
            else:
                st.metric("🧮 LP Optimized Cost", "N/A", "No optimization possible")
        
        with col6:
            # Show best strategy
            strategies = [
                ("Current", total_cost),
                ("Cheapest", cheapest_total_cost),
                ("Highest Perf", highest_perf_cost if highest_perf_cost > 0 else float('inf')),
                ("LP Optimized", lp_optimized_cost if lp_optimized_cost > 0 else float('inf'))
            ]
            best_strategy = min(strategies, key=lambda x: x[1])
            st.metric(
                "🎯 Best Strategy", 
                best_strategy[0],
                f"${best_strategy[1]:,.2f}"
            )

    # Third row - Additional metrics
    col7, col8, col9 = st.columns(3)
    with col7:
        st.metric("🛣️ Unique Lanes", f"{final_filtered_data['Lane'].nunique()}")
    with col8:
        st.metric("🚛 Unique SCACs", f"{final_filtered_data['Dray SCAC(FL)'].nunique()}")
    with col9:
        st.metric("📦 Total Container Count", f"{final_filtered_data['Container Count'].sum():,}")

# Show aggregate metrics
if len(final_filtered_data) > 0:
    total_cost = final_filtered_data['Total Rate'].sum()
    cheapest_total_cost = final_filtered_data['Cheapest Total Rate'].sum()
    total_potential_savings = final_filtered_data['Potential Savings'].sum()
    avg_rate = final_filtered_data['Base Rate'].mean()
    avg_cheapest_rate = final_filtered_data['Cheapest Base Rate'].mean()
    
    st.markdown('<div class="section-header">📈 Current Selection Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💰 Total Current Cost", f"${total_cost:,.2f}")
        st.metric("📊 Average Current Rate", f"${avg_rate:.2f}")
    
    with col2:
        st.metric("💵 Total Cheapest Cost", f"${cheapest_total_cost:,.2f}")
        st.metric("📉 Average Cheapest Rate", f"${avg_cheapest_rate:.2f}")
    
    with col3:
        st.metric("💡 Total Potential Savings", f"${total_potential_savings:,.2f}")
        st.metric("📊 Savings Percentage", f"{(total_potential_savings/total_cost*100):.1f}%")

    # Additional metrics row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🛣️ Unique Lanes", f"{final_filtered_data['Lane'].nunique()}")
    with col2:
        st.metric("🚛 Unique SCACs", f"{final_filtered_data['Dray SCAC(FL)'].nunique()}")
    with col3:
        st.metric("📦 Total Container Count", f"{final_filtered_data['Container Count'].sum():,}")



    # New Detailed Table with Performance
    st.markdown('<div class="section-header">📋 Detailed Analysis Table</div>', unsafe_allow_html=True)
    
    detailed_columns = ['Discharged Port', 'Dray SCAC(FL)', 'Lane', 'Facility', 
                       'Total Rate', 'Cheapest Total Rate', 'Potential Savings', 
                       'Base Rate', 'Cheapest Base Rate', 'Savings Percentage', 
                       'Week Number', 'Container Count']
    
    # Add performance column if available
    if 'Performance_Score' in final_filtered_data.columns:
        detailed_columns.append('Performance_Score')
    
    detailed_table = final_filtered_data[detailed_columns].copy()
    
    # Rename performance column for display
    if 'Performance_Score' in detailed_table.columns:
        detailed_table = detailed_table.rename(columns={'Performance_Score': 'Carrier Performance'})
    
    # Sort by potential savings (highest first)
    detailed_table = detailed_table.sort_values('Potential Savings', ascending=False)
    
    st.dataframe(detailed_table, use_container_width=True)

    # Summary tables
    st.markdown('<div class="section-header">📊 Summary Tables</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚢 By Port", "🚛 By SCAC", "🛣️ By Lane", "🏭 By Facility", "📅 By Week"])
    
    with tab1:
        port_agg = {
            'Container Count': 'sum',
            'Total Rate': 'sum',
            'Cheapest Total Rate': 'sum',
            'Potential Savings': 'sum',
            'Base Rate': 'mean',
            'Cheapest Base Rate': 'mean'
        }
        if 'Performance_Score' in final_filtered_data.columns:
            port_agg['Performance_Score'] = 'mean'
            
        port_summary = final_filtered_data.groupby('Discharged Port').agg(port_agg).round(2)
        port_summary['Savings %'] = (port_summary['Potential Savings'] / port_summary['Total Rate'] * 100).round(1)
        
        if 'Performance_Score' in port_summary.columns:
            port_summary = port_summary.rename(columns={'Performance_Score': 'Avg Carrier Performance'})
            
        st.dataframe(port_summary, use_container_width=True)
    
    with tab2:
        scac_agg = {
            'Container Count': 'sum',
            'Total Rate': 'sum',
            'Cheapest Total Rate': 'sum',
            'Potential Savings': 'sum',
            'Base Rate': 'mean',
            'Cheapest Base Rate': 'mean'
        }
        if 'Performance_Score' in final_filtered_data.columns:
            scac_agg['Performance_Score'] = 'mean'
            
        scac_summary = final_filtered_data.groupby('Dray SCAC(FL)').agg(scac_agg).round(2)
        scac_summary['Savings %'] = (scac_summary['Potential Savings'] / scac_summary['Total Rate'] * 100).round(1)
        
        if 'Performance_Score' in scac_summary.columns:
            scac_summary = scac_summary.rename(columns={'Performance_Score': 'Avg Carrier Performance'})
            
        st.dataframe(scac_summary, use_container_width=True)
    
    with tab3:
        lane_agg = {
            'Container Count': 'sum',
            'Total Rate': 'sum',
            'Cheapest Total Rate': 'sum',
            'Potential Savings': 'sum',
            'Base Rate': 'mean',
            'Cheapest Base Rate': 'mean'
        }
        if 'Performance_Score' in final_filtered_data.columns:
            lane_agg['Performance_Score'] = 'mean'
            
        lane_summary = final_filtered_data.groupby('Lane').agg(lane_agg).round(2)
        lane_summary['Savings %'] = (lane_summary['Potential Savings'] / lane_summary['Total Rate'] * 100).round(1)
        
        if 'Performance_Score' in lane_summary.columns:
            lane_summary = lane_summary.rename(columns={'Performance_Score': 'Avg Carrier Performance'})
            
        st.dataframe(lane_summary, use_container_width=True)
    
    with tab4:
        facility_agg = {
            'Container Count': 'sum',
            'Total Rate': 'sum',
            'Cheapest Total Rate': 'sum',
            'Potential Savings': 'sum',
            'Base Rate': 'mean',
            'Cheapest Base Rate': 'mean'
        }
        if 'Performance_Score' in final_filtered_data.columns:
            facility_agg['Performance_Score'] = 'mean'
            
        facility_summary = final_filtered_data.groupby('Facility').agg(facility_agg).round(2)
        facility_summary['Savings %'] = (facility_summary['Potential Savings'] / facility_summary['Total Rate'] * 100).round(1)
        
        if 'Performance_Score' in facility_summary.columns:
            facility_summary = facility_summary.rename(columns={'Performance_Score': 'Avg Carrier Performance'})
            
        st.dataframe(facility_summary, use_container_width=True)
    
    with tab5:
        week_agg = {
            'Container Count': 'sum',
            'Total Rate': 'sum',
            'Cheapest Total Rate': 'sum',
            'Potential Savings': 'sum',
            'Base Rate': 'mean',
            'Cheapest Base Rate': 'mean'
        }
        if 'Performance_Score' in final_filtered_data.columns:
            week_agg['Performance_Score'] = 'mean'
            
        week_summary = final_filtered_data.groupby('Week Number').agg(week_agg).round(2)
        week_summary['Savings %'] = (week_summary['Potential Savings'] / week_summary['Total Rate'] * 100).round(1)
        
        if 'Performance_Score' in week_summary.columns:
            week_summary = week_summary.rename(columns={'Performance_Score': 'Avg Carrier Performance'})
            
        st.dataframe(week_summary, use_container_width=True)
    
    # Top savings opportunities with performance
    st.markdown('<div class="section-header">🎯 Top Savings Opportunities</div>', unsafe_allow_html=True)
    top_savings_columns = ['Lane', 'Dray SCAC(FL)', 'Week Number', 'Container Count', 'Base Rate', 'Cheapest Base Rate', 'Potential Savings', 'Savings Percentage']
    
    if 'Performance_Score' in final_filtered_data.columns:
        top_savings_columns.append('Performance_Score')
        
    top_savings = final_filtered_data.nlargest(10, 'Potential Savings')[top_savings_columns]
    
    if 'Performance_Score' in top_savings.columns:
        top_savings = top_savings.rename(columns={'Performance_Score': 'Carrier Performance'})
        
    st.dataframe(top_savings, use_container_width=True)

    # Comprehensive data table
    st.markdown('<div class="section-header">📄 Complete Data Export</div>', unsafe_allow_html=True)
    if st.checkbox("🔍 Show Complete Data Table"):
        st.dataframe(final_filtered_data, use_container_width=True)

else:
    st.warning("⚠️ No data matches your selection.")

# Option to download filtered data
if len(final_filtered_data) > 0:
    csv = final_filtered_data.to_csv(index=False)
    st.download_button(
        label="📥 Download comprehensive filtered data as CSV",
        data=csv,
        file_name='comprehensive_carrier_data.csv',
        mime='text/csv',
        use_container_width=True
    )

# Moved Calculation Logic to the bottom
st.markdown('<div class="section-header">💡 Calculation Logic</div>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
<strong>Total Rate Calculation:</strong><br>
<code>Total Rate = Base Rate × Container Count</code><br><br>
<strong>Where:</strong><br>
• <strong>Base Rate:</strong> The per-container rate charged by the carrier for a specific SCAC-Port-Facility combination<br>
• <strong>Container Count:</strong> The number of containers shipped on that specific route during the selected time period<br><br>
<strong>Example:</strong> If Base Rate = $500 and Container Count = 10, then Total Rate = $5,000<br><br>

<strong>Cheapest Rate Calculation:</strong><br>
<code>Cheapest Base Rate = MIN(Base Rate) for each Lane</code><br><br>
<strong>How it works:</strong><br>
• <strong>Lane:</strong> A unique combination of Port + Facility (e.g., USLAX + IUSF)<br>
• <strong>Process:</strong> For each lane, the system finds all available carriers (SCACs) and identifies the one with the lowest rate<br>
• <strong>Cheapest Total Rate:</strong> Cheapest Base Rate × Container Count<br><br>

<strong>Potential Savings Calculation:</strong><br>
<code>Potential Savings = Total Rate - Cheapest Total Rate</code><br><br>
<strong>How it works:</strong><br>
• Shows the dollar amount that could be saved by switching to the cheapest available carrier for each lane<br>
• Represents the difference between what you're currently paying vs. the lowest available rate<br><br>

<strong>Week Number Calculation:</strong><br>
<code>Week Number = ISO Week Number from SSL ATA Date</code><br><br>
<strong>How it works:</strong><br>
• Extracted from the SSL ATA (Actual Time of Arrival) date in the GVT data<br>
• Uses ISO 8601 standard where weeks start on Monday and week 1 contains January 4th<br>
• Allows analysis of shipping patterns and costs by week<br><br>

<strong>Savings Percentage Calculation:</strong><br>
<code>Savings % = (Potential Savings ÷ Total Rate) × 100</code><br><br>
<strong>How it works:</strong><br>
• Shows what percentage of current costs could be saved by switching to cheapest rates<br>
• Higher percentages indicate greater optimization opportunities<br><br>

<strong>Performance Data Integration:</strong><br>
<code>Performance Score matched by Carrier (SCAC) + Week Number</code><br><br>
<strong>How it works:</strong><br>
• Performance data is matched when the Carrier in performance data equals the Dray SCAC(FL) in GVT data<br>
• Week numbers from both datasets must match exactly<br>
• Performance scores are displayed as percentages and averaged in summary tables<br>
• Allows evaluation of cost savings opportunities alongside carrier performance metrics<br><br>

<strong>Example:</strong> For lane USLAXIUSF:<br>
- SCAC A charges $500 per container<br>
- SCAC B charges $450 per container<br>
- SCAC C charges $475 per container<br>
- Cheapest Base Rate = $450 (SCAC B)<br>
- If you have 10 containers:<br>
  • Total Rate = $500 × 10 = $5,000<br>
  • Cheapest Total Rate = $450 × 10 = $4,500<br>
  • Potential Savings = $5,000 - $4,500 = $500<br>
  • Savings % = ($500 ÷ $5,000) × 100 = 10%<br>
  • Performance Score = 82.1% (if SCAC A has 82.1% performance for that week)
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("*Dashboard created for Carrier Tender Optimization Analysis*")

# Debug performance merge - Add this after the merge operations and before filters
with st.expander("🔍 Debug Performance Merge (Click to expand)"):
    # Check if performance data exists and was merged
    st.write(f"**Has performance data:** {has_performance}")
    if has_performance:
        st.write(f"**Performance records available:** {len(performance_clean)}")
        
        # Show sample performance data
        if st.checkbox("Show Sample Performance Data"):
            st.dataframe(performance_clean.head())
        
        # Show unique carriers and weeks in performance data
        st.write(f"**Unique carriers in performance data:** {sorted(performance_clean['Carrier'].unique())}")
        st.write(f"**Unique weeks in performance data:** {sorted(performance_clean['Week Number'].unique())}")

    # Check merged data
    st.write(f"**Performance_Score column exists in merged data:** {'Performance_Score' in merged_data.columns}")
    
    if 'Performance_Score' in merged_data.columns:
        st.write(f"**Performance records with non-null values:** {merged_data['Performance_Score'].notna().sum()}")
        
        # Show sample of merged data with performance
        if st.checkbox("Show Sample Merged Data"):
            merged_with_perf = merged_data[merged_data['Performance_Score'].notna()]
            if len(merged_with_perf) > 0:
                st.dataframe(merged_with_perf[['Dray SCAC(FL)', 'Week Number', 'Performance_Score']].head())

# Linear Programming Optimization Section
st.markdown('<div class="section-header">🧮 Linear Programming Optimization</div>', unsafe_allow_html=True)

if 'Performance_Score' in final_filtered_data.columns and len(final_filtered_data) > 0:
    st.markdown("**Find the optimal balance between cost savings and carrier performance using linear programming.**")
    
    # Check if we have performance data in filtered results
    perf_data_available = final_filtered_data['Performance_Score'].notna().sum()
    st.write(f"**Records with performance data:** {perf_data_available} out of {len(final_filtered_data)}")
    
    if perf_data_available == 0:
        st.warning("⚠️ No performance data found in filtered results. The optimization requires performance scores.")
        st.info("Try adjusting your filters to include data with performance scores, or check the debug section above to see why performance data isn't being merged.")
    else:
        # DEBUG: Show performance score distribution
        with st.expander("🔍 Performance Score Analysis"):
            perf_records = final_filtered_data.dropna(subset=['Performance_Score'])
            st.write(f"**Performance Score Statistics:**")
            st.write(f"- Minimum: {perf_records['Performance_Score'].min():.1f}%")
            st.write(f"- Maximum: {perf_records['Performance_Score'].max():.1f}%")
            st.write(f"- Average: {perf_records['Performance_Score'].mean():.1f}%")
            st.write(f"- Median: {perf_records['Performance_Score'].median():.1f}%")
            
            # Show distribution
            st.write("**Performance Score Distribution:**")
            perf_dist = perf_records['Performance_Score'].value_counts().sort_index()
            st.write(perf_dist)
            
            # Show sample records with performance
            st.write("**Sample records with performance data:**")
            sample_cols = ['Dray SCAC(FL)', 'Week Number', 'Performance_Score', 'Base Rate', 'Container Count']
            st.dataframe(perf_records[sample_cols].head(10))
            
            # Show unique performance scores
            unique_scores = sorted(perf_records['Performance_Score'].unique())
            st.write(f"**Unique Performance Scores:** {unique_scores}")
        
        # Optimization parameters
        opt_col1, opt_col2, opt_col3 = st.columns(3)
        
        with opt_col1:
            cost_weight = st.slider(
                "Cost Weight (importance)", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.7, 
                step=0.1,
                help="Higher values prioritize cost savings"
            )
        
        with opt_col2:
            performance_weight = st.slider(
                "Performance Weight (importance)", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.3, 
                step=0.1,
                help="Higher values prioritize carrier performance"
            )
        
        with opt_col3:
            # Get actual performance range for better default
            perf_records = final_filtered_data.dropna(subset=['Performance_Score'])
            min_perf = float(perf_records['Performance_Score'].min()) if len(perf_records) > 0 else 0.0
            max_perf = float(perf_records['Performance_Score'].max()) if len(perf_records) > 0 else 1.0
            
            # Check if scores are in decimal format (0-1) or percentage format (0-100)
            if max_perf <= 1.0:
                # Decimal format (0.7 = 70%)
                slider_min = 0.0
                slider_max = 1.0
                default_threshold = max(min_perf - 0.05, 0.0)
                step_size = 0.01
                
                min_performance_threshold = st.slider(
                    f"Minimum Performance Threshold - Range: {min_perf*100:.1f}% to {max_perf*100:.1f}%", 
                    min_value=slider_min, 
                    max_value=slider_max, 
                    value=default_threshold, 
                    step=step_size,
                    format="%.2f",
                    help=f"Carriers below this performance will be excluded. Current data range: {min_perf*100:.1f}% - {max_perf*100:.1f}% (showing as decimal 0-1)"
                )
                
                # Display the threshold as percentage for clarity
                st.write(f"**Selected threshold:** {min_performance_threshold*100:.1f}%")
                
            else:
                # Percentage format (70 = 70%)
                default_threshold = max(min_perf - 5, 0.0)
                
                min_performance_threshold = st.slider(
                    f"Minimum Performance Threshold (%) - Range: {min_perf:.1f}% to {max_perf:.1f}%", 
                    min_value=0.0, 
                    max_value=100.0, 
                    value=default_threshold, 
                    step=1.0,
                    help=f"Carriers below this performance will be excluded. Current data range: {min_perf:.1f}% - {max_perf:.1f}%"
                )
        
        # Show preview of data that will be used
        preview_data = final_filtered_data.dropna(subset=['Performance_Score'])
        preview_data = preview_data[preview_data['Performance_Score'] >= min_performance_threshold]
        
        st.write(f"**Preview: {len(preview_data)} records meet performance threshold of {min_performance_threshold}%**")
        
        # Show threshold impact
        if len(preview_data) == 0:
            st.error(f"❌ No records meet the {min_performance_threshold}% threshold. Minimum performance in your data is {min_perf:.1f}%")
            st.info(f"💡 Suggestion: Set threshold to {min_perf - 1:.1f}% or lower to include data")
        else:
            # Show sample of data to be optimized
            preview_cols = ['Lane', 'Dray SCAC(FL)', 'Week Number', 'Base Rate', 'Performance_Score', 'Container Count']
            st.write("**Sample data for optimization:**")
            st.dataframe(preview_data[preview_cols].head(10))
            
            # Show lane-week combinations
            lane_week_combos = preview_data.groupby(['Lane', 'Week Number']).agg({
                'Dray SCAC(FL)': 'count',
                'Base Rate': ['min', 'max'],
                'Performance_Score': ['min', 'max']
            }).round(2)
            
            # Flatten column names
            lane_week_combos.columns = ['Carrier_Count', 'Min_Rate', 'Max_Rate', 'Min_Perf', 'Max_Perf']
            lane_week_combos = lane_week_combos.reset_index()
            
            st.write(f"**Lane-Week combinations to optimize:** {len(lane_week_combos)}")
            
            # Show only combinations with multiple carriers
            multi_carrier = lane_week_combos[lane_week_combos['Carrier_Count'] > 1]
            st.write(f"**Lane-Week combinations with multiple carriers (optimizable):** {len(multi_carrier)}")
            
            if len(multi_carrier) > 0:
                st.dataframe(multi_carrier.head(10))
            else:
                st.warning("⚠️ No Lane-Week combinations have multiple carriers. Optimization requires choices.")
                st.write("**All Lane-Week combinations (single carrier each):**")
                st.dataframe(lane_week_combos.head(10))
        
        if st.button("🚀 Run Optimization", type="primary"):
            with st.spinner("Running linear programming optimization..."):
                
                # Prepare data for optimization
                opt_data = final_filtered_data.copy()
                
                # Remove records without performance data
                opt_data = opt_data.dropna(subset=['Performance_Score'])
                st.write(f"After removing records without performance: {len(opt_data)} records")
                
                # Filter by minimum performance threshold
                opt_data = opt_data[opt_data['Performance_Score'] >= min_performance_threshold]
                st.write(f"After performance threshold filter: {len(opt_data)} records")
                
                if len(opt_data) == 0:
                    st.error("❌ No data meets the performance threshold. Try lowering the minimum performance requirement.")
                else:
                    # Check if we have multiple carriers per lane-week combination
                    lane_week_counts = opt_data.groupby(['Lane', 'Week Number']).size()
                    multi_carrier_lanes = lane_week_counts[lane_week_counts > 1]
                    
                    st.write(f"**Lane-Week combinations with multiple carriers:** {len(multi_carrier_lanes)}")
                    st.write(f"**Lane-Week combinations with single carrier:** {len(lane_week_counts) - len(multi_carrier_lanes)}")
                    
                    if len(multi_carrier_lanes) == 0:
                        st.warning("⚠️ No lane-week combinations have multiple carrier options. Optimization requires choices between carriers.")
                        st.info("Current data shows only one carrier per lane-week combination, so no optimization is possible.")
                        
                        # Show the single-carrier summary
                        single_carrier_summary = opt_data.groupby(['Lane', 'Week Number']).agg({
                            'Dray SCAC(FL)': 'first',
                            'Base Rate': 'first', 
                            'Performance_Score': 'first',
                            'Container Count': 'sum',
                            'Total Rate': 'sum'
                        }).reset_index()
                        
                        single_carrier_summary.columns = ['Lane', 'Week Number', 'Only Available SCAC', 'Base Rate', 'Performance Score', 'Container Count', 'Total Cost']
                        st.dataframe(single_carrier_summary)
                        
                    else:
                        try:
                            # Show which lane-week combinations have multiple options
                            st.write("**Lane-Week combinations with optimization opportunities:**")
                            multi_options = opt_data[opt_data.groupby(['Lane', 'Week Number'])['Lane'].transform('count') > 1]
                            multi_summary = multi_options.groupby(['Lane', 'Week Number']).agg({
                                'Dray SCAC(FL)': lambda x: ', '.join(sorted(x)),
                                'Base Rate': ['min', 'max', 'count'],
                                'Performance_Score': ['min', 'max'],
                                'Container Count': 'first'
                            }).round(2)
                            
                            # Flatten column names
                            multi_summary.columns = ['Available_SCACs', 'Min_Rate', 'Max_Rate', 'SCAC_Count', 'Min_Perf', 'Max_Perf', 'Containers']
                            multi_summary = multi_summary.reset_index()
                            st.dataframe(multi_summary)
                            
                            # Prepare data for optimization
                            lane_options = opt_data[['Lane', 'Week Number', 'Dray SCAC(FL)', 'Base Rate', 'Performance_Score', 'Container Count']].copy()
                            lane_options = lane_options.rename(columns={'Dray SCAC(FL)': 'SCAC', 'Performance_Score': 'Performance'})
                            
                            # Create optimization problem
                            prob = LpProblem("Carrier_Optimization", LpMinimize)
                            
                            # Decision variables: binary variable for each row (carrier-lane-week combination)
                            choices = []
                            for idx, row in lane_options.iterrows():
                                var_name = f"choose_{idx}"  # Simplified variable naming
                                choices.append(LpVariable(var_name, cat='Binary'))
                            
                            lane_options['choice_var'] = choices
                            
                            # Normalize costs and performance for objective function
                            max_rate = lane_options['Base Rate'].max()
                            min_rate = lane_options['Base Rate'].min()
                            max_perf = lane_options['Performance'].max()
                            min_perf = lane_options['Performance'].min()
                            
                            st.write(f"**Rate range:** ${min_rate:.2f} - ${max_rate:.2f}")
                            st.write(f"**Performance range:** {min_perf:.1f}% - {max_perf:.1f}%")
                            
                            # Avoid division by zero
                            rate_range = max_rate - min_rate if max_rate != min_rate else 1
                            perf_range = max_perf - min_perf if max_perf != min_perf else 1
                            
                            # Normalized cost (0-1, where 0 is cheapest)
                            lane_options['norm_cost'] = (lane_options['Base Rate'] - min_rate) / rate_range
                            
                            # Normalized performance (0-1, where 1 is best performance)
                            lane_options['norm_performance'] = (lane_options['Performance'] - min_perf) / perf_range
                            
                            # Normalize weights to sum to 1
                            total_weight = cost_weight + performance_weight
                            if total_weight > 0:
                                norm_cost_weight = cost_weight / total_weight
                                norm_performance_weight = performance_weight / total_weight
                            else:
                                norm_cost_weight = 0.5
                                norm_performance_weight = 0.5
                            
                            st.write(f"**Normalized weights:** Cost={norm_cost_weight:.2f}, Performance={norm_performance_weight:.2f}")
                            
                            # Objective function: minimize (cost_weight * cost - performance_weight * performance)
                            objective_terms = []
                            for idx, row in lane_options.iterrows():
                                # Cost component (minimize cost)
                                cost_component = norm_cost_weight * row['norm_cost'] * row['Container Count']
                                # Performance component (maximize performance, so subtract it)
                                perf_component = norm_performance_weight * row['norm_performance'] * row['Container Count']
                                
                                objective_terms.append(row['choice_var'] * (cost_component - perf_component))
                            
                            prob += lpSum(objective_terms)
                            
                            # Constraints: exactly one carrier per unique lane-week combination
                            constraint_count = 0
                            for (lane, week), group in lane_options.groupby(['Lane', 'Week Number']):
                                if len(group) > 1:  # Only add constraint if there are multiple options
                                    prob += lpSum([row['choice_var'] for _, row in group.iterrows()]) == 1
                                    constraint_count += 1
                                else:
                                    # If only one option, force it to be selected
                                    prob += group.iloc[0]['choice_var'] == 1
                            
                            st.write(f"**Optimization constraints added:** {constraint_count}")
                            st.write(f"**Decision variables:** {len(choices)}")
                            
                            # Solve the problem
                            status = prob.solve(PULP_CBC_CMD(msg=0))
                            
                            st.write(f"**Solver status:** {LpStatus[status]}")
                            
                            # Extract results
                            if LpStatus[status] == 'Optimal':
                                st.success("✅ Optimization completed successfully!")
                                
                                # Get selected carriers
                                selected_carriers = []
                                for idx, row in lane_options.iterrows():
                                    if row['choice_var'].varValue and row['choice_var'].varValue > 0.5:  # Selected
                                        selected_carriers.append({
                                            'Lane': row['Lane'],
                                            'Week Number': row['Week Number'],
                                            'Selected SCAC': row['SCAC'],
                                            'Base Rate': row['Base Rate'],
                                            'Performance Score': row['Performance'],
                                            'Container Count': row['Container Count'],
                                            'Total Cost': row['Base Rate'] * row['Container Count']
                                        })
                                
                                if len(selected_carriers) == 0:
                                    st.error("❌ No carriers were selected in the optimization result. This may indicate a problem with the optimization setup.")
                                else:
                                    results_df = pd.DataFrame(selected_carriers)
                                    
                                    # Calculate optimization results
                                    total_optimized_cost = results_df['Total Cost'].sum()
                                    avg_optimized_performance = (results_df['Performance Score'] * results_df['Container Count']).sum() / results_df['Container Count'].sum()
                                    total_containers = results_df['Container Count'].sum()
                                    
                                    # Compare with current costs and performance (from opt_data)
                                    current_cost = opt_data['Total Rate'].sum()
                                    current_avg_performance = (opt_data['Performance_Score'] * opt_data['Container Count']).sum() / opt_data['Container Count'].sum()
                                    
                                    # Find cheapest possible cost (ignoring performance)
                                    cheapest_by_lane_week = opt_data.groupby(['Lane', 'Week Number'])['Total Rate'].min().sum()
                                    
                                    # Display optimization results
                                    st.markdown("### 📊 Optimization Results")
                                    
                                    result_col1, result_col2, result_col3, result_col4 = st.columns(4)
                                    
                                    with result_col1:
                                        cost_diff = total_optimized_cost - current_cost
                                        st.metric(
                                            "💰 Optimized Total Cost",
                                            f"${total_optimized_cost:,.2f}",
                                            f"${cost_diff:,.2f}" if cost_diff != 0 else "No change"
                                        )
                                    
                                    with result_col2:
                                        perf_diff = avg_optimized_performance - current_avg_performance
                                        st.metric(
                                            "🎯 Avg Performance",
                                            f"{avg_optimized_performance:.1f}%",
                                            f"{perf_diff:+.1f}%" if abs(perf_diff) > 0.1 else "No change"
                                        )
                                    
                                    with result_col3:
                                        cost_vs_cheapest = total_optimized_cost - cheapest_by_lane_week
                                        st.metric(
                                            "💡 Cost vs Cheapest",
                                            f"${cost_vs_cheapest:,.2f}",
                                            "Performance premium"
                                        )
                                    
                                    with result_col4:
                                        savings_pct = ((current_cost - total_optimized_cost) / current_cost * 100) if current_cost > 0 else 0
                                        st.metric(
                                            "📈 Total Savings",
                                            f"{savings_pct:.1f}%",
                                            f"${current_cost - total_optimized_cost:,.2f}"
                                        )
                                    
                                    # Detailed optimization results
                                    st.markdown("### 📋 Optimized Carrier Selection")
                                    results_display = results_df.copy()
                                    results_display['Base Rate'] = results_display['Base Rate'].apply(lambda x: f"${x:.2f}")
                                    results_display['Performance Score'] = results_display['Performance Score'].apply(lambda x: f"{x:.1f}%")
                                    results_display['Total Cost'] = results_display['Total Cost'].apply(lambda x: f"${x:,.2f}")
                                    
                                    st.dataframe(results_display.sort_values('Lane'), use_container_width=True)
                                    
                                    # Download optimized results
                                    csv_results = results_df.to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download Optimized Selection",
                                        data=csv_results,
                                        file_name='optimized_carrier_selection.csv',
                                        mime='text/csv',
                                        use_container_width=True
                                    )
                            else:
                                st.error(f"❌ Optimization failed. Status: {LpStatus[status]}")
                                st.write("This could be due to:")
                                st.write("- Infeasible constraints")
                                st.write("- No valid solution found")
                                st.write("- Solver configuration issues")
                        
                        except Exception as e:
                            st.error(f"❌ Optimization error: {str(e)}")
                            st.write("Please check your data and try again.")
                            import traceback
                            st.code(traceback.format_exc())
                            
else:
    st.info("ℹ️ Linear programming optimization requires performance data. Please upload performance data to use this feature.")

# Add explanation of optimization methodology
with st.expander("🔍 How Linear Programming Optimization Works"):
    st.markdown("""
    **Prerequisites:**
    - Performance data must be available and matched with GVT data
    - Multiple carrier options per lane-week combination are needed for optimization
    - Carriers must meet the minimum performance threshold
    
    **Objective Function:**
    - Minimizes: `(Cost Weight × Normalized Cost) - (Performance Weight × Normalized Performance)`
    - Cost and performance are normalized to 0-1 scale for fair comparison
    - Container count is used as a multiplier to weight decisions by volume
    
    **Constraints:**
    - Exactly one carrier must be selected for each Lane-Week combination
    - Only carriers meeting the minimum performance threshold are considered
    - Binary decision variables ensure discrete carrier selection
    
    **Optimization Goals:**
    - **Cost Focus (high cost weight):** Prioritizes finding cheaper carriers
    - **Performance Focus (high performance weight):** Prioritizes reliable carriers
    - **Balanced Approach:** Finds optimal trade-off between cost and performance
    
    **Common Issues:**
    - **No results:** Check if performance data is being merged properly
    - **Single carrier per lane:** Optimization requires multiple options to choose from
    - **No performance data:** Upload and verify performance data is being processed
    - **Threshold too high:** Performance threshold excludes all carriers
    """)

# Advanced Analytics & Machine Learning Section
st.markdown('<div class="section-header">🔮 Advanced Analytics & Machine Learning</div>', unsafe_allow_html=True)

if len(final_filtered_data) > 0:
    analytics_tabs = st.tabs(["📈 Predictive Analytics", "🎯 Performance Trends", "🔍 Anomaly Detection"])
    
    with analytics_tabs[0]:
        st.markdown("**📊 Container Volume Forecasting**")
        
        # Prepare time series data
        weekly_data = final_filtered_data.groupby(['Week Number', 'Lane']).agg({
            'Container Count': 'sum',
            'Total Rate': 'sum',
            'Base Rate': 'mean'
        }).reset_index()
        
        if len(weekly_data) >= 4:  # Need minimum data for forecasting
            col1, col2 = st.columns(2)
            
            with col1:
                selected_lane = st.selectbox(
                    "Select Lane for Forecasting",
                    options=weekly_data['Lane'].unique(),
                    key="forecast_lane"
                )
                
                forecast_weeks = st.slider("Weeks to Forecast", 1, 8, 4)
            
            with col2:
                st.write("**Forecast Parameters:**")
                confidence_level = st.slider("Confidence Level (%)", 80, 99, 95)
                
            if st.button("🚀 Generate Forecast"):
                lane_data = weekly_data[weekly_data['Lane'] == selected_lane].sort_values('Week Number')
                
                if len(lane_data) >= 3:
                    # Simple forecasting using linear trend
                    X = lane_data['Week Number'].values.reshape(-1, 1)
                    y = lane_data['Container Count'].values
                    
                    from sklearn.linear_model import LinearRegression
                    model = LinearRegression()
                    model.fit(X, y)
                    
                    # Generate forecast
                    last_week = lane_data['Week Number'].max()
                    future_weeks = np.arange(last_week + 1, last_week + 1 + forecast_weeks).reshape(-1, 1)
                    forecast = model.predict(future_weeks)
                    
                    # Create visualization
                    fig = go.Figure()
                    
                    # Historical data
                    fig.add_trace(go.Scatter(
                        x=lane_data['Week Number'],
                        y=lane_data['Container Count'],
                        mode='lines+markers',
                        name='Historical',
                        line=dict(color='blue')
                    ))
                    
                    # Forecast
                    fig.add_trace(go.Scatter(
                        x=future_weeks.flatten(),
                        y=forecast,
                        mode='lines+markers',
                        name='Forecast',
                        line=dict(color='red', dash='dash')
                    ))
                    
                    fig.update_layout(
                        title=f'Container Volume Forecast - {selected_lane}',
                        xaxis_title='Week Number',
                        yaxis_title='Container Count',
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Forecast summary
                    forecast_df = pd.DataFrame({
                        'Week': future_weeks.flatten(),
                        'Forecasted Containers': forecast.astype(int),
                        'Confidence Level': f"{confidence_level}%"
                    })
                    st.dataframe(forecast_df, use_container_width=True)
                else:
                    st.warning("Not enough historical data for this lane. Select a different lane.")
        else:
            st.info("Need at least 4 weeks of data for forecasting. Add more data or adjust filters.")
    
    with analytics_tabs[1]:
        st.markdown("**📊 Carrier Performance Trends**")
        
        if 'Performance_Score' in final_filtered_data.columns:
            # Performance trend analysis
            perf_trends = final_filtered_data.groupby(['Week Number', 'Dray SCAC(FL)']).agg({
                'Performance_Score': 'mean',
                'Container Count': 'sum',
                'Base Rate': 'mean'
            }).reset_index()
            
            # Select top carriers by volume
            top_carriers = final_filtered_data.groupby('Dray SCAC(FL)')['Container Count'].sum().nlargest(5).index.tolist()
            
            trend_col1, trend_col2 = st.columns(2)
            
            with trend_col1:
                selected_carriers = st.multiselect(
                    "Select Carriers for Trend Analysis",
                    options=final_filtered_data['Dray SCAC(FL)'].unique(),
                    default=top_carriers[:3],
                    key="trend_carriers"
                )
            
            with trend_col2:
                trend_metric = st.selectbox(
                    "Trend Metric",
                    ["Performance_Score", "Base Rate", "Container Count"]
                )
            
            if selected_carriers:
                trend_data = perf_trends[perf_trends['Dray SCAC(FL)'].isin(selected_carriers)]
                
                fig = px.line(
                    trend_data,
                    x='Week Number',
                    y=trend_metric,
                    color='Dray SCAC(FL)',
                    title=f'{trend_metric} Trends by Carrier',
                    markers=True
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Performance ranking
                current_perf = final_filtered_data.groupby('Dray SCAC(FL)')['Performance_Score'].mean().sort_values(ascending=False)
                st.write("**Current Performance Ranking:**")
                perf_rank_df = pd.DataFrame({
                    'Rank': range(1, len(current_perf) + 1),
                    'Carrier': current_perf.index,
                    'Avg Performance': current_perf.values.round(1)
                })
                st.dataframe(perf_rank_df.head(10), use_container_width=True)
        else:
            st.info("Performance data required for trend analysis. Upload performance data to enable this feature.")
    
    with analytics_tabs[2]:
        st.markdown("**🚨 Anomaly Detection**")
        
        # Rate anomaly detection
        Q1 = final_filtered_data['Base Rate'].quantile(0.25)
        Q3 = final_filtered_data['Base Rate'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        anomalies = final_filtered_data[
            (final_filtered_data['Base Rate'] < lower_bound) | 
            (final_filtered_data['Base Rate'] > upper_bound)
        ]
        
        anom_col1, anom_col2, anom_col3 = st.columns(3)
        
        with anom_col1:
            st.metric("🔍 Rate Anomalies", len(anomalies))
        with anom_col2:
            st.metric("📊 Normal Range", f"${lower_bound:.0f} - ${upper_bound:.0f}")
        with anom_col3:
            anomaly_pct = (len(anomalies) / len(final_filtered_data) * 100)
            st.metric("📈 Anomaly Rate", f"{anomaly_pct:.1f}%")
        
        if len(anomalies) > 0:
            st.write("**Detected Rate Anomalies:**")
            anomaly_display = anomalies[['Lane', 'Dray SCAC(FL)', 'Week Number', 'Base Rate', 'Container Count']].copy()
            anomaly_display['Anomaly Type'] = anomaly_display['Base Rate'].apply(
                lambda x: 'Unusually Low' if x < lower_bound else 'Unusually High'
            )
            st.dataframe(anomaly_display.sort_values('Base Rate'), use_container_width=True)
            
            # Visualization
            fig = px.box(
                final_filtered_data,
                y='Base Rate',
                title='Rate Distribution with Anomalies',
                points='outliers'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# Interactive Visualizations Section
st.markdown('<div class="section-header">📊 Interactive Visualizations</div>', unsafe_allow_html=True)

if len(final_filtered_data) > 0:
    viz_tabs = st.tabs(["🎯 Cost vs Performance", "🌍 Geographic Analysis", "📈 Time Series", "🔄 Correlation Matrix"])
    
    with viz_tabs[0]:
        st.markdown("**💰 Cost vs Performance Scatter Analysis**")
        
        if 'Performance_Score' in final_filtered_data.columns:
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                size_metric = st.selectbox("Bubble Size", ["Container Count", "Total Rate", "Potential Savings"])
                color_metric = st.selectbox("Color By", ["Dray SCAC(FL)", "Week Number", "Lane"])
            
            with viz_col2:
                min_containers = st.slider("Min Container Count", 1, int(final_filtered_data['Container Count'].max()), 1)
                
            # Filter data
            viz_data = final_filtered_data[final_filtered_data['Container Count'] >= min_containers]
            
            fig = px.scatter(
                viz_data,
                x='Base Rate',
                y='Performance_Score',
                size=size_metric,
                color=color_metric,
                hover_data=['Lane', 'Week Number', 'Container Count'],
                title="Cost vs Performance Analysis",
                labels={'Base Rate': 'Base Rate ($)', 'Performance_Score': 'Performance Score (%)'}
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Quadrant analysis
            med_rate = viz_data['Base Rate'].median()
            med_perf = viz_data['Performance_Score'].median()
            
            quadrants = []
            for _, row in viz_data.iterrows():
                if row['Base Rate'] <= med_rate and row['Performance_Score'] >= med_perf:
                    quad = "🟢 Low Cost, High Performance"
                elif row['Base Rate'] <= med_rate and row['Performance_Score'] < med_perf:
                    quad = "🟡 Low Cost, Low Performance"
                elif row['Base Rate'] > med_rate and row['Performance_Score'] >= med_perf:
                    quad = "🟠 High Cost, High Performance"
                else:
                    quad = "🔴 High Cost, Low Performance"
                quadrants.append(quad)
            
            viz_data_quad = viz_data.copy()
            viz_data_quad['Quadrant'] = quadrants
            
            quad_summary = viz_data_quad.groupby('Quadrant').agg({
                'Container Count': 'sum',
                'Total Rate': 'sum',
                'Dray SCAC(FL)': 'nunique'
            }).round(2)
            quad_summary.columns = ['Total Containers', 'Total Cost', 'Unique Carriers']
            
            st.write("**Quadrant Analysis:**")
            st.dataframe(quad_summary, use_container_width=True)
        else:
            st.info("Performance data required for cost vs performance analysis.")
    
    with viz_tabs[1]:
        st.markdown("**🌍 Geographic and Route Analysis**")
        
        # Port analysis
        port_analysis = final_filtered_data.groupby('Discharged Port').agg({
            'Container Count': 'sum',
            'Total Rate': 'sum',
            'Potential Savings': 'sum',
            'Dray SCAC(FL)': 'nunique'
        }).reset_index()
        
        geo_col1, geo_col2 = st.columns(2)
        
        with geo_col1:
            geo_metric = st.selectbox("Map Metric", ["Container Count", "Total Rate", "Potential Savings"])
            
        with geo_col2:
            top_n_ports = st.slider("Show Top N Ports", 5, 20, 10)
        
        # Port volume chart
        top_ports = port_analysis.nlargest(top_n_ports, geo_metric)
        
        fig = px.bar(
            top_ports,
            x='Discharged Port',
            y=geo_metric,
            title=f'Top {top_n_ports} Ports by {geo_metric}',
            color=geo_metric,
            color_continuous_scale='viridis'
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Lane analysis heatmap
        st.write("**Lane Performance Heatmap:**")
        lane_heatmap = final_filtered_data.pivot_table(
            values='Potential Savings',
            index='Discharged Port',
            columns='Facility',
            aggfunc='sum',
            fill_value=0
        )
        
        # Limit to top ports and facilities for readability
        if len(lane_heatmap) > 15:
            top_ports_for_heatmap = lane_heatmap.sum(axis=1).nlargest(15).index
            lane_heatmap = lane_heatmap.loc[top_ports_for_heatmap]
        
        if len(lane_heatmap.columns) > 15:
            top_facilities = lane_heatmap.sum(axis=0).nlargest(15).index
            lane_heatmap = lane_heatmap[top_facilities]
        
        fig = px.imshow(
            lane_heatmap.values,
            labels=dict(x="Facility", y="Port", color="Potential Savings"),
            x=lane_heatmap.columns,
            y=lane_heatmap.index,
            aspect="auto",
            title="Potential Savings by Port-Facility Combination"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with viz_tabs[2]:
        st.markdown("**📈 Time Series Analysis**")
        
        # Weekly trends
        weekly_trends = final_filtered_data.groupby('Week Number').agg({
            'Container Count': 'sum',
            'Total Rate': 'sum',
            'Potential Savings': 'sum',
            'Base Rate': 'mean'
        }).reset_index()
        
        # Multiple metrics chart
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Container Volume', 'Total Costs', 'Potential Savings', 'Average Rate'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(
            go.Scatter(x=weekly_trends['Week Number'], y=weekly_trends['Container Count'], 
                      mode='lines+markers', name='Containers'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=weekly_trends['Week Number'], y=weekly_trends['Total Rate'], 
                      mode='lines+markers', name='Total Cost'),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=weekly_trends['Week Number'], y=weekly_trends['Potential Savings'], 
                      mode='lines+markers', name='Savings'),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=weekly_trends['Week Number'], y=weekly_trends['Base Rate'], 
                      mode='lines+markers', name='Avg Rate'),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False, title_text="Weekly Trends Analysis")
        st.plotly_chart(fig, use_container_width=True)
        
        # Growth rate calculation
        weekly_trends['Container_Growth'] = weekly_trends['Container Count'].pct_change() * 100
        weekly_trends['Cost_Growth'] = weekly_trends['Total Rate'].pct_change() * 100
        
        growth_summary = pd.DataFrame({
            'Week': weekly_trends['Week Number'],
            'Volume Growth (%)': weekly_trends['Container_Growth'].round(1),
            'Cost Growth (%)': weekly_trends['Cost_Growth'].round(1)
        }).dropna()
        
        st.write("**Week-over-Week Growth Rates:**")
        st.dataframe(growth_summary, use_container_width=True)
    
    with viz_tabs[3]:
        st.markdown("**🔄 Correlation Analysis**")
        
        # Prepare numeric data for correlation
        numeric_cols = ['Base Rate', 'Container Count', 'Total Rate', 'Potential Savings', 'Week Number']
        if 'Performance_Score' in final_filtered_data.columns:
            numeric_cols.append('Performance_Score')
        
        corr_data = final_filtered_data[numeric_cols].corr()
        
        # Correlation heatmap
        fig = px.imshow(
            corr_data.values,
            labels=dict(color="Correlation"),
            x=corr_data.columns,
            y=corr_data.index,
            color_continuous_scale='RdBu',
            aspect="auto",
            title="Correlation Matrix of Key Metrics"
        )
        
        # Add correlation values as text
        for i in range(len(corr_data.columns)):
            for j in range(len(corr_data.columns)):
                fig.add_annotation(
                    x=i, y=j,
                    text=str(round(corr_data.iloc[j, i], 2)),
                    showarrow=False,
                    font=dict(color="white" if abs(corr_data.iloc[j, i]) > 0.5 else "black")
                )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        st.write("**Key Correlations:**")
        insights = []
        
        for i, col1 in enumerate(corr_data.columns):
            for j, col2 in enumerate(corr_data.columns):
                if i < j:  # Avoid duplicates
                    corr_val = corr_data.iloc[i, j]
                    if abs(corr_val) > 0.3:  # Significant correlation
                        strength = "Strong" if abs(corr_val) > 0.7 else "Moderate"
                        direction = "Positive" if corr_val > 0 else "Negative"
                        insights.append({
                            'Variables': f"{col1} vs {col2}",
                            'Correlation': f"{corr_val:.3f}",
                            'Relationship': f"{strength} {direction}"
                        })
        
        if insights:
            insights_df = pd.DataFrame(insights)
            st.dataframe(insights_df, use_container_width=True)
        else:
            st.info("No significant correlations found (threshold: |r| > 0.3)")

# Advanced Optimization Scenarios Section
st.markdown('<div class="section-header">🎯 Advanced Optimization Scenarios</div>', unsafe_allow_html=True)

if 'Performance_Score' in final_filtered_data.columns and len(final_filtered_data) > 0:
    scenario_tabs = st.tabs(["🚀 What-If Analysis", "📈 Capacity Constraints", "🔄 Dynamic Pricing", "🌍 Multi-Criteria"])
    
    with scenario_tabs[0]:
        st.markdown("**🔮 What-If Scenario Builder**")
        
        scenario_col1, scenario_col2 = st.columns(2)
        
        with scenario_col1:
            st.markdown("**Market Changes:**")
            volume_change = st.slider("Volume Change (%)", -50, 100, 0, key="scenario_volume")
            rate_change = st.slider("Overall Rate Change (%)", -30, 30, 0, key="scenario_rate")
            fuel_surcharge = st.slider("Fuel Surcharge (%)", 0, 25, 0, key="scenario_fuel")
        
        with scenario_col2:
            st.markdown("**Performance Requirements:**")
            min_performance = st.slider("Minimum Performance (%)", 50, 95, 75, key="scenario_perf")
            max_risk_carriers = st.slider("Max % of Volume from Single Carrier", 10, 80, 50, key="scenario_risk")
        
        if st.button("🔍 Run What-If Analysis", key="whatif_button"):
            # Create scenario data
            scenario_data = final_filtered_data.copy()
            
            # Apply changes
            scenario_data['Container Count'] = scenario_data['Container Count'] * (1 + volume_change/100)
            scenario_data['Base Rate'] = scenario_data['Base Rate'] * (1 + rate_change/100) * (1 + fuel_surcharge/100)
            scenario_data['Total Rate'] = scenario_data['Base Rate'] * scenario_data['Container Count']
            
            # Filter by performance
            scenario_data = scenario_data[scenario_data['Performance_Score'] >= min_performance]
            
            # Calculate scenario results
            original_cost = final_filtered_data['Total Rate'].sum()
            scenario_cost = scenario_data['Total Rate'].sum()
            
            scenario_col1, scenario_col2, scenario_col3 = st.columns(3)
            
            with scenario_col1:
                cost_impact = scenario_cost - original_cost
                st.metric(
                    "💰 Cost Impact",
                    f"${scenario_cost:,.2f}",
                    f"${cost_impact:,.2f}"
                )
            
            with scenario_col2:
                volume_impact = scenario_data['Container Count'].sum() - final_filtered_data['Container Count'].sum()
                st.metric(
                    "📦 Volume Impact",
                    f"{scenario_data['Container Count'].sum():,.0f}",
                    f"{volume_impact:,.0f}"
                )
            
            with scenario_col3:
                available_carriers = scenario_data['Dray SCAC(FL)'].nunique()
                st.metric(
                    "🚛 Available Carriers",
                    f"{available_carriers}",
                    f"{available_carriers - final_filtered_data['Dray SCAC(FL)'].nunique()}"
                )
            
            # Carrier concentration risk
            carrier_volumes = scenario_data.groupby('Dray SCAC(FL)')['Container Count'].sum()
            total_volume = carrier_volumes.sum()
            carrier_share = (carrier_volumes / total_volume * 100).sort_values(ascending=False)
            
            st.write("**Carrier Volume Concentration:**")
            concentration_df = pd.DataFrame({
                'Carrier': carrier_share.index[:10],
                'Volume Share (%)': carrier_share.values[:10].round(1),
                'Risk Level': ['High' if x > max_risk_carriers else 'Medium' if x > max_risk_carriers/2 else 'Low' 
                              for x in carrier_share.values[:10]]
            })
            st.dataframe(concentration_df, use_container_width=True)
    
    with scenario_tabs[1]:
        st.markdown("**📊 Capacity-Constrained Optimization**")
        
        cap_col1, cap_col2 = st.columns(2)
        
        with cap_col1:
            default_capacity = int(final_filtered_data.groupby('Dray SCAC(FL)')['Container Count'].sum().mean())
            carrier_capacity = st.number_input(
                "Default Carrier Capacity (containers/week)", 
                min_value=1, 
                value=default_capacity,
                key="carrier_capacity"
            )
            
            capacity_buffer = st.slider("Capacity Buffer (%)", 5, 30, 15, key="capacity_buffer")
        
        with cap_col2:
            min_service_level = st.slider("Minimum Service Level (%)", 85, 100, 95, key="service_level")
            priority_lanes = st.multiselect(
                "Priority Lanes (must be served)",
                options=final_filtered_data['Lane'].unique()[:10],
                key="priority_lanes"
            )
        
        if st.button("⚖️ Run Capacity Analysis", key="capacity_button"):
            # Analyze current capacity utilization
            current_utilization = final_filtered_data.groupby('Dray SCAC(FL)')['Container Count'].sum()
            
            capacity_analysis = pd.DataFrame({
                'Carrier': current_utilization.index,
                'Current Volume': current_utilization.values,
                'Capacity Limit': carrier_capacity,
                'Utilization (%)': (current_utilization.values / carrier_capacity * 100).round(1),
                'Available Capacity': carrier_capacity - current_utilization.values
            })
            
            # Add capacity status
            capacity_analysis['Status'] = capacity_analysis['Utilization (%)'].apply(
                lambda x: '🔴 Over Capacity' if x > 100 else 
                         '🟡 Near Capacity' if x > 85 else 
                         '🟢 Available'
            )
            
            st.write("**Current Capacity Analysis:**")
            st.dataframe(capacity_analysis.sort_values('Utilization (%)', ascending=False), use_container_width=True)
            
            # Capacity constraints visualization
            fig = px.bar(
                capacity_analysis,
                x='Carrier',
                y=['Current Volume', 'Available Capacity'],
                title='Carrier Capacity Utilization',
                barmode='stack'
            )
            fig.add_hline(y=carrier_capacity, line_dash="dash", line_color="red", 
                         annotation_text="Capacity Limit")
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    with scenario_tabs[2]:
        st.markdown("**💹 Dynamic Pricing Analysis**")
        
        pricing_col1, pricing_col2 = st.columns(2)
        
        with pricing_col1:
            st.markdown("**Market Conditions:**")
            peak_season_weeks = st.multiselect(
                "Peak Season Weeks",
                options=sorted(final_filtered_data['Week Number'].unique()),
                key="peak_weeks"
            )
            peak_multiplier = st.slider("Peak Season Rate Multiplier", 1.0, 2.5, 1.3, key="peak_mult")
            
        with pricing_col2:
            st.markdown("**Fuel & Surcharges:**")
            fuel_base_price = st.number_input("Base Fuel Price ($/gallon)", 3.0, 8.0, 4.5, key="fuel_base")
            current_fuel_price = st.number_input("Current Fuel Price ($/gallon)", 3.0, 8.0, 5.0, key="fuel_current")
            
        if st.button("📈 Analyze Dynamic Pricing", key="pricing_button"):
            dynamic_data = final_filtered_data.copy()
            
            # Apply peak season pricing
            if peak_season_weeks:
                peak_mask = dynamic_data['Week Number'].isin(peak_season_weeks)
                dynamic_data.loc[peak_mask, 'Base Rate'] *= peak_multiplier
            
            # Apply fuel surcharge
            fuel_surcharge_rate = (current_fuel_price - fuel_base_price) / fuel_base_price
            if fuel_surcharge_rate > 0:
                dynamic_data['Base Rate'] *= (1 + fuel_surcharge_rate * 0.1)  # 10% pass-through rate
            
            dynamic_data['Total Rate'] = dynamic_data['Base Rate'] * dynamic_data['Container Count']
            
            # Compare original vs dynamic pricing
            original_total = final_filtered_data['Total Rate'].sum()
            dynamic_total = dynamic_data['Total Rate'].sum()
            
            pricing_impact = pd.DataFrame({
                'Scenario': ['Original Pricing', 'Dynamic Pricing'],
                'Total Cost': [original_total, dynamic_total],
                'Average Rate': [
                    final_filtered_data['Base Rate'].mean(),
                    dynamic_data['Base Rate'].mean()
                ],
                'Cost Difference': [0, dynamic_total - original_total]
            })
            
            st.write("**Pricing Impact Summary:**")
            st.dataframe(pricing_impact, use_container_width=True)
            
            # Weekly pricing analysis
            weekly_pricing = dynamic_data.groupby('Week Number').agg({
                'Base Rate': 'mean',
                'Total Rate': 'sum',
                'Container Count': 'sum'
            }).reset_index()
            
            fig = px.line(
                weekly_pricing,
                x='Week Number',
                y='Base Rate',
                title='Dynamic Pricing by Week',
                markers=True
            )
            
            # Highlight peak weeks
            if peak_season_weeks:
                for week in peak_season_weeks:
                    fig.add_vline(x=week, line_dash="dash", line_color="red", 
                                 annotation_text=f"Peak Week {week}")
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with scenario_tabs[3]:
        st.markdown("**🎯 Multi-Criteria Decision Analysis**")
        
        st.write("**Define Your Optimization Criteria:**")
        
        criteria_col1, criteria_col2 = st.columns(2)
        
        with criteria_col1:
            cost_weight = st.slider("Cost Importance", 0.0, 1.0, 0.4, key="mcda_cost")
            performance_weight = st.slider("Performance Importance", 0.0, 1.0, 0.3, key="mcda_perf")
            reliability_weight = st.slider("Reliability Importance", 0.0, 1.0, 0.2, key="mcda_rel")
        
        with criteria_col2:
            sustainability_weight = st.slider("Sustainability Importance", 0.0, 1.0, 0.1, key="mcda_sust")
            
            # Normalize weights
            total_weight = cost_weight + performance_weight + reliability_weight + sustainability_weight
            if total_weight > 0:
                cost_weight /= total_weight
                performance_weight /= total_weight
                reliability_weight /= total_weight
                sustainability_weight /= total_weight
        
        st.write(f"**Normalized Weights:** Cost: {cost_weight:.2f}, Performance: {performance_weight:.2f}, Reliability: {reliability_weight:.2f}, Sustainability: {sustainability_weight:.2f}")
        
        if st.button("🔍 Run Multi-Criteria Analysis", key="mcda_button"):
            # Create scoring matrix
            carrier_scores = final_filtered_data.groupby('Dray SCAC(FL)').agg({
                'Base Rate': 'mean',
                'Performance_Score': 'mean',
                'Container Count': 'sum',
                'Week Number': 'nunique'  # Reliability proxy
            }).reset_index()
            
            # Normalize scores (0-1 scale)
            carrier_scores['Cost_Score'] = 1 - (carrier_scores['Base Rate'] - carrier_scores['Base Rate'].min()) / (carrier_scores['Base Rate'].max() - carrier_scores['Base Rate'].min())
            carrier_scores['Perf_Score'] = (carrier_scores['Performance_Score'] - carrier_scores['Performance_Score'].min()) / (carrier_scores['Performance_Score'].max() - carrier_scores['Performance_Score'].min())
            carrier_scores['Rel_Score'] = (carrier_scores['Week Number'] - carrier_scores['Week Number'].min()) / (carrier_scores['Week Number'].max() - carrier_scores['Week Number'].min())
            carrier_scores['Sust_Score'] = 0.5  # Placeholder - would need sustainability data
            
            # Calculate composite score
            carrier_scores['Composite_Score'] = (
                cost_weight * carrier_scores['Cost_Score'] +
                performance_weight * carrier_scores['Perf_Score'] +
                reliability_weight * carrier_scores['Rel_Score'] +
                sustainability_weight * carrier_scores['Sust_Score']
            )
            
            # Rank carriers
            carrier_ranking = carrier_scores.sort_values('Composite_Score', ascending=False)
            
            ranking_display = carrier_ranking[['Dray SCAC(FL)', 'Composite_Score', 'Cost_Score', 'Perf_Score', 'Rel_Score']].copy()
            ranking_display.columns = ['Carrier', 'Overall Score', 'Cost Score', 'Performance Score', 'Reliability Score']
            ranking_display = ranking_display.round(3)
            
            st.write("**Multi-Criteria Carrier Ranking:**")
            st.dataframe(ranking_display.head(15), use_container_width=True)
            
            # Radar chart for top 5 carriers
            top_5_carriers = carrier_ranking.head(5)
            
            fig = go.Figure()
            
            for idx, (_, carrier) in enumerate(top_5_carriers.iterrows()):
                fig.add_trace(go.Scatterpolar(
                    r=[carrier['Cost_Score'], carrier['Perf_Score'], carrier['Rel_Score'], carrier['Sust_Score']],
                    theta=['Cost', 'Performance', 'Reliability', 'Sustainability'],
                    fill='toself',
                    name=carrier['Dray SCAC(FL)']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=True,
                title="Top 5 Carriers - Multi-Criteria Comparison",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("⚠️ Advanced optimization scenarios require performance data. Please upload performance data to enable these features.")
