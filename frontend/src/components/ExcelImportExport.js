import React from 'react';
import { Box, Button, Typography, Alert, CircularProgress } from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DownloadIcon from '@mui/icons-material/Download';
import { useState } from 'react';
import api from '../services/api';

const ExcelImportExport = ({ module, onImportSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState('');

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
      setError('Please upload an Excel file (.xlsx or .xls)');
      return;
    }

    setUploading(true);
    setError('');
    setUploadResult(null);

    const formData = new FormData();
    formData.append('file', file);

    // Check if online
    const isOnline = navigator.onLine;

    try {
      if (isOnline) {
        // Online: Upload directly
        const response = await api.post(`/excel/${module}/import`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        setUploadResult(response.data);
        
        // Call parent callback to refresh data
        if (onImportSuccess) {
          setTimeout(() => onImportSuccess(), 1000);
        }

        // Store in IndexedDB for offline access
        if ('indexedDB' in window) {
          const db = await openDB();
          await saveToIndexedDB(db, module, response.data);
        }
      } else {
        // Offline: Queue for later sync
        await queueForSync(file, module);
        setUploadResult({ 
          imported: 0, 
          updated: 0, 
          offline: true,
          message: 'File saved for upload when online' 
        });
      }

    } catch (err) {
      if (!navigator.onLine) {
        // If error due to being offline, queue it
        try {
          await queueForSync(file, module);
          setUploadResult({ 
            offline: true,
            message: 'File saved for upload when online' 
          });
        } catch (queueErr) {
          setError('Failed to queue file for offline sync');
        }
      } else {
        setError(err.response?.data?.error || 'Failed to upload file');
      }
    } finally {
      setUploading(false);
      event.target.value = ''; // Reset file input
    }
  };

  const handleExport = async () => {
    setDownloading(true);
    setError('');

    try {
      const response = await api.get(`/excel/${module}/export`, {
        responseType: 'blob',
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${module}_${new Date().toISOString().split('T')[0]}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

    } catch (err) {
      setError(err.response?.data?.error || 'Failed to download file');
    } finally {
      setDownloading(false);
    }
  };

  // IndexedDB functions for offline support
  const openDB = () => {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('KDRTBusinessDB', 1);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
      
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('imports')) {
          db.createObjectStore('imports', { keyPath: 'id', autoIncrement: true });
        }
      };
    });
  };

  const saveToIndexedDB = async (db, module, data) => {
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['imports'], 'readwrite');
      const store = transaction.objectStore('imports');
      
      const record = {
        module,
        data,
        timestamp: new Date().toISOString(),
      };
      
      const request = store.add(record);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  };

  // Queue file for upload when back online
  const queueForSync = async (file, module) => {
    return new Promise(async (resolve, reject) => {
      try {
        const db = await openDB();
        
        // Ensure pendingSync store exists
        if (!db.objectStoreNames.contains('pendingSync')) {
          db.close();
          reject(new Error('PendingSync store not available'));
          return;
        }
        
        // Read file as base64
        const reader = new FileReader();
        reader.onload = async (e) => {
          try {
            const transaction = db.transaction(['pendingSync'], 'readwrite');
            const store = transaction.objectStore('pendingSync');
            
            const token = localStorage.getItem('access_token');
            const record = {
              url: `/api/v1/excel/${module}/import`,
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${token}`
              },
              fileData: e.target.result,
              fileName: file.name,
              module,
              timestamp: new Date().toISOString(),
            };
            
            const request = store.add(record);
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
          } catch (error) {
            reject(error);
          }
        };
        
        reader.onerror = () => reject(new Error('Failed to read file'));
        reader.readAsDataURL(file);
      } catch (error) {
        reject(error);
      }
    });
  };

  return (
    <Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
      <Typography variant="h6" gutterBottom>
        Excel Import/Export
      </Typography>
      
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Button
          variant="contained"
          component="label"
          startIcon={uploading ? <CircularProgress size={20} color="inherit" /> : <UploadFileIcon />}
          disabled={uploading}
        >
          {uploading ? 'Uploading...' : 'Import Excel'}
          <input
            type="file"
            hidden
            accept=".xlsx,.xls"
            onChange={handleFileUpload}
          />
        </Button>

        <Button
          variant="outlined"
          startIcon={downloading ? <CircularProgress size={20} /> : <DownloadIcon />}
          onClick={handleExport}
          disabled={downloading}
        >
          {downloading ? 'Downloading...' : 'Export to Excel'}
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {uploadResult && (
        <Alert 
          severity={uploadResult.offline ? 'info' : uploadResult.errors && uploadResult.errors.length > 0 ? 'warning' : 'success'} 
          sx={{ mb: 2 }}
          onClose={() => setUploadResult(null)}
        >
          {uploadResult.offline ? (
            <>
              <Typography variant="body2">
                <strong>Offline Mode:</strong>
              </Typography>
              <Typography variant="body2">
                {uploadResult.message || 'File will be uploaded when connection is restored'}
              </Typography>
            </>
          ) : (
            <>
              <Typography variant="body2">
                <strong>Import Results:</strong>
              </Typography>
              {uploadResult.imported > 0 && (
                <Typography variant="body2">✓ Imported: {uploadResult.imported} records</Typography>
              )}
              {uploadResult.updated > 0 && (
                <Typography variant="body2">✓ Updated: {uploadResult.updated} records</Typography>
              )}
              {uploadResult.errors && uploadResult.errors.length > 0 && (
                <Box sx={{ mt: 1 }}>
                  <Typography variant="body2" color="error">
                    <strong>Errors:</strong>
                  </Typography>
                  {uploadResult.errors.slice(0, 5).map((err, idx) => (
                    <Typography key={idx} variant="caption" display="block">
                      • {err}
                    </Typography>
                  ))}
                  {uploadResult.errors.length > 5 && (
                    <Typography variant="caption" color="text.secondary">
                      ... and {uploadResult.errors.length - 5} more errors
                    </Typography>
                  )}
                </Box>
              )}
            </>
          )}
        </Alert>
      )}

      <Typography variant="caption" color="text.secondary" display="block">
        Upload Excel files (.xlsx or .xls) to bulk import data or export current data to Excel
      </Typography>
    </Box>
  );
};

export default ExcelImportExport;
