import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Container,
  Paper,
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Checkbox,
  Button,
  Alert,
  CircularProgress,
  Chip
} from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';

const AVAILABLE_TABS = [
  { name: 'products', label: 'Products & Services' },
  { name: 'inventory', label: 'Inventory' },
  { name: 'sales', label: 'Sales' },
  { name: 'payroll', label: 'Payroll' },
  { name: 'financial', label: 'Financial Reports' }
];

function TabPermissions() {
  const [users, setUsers] = useState([]);
  const [permissions, setPermissions] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');
      const config = {
        headers: { Authorization: `Bearer ${token}` }
      };

      // Load users and permissions in parallel
      const [usersRes, permsRes] = await Promise.all([
        axios.get('http://127.0.0.1:5000/api/v1/settings/users', config),
        axios.get('http://127.0.0.1:5000/api/v1/settings/tab-permissions', config)
      ]);

      setUsers(usersRes.data);

      // Organize permissions by user and tab
      const permMap = {};
      permsRes.data.forEach(perm => {
        if (!permMap[perm.user_id]) {
          permMap[perm.user_id] = {};
        }
        permMap[perm.user_id][perm.tab_name] = perm.is_locked;
      });
      setPermissions(permMap);
    } catch (err) {
      console.error('Error loading data:', err);
      setError(err.response?.data?.error || 'Failed to load settings data');
    } finally {
      setLoading(false);
    }
  };

  const handleTogglePermission = (userId, tabName) => {
    setPermissions(prev => ({
      ...prev,
      [userId]: {
        ...(prev[userId] || {}),
        [tabName]: !(prev[userId]?.[tabName] || false)
      }
    }));
  };

  const handleSavePermissions = async (userId) => {
    try {
      setSaving(true);
      setError(null);
      setSuccess(null);

      const token = localStorage.getItem('token');
      const config = {
        headers: { Authorization: `Bearer ${token}` }
      };

      // Prepare tab permissions for this user
      const tabPermissions = AVAILABLE_TABS.map(tab => ({
        tab_name: tab.name,
        is_locked: permissions[userId]?.[tab.name] || false
      }));

      await axios.post(
        'http://127.0.0.1:5000/api/v1/settings/tab-permissions/bulk',
        {
          user_id: userId,
          tab_permissions: tabPermissions
        },
        config
      );

      setSuccess('Permissions saved successfully');
      setTimeout(() => setSuccess(null), 3000);
      
      // Reload to sync with backend
      await loadData();
    } catch (err) {
      console.error('Error saving permissions:', err);
      setError(err.response?.data?.error || 'Failed to save permissions');
    } finally {
      setSaving(false);
    }
  };

  const getUserRole = (role) => {
    const roleMap = {
      'ADMIN': { label: 'Administrator', color: 'error' },
      'OPERATIONS_MANAGER': { label: 'Operations Manager', color: 'primary' },
      'FINANCE_MANAGER': { label: 'Finance Manager', color: 'success' },
      'EMPLOYEE': { label: 'Employee', color: 'default' }
    };
    return roleMap[role] || { label: role, color: 'default' };
  };

  const getLockedTabsCount = (userId) => {
    const userPerms = permissions[userId] || {};
    return Object.values(userPerms).filter(locked => locked).length;
  };

  if (loading) {
    return (
      <Container>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        User Tab Permissions
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      <Paper sx={{ p: 3 }}>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Lock tabs to restrict access for specific users. Locked tabs will be hidden from the user's navigation menu.
        </Typography>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 600 }}>User</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>Role</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>Email</TableCell>
                {AVAILABLE_TABS.map(tab => (
                  <TableCell key={tab.name} align="center" sx={{ fontWeight: 600 }}>
                    {tab.label}
                  </TableCell>
                ))}
                <TableCell align="center" sx={{ fontWeight: 600 }}>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map(user => {
                const roleInfo = getUserRole(user.role);
                const lockedCount = getLockedTabsCount(user.id);
                
                return (
                  <TableRow key={user.id} hover>
                    <TableCell>
                      <Box>
                        <Typography variant="body1">
                          {user.first_name} {user.last_name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          @{user.username}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={roleInfo.label} 
                        color={roleInfo.color} 
                        size="small" 
                      />
                    </TableCell>
                    <TableCell>{user.email}</TableCell>
                    {AVAILABLE_TABS.map(tab => {
                      const isLocked = permissions[user.id]?.[tab.name] || false;
                      return (
                        <TableCell key={tab.name} align="center">
                          <Checkbox
                            checked={isLocked}
                            onChange={() => handleTogglePermission(user.id, tab.name)}
                            icon={<LockOpenIcon />}
                            checkedIcon={<LockIcon />}
                            color="error"
                          />
                        </TableCell>
                      );
                    })}
                    <TableCell align="center">
                      <Button
                        variant="contained"
                        size="small"
                        onClick={() => handleSavePermissions(user.id)}
                        disabled={saving}
                      >
                        Save
                      </Button>
                      {lockedCount > 0 && (
                        <Typography variant="caption" display="block" color="text.secondary" sx={{ mt: 0.5 }}>
                          {lockedCount} tab{lockedCount > 1 ? 's' : ''} locked
                        </Typography>
                      )}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>

        {users.length === 0 && (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography color="text.secondary">
              No users found. Only non-admin users can have tab permissions assigned.
            </Typography>
          </Box>
        )}
      </Paper>
    </Container>
  );
}

export default TabPermissions;
