import * as XLSX from 'xlsx';

// Sample data loader utility
export const loadSampleData = async () => {
  try {
    // Fetch the sample Excel file from attached_assets
    const response = await fetch('/attached_assets/AEM (1)_1755355780712.xlsx');
    if (!response.ok) {
      throw new Error('Failed to fetch sample data file');
    }
    
    const arrayBuffer = await response.arrayBuffer();
    const workbook = XLSX.read(arrayBuffer, { type: 'array' });
    
    const result = {};
    
    // Process each sheet in the workbook
    workbook.SheetNames.forEach(sheetName => {
      const worksheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(worksheet, { 
        header: 1,
        defval: '',
        raw: false
      });
      
      if (jsonData.length > 0) {
        // First row as headers
        const headers = jsonData[0];
        
        // Convert remaining rows to objects
        const data = jsonData.slice(1).map(row => {
          const obj = {};
          headers.forEach((header, index) => {
            obj[header] = row[index] || '';
          });
          return obj;
        }).filter(row => {
          // Filter out empty rows
          return Object.values(row).some(value => value && value.toString().trim());
        });
        
        if (data.length > 0) {
          result[sheetName] = data;
        }
      }
    });
    
    return result;
  } catch (error) {
    console.error('Error loading sample data:', error);
    return null;
  }
};

// Function to check if data is sample data (for UI indicators)
export const isSampleData = (data) => {
  if (!data) return false;
  
  // Check if it's the sample data by looking for specific characteristics
  const firstSheet = Object.keys(data)[0];
  if (!firstSheet || !data[firstSheet] || !Array.isArray(data[firstSheet])) {
    return false;
  }
  
  // You can add more specific checks here if needed
  return true;
};