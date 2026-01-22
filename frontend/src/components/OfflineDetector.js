import React, { useState, useEffect } from 'react';
import { Snackbar, Alert, Box, Typography } from '@mui/material';
import WifiOffIcon from '@mui/icons-material/WifiOff';
import WifiIcon from '@mui/icons-material/Wifi';

const OfflineDetector = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [showNotification, setShowNotification] = useState(false);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      setShowNotification(true);
      
      // Trigger background sync when coming back online
      if ('serviceWorker' in navigator && 'sync' in ServiceWorkerRegistration.prototype) {
        navigator.serviceWorker.ready.then((registration) => {
          registration.sync.register('sync-data').catch((error) => {
            console.error('Background sync registration failed:', error);
          });
        });
      }
    };

    const handleOffline = () => {
      setIsOnline(false);
      setShowNotification(true);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const handleClose = () => {
    setShowNotification(false);
  };

  return (
    <>
      {/* Persistent offline indicator */}
      {!isOnline && (
        <Box
          sx={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bgcolor: 'warning.dark',
            color: 'warning.contrastText',
            py: 1,
            px: 2,
            zIndex: 9999,
            display: 'flex',
            alignItems: 'center',
            gap: 1,
          }}
        >
          <WifiOffIcon />
          <Typography variant="body2">
            You are currently offline. Changes will be synced when connection is restored.
          </Typography>
        </Box>
      )}

      {/* Notification snackbar */}
      <Snackbar
        open={showNotification}
        autoHideDuration={6000}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={handleClose}
          severity={isOnline ? 'success' : 'warning'}
          icon={isOnline ? <WifiIcon /> : <WifiOffIcon />}
          sx={{ width: '100%' }}
        >
          {isOnline
            ? 'Connection restored. Syncing offline changes...'
            : 'You are now offline. Data will be cached locally.'}
        </Alert>
      </Snackbar>
    </>
  );
};

export default OfflineDetector;
