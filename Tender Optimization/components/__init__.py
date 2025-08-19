"""
Main imports file for all dashboard components
"""

# Configuration and styling
from .config_styling import configure_page, apply_custom_css, show_header, section_header

# Data loading and processing
from .data_loader import show_file_upload_section, load_data_files, process_performance_data
from .data_processor import (
    validate_and_process_gvt_data, 
    validate_and_process_rate_data, 
    perform_lane_analysis, 
    merge_all_data, 
    apply_volume_weighted_performance,
    create_comprehensive_data
)

# Filtering
from .filters import (
    show_filter_interface, 
    apply_filters_to_data, 
    show_selection_summary
)

# Metrics and analysis
from .metrics import (
    calculate_enhanced_metrics, 
    display_current_metrics, 
    show_detailed_analysis_table, 
    show_top_savings_opportunities,
    show_complete_data_export,
    show_suboptimal_analysis,
    show_performance_score_analysis,
    show_carrier_performance_matrix
)

# Summary tables
from .summary_tables import show_summary_tables

# Optimization
from .optimization import show_optimization_section, get_optimization_results, show_missing_rate_analysis_for_optimization

# Analytics
from .analytics import show_advanced_analytics

# Visualizations
from .visualizations import show_interactive_visualizations

# Suboptimal analysis
from .suboptimal_analysis import show_suboptimal_analysis

# Calculation logic and utilities
from .calculation_logic import show_calculation_logic, show_debug_performance_merge, show_footer
from .performance_assignments import show_performance_assignments_table, export_performance_assignments

__all__ = [
    # Configuration
    'configure_page', 'apply_custom_css', 'show_header', 'section_header',
    
    # Data handling
    'show_file_upload_section', 'load_data_files', 'process_performance_data',
    'validate_and_process_gvt_data', 'validate_and_process_rate_data', 
    'perform_lane_analysis', 'merge_all_data', 'create_comprehensive_data',
    
    # Filtering
    'show_filter_interface', 'apply_filters_to_data', 'show_selection_summary',
    
    # Metrics
    'calculate_enhanced_metrics', 'display_current_metrics', 'show_detailed_analysis_table',
    'show_top_savings_opportunities', 'show_complete_data_export', 'show_performance_score_analysis',
    'show_carrier_performance_matrix',
    
    # Tables and analysis
    'show_summary_tables',
    
    # Optimization
    'show_optimization_section', 'get_optimization_results', 'show_missing_rate_analysis_for_optimization',
    
    # Analytics and visualizations
    'show_advanced_analytics', 'show_interactive_visualizations',
    
    # Suboptimal analysis
    'show_suboptimal_analysis',
    
    # Utilities
    'show_calculation_logic', 'show_debug_performance_merge', 'show_footer',
    'show_performance_assignments_table', 'export_performance_assignments'
]
