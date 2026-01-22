import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Box, AppBar, Toolbar, Typography, IconButton, Drawer, List, ListItem, ListItemIcon, ListItemText, ListItemButton, Divider, Avatar, Menu, MenuItem, Tooltip, Chip } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import DashboardIcon from '@mui/icons-material/Dashboard';
import InventoryIcon from '@mui/icons-material/Inventory';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import ReceiptIcon from '@mui/icons-material/Receipt';
import PeopleIcon from '@mui/icons-material/People';
import AssessmentIcon from '@mui/icons-material/Assessment';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import CategoryIcon from '@mui/icons-material/Category';
import LockIcon from '@mui/icons-material/Lock';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import BusinessName from '../BusinessName';

const drawerWidth = 240;

const Layout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();
  const { user, logout, hasRole } = useAuth();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/', roles: ['admin', 'operations_manager', 'finance_manager'] },
    { text: 'Product/Service Listing', icon: <CategoryIcon />, path: '/products', roles: ['admin', 'operations_manager'] },
    { text: 'Inventory Management', icon: <InventoryIcon />, path: '/inventory', roles: ['admin', 'operations_manager'] },
    { text: 'Sales Management', icon: <ShoppingCartIcon />, path: '/sales', roles: ['admin', 'operations_manager'] },
    { text: 'Payroll Management', icon: <PeopleIcon />, path: '/payroll', roles: ['admin', 'finance_manager'] },
    { text: 'Financial Management', icon: <AssessmentIcon />, path: '/financial', roles: ['admin', 'finance_manager'] },
  ];

  const isAdmin = user?.role === 'admin';

  const getRoleDisplayName = (role) => {
    switch (role) {
      case 'admin': return 'Administrator';
      case 'operations_manager': return 'Operations Manager';
      case 'finance_manager': return 'Chief Finance Manager';
      default: return 'Employee';
    }
  };

  const drawer = (
    <div>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
          <ReceiptIcon sx={{ mr: 1 }} />
          <Typography variant="h6" noWrap>
            KDRT
          </Typography>
        </Box>
      </Toolbar>
      <Divider />
      <Box sx={{ p: 2 }}>
        <Chip 
          label={getRoleDisplayName(user?.role)} 
          color={isAdmin ? 'primary' : 'default'} 
          size="small"
          sx={{ width: '100%' }}
        />
      </Box>
      <Divider />
      <List>
        {menuItems.map((item) => {
          const hasAccess = hasRole(item.roles);
          return (
            <ListItem key={item.text} disablePadding>
              <Tooltip 
                title={hasAccess ? '' : 'Access restricted for your role'} 
                placement="right"
              >
                <span style={{ width: '100%' }}>
                  <ListItemButton 
                    onClick={() => hasAccess && navigate(item.path)}
                    disabled={!hasAccess}
                    sx={{
                      opacity: hasAccess ? 1 : 0.5,
                      '&.Mui-disabled': {
                        opacity: 0.5,
                        backgroundColor: 'rgba(0, 0, 0, 0.12)',
                      }
                    }}
                  >
                    <ListItemIcon sx={{ opacity: hasAccess ? 1 : 0.5 }}>
                      {hasAccess ? item.icon : <LockIcon />}
                    </ListItemIcon>
                    <ListItemText 
                      primary={item.text} 
                      sx={{ opacity: hasAccess ? 1 : 0.5 }}
                    />
                  </ListItemButton>
                </span>
              </Tooltip>
            </ListItem>
          );
        })}
      </List>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton onClick={() => navigate('/settings')}>
            <ListItemIcon><SettingsIcon /></ListItemIcon>
            <ListItemText primary="Settings" />
          </ListItemButton>
        </ListItem>
        {isAdmin && (
          <ListItem disablePadding>
            <ListItemButton onClick={() => navigate('/tab-permissions')}>
              <ListItemIcon><AdminPanelSettingsIcon /></ListItemIcon>
              <ListItemText primary="Tab Permissions" />
            </ListItemButton>
          </ListItem>
        )}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex', width: '100%' }}>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Box sx={{ flexGrow: 1 }}>
            <BusinessName />
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography variant="body2" sx={{ mr: 2 }}>
              {user?.first_name} {user?.last_name}
            </Typography>
            <IconButton onClick={handleMenuOpen} color="inherit">
              <Avatar sx={{ width: 32, height: 32 }}>
                {user?.first_name?.[0]}{user?.last_name?.[0]}
              </Avatar>
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
            >
              <MenuItem onClick={() => { handleMenuClose(); navigate('/settings'); }}>
                <SettingsIcon fontSize="small" sx={{ mr: 1 }} />
                Settings
              </MenuItem>
              <MenuItem onClick={handleLogout}>
                <LogoutIcon fontSize="small" sx={{ mr: 1 }} />
                Logout
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>

      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8,
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default Layout;
