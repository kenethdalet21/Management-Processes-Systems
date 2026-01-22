import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import App from './App';
import { AuthProvider } from './context/AuthContext';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#3f51b5',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#0a1929',
      paper: '#1e2a3a',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <AuthProvider>
          <App />
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
);

// Properly unregister all service workers and clear cache (development only)
if (process.env.NODE_ENV === 'development' && 'serviceWorker' in navigator) {
  navigator.serviceWorker.getRegistrations().then((registrations) => {
    for (let registration of registrations) {
      registration.unregister().then((success) => {
        if (success) {
          console.log('Service Worker unregistered successfully');
        }
      });
    }
  }).catch((error) => {
    console.error('Error unregistering service workers:', error);
  });
  
  // Clear all service worker caches
  if ('caches' in window) {
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          console.log('Deleting cache:', cacheName);
          return caches.delete(cacheName);
        })
      );
    }).catch((error) => {
      console.error('Error clearing caches:', error);
    });
  }
}

// Initialize IndexedDB for offline storage and sync
if ('indexedDB' in window) {
  const dbRequest = indexedDB.open('KDRTBusinessDB', 1);
  
  dbRequest.onupgradeneeded = (event) => {
    const db = event.target.result;
    
    // Create object stores if they don't exist
    if (!db.objectStoreNames.contains('imports')) {
      db.createObjectStore('imports', { keyPath: 'id', autoIncrement: true });
    }
    
    if (!db.objectStoreNames.contains('pendingSync')) {
      db.createObjectStore('pendingSync', { keyPath: 'id', autoIncrement: true });
    }
    
    if (!db.objectStoreNames.contains('offlineData')) {
      db.createObjectStore('offlineData', { keyPath: 'key' });
    }
  };
  
  dbRequest.onsuccess = () => {
    console.log('IndexedDB initialized successfully');
    
    // Try to sync any pending data when coming online
    window.addEventListener('online', () => {
      syncPendingData();
    });
  };
  
  dbRequest.onerror = (error) => {
    console.error('IndexedDB initialization failed:', error);
  };
}

// Function to sync pending data when back online
async function syncPendingData() {
  if (!('indexedDB' in window)) return;
  
  try {
    const db = await new Promise((resolve, reject) => {
      const request = indexedDB.open('KDRTBusinessDB', 1);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
    
    if (!db.objectStoreNames.contains('pendingSync')) {
      return;
    }
    
    const transaction = db.transaction(['pendingSync'], 'readonly');
    const store = transaction.objectStore('pendingSync');
    const getAllRequest = store.getAll();
    
    getAllRequest.onsuccess = async () => {
      const pendingItems = getAllRequest.result;
      
      if (pendingItems.length === 0) {
        console.log('No pending items to sync');
        return;
      }
      
      console.log(`Syncing ${pendingItems.length} pending items...`);
      
      for (const item of pendingItems) {
        try {
          // Convert base64 file data back to FormData
          const formData = new FormData();
          
          if (item.fileData) {
            // Convert base64 back to blob
            const response = await fetch(item.fileData);
            const blob = await response.blob();
            const file = new File([blob], item.fileName, { type: blob.type });
            formData.append('file', file);
          } else if (item.body) {
            formData.append('data', item.body);
          }
          
          const apiUrl = `http://localhost:5000${item.url}`;
          const uploadResponse = await fetch(apiUrl, {
            method: item.method,
            headers: item.headers,
            body: formData
          });
          
          if (uploadResponse.ok) {
            // Remove from pending sync after successful upload
            const deleteTransaction = db.transaction(['pendingSync'], 'readwrite');
            const deleteStore = deleteTransaction.objectStore('pendingSync');
            deleteStore.delete(item.id);
            console.log('Synced item:', item.id);
            
            // Show success notification
            alert(`Successfully synced offline file: ${item.fileName || 'data'}`);
          } else {
            console.error('Failed to sync item:', item.id, uploadResponse.statusText);
          }
        } catch (error) {
          console.error('Failed to sync item:', item.id, error);
        }
      }
      
      console.log('Sync completed');
      
      // Reload page to refresh data
      if (pendingItems.length > 0) {
        setTimeout(() => window.location.reload(), 2000);
      }
    };
    
    getAllRequest.onerror = () => {
      console.error('Failed to get pending items');
    };
  } catch (error) {
    console.error('Error during sync:', error);
  }
}
