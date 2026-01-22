import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Paper, Button, TextField, Dialog, DialogTitle, DialogContent,
  DialogActions, Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  IconButton, Chip, Alert, Grid, Card, CardContent, Tabs, Tab, TablePagination,
  MenuItem, Select, FormControl, InputLabel, Divider, List, ListItem, ListItemText, Checkbox
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import VisibilityIcon from '@mui/icons-material/Visibility';
import PersonIcon from '@mui/icons-material/Person';
import ReceiptIcon from '@mui/icons-material/Receipt';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip, ResponsiveContainer } from 'recharts';
import api from '../services/api';
import ExcelImportExport from '../components/ExcelImportExport';

const SalesManagement = () => {
  const [tabValue, setTabValue] = useState(0);
  const [sales, setSales] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [total, setTotal] = useState(0);
  
  const [openSale, setOpenSale] = useState(false);
  const [openCustomer, setOpenCustomer] = useState(false);
  const [openView, setOpenView] = useState(false);
  const [viewingSale, setViewingSale] = useState(null);
  const [selected, setSelected] = useState([]);
  
  const [saleItems, setSaleItems] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState('');
  const [customerForm, setCustomerForm] = useState({ name: '', email: '', phone: '', address: '' });

  useEffect(() => {
    fetchSales();
    fetchCustomers();
    fetchProducts();
    fetchAnalysis();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, rowsPerPage]);

  const fetchSales = async () => {
    try {
      const response = await api.get(`/sales?page=${page + 1}&per_page=${rowsPerPage}`);
      setSales(response.data.sales);
      setTotal(response.data.total);
    } catch (err) {
      setError('Failed to fetch sales');
    }
  };

  const fetchCustomers = async () => {
    try {
      const response = await api.get('/sales/customers');
      setCustomers(response.data);
    } catch (err) {
      console.error('Failed to fetch customers');
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await api.get('/products');
      setProducts(response.data.products || []);
    } catch (err) {
      console.error('Failed to fetch products');
    }
  };

  const fetchAnalysis = async () => {
    try {
      const response = await api.get('/sales/analysis');
      setAnalysis(response.data);
    } catch (err) {
      console.error('Failed to fetch analysis');
    }
  };

  const handleAddItem = () => {
    setSaleItems([...saleItems, { product_id: '', quantity: 1, unit_price: 0 }]);
  };

  const handleRemoveItem = (index) => {
    setSaleItems(saleItems.filter((_, i) => i !== index));
  };

  const handleItemChange = (index, field, value) => {
    const newItems = [...saleItems];
    newItems[index][field] = value;
    if (field === 'product_id') {
      const product = products.find(p => p.id === value);
      if (product) {
        newItems[index].unit_price = product.selling_price;
      }
    }
    setSaleItems(newItems);
  };

  const calculateTotal = () => {
    return saleItems.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0);
  };

  const handleCreateSale = async () => {
    try {
      if (saleItems.length === 0) {
        setError('Please add at least one item');
        return;
      }
      await api.post('/sales', {
        customer_id: selectedCustomer || null,
        items: saleItems.map(item => ({
          product_id: item.product_id,
          quantity: parseInt(item.quantity),
          unit_price: parseFloat(item.unit_price)
        }))
      });
      setSuccess('Sale created successfully');
      setOpenSale(false);
      setSaleItems([]);
      setSelectedCustomer('');
      fetchSales();
      fetchAnalysis();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create sale');
    }
  };

  const handleCreateCustomer = async () => {
    try {
      await api.post('/sales/customers', customerForm);
      setSuccess('Customer created successfully');
      setOpenCustomer(false);
      setCustomerForm({ name: '', email: '', phone: '', address: '' });
      fetchCustomers();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create customer');
    }
  };

  const handleDeleteSale = async (id) => {
    if (window.confirm('Are you sure you want to delete this sale?')) {
      try {
        await api.delete(`/sales/${id}`);
        setSuccess('Sale deleted successfully');
        fetchSales();
        fetchAnalysis();
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to delete sale');
      }
    }
  };

  const handleSelectAll = (event) => {
    if (event.target.checked) {
      const newSelected = sales.map((s) => s.id);
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
    if (window.confirm(`Are you sure you want to delete ${selected.length} selected sale(s)?`)) {
      try {
        await Promise.all(selected.map(id => api.delete(`/sales/${id}`)));
        setSuccess(`Successfully deleted ${selected.length} sale(s)`);
        setSelected([]);
        fetchSales();
        fetchAnalysis();
      } catch (err) {
        setError('Failed to delete some sales');
      }
    }
  };

  const dailyData = analysis?.daily_sales?.map(d => ({ date: d.date.substring(5), revenue: d.revenue, orders: d.orders })) || [];
  const topProducts = analysis?.top_products?.slice(0, 5) || [];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Sales Management</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>{success}</Alert>}

      {/* Excel Import/Export */}
      <ExcelImportExport module="sales" onImportSuccess={() => { fetchSales(); fetchAnalysis(); }} />

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} md={3}>
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Total Sales</Typography><Typography variant="h5">{analysis?.total_sales || 0}</Typography></Box>
            <ReceiptIcon color="primary" />
          </Box></CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Total Revenue</Typography><Typography variant="h5">₱{(analysis?.total_revenue || 0).toFixed(2)}</Typography></Box>
            <AttachMoneyIcon color="success" />
          </Box></CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Avg Order Value</Typography><Typography variant="h5">₱{(analysis?.avg_order_value || 0).toFixed(2)}</Typography></Box>
            <TrendingUpIcon color="info" />
          </Box></CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Customers</Typography><Typography variant="h5">{customers.length}</Typography></Box>
            <PersonIcon color="secondary" />
          </Box></CardContent></Card>
        </Grid>
      </Grid>

      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => { setSaleItems([{ product_id: '', quantity: 1, unit_price: 0 }]); setOpenSale(true); }}>New Sale</Button>
        <Button variant="outlined" startIcon={<PersonIcon />} onClick={() => setOpenCustomer(true)}>Add Customer</Button>
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
        <Tab label="Sales History" /><Tab label="Customers" /><Tab label="Analytics" />
      </Tabs>

      {tabValue === 0 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead><TableRow>
              <TableCell padding="checkbox">
                <Checkbox
                  indeterminate={selected.length > 0 && selected.length < sales.length}
                  checked={sales.length > 0 && selected.length === sales.length}
                  onChange={handleSelectAll}
                />
              </TableCell>
              <TableCell>Invoice #</TableCell><TableCell>Date</TableCell><TableCell>Customer</TableCell>
              <TableCell align="right">Items</TableCell><TableCell align="right">Total</TableCell>
              <TableCell>Status</TableCell><TableCell align="center">Actions</TableCell>
            </TableRow></TableHead>
            <TableBody>
              {sales.map((sale) => {
                const isSelected = selected.indexOf(sale.id) !== -1;
                return (
                  <TableRow key={sale.id} selected={isSelected}>
                    <TableCell padding="checkbox">
                      <Checkbox
                        checked={isSelected}
                        onChange={() => handleSelectOne(sale.id)}
                      />
                    </TableCell>
                    <TableCell>{sale.invoice_number}</TableCell>
                  <TableCell>{new Date(sale.created_at).toLocaleDateString()}</TableCell>
                  <TableCell>{sale.customer?.name || 'Walk-in'}</TableCell>
                  <TableCell align="right">{sale.items?.length || 0}</TableCell>
                  <TableCell align="right">₱{sale.total_amount.toFixed(2)}</TableCell>
                  <TableCell><Chip label={sale.status} size="small" color={sale.status === 'completed' ? 'success' : sale.status === 'pending' ? 'warning' : 'error'} /></TableCell>
                  <TableCell align="center">
                    <IconButton size="small" onClick={() => { setViewingSale(sale); setOpenView(true); }}><VisibilityIcon /></IconButton>
                    <IconButton size="small" color="error" onClick={() => handleDeleteSale(sale.id)}><DeleteIcon /></IconButton>
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
            <TableHead><TableRow><TableCell>Name</TableCell><TableCell>Email</TableCell><TableCell>Phone</TableCell><TableCell>Address</TableCell><TableCell>Since</TableCell></TableRow></TableHead>
            <TableBody>
              {customers.map((customer) => (
                <TableRow key={customer.id}>
                  <TableCell>{customer.name}</TableCell>
                  <TableCell>{customer.email || '-'}</TableCell>
                  <TableCell>{customer.phone || '-'}</TableCell>
                  <TableCell>{customer.address || '-'}</TableCell>
                  <TableCell>{new Date(customer.created_at).toLocaleDateString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {tabValue === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2 }}><Typography variant="h6" gutterBottom>Daily Sales (Last 30 Days)</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={dailyData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="date" /><YAxis /><ChartTooltip />
                  <Line type="monotone" dataKey="revenue" stroke="#8884d8" name="Revenue" />
                </LineChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}><Typography variant="h6" gutterBottom>Top Products</Typography>
              <List>{topProducts.map((p, i) => (
                <ListItem key={i}><ListItemText primary={p.product} secondary={`${p.quantity_sold} units - ₱${p.revenue.toFixed(2)}`} /></ListItem>
              ))}</List>
            </Paper>
          </Grid>
        </Grid>
      )}

      {/* New Sale Dialog */}
      <Dialog open={openSale} onClose={() => setOpenSale(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Sale</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <FormControl fullWidth><InputLabel>Customer (Optional)</InputLabel>
                <Select value={selectedCustomer} onChange={(e) => setSelectedCustomer(e.target.value)} label="Customer (Optional)">
                  <MenuItem value="">Walk-in Customer</MenuItem>
                  {customers.map((c) => (<MenuItem key={c.id} value={c.id}>{c.name}</MenuItem>))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}><Divider><Typography variant="caption">Line Items</Typography></Divider></Grid>
            {saleItems.map((item, index) => (
              <Grid item xs={12} key={index}>
                <Box display="flex" gap={2} alignItems="center">
                  <FormControl sx={{ minWidth: 200 }}><InputLabel>Product</InputLabel>
                    <Select value={item.product_id} onChange={(e) => handleItemChange(index, 'product_id', e.target.value)} label="Product">
                      {products.map((p) => (<MenuItem key={p.id} value={p.id}>{p.name}</MenuItem>))}
                    </Select>
                  </FormControl>
                  <TextField label="Qty" type="number" value={item.quantity} onChange={(e) => handleItemChange(index, 'quantity', e.target.value)} sx={{ width: 80 }} />
                  <TextField label="Price" type="number" value={item.unit_price} onChange={(e) => handleItemChange(index, 'unit_price', e.target.value)} sx={{ width: 100 }} />
                  <Typography sx={{ minWidth: 80 }}>₱{(item.quantity * item.unit_price).toFixed(2)}</Typography>
                  <IconButton color="error" onClick={() => handleRemoveItem(index)}><DeleteIcon /></IconButton>
                </Box>
              </Grid>
            ))}
            <Grid item xs={12}><Button startIcon={<AddIcon />} onClick={handleAddItem}>Add Item</Button></Grid>
            <Grid item xs={12}><Paper sx={{ p: 2, bgcolor: 'primary.dark' }}><Typography variant="h6">Total: ₱{calculateTotal().toFixed(2)}</Typography></Paper></Grid>
          </Grid>
        </DialogContent>
        <DialogActions><Button onClick={() => setOpenSale(false)}>Cancel</Button><Button onClick={handleCreateSale} variant="contained">Create Sale</Button></DialogActions>
      </Dialog>

      {/* Add Customer Dialog */}
      <Dialog open={openCustomer} onClose={() => setOpenCustomer(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Customer</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}><TextField fullWidth label="Name" value={customerForm.name} onChange={(e) => setCustomerForm({ ...customerForm, name: e.target.value })} required /></Grid>
            <Grid item xs={12}><TextField fullWidth label="Email" type="email" value={customerForm.email} onChange={(e) => setCustomerForm({ ...customerForm, email: e.target.value })} /></Grid>
            <Grid item xs={12}><TextField fullWidth label="Phone" value={customerForm.phone} onChange={(e) => setCustomerForm({ ...customerForm, phone: e.target.value })} /></Grid>
            <Grid item xs={12}><TextField fullWidth label="Address" multiline rows={2} value={customerForm.address} onChange={(e) => setCustomerForm({ ...customerForm, address: e.target.value })} /></Grid>
          </Grid>
        </DialogContent>
        <DialogActions><Button onClick={() => setOpenCustomer(false)}>Cancel</Button><Button onClick={handleCreateCustomer} variant="contained">Add Customer</Button></DialogActions>
      </Dialog>

      {/* View Sale Dialog */}
      <Dialog open={openView} onClose={() => setOpenView(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Sale Details - {viewingSale?.invoice_number}</DialogTitle>
        <DialogContent>
          {viewingSale && (
            <Box>
              <Typography><strong>Date:</strong> {new Date(viewingSale.created_at).toLocaleString()}</Typography>
              <Typography><strong>Customer:</strong> {viewingSale.customer?.name || 'Walk-in'}</Typography>
              <Divider sx={{ my: 2 }} />
              <Table size="small">
                <TableHead><TableRow><TableCell>Product</TableCell><TableCell align="right">Qty</TableCell><TableCell align="right">Price</TableCell><TableCell align="right">Total</TableCell></TableRow></TableHead>
                <TableBody>
                  {viewingSale.items?.map((item, i) => (
                    <TableRow key={i}><TableCell>{item.product?.name}</TableCell><TableCell align="right">{item.quantity}</TableCell><TableCell align="right">₱{item.unit_price.toFixed(2)}</TableCell><TableCell align="right">₱{item.total_price.toFixed(2)}</TableCell></TableRow>
                  ))}
                </TableBody>
              </Table>
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" align="right">Total: ₱{viewingSale.total_amount.toFixed(2)}</Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions><Button onClick={() => setOpenView(false)}>Close</Button></DialogActions>
      </Dialog>
    </Box>
  );
};

export default SalesManagement;
