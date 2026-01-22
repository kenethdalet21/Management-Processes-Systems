import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Paper, Button, TextField, Dialog, DialogTitle, DialogContent,
  DialogActions, Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  IconButton, Chip, FormControlLabel, Switch, InputAdornment, Alert, Grid, Card,
  CardContent, Tooltip, TablePagination, Tabs, Tab, Checkbox
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import SearchIcon from '@mui/icons-material/Search';
import InventoryIcon from '@mui/icons-material/Inventory';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import api from '../services/api';
import ExcelImportExport from '../components/ExcelImportExport';

const ProductManagement = () => {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [total, setTotal] = useState(0);
  const [tabValue, setTabValue] = useState(0); // 0 for Products, 1 for Services
  const [selected, setSelected] = useState([]);
  
  // Dialog state
  const [openDialog, setOpenDialog] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [formData, setFormData] = useState({
    name: '', sku: '', description: '', category_id: '',
    item_cost: '', tax_amount: '0', other_costs: '0', selling_price: '',
    is_service: false, track_inventory: true, current_stock: 0, low_stock_threshold: 10
  });

  useEffect(() => {
    fetchProducts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, rowsPerPage, search, tabValue]);

  const fetchProducts = async () => {
    try {
      const response = await api.get(`/products?page=${page + 1}&per_page=${rowsPerPage}&search=${search}`);
      setProducts(Array.isArray(response.data?.products) ? response.data.products : []);
      setTotal(response.data?.total || 0);
    } catch (err) {
      setError('Failed to fetch products');
      setProducts([]);
    }
  };

  const handleOpenDialog = (product = null) => {
    if (product) {
      setEditingProduct(product);
      setFormData({
        name: product.name, sku: product.sku, description: product.description || '',
        category_id: product.category_id || '', item_cost: product.item_cost,
        tax_amount: product.tax_amount || 0, other_costs: product.other_costs || 0,
        selling_price: product.selling_price, is_service: product.is_service,
        track_inventory: product.track_inventory, current_stock: product.current_stock,
        low_stock_threshold: product.low_stock_threshold
      });
    } else {
      // Pre-set is_service based on current tab
      setEditingProduct(null);
      setFormData({
        name: '', sku: '', description: '', category_id: '',
        item_cost: '', tax_amount: '0', other_costs: '0', selling_price: '',
        is_service: tabValue === 1, // true for Services tab
        track_inventory: tabValue === 0, // true for Products tab only
        current_stock: 0, low_stock_threshold: 10
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingProduct(null);
    setError('');
  };

  const handleSubmit = async () => {
    try {
      if (editingProduct) {
        await api.put(`/products/${editingProduct.id}`, formData);
        setSuccess('Product updated successfully');
      } else {
        await api.post('/products', formData);
        setSuccess('Product created successfully');
      }
      handleCloseDialog();
      fetchProducts();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save product');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await api.delete(`/products/${id}`);
        setSuccess('Product deleted successfully');
        fetchProducts();
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to delete product');
      }
    }
  };

  const handleSelectAll = (event) => {
    if (event.target.checked) {
      const newSelected = filteredProducts.map((p) => p.id);
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

    if (window.confirm(`Are you sure you want to delete ${selected.length} selected item(s)?`)) {
      try {
        await Promise.all(selected.map(id => api.delete(`/products/${id}`)));
        setSuccess(`Successfully deleted ${selected.length} product(s)`);
        setSelected([]);
        fetchProducts();
      } catch (err) {
        setError('Failed to delete some products');
      }
    }
  };

  const calculateProfit = () => {
    const cost = parseFloat(formData.item_cost) || 0;
    const tax = parseFloat(formData.tax_amount) || 0;
    const other = parseFloat(formData.other_costs) || 0;
    const price = parseFloat(formData.selling_price) || 0;
    const totalCost = cost + tax + other;
    const profit = price - totalCost;
    const margin = price > 0 ? (profit / price) * 100 : 0;
    return { profit: profit.toFixed(2), margin: margin.toFixed(1) };
  };

  const stats = {
    totalProducts: total,
    totalValue: Array.isArray(products) ? products.reduce((sum, p) => sum + (p.item_cost * p.current_stock), 0) : 0,
    lowStock: Array.isArray(products) ? products.filter(p => p.current_stock <= p.low_stock_threshold && p.current_stock > 0).length : 0,
    outOfStock: Array.isArray(products) ? products.filter(p => p.current_stock === 0 && p.track_inventory).length : 0
  };

  // Filter products based on tab
  const filteredProducts = Array.isArray(products) ? products.filter(p => 
    tabValue === 0 ? !p.is_service : p.is_service
  ) : [];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Product/Service Management</Typography>
      
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>{success}</Alert>}

      {/* Excel Import/Export */}
      <ExcelImportExport module="products" onImportSuccess={fetchProducts} />

      {/* Stats Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} md={3}>
          <Card><CardContent>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box>
                <Typography variant="caption" color="text.secondary">Total Items</Typography>
                <Typography variant="h5">{stats.totalProducts}</Typography>
              </Box>
              <InventoryIcon color="primary" />
            </Box>
          </CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box>
                <Typography variant="caption" color="text.secondary">Inventory Value</Typography>
                <Typography variant="h5">₱{stats.totalValue.toFixed(2)}</Typography>
              </Box>
              <AttachMoneyIcon color="success" />
            </Box>
          </CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card sx={{ bgcolor: stats.lowStock > 0 ? 'warning.dark' : 'inherit' }}><CardContent>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box>
                <Typography variant="caption" color="text.secondary">Low Stock</Typography>
                <Typography variant="h5">{stats.lowStock}</Typography>
              </Box>
              <TrendingUpIcon color="warning" />
            </Box>
          </CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card sx={{ bgcolor: stats.outOfStock > 0 ? 'error.dark' : 'inherit' }}><CardContent>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box>
                <Typography variant="caption" color="text.secondary">Out of Stock</Typography>
                <Typography variant="h5">{stats.outOfStock}</Typography>
              </Box>
              <InventoryIcon color="error" />
            </Box>
          </CardContent></Card>
        </Grid>
      </Grid>

      {/* Tabs for Products/Services */}
      <Paper sx={{ mb: 2 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab label="Products" />
          <Tab label="Services" />
        </Tabs>
      </Paper>

      {/* Search and Add */}
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField
          placeholder={`Search ${tabValue === 0 ? 'products' : 'services'}...`}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          InputProps={{ startAdornment: <InputAdornment position="start"><SearchIcon /></InputAdornment> }}
          sx={{ flexGrow: 1 }}
        />
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
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => handleOpenDialog()}>
          Add {tabValue === 0 ? 'Product' : 'Service'}
        </Button>
      </Box>

      {/* Products/Services Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell padding="checkbox">
                <Checkbox
                  indeterminate={selected.length > 0 && selected.length < filteredProducts.length}
                  checked={filteredProducts.length > 0 && selected.length === filteredProducts.length}
                  onChange={handleSelectAll}
                />
              </TableCell>
              <TableCell>SKU</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Category</TableCell>
              <TableCell align="right">Cost</TableCell>
              <TableCell align="right">Price</TableCell>
              <TableCell align="right">Margin</TableCell>
              {tabValue === 0 && <TableCell align="right">Stock</TableCell>}
              <TableCell>Status</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredProducts.map((product) => {
              const margin = product.selling_price > 0 
                ? ((product.selling_price - product.item_cost) / product.selling_price * 100).toFixed(1) 
                : 0;
              const isSelected = selected.indexOf(product.id) !== -1;
              return (
                <TableRow key={product.id} selected={isSelected}>
                  <TableCell padding="checkbox">
                    <Checkbox
                      checked={isSelected}
                      onChange={() => handleSelectOne(product.id)}
                    />
                  </TableCell>
                  <TableCell>{product.sku}</TableCell>
                  <TableCell>{product.name}</TableCell>
                  <TableCell>{product.category?.name || '-'}</TableCell>
                  <TableCell align="right">₱{product.item_cost?.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) || '0.00'}</TableCell>
                  <TableCell align="right">₱{product.selling_price?.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) || '0.00'}</TableCell>
                  <TableCell align="right">{margin}%</TableCell>
                  {tabValue === 0 && (
                    <TableCell align="right">
                      {product.track_inventory ? product.current_stock?.toLocaleString() : 'N/A'}
                    </TableCell>
                  )}
                  <TableCell>
                    {product.is_service ? (
                      <Chip label="Service" size="small" color="info" />
                    ) : product.current_stock === 0 ? (
                      <Chip label="Out of Stock" size="small" color="error" />
                    ) : product.current_stock <= product.low_stock_threshold ? (
                      <Chip label="Low Stock" size="small" color="warning" />
                    ) : (
                      <Chip label="In Stock" size="small" color="success" />
                    )}
                  </TableCell>
                  <TableCell align="center">
                    <Tooltip title="Edit">
                      <IconButton size="small" onClick={() => handleOpenDialog(product)}>
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete">
                      <IconButton size="small" color="error" onClick={() => handleDelete(product.id)}>
                        <DeleteIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
        <TablePagination
          component="div"
          count={total}
          page={page}
          onPageChange={(e, newPage) => setPage(newPage)}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={(e) => { setRowsPerPage(parseInt(e.target.value, 10)); setPage(0); }}
        />
      </TableContainer>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>{editingProduct ? 'Edit Product' : 'Add New Product'}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Product Name" value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })} required />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="SKU" value={formData.sku}
                onChange={(e) => setFormData({ ...formData, sku: e.target.value })} 
                required disabled={!!editingProduct} />
            </Grid>
            <Grid item xs={12}>
              <TextField fullWidth label="Description" multiline rows={2} value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Item Cost" type="number" value={formData.item_cost}
                onChange={(e) => setFormData({ ...formData, item_cost: e.target.value })}
                InputProps={{ startAdornment: <InputAdornment position="start">₱</InputAdornment> }} required />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Tax Amount" type="number" value={formData.tax_amount}
                onChange={(e) => setFormData({ ...formData, tax_amount: e.target.value })}
                InputProps={{ startAdornment: <InputAdornment position="start">₱</InputAdornment> }} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Other Costs" type="number" value={formData.other_costs}
                onChange={(e) => setFormData({ ...formData, other_costs: e.target.value })}
                InputProps={{ startAdornment: <InputAdornment position="start">₱</InputAdornment> }} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Selling Price" type="number" value={formData.selling_price}
                onChange={(e) => setFormData({ ...formData, selling_price: e.target.value })}
                InputProps={{ startAdornment: <InputAdornment position="start">₱</InputAdornment> }} required />
            </Grid>
            {formData.item_cost && formData.selling_price && (
              <Grid item xs={12}>
                <Paper sx={{ p: 2, bgcolor: 'success.dark' }}>
                  <Typography>Profit: ₱{calculateProfit().profit} | Margin: {calculateProfit().margin}%</Typography>
                </Paper>
              </Grid>
            )}
            <Grid item xs={12} md={4}>
              <FormControlLabel control={<Switch checked={formData.is_service}
                onChange={(e) => setFormData({ ...formData, is_service: e.target.checked })} />}
                label="Is Service" />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControlLabel control={<Switch checked={formData.track_inventory}
                onChange={(e) => setFormData({ ...formData, track_inventory: e.target.checked })} />}
                label="Track Inventory" disabled={formData.is_service} />
            </Grid>
            {formData.track_inventory && !formData.is_service && (
              <>
                <Grid item xs={6} md={4}>
                  <TextField fullWidth label="Current Stock" type="number" value={formData.current_stock}
                    onChange={(e) => setFormData({ ...formData, current_stock: parseInt(e.target.value) || 0 })} />
                </Grid>
                <Grid item xs={6} md={4}>
                  <TextField fullWidth label="Low Stock Threshold" type="number" value={formData.low_stock_threshold}
                    onChange={(e) => setFormData({ ...formData, low_stock_threshold: parseInt(e.target.value) || 10 })} />
                </Grid>
              </>
            )}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">{editingProduct ? 'Update' : 'Create'}</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ProductManagement;
