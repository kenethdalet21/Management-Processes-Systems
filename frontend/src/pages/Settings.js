import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  TextField, 
  Button, 
  Alert, 
  Divider,
  Grid,
  Card,
  CardContent,
  Chip
} from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import PersonIcon from '@mui/icons-material/Person';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

const Settings = () => {
  const { user } = useAuth();
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState({ type: '', text: '' });
  const [loading, setLoading] = useState(false);

  const getRoleDisplayName = (role) => {
    switch (role) {
      case 'admin': return 'Administrator';
      case 'operations_manager': return 'Operations Manager';
      case 'finance_manager': return 'Chief Finance Manager';
      default: return 'Employee';
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'admin': return 'primary';
      case 'operations_manager': return 'success';
      case 'finance_manager': return 'warning';
      default: return 'default';
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setMessage({ type: '', text: '' });

    if (newPassword !== confirmPassword) {
      setMessage({ type: 'error', text: 'New passwords do not match' });
      return;
    }

    if (newPassword.length < 6) {
      setMessage({ type: 'error', text: 'Password must be at least 6 characters' });
      return;
    }

    setLoading(true);
    try {
      await api.put('/auth/change-password', {
        old_password: oldPassword,
        new_password: newPassword
      });
      setMessage({ type: 'success', text: 'Password changed successfully' });
      setOldPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.error || 'Failed to change password' 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Settings</Typography>
      
      <Grid container spacing={3}>
        {/* User Profile Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <PersonIcon sx={{ mr: 1 }} />
                <Typography variant="h6">User Profile</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Typography variant="caption" color="text.secondary">Username</Typography>
                  <Typography variant="body1">{user?.username}</Typography>
                </Box>
                <Box>
                  <Typography variant="caption" color="text.secondary">Full Name</Typography>
                  <Typography variant="body1">{user?.first_name} {user?.last_name}</Typography>
                </Box>
                <Box>
                  <Typography variant="caption" color="text.secondary">Email</Typography>
                  <Typography variant="body1">{user?.email}</Typography>
                </Box>
                <Box>
                  <Typography variant="caption" color="text.secondary">Role</Typography>
                  <Box sx={{ mt: 0.5 }}>
                    <Chip 
                      label={getRoleDisplayName(user?.role)} 
                      color={getRoleColor(user?.role)}
                      size="small"
                    />
                  </Box>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Change Password Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <LockIcon sx={{ mr: 1 }} />
                <Typography variant="h6">Change Password</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              
              {message.text && (
                <Alert severity={message.type} sx={{ mb: 2 }}>
                  {message.text}
                </Alert>
              )}
              
              <form onSubmit={handleChangePassword}>
                <TextField
                  fullWidth
                  label="Current Password"
                  type="password"
                  value={oldPassword}
                  onChange={(e) => setOldPassword(e.target.value)}
                  margin="normal"
                  required
                />
                <TextField
                  fullWidth
                  label="New Password"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  margin="normal"
                  required
                  helperText="Minimum 6 characters"
                />
                <TextField
                  fullWidth
                  label="Confirm New Password"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  margin="normal"
                  required
                />
                <Button
                  type="submit"
                  variant="contained"
                  fullWidth
                  sx={{ mt: 2 }}
                  disabled={loading}
                >
                  {loading ? 'Changing Password...' : 'Change Password'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </Grid>

        {/* Access Permissions Info */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Access Permissions</Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, backgroundColor: 'primary.dark' }}>
                    <Typography variant="subtitle1" fontWeight="bold">Administrator</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Full access to all modules:
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                      <Chip label="Dashboard" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Products" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Inventory" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Sales" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Payroll" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Financial" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Settings" size="small" sx={{ m: 0.25 }} />
                    </Box>
                  </Paper>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, backgroundColor: 'success.dark' }}>
                    <Typography variant="subtitle1" fontWeight="bold">Operations Manager</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Access to operations modules:
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                      <Chip label="Dashboard" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Products" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Inventory" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Sales" size="small" sx={{ m: 0.25 }} />
                    </Box>
                  </Paper>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, backgroundColor: 'warning.dark' }}>
                    <Typography variant="subtitle1" fontWeight="bold">Chief Finance Manager</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Access to finance modules:
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                      <Chip label="Dashboard" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Payroll" size="small" sx={{ m: 0.25 }} />
                      <Chip label="Financial" size="small" sx={{ m: 0.25 }} />
                    </Box>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings;
