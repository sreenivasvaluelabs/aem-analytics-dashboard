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

function DashboardTab({ uploadedData, isSampleData }) {
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

    const { data, categoricalColumns, totalRecords } = dashboardData;
    const metrics = [
      {
        label: 'Total Employees',
        value: totalRecords.toLocaleString(),
        icon: '👥'
      }
    ];

    // Count unique competencies
    if (categoricalColumns.length > 0) {
      const competencyCol = categoricalColumns.find(col => 
        col.toLowerCase().includes('competency') || 
        col.toLowerCase().includes('skill') ||
        col.toLowerCase().includes('technology')
      ) || categoricalColumns[0];
      
      const uniqueCompetencies = new Set(data.map(row => row[competencyCol]).filter(val => val && val.toString().trim()));
      
      metrics.push({
        label: 'Unique Competencies',
        value: uniqueCompetencies.size.toString(),
        icon: '🎯'
      });
    }

    // Count active projects or roles
    if (categoricalColumns.length > 1) {
      const roleCol = categoricalColumns.find(col => 
        col.toLowerCase().includes('role') || 
        col.toLowerCase().includes('position') ||
        col.toLowerCase().includes('title')
      ) || categoricalColumns[1];
      
      const uniqueRoles = new Set(data.map(row => row[roleCol]).filter(val => val && val.toString().trim()));
      
      metrics.push({
        label: 'Active Roles',
        value: uniqueRoles.size.toString(),
        icon: '💼'
      });
    }

    metrics.push({
      label: 'System Status',
      value: 'Online',
      icon: '✅'
    });

    return metrics;
  };

  const getCompetencyChart = () => {
    if (!dashboardData || dashboardData.categoricalColumns.length === 0) return null;

    const { data, categoricalColumns } = dashboardData;
    
    // Find competency-related column
    const competencyCol = categoricalColumns.find(col => 
      col.toLowerCase().includes('competency') || 
      col.toLowerCase().includes('skill') ||
      col.toLowerCase().includes('technology') ||
      col.toLowerCase().includes('expertise')
    ) || categoricalColumns[0];
    
    // Count competency occurrences
    const counts = {};
    data.forEach(row => {
      const value = row[competencyCol]?.toString().trim();
      if (value) {
        counts[value] = (counts[value] || 0) + 1;
      }
    });

    const sortedEntries = Object.entries(counts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 8);

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
            text: 'Competency Distribution'
          },
          legend: {
            position: 'bottom'
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

  const getPrimarySkillChart = () => {
    if (!dashboardData || dashboardData.categoricalColumns.length === 0) {
      return null;
    }

    const { data, categoricalColumns } = dashboardData;
    
    // Find primary skill column
    const skillCol = categoricalColumns.find(col => 
      col.toLowerCase().includes('primary') || 
      col.toLowerCase().includes('skill') ||
      col.toLowerCase().includes('main') ||
      col.toLowerCase().includes('core')
    ) || categoricalColumns[1] || categoricalColumns[0];

    // Count skill occurrences
    const skillCounts = {};
    data.forEach(row => {
      const skill = row[skillCol]?.toString().trim();
      if (skill) {
        skillCounts[skill] = (skillCounts[skill] || 0) + 1;
      }
    });

    const sortedSkills = Object.entries(skillCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10);

    return {
      data: {
        labels: sortedSkills.map(([key]) => key),
        datasets: [{
          label: 'Employee Count',
          data: sortedSkills.map(([,value]) => value),
          backgroundColor: colorPalette[0],
          borderColor: cognizantColors.secondary,
          borderWidth: 1,
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Primary Skill Distribution'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Number of Employees'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Primary Skills'
            }
          }
        },
        indexAxis: 'x'
      }
    };
  };

  if (!uploadedData) {
    return (
      <div className="dashboard-tab">
        <div className="card">
          <div className="message message-warning">
            ⚠️ Loading dashboard data...
          </div>
        </div>
      </div>
    );
  }

  const sheets = Object.keys(uploadedData);
  const metrics = getKPIMetrics();
  const competencyChart = getCompetencyChart();
  const categoryChart = getCategoryChart();
  const primarySkillChart = getPrimarySkillChart();

  return (
    <div className="dashboard-tab">
      {/* Controls */}
      <div className="card">
        {isSampleData && (
          <div style={{ 
            backgroundColor: '#e3f2fd', 
            padding: '0.5rem 1rem', 
            borderRadius: '4px', 
            marginBottom: '1rem',
            fontSize: '0.9rem',
            color: '#1976d2'
          }}>
            📋 Sample Data Preview - Upload your own Excel file to replace this data
          </div>
        )}
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
        {/* Competency Distribution Chart */}
        {competencyChart && (
          <div className="chart-container">
            <div className="chart-title">🎯 Competency Distribution</div>
            <Pie data={competencyChart.data} options={competencyChart.options} />
          </div>
        )}

        {/* Category Distribution */}
        {categoryChart && (
          <div className="chart-container">
            <div className="chart-title">🥧 Category Distribution</div>
            <Doughnut data={categoryChart.data} options={categoryChart.options} />
          </div>
        )}

        {/* Primary Skill Chart */}
        {primarySkillChart && (
          <div className="chart-container">
            <div className="chart-title">💼 Primary Skill Analysis</div>
            <Bar data={primarySkillChart.data} options={primarySkillChart.options} />
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