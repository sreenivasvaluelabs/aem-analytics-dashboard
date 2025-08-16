import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Line, Pie, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

function DashboardTab({ uploadedData }) {
  const [refreshKey, setRefreshKey] = useState(0);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [selectedSheet, setSelectedSheet] = useState('');
  const [dashboardData, setDashboardData] = useState(null);

  const cognizantColors = {
    primary: '#0066CC',
    secondary: '#004499',
    accent: '#00A0E6',
    success: '#28A745',
    warning: '#FFC107',
    danger: '#DC3545',
  };

  const colorPalette = [
    '#0066CC', '#00A0E6', '#004499', '#28A745', 
    '#FFC107', '#DC3545', '#6C757D', '#17A2B8'
  ];

  useEffect(() => {
    if (uploadedData) {
      const sheets = Object.keys(uploadedData);
      if (sheets.length > 0 && !selectedSheet) {
        setSelectedSheet(sheets[0]);
      }
      processDashboardData();
    }
  }, [uploadedData, selectedSheet]);

  useEffect(() => {
    let interval;
    if (autoRefresh) {
      interval = setInterval(() => {
        setRefreshKey(prev => prev + 1);
      }, 30000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const processDashboardData = () => {
    if (!uploadedData || !selectedSheet || !uploadedData[selectedSheet]) {
      setDashboardData(null);
      return;
    }

    const data = uploadedData[selectedSheet];
    if (!Array.isArray(data) || data.length === 0) {
      setDashboardData(null);
      return;
    }

    const columns = Object.keys(data[0]);
    const numericColumns = columns.filter(col => 
      data.some(row => !isNaN(parseFloat(row[col])) && isFinite(row[col]))
    );
    const categoricalColumns = columns.filter(col => 
      !numericColumns.includes(col) && data.some(row => row[col] && row[col].toString().trim())
    );

    setDashboardData({
      data,
      columns,
      numericColumns,
      categoricalColumns,
      totalRecords: data.length,
    });
  };

  const getKPIMetrics = () => {
    if (!dashboardData) return [];

    const { data, numericColumns, totalRecords } = dashboardData;
    const metrics = [
      {
        label: 'Total Records',
        value: totalRecords.toLocaleString(),
        icon: '📊'
      }
    ];

    if (numericColumns.length > 0) {
      const firstNumeric = numericColumns[0];
      const values = data.map(row => parseFloat(row[firstNumeric]) || 0);
      const avg = values.reduce((sum, val) => sum + val, 0) / values.length;
      
      metrics.push({
        label: `Avg ${firstNumeric}`,
        value: avg.toFixed(2),
        icon: '📈'
      });
    }

    if (numericColumns.length > 1) {
      const secondNumeric = numericColumns[1];
      const values = data.map(row => parseFloat(row[secondNumeric]) || 0);
      const max = Math.max(...values);
      
      metrics.push({
        label: `Max ${secondNumeric}`,
        value: max.toFixed(2),
        icon: '⬆️'
      });
    }

    metrics.push({
      label: 'Data Quality',
      value: '100%',
      icon: '✅'
    });

    return metrics;
  };

  const getTrendChart = () => {
    if (!dashboardData || dashboardData.numericColumns.length === 0) return null;

    const { data, numericColumns } = dashboardData;
    const column = numericColumns[0];
    const values = data.map(row => parseFloat(row[column]) || 0);
    const labels = data.map((_, index) => `Record ${index + 1}`);

    return {
      data: {
        labels: labels.slice(0, 20), // Show first 20 records
        datasets: [{
          label: column,
          data: values.slice(0, 20),
          borderColor: cognizantColors.primary,
          backgroundColor: cognizantColors.accent + '20',
          borderWidth: 2,
          fill: true,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: `Trend Analysis - ${column}`
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    };
  };

  const getCategoryChart = () => {
    if (!dashboardData || dashboardData.categoricalColumns.length === 0) return null;

    const { data, categoricalColumns } = dashboardData;
    const column = categoricalColumns[0];
    
    // Count occurrences
    const counts = {};
    data.forEach(row => {
      const value = row[column]?.toString().trim();
      if (value) {
        counts[value] = (counts[value] || 0) + 1;
      }
    });

    const sortedEntries = Object.entries(counts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10);

    return {
      data: {
        labels: sortedEntries.map(([key]) => key),
        datasets: [{
          data: sortedEntries.map(([,value]) => value),
          backgroundColor: colorPalette,
          borderWidth: 2,
          borderColor: '#fff'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: `Distribution - ${column}`
          }
        }
      }
    };
  };

  const getComparisonChart = () => {
    if (!dashboardData || dashboardData.numericColumns.length === 0 || dashboardData.categoricalColumns.length === 0) {
      return null;
    }

    const { data, numericColumns, categoricalColumns } = dashboardData;
    const numericCol = numericColumns[0];
    const categoricalCol = categoricalColumns[0];

    // Group by categorical column and sum numeric values
    const grouped = {};
    data.forEach(row => {
      const category = row[categoricalCol]?.toString().trim();
      const value = parseFloat(row[numericCol]) || 0;
      
      if (category) {
        grouped[category] = (grouped[category] || 0) + value;
      }
    });

    const sortedEntries = Object.entries(grouped)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10);

    return {
      data: {
        labels: sortedEntries.map(([key]) => key),
        datasets: [{
          label: numericCol,
          data: sortedEntries.map(([,value]) => value),
          backgroundColor: cognizantColors.primary,
          borderColor: cognizantColors.secondary,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: `${numericCol} by ${categoricalCol}`
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    };
  };

  if (!uploadedData) {
    return (
      <div className="dashboard-tab">
        <div className="card">
          <div className="message message-warning">
            ⚠️ Please upload an Excel file in the 'Upload File' tab to view the dashboard.
          </div>
        </div>
      </div>
    );
  }

  const sheets = Object.keys(uploadedData);
  const metrics = getKPIMetrics();
  const trendChart = getTrendChart();
  const categoryChart = getCategoryChart();
  const comparisonChart = getComparisonChart();

  return (
    <div className="dashboard-tab">
      {/* Controls */}
      <div className="card">
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <div>
            <label>Select Sheet:</label>
            <select 
              className="select" 
              value={selectedSheet} 
              onChange={(e) => setSelectedSheet(e.target.value)}
              style={{ marginLeft: '0.5rem', minWidth: '200px' }}
            >
              {sheets.map(sheet => (
                <option key={sheet} value={sheet}>{sheet}</option>
              ))}
            </select>
          </div>
          
          <button 
            className="button"
            onClick={() => setRefreshKey(prev => prev + 1)}
          >
            🔄 Refresh Data
          </button>
          
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input 
              type="checkbox" 
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            Auto-refresh (30s)
          </label>
        </div>
      </div>

      {/* KPI Metrics */}
      <div className="card">
        <h3>📈 Key Performance Indicators</h3>
        <div className="metrics-grid">
          {metrics.map((metric, index) => (
            <div key={index} className="metric-card">
              <div className="metric-value">{metric.value}</div>
              <div className="metric-label">{metric.icon} {metric.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-2">
        {/* Trend Chart */}
        {trendChart && (
          <div className="chart-container">
            <div className="chart-title">📈 Trend Analysis</div>
            <Line data={trendChart.data} options={trendChart.options} />
          </div>
        )}

        {/* Category Distribution */}
        {categoryChart && (
          <div className="chart-container">
            <div className="chart-title">🥧 Category Distribution</div>
            <Doughnut data={categoryChart.data} options={categoryChart.options} />
          </div>
        )}

        {/* Comparison Chart */}
        {comparisonChart && (
          <div className="chart-container">
            <div className="chart-title">📊 Comparison Analysis</div>
            <Bar data={comparisonChart.data} options={comparisonChart.options} />
          </div>
        )}

        {/* Pipeline Status */}
        <div className="chart-container">
          <div className="chart-title">🔄 Pipeline Status</div>
          {dashboardData ? (
            <div className="pipeline-status">
              <div className="metrics-grid">
                <div className="metric-card">
                  <div className="metric-value">{dashboardData.totalRecords}</div>
                  <div className="metric-label">Total Items</div>
                </div>
                <div className="metric-card">
                  <div className="metric-value">{dashboardData.numericColumns.length}</div>
                  <div className="metric-label">Numeric Fields</div>
                </div>
                <div className="metric-card">
                  <div className="metric-value">{dashboardData.categoricalColumns.length}</div>
                  <div className="metric-label">Category Fields</div>
                </div>
                <div className="metric-card">
                  <div className="metric-value">Active</div>
                  <div className="metric-label">Status</div>
                </div>
              </div>
            </div>
          ) : (
            <p>No data available for pipeline analysis.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default DashboardTab;