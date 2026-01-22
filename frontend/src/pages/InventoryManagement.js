import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Paper, Button, TextField, Dialog, DialogTitle, DialogContent,
  DialogActions, Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Chip, Alert, Grid, Card, CardContent, Tabs, Tab, TablePagination, MenuItem, Select,
  FormControl, InputLabel, Checkbox, IconButton
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import DeleteIcon from '@mui/icons-material/Delete';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import InventoryIcon from '@mui/icons-material/Inventory';
import WarningIcon from '@mui/icons-material/Warning';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import api from '../services/api';

const InventoryManagement = () => {
  const [tabValue, setTabValue] = useState(0);
  const [products, setProducts] = useState([]);
  const [logs, setLogs] = useState([]);
  const [lowStock, setLowStock] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [total, setTotal] = useState(0);
  const [selected, setSelected] = useState([]);
  
  const [openStockIn, setOpenStockIn] = useState(false);
  const [openStockOut, setOpenStockOut] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState('');
  const [quantity, setQuantity] = useState('');
  const [notes, setNotes] = useState('');
  const [reference, setReference] = useState('');

  useEffect(() => {
    fetchProducts();
    fetchLogs();
    fetchLowStock();
    fetchAnalysis();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, rowsPerPage]);

  const fetchProducts = async () => {
    try {
      const response = await api.get('/inventory/products');
      setProducts(response.data);
    } catch (err) {
      console.error('Failed to fetch products');
    }
  };

  const fetchLogs = async () => {
    try {
      const response = await api.get(`/inventory/logs?page=${page + 1}&per_page=${rowsPerPage}`);
      setLogs(response.data.logs);
      setTotal(response.data.total);
    } catch (err) {
      setError('Failed to fetch inventory logs');
    }
  };

  const fetchLowStock = async () => {
    try {
      const response = await api.get('/inventory/low-stock');
      setLowStock(response.data);
    } catch (err) {
      console.error('Failed to fetch low stock items');
    }
  };

  const fetchAnalysis = async () => {
    try {
      const response = await api.get('/inventory/analysis');
      setAnalysis(response.data);
    } catch (err) {
      console.error('Failed to fetch analysis');
    }
  };

  const handleStockIn = async () => {
    try {
      await api.post('/inventory/stock-in', {
        product_id: selectedProduct,
        quantity: parseInt(quantity),
        notes: notes,
        reference_number: reference
      });
      setSuccess('Stock added successfully');
      handleCloseDialog();
      fetchLogs(); fetchProducts(); fetchLowStock(); fetchAnalysis();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add stock');
    }
  };

  const handleStockOut = async () => {
    try {
      await api.post('/inventory/stock-out', {
        product_id: selectedProduct,
        quantity: parseInt(quantity),
        notes: notes,
        reference_number: reference
      });
      setSuccess('Stock removed successfully');
      handleCloseDialog();
      fetchLogs(); fetchProducts(); fetchLowStock(); fetchAnalysis();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to remove stock');
    }
  };

  const handleCloseDialog = () => {
    setOpenStockIn(false); setOpenStockOut(false);
    setSelectedProduct(''); setQuantity(''); setNotes(''); setReference('');
  };

  const handleDeleteLog = async (id) => {
    if (window.confirm('Are you sure you want to delete this inventory log?')) {
      try {
        await api.delete(`/inventory/logs/${id}`);
        setSuccess('Inventory log deleted successfully');
        fetchLogs();
        fetchProducts();
        fetchAnalysis();
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to delete log');
      }
    }
  };

  const handleSelectAll = (event) => {
    if (event.target.checked) {
      const newSelected = logs.map((log) => log.id);
      setSelected(newSelected);
    } else {
      setSelected([]);
    }
  };

  const handleSelectOne = (id) => {
    const selectedIndex = selected.indexOf(id);
    let newSelected = [];
    if (selectedIndex === -1) {
      newSelected = [...selected, id];
    } else {
      newSelected = selected.filter((selectedId) => selectedId !== id);
    }
    setSelected(newSelected);
  };

  const handleBulkDelete = async () => {
    if (selected.length === 0) {
      setError('Please select items to delete');
      return;
    }
    if (window.confirm(`Are you sure you want to delete ${selected.length} selected inventory log(s)?`)) {
      try {
        await Promise.all(selected.map(id => api.delete(`/inventory/logs/${id}`)));
        setSuccess(`Successfully deleted ${selected.length} inventory log(s)`);
        setSelected([]);
        fetchLogs();
        fetchProducts();
        fetchAnalysis();
      } catch (err) {
        setError('Failed to delete some inventory logs');
      }
    }
  };

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#0088FE'];
  const categoryData = analysis?.by_category?.map(cat => ({ name: cat.category || 'Uncategorized', value: cat.total_value })) || [];
  const movementData = analysis?.recent_movement?.slice(0, 10).map(item => ({ name: item.product.substring(0, 10), in: item.stock_in, out: item.stock_out })) || [];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Inventory Management</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>{success}</Alert>}

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} md={3}>
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Total Products</Typography><Typography variant="h5">{analysis?.total_products || 0}</Typography></Box>
            <InventoryIcon color="primary" />
          </Box></CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Total Units</Typography><Typography variant="h5">{analysis?.total_units || 0}</Typography></Box>
            <TrendingUpIcon color="success" />
          </Box></CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Total Value</Typography><Typography variant="h5">₱{(analysis?.total_value || 0).toFixed(2)}</Typography></Box>
            <TrendingUpIcon color="info" />
          </Box></CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card sx={{ bgcolor: lowStock.length > 0 ? 'warning.dark' : 'inherit' }}><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Low Stock Alerts</Typography><Typography variant="h5">{lowStock.length}</Typography></Box>
            <WarningIcon color="warning" />
          </Box></CardContent></Card>
        </Grid>
      </Grid>

      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Button variant="contained" color="success" startIcon={<AddIcon />} onClick={() => setOpenStockIn(true)}>Stock In</Button>
        <Button variant="contained" color="error" startIcon={<RemoveIcon />} onClick={() => setOpenStockOut(true)}>Stock Out</Button>
        {selected.length > 0 && (
          <Button 
            variant="contained" 
            color="error" 
            startIcon={<DeleteSweepIcon />} 
            onClick={handleBulkDelete}
          >
            Delete Selected ({selected.length})
          </Button>
        )}
      </Box>

      <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)} sx={{ mb: 2 }}>
        <Tab label="Inventory Log" /><Tab label="Low Stock Alerts" /><Tab label="Analytics" />
      </Tabs>

      {tabValue === 0 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead><TableRow>
              <TableCell padding="checkbox">
                <Checkbox
                  indeterminate={selected.length > 0 && selected.length < logs.length}
                  checked={logs.length > 0 && selected.length === logs.length}
                  onChange={handleSelectAll}
                />
              </TableCell>
              <TableCell>Date</TableCell><TableCell>Product</TableCell><TableCell>Type</TableCell>
              <TableCell align="right">Quantity</TableCell><TableCell align="right">Balance</TableCell>
              <TableCell>Reference</TableCell><TableCell>Notes</TableCell><TableCell>Status</TableCell><TableCell align="center">Actions</TableCell>
            </TableRow></TableHead>
            <TableBody>
              {logs.map((log) => {
                const isSelected = selected.indexOf(log.id) !== -1;
                return (
                  <TableRow key={log.id} selected={isSelected}>
                    <TableCell padding="checkbox">
                      <Checkbox
                        checked={isSelected}
                        onChange={() => handleSelectOne(log.id)}
                      />
                    </TableCell>
                    <TableCell>{new Date(log.created_at).toLocaleDateString()}</TableCell>
                  <TableCell>{log.product?.name || 'Unknown'}</TableCell>
                  <TableCell><Chip label={log.type} size="small" color={log.type === 'stock_in' ? 'success' : 'error'} icon={log.type === 'stock_in' ? <TrendingUpIcon /> : <TrendingDownIcon />} /></TableCell>
                  <TableCell align="right">{log.quantity}</TableCell>
                  <TableCell align="right">{log.balance_after}</TableCell>
                  <TableCell>{log.reference_number || '-'}</TableCell>
                  <TableCell>{log.notes || '-'}</TableCell>
                  <TableCell><Chip label={log.status} size="small" color={log.status === 'completed' ? 'success' : 'warning'} /></TableCell>
                  <TableCell align="center">
                    <IconButton size="small" color="error" onClick={() => handleDeleteLog(log.id)}><DeleteIcon /></IconButton>
                  </TableCell>
                </TableRow>
              );
              })}
            </TableBody>
          </Table>
          <TablePagination component="div" count={total} page={page} onPageChange={(e, newPage) => setPage(newPage)} rowsPerPage={rowsPerPage} onRowsPerPageChange={(e) => { setRowsPerPage(parseInt(e.target.value, 10)); setPage(0); }} />
        </TableContainer>
      )}

      {tabValue === 1 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead><TableRow><TableCell>SKU</TableCell><TableCell>Product Name</TableCell><TableCell align="right">Current Stock</TableCell><TableCell align="right">Threshold</TableCell><TableCell>Status</TableCell><TableCell>Action</TableCell></TableRow></TableHead>
            <TableBody>
              {lowStock.length === 0 ? <TableRow><TableCell colSpan={6} align="center">No low stock alerts</TableCell></TableRow> : lowStock.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.sku}</TableCell><TableCell>{item.name}</TableCell>
                  <TableCell align="right">{item.current_stock}</TableCell><TableCell align="right">{item.low_stock_threshold}</TableCell>
                  <TableCell><Chip label={item.current_stock === 0 ? 'Out of Stock' : 'Low Stock'} size="small" color={item.current_stock === 0 ? 'error' : 'warning'} /></TableCell>
                  <TableCell><Button size="small" variant="outlined" onClick={() => { setSelectedProduct(item.id); setOpenStockIn(true); }}>Restock</Button></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {tabValue === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}><Typography variant="h6" gutterBottom>Value by Category</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart><Pie data={categoryData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} label>
                  {categoryData.map((entry, index) => (<Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />))}
                </Pie><ChartTooltip /></PieChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}><Typography variant="h6" gutterBottom>Stock Movement (Top 10)</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={movementData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis /><ChartTooltip />
                  <Bar dataKey="in" fill="#82ca9d" name="Stock In" /><Bar dataKey="out" fill="#ff8042" name="Stock Out" />
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        </Grid>
      )}

      <Dialog open={openStockIn} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Stock In</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}><FormControl fullWidth><InputLabel>Product</InputLabel><Select value={selectedProduct} onChange={(e) => setSelectedProduct(e.target.value)} label="Product">{products.map((p) => (<MenuItem key={p.id} value={p.id}>{p.name} (Current: {p.current_stock})</MenuItem>))}</Select></FormControl></Grid>
            <Grid item xs={12}><TextField fullWidth label="Quantity" type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} required /></Grid>
            <Grid item xs={12}><TextField fullWidth label="Reference Number" value={reference} onChange={(e) => setReference(e.target.value)} /></Grid>
            <Grid item xs={12}><TextField fullWidth label="Notes" multiline rows={2} value={notes} onChange={(e) => setNotes(e.target.value)} /></Grid>
          </Grid>
        </DialogContent>
        <DialogActions><Button onClick={handleCloseDialog}>Cancel</Button><Button onClick={handleStockIn} variant="contained" color="success">Add Stock</Button></DialogActions>
      </Dialog>

      <Dialog open={openStockOut} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Stock Out</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}><FormControl fullWidth><InputLabel>Product</InputLabel><Select value={selectedProduct} onChange={(e) => setSelectedProduct(e.target.value)} label="Product">{products.map((p) => (<MenuItem key={p.id} value={p.id}>{p.name} (Current: {p.current_stock})</MenuItem>))}</Select></FormControl></Grid>
            <Grid item xs={12}><TextField fullWidth label="Quantity" type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} required /></Grid>
            <Grid item xs={12}><TextField fullWidth label="Reference Number" value={reference} onChange={(e) => setReference(e.target.value)} /></Grid>
            <Grid item xs={12}><TextField fullWidth label="Notes" multiline rows={2} value={notes} onChange={(e) => setNotes(e.target.value)} /></Grid>
          </Grid>
        </DialogContent>
        <DialogActions><Button onClick={handleCloseDialog}>Cancel</Button><Button onClick={handleStockOut} variant="contained" color="error">Remove Stock</Button></DialogActions>
      </Dialog>
    </Box>
  );
};

export default InventoryManagement;
