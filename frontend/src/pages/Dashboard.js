import React, { useState, useEffect, useCallback } from 'react';
import {
  Box, Grid, Paper, Typography, Card, CardContent, Select, MenuItem, FormControl,
  InputLabel, Alert, Chip, Divider, List, ListItem, ListItemText, LinearProgress
} from '@mui/material';
import {
  BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area
} from 'recharts';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import ReceiptIcon from '@mui/icons-material/Receipt';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import InventoryIcon from '@mui/icons-material/Inventory';
import WarningIcon from '@mui/icons-material/Warning';
import PaymentIcon from '@mui/icons-material/Payment';
import api from '../services/api';

const Dashboard = () => {
  const [year, setYear] = useState(new Date().getFullYear());
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [salesAnalysis, setSalesAnalysis] = useState(null);
  const [inventoryAnalysis, setInventoryAnalysis] = useState(null);
  const [payrollSummary, setPayrollSummary] = useState(null);
  const [financialData, setFinancialData] = useState(null);
  const [lowStock, setLowStock] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#0088FE', '#00C49F'];

  const fetchAllData = useCallback(async () => {

    try {
      setLoading(true);
      const [, salesRes, invRes, payRes, finStatementsRes, finRatiosRes, lowStockRes] = await Promise.all([
        api.get(`/dashboard/metrics?year=${year}&month=${month}`).catch(() => ({ data: null })),
        api.get('/sales/analysis').catch(() => ({ data: null })),
        api.get('/inventory/analysis').catch(() => ({ data: null })),
        api.get(`/payroll/summary?year=${year}&month=${month}`).catch(() => ({ data: null })),
        api.get('/financial/statements').catch(() => ({ data: null })),
        api.get('/financial/ratios').catch(() => ({ data: null })),
        api.get('/inventory/low-stock').catch(() => ({ data: [] }))
      ]);
      setSalesAnalysis(salesRes.data);
      setInventoryAnalysis(invRes.data);
      setPayrollSummary(payRes.data);
      setFinancialData({ statements: finStatementsRes.data, ratios: finRatiosRes.data });
      setLowStock(Array.isArray(lowStockRes.data) ? lowStockRes.data : []);
    } catch (err) {
      setError('Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  }, [year, month]);

  useEffect(() => { fetchAllData(); }, [fetchAllData]);

  const formatCurrency = (value) => `₱${parseFloat(value || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

  const MetricCard = ({ title, value, icon: Icon, color, subtitle }) => (
    <Card sx={{ bgcolor: `${color}.dark`, height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box sx={{ overflow: 'hidden', flex: 1, mr: 1 }}>
            <Typography variant="caption" color="white" sx={{ opacity: 0.8 }}>{title}</Typography>
            <Typography variant="h6" color="white" fontWeight="bold" sx={{ fontSize: { xs: '0.9rem', md: '1.15rem' }, wordBreak: 'break-word' }}>{value}</Typography>
            {subtitle && <Typography variant="caption" color="white" sx={{ opacity: 0.7 }}>{subtitle}</Typography>}
          </Box>
          <Icon sx={{ fontSize: { xs: 30, md: 40 }, color: 'white', opacity: 0.8, flexShrink: 0 }} />
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) return <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh"><Typography>Loading dashboard...</Typography></Box>;

  const income = financialData?.statements?.income_statement || {};
  const balance = financialData?.statements?.balance_sheet || {};
  const ratios = financialData?.ratios || {};
  const dailySales = salesAnalysis?.daily_sales?.slice(-14) || [];
  const topProducts = salesAnalysis?.top_products?.slice(0, 5) || [];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Business Dashboard</Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl size="small" sx={{ minWidth: 100 }}>
            <InputLabel>Year</InputLabel>
            <Select value={year} onChange={(e) => setYear(e.target.value)} label="Year">
              {[2023, 2024, 2025, 2026].map((y) => <MenuItem key={y} value={y}>{y}</MenuItem>)}
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Month</InputLabel>
            <Select value={month} onChange={(e) => setMonth(e.target.value)} label="Month">
              {months.map((m, idx) => <MenuItem key={idx} value={idx + 1}>{m}</MenuItem>)}
            </Select>
          </FormControl>
        </Box>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}

      {/* Key Metrics Row */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} md={2.4}><MetricCard title="Total Revenue" value={formatCurrency(income.total_revenue)} icon={AttachMoneyIcon} color="success" /></Grid>
        <Grid item xs={6} md={2.4}><MetricCard title="Net Income" value={formatCurrency(income.net_income)} icon={TrendingUpIcon} color="primary" /></Grid>
        <Grid item xs={6} md={2.4}><MetricCard title="Total Sales" value={salesAnalysis?.total_sales || 0} icon={ReceiptIcon} color="info" subtitle={`Avg: ${formatCurrency(salesAnalysis?.avg_order_value)}`} /></Grid>
        <Grid item xs={6} md={2.4}><MetricCard title="Inventory Value" value={formatCurrency(inventoryAnalysis?.total_value)} icon={InventoryIcon} color="warning" subtitle={`${inventoryAnalysis?.total_units || 0} units`} /></Grid>
        <Grid item xs={6} md={2.4}><MetricCard title="Payroll (Month)" value={formatCurrency(payrollSummary?.total_gross)} icon={PaymentIcon} color="secondary" subtitle={`${payrollSummary?.pending_count || 0} pending`} /></Grid>
      </Grid>

      {/* Charts Row 1 */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Sales Trend (Last 14 Days)</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={dailySales}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tickFormatter={(d) => d.substring(5)} />
                <YAxis />
                <Tooltip formatter={(v) => formatCurrency(v)} labelFormatter={(l) => `Date: ${l}`} />
                <Area type="monotone" dataKey="revenue" stroke="#8884d8" fill="#8884d8" fillOpacity={0.3} name="Revenue" />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>Inventory Status</Typography>
            <Box sx={{ mt: 2 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography>Products</Typography>
                <Chip label={inventoryAnalysis?.total_products || 0} color="primary" />
              </Box>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography>Low Stock Alerts</Typography>
                <Chip label={Array.isArray(lowStock) ? lowStock.length : 0} color={(Array.isArray(lowStock) && lowStock.length > 0) ? 'warning' : 'success'} icon={<WarningIcon />} />
              </Box>
              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle2" gutterBottom>Low Stock Items:</Typography>
              <List dense>
                {Array.isArray(lowStock) && lowStock.slice(0, 3).map((item, i) => (
                  <ListItem key={i}><ListItemText primary={item.name} secondary={`Stock: ${item.current_stock}`} /></ListItem>
                ))}
                {(!Array.isArray(lowStock) || lowStock.length === 0) && <ListItem><ListItemText primary="No low stock items" /></ListItem>}
                {Array.isArray(lowStock) && lowStock.length > 3 && <ListItem><ListItemText primary={`+${lowStock.length - 3} more items`} /></ListItem>}
              </List>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Charts Row 2 */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Top Selling Products</Typography>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={topProducts} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="product" type="category" width={80} tick={{ fontSize: 11 }} />
                <Tooltip formatter={(v) => formatCurrency(v)} />
                <Bar dataKey="revenue" fill="#82ca9d" name="Revenue" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Inventory by Category</Typography>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={inventoryAnalysis?.by_category || []} dataKey="total_value" nameKey="category" cx="50%" cy="50%" outerRadius={80} label={(e) => e.category?.substring(0, 8)}>
                  {(inventoryAnalysis?.by_category || []).map((entry, index) => (<Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />))}
                </Pie>
                <Tooltip formatter={(v) => formatCurrency(v)} />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Key Financial Ratios</Typography>
            <Box sx={{ mt: 1 }}>
              <Box mb={2}>
                <Box display="flex" justifyContent="space-between"><Typography variant="body2">Gross Margin</Typography><Typography variant="body2" fontWeight="bold">{((ratios.profitability?.gross_margin || 0) * 100).toFixed(1)}%</Typography></Box>
                <LinearProgress variant="determinate" value={Math.min((ratios.profitability?.gross_margin || 0) * 100, 100)} color="success" />
              </Box>
              <Box mb={2}>
                <Box display="flex" justifyContent="space-between"><Typography variant="body2">Current Ratio</Typography><Typography variant="body2" fontWeight="bold">{(ratios.liquidity?.current_ratio || 0).toFixed(2)}</Typography></Box>
                <LinearProgress variant="determinate" value={Math.min((ratios.liquidity?.current_ratio || 0) * 50, 100)} color="info" />
              </Box>
              <Box mb={2}>
                <Box display="flex" justifyContent="space-between"><Typography variant="body2">Net Profit Margin</Typography><Typography variant="body2" fontWeight="bold">{((ratios.profitability?.net_margin || 0) * 100).toFixed(1)}%</Typography></Box>
                <LinearProgress variant="determinate" value={Math.min((ratios.profitability?.net_margin || 0) * 100, 100)} color="primary" />
              </Box>
              <Box mb={2}>
                <Box display="flex" justifyContent="space-between"><Typography variant="body2">ROE</Typography><Typography variant="body2" fontWeight="bold">{((ratios.profitability?.roe || 0) * 100).toFixed(1)}%</Typography></Box>
                <LinearProgress variant="determinate" value={Math.min((ratios.profitability?.roe || 0) * 100, 100)} color="secondary" />
              </Box>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Summary Row */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Income Summary</Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}><Typography variant="body2" color="text.secondary">Total Revenue</Typography><Typography variant="h6">{formatCurrency(income.total_revenue)}</Typography></Grid>
              <Grid item xs={6}><Typography variant="body2" color="text.secondary">Cost of Goods Sold</Typography><Typography variant="h6">{formatCurrency(income.cost_of_goods_sold)}</Typography></Grid>
              <Grid item xs={6}><Typography variant="body2" color="text.secondary">Gross Profit</Typography><Typography variant="h6" color="success.main">{formatCurrency(income.gross_profit)}</Typography></Grid>
              <Grid item xs={6}><Typography variant="body2" color="text.secondary">Operating Expenses</Typography><Typography variant="h6">{formatCurrency(income.operating_expenses)}</Typography></Grid>
              <Grid item xs={12}><Divider /></Grid>
              <Grid item xs={6}><Typography variant="body2" color="text.secondary">Net Income</Typography><Typography variant="h5" color="primary.main">{formatCurrency(income.net_income)}</Typography></Grid>
            </Grid>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Balance Sheet Summary</Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}><Typography variant="body2" color="text.secondary">Total Assets</Typography><Typography variant="h6">{formatCurrency(balance.total_assets)}</Typography></Grid>
              <Grid item xs={6}><Typography variant="body2" color="text.secondary">Total Liabilities</Typography><Typography variant="h6">{formatCurrency(balance.total_liabilities)}</Typography></Grid>
              <Grid item xs={6}><Typography variant="body2" color="text.secondary">Cash</Typography><Typography variant="h6" color="success.main">{formatCurrency(balance.cash)}</Typography></Grid>
              <Grid item xs={6}><Typography variant="body2" color="text.secondary">Inventory Value</Typography><Typography variant="h6">{formatCurrency(balance.inventory_value)}</Typography></Grid>
              <Grid item xs={12}><Divider /></Grid>
              <Grid item xs={6}><Typography variant="body2" color="text.secondary">Shareholders' Equity</Typography><Typography variant="h5" color="primary.main">{formatCurrency(balance.shareholders_equity)}</Typography></Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
