import React, { useState } from 'react';
import UploadTab from './components/UploadTab.jsx';
import DashboardTab from './components/DashboardTab.jsx';
import DataTableTab from './components/DataTableTab.jsx';

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [uploadedData, setUploadedData] = useState(null);
  const [lastUploadTime, setLastUploadTime] = useState(null);

  const tabs = [
    { id: 'upload', label: '📁 Upload File', icon: '📁' },
    { id: 'dashboard', label: '📊 Dashboard', icon: '📊' },
    { id: 'data-table', label: '📋 Data Table', icon: '📋' }
  ];

  const handleDataUpload = (data) => {
    setUploadedData(data);
    setLastUploadTime(new Date());
  };

  return (
    <div className="App">
      {/* Header */}
      <div className="header">
        <h1>📊 Cognizant Analytics Dashboard</h1>
        <p>Professional Data Analytics for Demand/Supply/TAG Pipeline Analysis</p>
      </div>

      {/* Main Container */}
      <div className="container">
        {/* Tab Navigation */}
        <div className="tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'upload' && (
            <UploadTab
              onDataUpload={handleDataUpload}
              uploadedData={uploadedData}
              lastUploadTime={lastUploadTime}
            />
          )}
          
          {activeTab === 'dashboard' && (
            <DashboardTab
              uploadedData={uploadedData}
            />
          )}
          
          {activeTab === 'data-table' && (
            <DataTableTab
              uploadedData={uploadedData}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;