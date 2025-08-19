# Carrier Tender Optimization Dashboard

A comprehensive Streamlit dashboard for analyzing carrier tender data, optimizing costs, and evaluating performance metrics.

## 📁 Project Structure

```
Tender Optimization/
├── dashboard.py                    # Main application file
├── dashboard_old.py               # Original monolithic version (backup)
├── requirements.txt               # Python dependencies
├── README.md                     # This file
└── components/                   # Modular components
    ├── __init__.py              # Component imports
    ├── config_styling.py        # Page configuration and CSS
    ├── data_loader.py           # File upload and data loading
    ├── data_processor.py        # Data validation and processing
    ├── filters.py               # Interactive filtering interface
    ├── metrics.py               # KPI calculations and display
    ├── summary_tables.py        # Summary analysis tables
    ├── optimization.py          # Linear programming optimization
    ├── analytics.py             # Advanced analytics and ML
    ├── visualizations.py        # Interactive charts and plots
    └── calculation_logic.py     # Documentation and debug utils
```

## 🚀 Getting Started

### Installation

1. Install required packages:

```bash
pip install -r requirements.txt
```

2. Run the dashboard:

```bash
streamlit run dashboard.py
```

## 📊 Features

### Data Management

- **File Upload**: Support for Excel files (GVT data, Rate data, Performance data)
- **Data Validation**: Automatic validation of required columns and data types
- **Performance Integration**: Optional performance data integration with week-based matching

### Analysis & Optimization

- **Cost Analysis**: Calculate total rates, potential savings, and optimization opportunities
- **Performance Tracking**: Carrier performance scoring and trend analysis
- **Linear Programming**: Multi-criteria optimization balancing cost and performance
- **Anomaly Detection**: Identify unusual rates and performance patterns

### Interactive Features

- **Advanced Filtering**: Multi-dimensional filtering with search capabilities
- **Real-time Metrics**: Dynamic KPI calculations based on selected filters
- **Summary Tables**: Aggregated views by Port, SCAC, Lane, Facility, and Week
- **Export Capabilities**: Download filtered data and optimization results

### Visualizations

- **Cost vs Performance**: Scatter plots with quadrant analysis
- **Geographic Analysis**: Port and lane performance heatmaps
- **Time Series**: Weekly trends and growth rate analysis
- **Correlation Matrix**: Statistical relationships between metrics

### Advanced Analytics

- **Predictive Analytics**: Container volume forecasting
- **Performance Trends**: Carrier reliability tracking over time
- **Machine Learning**: Anomaly detection using statistical methods

## 📋 Component Details

### Core Components

1. **config_styling.py**: Page setup, CSS styling, and UI helpers
2. **data_loader.py**: File upload interface and data loading logic
3. **data_processor.py**: Data validation, cleaning, and merging operations
4. **filters.py**: Interactive filtering system with session state management
5. **metrics.py**: KPI calculations and enhanced metrics display
6. **summary_tables.py**: Tabular analysis views with aggregations
7. **optimization.py**: Linear programming optimization with PuLP
8. **analytics.py**: Advanced analytics including forecasting and anomaly detection
9. **visualizations.py**: Interactive charts using Plotly
10. **calculation_logic.py**: Documentation and debugging utilities

### Key Calculations

- **Total Rate**: Base Rate × Container Count
- **Potential Savings**: Current Total Rate - Cheapest Total Rate
- **Savings Percentage**: (Potential Savings ÷ Total Rate) × 100
- **Lane Analysis**: Port + Facility combination analysis
- **Performance Matching**: Carrier + Week Number matching

## 🔧 Technical Architecture

### Modular Design

The dashboard is built with a modular architecture where each component handles specific functionality:

- **Separation of Concerns**: Each module has a single responsibility
- **Reusability**: Components can be easily reused or modified
- **Maintainability**: Easy to update individual features without affecting others
- **Testability**: Components can be tested independently

### Data Flow

1. **Data Loading** → File upload and validation
2. **Data Processing** → Cleaning, merging, and calculations
3. **Filtering** → User-driven data selection
4. **Analysis** → Metrics calculation and optimization
5. **Visualization** → Interactive charts and tables
6. **Export** → Data download and reporting

### Session State Management

Uses Streamlit's session state for:

- Filter persistence across interactions
- User preference storage
- Performance optimization

## 📈 Usage Examples

### Basic Analysis

1. Upload GVT and Rate data files
2. Apply filters to focus on specific ports, weeks, or carriers
3. Review metrics and potential savings
4. Export filtered results

### Advanced Optimization

1. Upload performance data in addition to basic files
2. Use linear programming optimization with custom weights
3. Compare different optimization strategies
4. Download optimized carrier selections

### Performance Monitoring

1. Load historical performance data
2. Use performance trend analysis
3. Set up anomaly detection alerts
4. Generate forecasts for future planning

## 🔍 Troubleshooting

### Common Issues

- **Missing Columns**: Ensure your data files have all required columns
- **Performance Matching**: Check that carrier names and week numbers match between files
- **Optimization Failures**: Verify you have multiple carrier options per lane-week combination

### Debug Features

- Use the "Debug Performance Merge" expander to troubleshoot data integration
- Check the calculation logic section for detailed methodology
- Review sample data displays to verify data loading

## 🛠️ Customization

The modular structure makes it easy to customize:

- **Add New Metrics**: Extend the metrics.py module
- **Custom Visualizations**: Add charts to visualizations.py
- **Additional Filters**: Enhance the filters.py module
- **New Optimization Methods**: Extend optimization.py

## 📝 License

This project is for internal use in carrier tender optimization analysis.

## 🤝 Contributing

When making changes:

1. Follow the modular structure
2. Update relevant component files
3. Test individual components
4. Update documentation
5. Maintain backward compatibility with existing data formats
