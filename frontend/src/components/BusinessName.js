import React, { useState, useEffect } from 'react';
import { Box, Typography, IconButton, TextField, Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';

const BusinessName = () => {
  const [businessName, setBusinessName] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [tempName, setTempName] = useState('');

  useEffect(() => {
    // Load business name from localStorage
    const savedName = localStorage.getItem('businessName') || 'KDRT Business Management';
    setBusinessName(savedName);
    setTempName(savedName);
  }, []);

  const handleOpenDialog = () => {
    setTempName(businessName);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSave = () => {
    if (tempName.trim()) {
      setBusinessName(tempName.trim());
      localStorage.setItem('businessName', tempName.trim());
      setOpenDialog(false);
    }
  };

  return (
    <>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Typography variant="h6" noWrap component="div">
          {businessName}
        </Typography>
        <IconButton
          size="small"
          onClick={handleOpenDialog}
          sx={{ 
            color: 'inherit',
            '&:hover': { backgroundColor: 'rgba(255, 255, 255, 0.1)' }
          }}
        >
          <EditIcon fontSize="small" />
        </IconButton>
      </Box>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Business Name</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Business Name"
            type="text"
            fullWidth
            variant="outlined"
            value={tempName}
            onChange={(e) => setTempName(e.target.value)}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSave} variant="contained">Save</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default BusinessName;
