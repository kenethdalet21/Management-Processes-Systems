import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Paper, Grid, Card, CardContent, Tabs, Tab, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, Alert, LinearProgress
} from '@mui/material';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import AssessmentIcon from '@mui/icons-material/Assessment';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as ChartTooltip } from 'recharts';
import api from '../services/api';
import ExcelImportExport from '../components/ExcelImportExport';

const formatCurrency = (value) => `₱${parseFloat(value || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

const FinancialManagement = () => {
  const [tabValue, setTabValue] = useState(0);
  const [statements, setStatements] = useState(null);
  const [ratios, setRatios] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchFinancialData();
  }, []);

  const fetchFinancialData = async () => {
    try {
      setLoading(true);
      const [statementsRes, ratiosRes] = await Promise.all([
        api.get('/financial/statements'),
        api.get('/financial/ratios')
      ]);
      setStatements(statementsRes.data);
      setRatios(ratiosRes.data);
    } catch (err) {
      setError('Failed to fetch financial data');
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#0088FE', '#00C49F'];

  const RatioCard = ({ title, value, benchmark, description, inverse = false }) => {
    const numValue = parseFloat(value) || 0;
    const numBenchmark = parseFloat(benchmark) || 1;
    const isGood = inverse ? numValue < numBenchmark : numValue >= numBenchmark;
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Typography variant="caption" color="text.secondary">{title}</Typography>
          <Box display="flex" alignItems="center" gap={1}>
            <Typography variant="h5">{typeof value === 'number' ? value.toFixed(2) : value}</Typography>
            {isGood ? <TrendingUpIcon color="success" /> : <TrendingDownIcon color="error" />}
          </Box>
          <Typography variant="caption" color="text.secondary">{description}</Typography>
          <LinearProgress variant="determinate" value={Math.min((numValue / numBenchmark) * 100, 100)} color={isGood ? 'success' : 'error'} sx={{ mt: 1 }} />
          <Typography variant="caption">Benchmark: {benchmark}</Typography>
        </CardContent>
      </Card>
    );
  };

  if (loading) return <Box><Typography>Loading financial data...</Typography></Box>;

  const incomeData = statements?.income_statement || {};
  const balanceData = statements?.balance_sheet || {};
  const cashFlowData = statements?.cash_flow || {};
  const ratioData = ratios || {};

  const revenueBreakdown = [
    { name: 'Revenue', value: incomeData.total_revenue || 0 },
    { name: 'COGS', value: incomeData.cost_of_goods_sold || 0 },
    { name: 'Gross Profit', value: incomeData.gross_profit || 0 }
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Financial Management</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}

      {/* Excel Import/Export */}
      <ExcelImportExport module="financial" onImportSuccess={fetchFinancialData} />

      {/* Summary Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} md={3}>
          <Card sx={{ cursor: 'pointer', '&:hover': { transform: 'translateY(-2px)', boxShadow: 4 }, transition: 'all 0.2s' }} onClick={() => setTabValue(0)}>
            <CardContent>
            <Box display="flex" alignItems="center" gap={1} mb={0.5}>
              <TrendingUpIcon color="success" sx={{ fontSize: 20 }} />
              <Typography variant="caption" color="text.secondary">Total Revenue</Typography>
            </Box>
            <Typography variant="h5" sx={{ fontSize: { xs: '0.9rem', md: '1.2rem' }, wordBreak: 'break-word' }}>{formatCurrency(incomeData.total_revenue)}</Typography>
          </CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card sx={{ cursor: 'pointer', '&:hover': { transform: 'translateY(-2px)', boxShadow: 4 }, transition: 'all 0.2s' }} onClick={() => setTabValue(0)}>
            <CardContent>
            <Box display="flex" alignItems="center" gap={1} mb={0.5}>
              <AccountBalanceIcon color="primary" sx={{ fontSize: 20 }} />
              <Typography variant="caption" color="text.secondary">Net Income</Typography>
            </Box>
            <Typography variant="h5" sx={{ fontSize: { xs: '0.9rem', md: '1.2rem' }, wordBreak: 'break-word' }}>{formatCurrency(incomeData.net_income)}</Typography>
          </CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card sx={{ cursor: 'pointer', '&:hover': { transform: 'translateY(-2px)', boxShadow: 4 }, transition: 'all 0.2s' }} onClick={() => setTabValue(1)}>
            <CardContent>
            <Box display="flex" alignItems="center" gap={1} mb={0.5}>
              <AssessmentIcon color="info" sx={{ fontSize: 20 }} />
              <Typography variant="caption" color="text.secondary">Total Assets</Typography>
            </Box>
            <Typography variant="h5" sx={{ fontSize: { xs: '0.9rem', md: '1.2rem' }, wordBreak: 'break-word' }}>{formatCurrency(balanceData.total_assets)}</Typography>
          </CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card sx={{ cursor: 'pointer', '&:hover': { transform: 'translateY(-2px)', boxShadow: 4 }, transition: 'all 0.2s' }} onClick={() => setTabValue(3)}>
            <CardContent>
            <Box display="flex" alignItems="center" gap={1} mb={0.5}>
              <TrendingUpIcon color="success" sx={{ fontSize: 20 }} />
              <Typography variant="caption" color="text.secondary">Gross Margin</Typography>
            </Box>
            <Typography variant="h5" sx={{ fontSize: { xs: '1.1rem', md: '1.4rem' } }}>{((ratioData.profitability?.gross_margin || 0) * 100).toFixed(1)}%</Typography>
          </CardContent></Card>
        </Grid>
      </Grid>

      <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)} sx={{ mb: 2 }}>
        <Tab label="Income Statement" /><Tab label="Balance Sheet" /><Tab label="Cash Flow" /><Tab label="Financial Ratios" />
      </Tabs>

      {/* Income Statement Tab */}
      {tabValue === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={7}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead><TableRow><TableCell colSpan={2}><Typography variant="h6">Income Statement</Typography></TableCell></TableRow></TableHead>
                <TableBody>
                  <TableRow><TableCell><strong>Revenue</strong></TableCell><TableCell align="right">{formatCurrency(incomeData.total_revenue)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Sales Revenue</TableCell><TableCell align="right">{formatCurrency(incomeData.sales_revenue)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Service Revenue</TableCell><TableCell align="right">{formatCurrency(incomeData.service_revenue)}</TableCell></TableRow>
                  <TableRow><TableCell><strong>Cost of Goods Sold</strong></TableCell><TableCell align="right">({formatCurrency(incomeData.cost_of_goods_sold)})</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'action.hover' }}><TableCell><strong>Gross Profit</strong></TableCell><TableCell align="right"><strong>{formatCurrency(incomeData.gross_profit)}</strong></TableCell></TableRow>
                  <TableRow><TableCell><strong>Operating Expenses</strong></TableCell><TableCell align="right">({formatCurrency(incomeData.operating_expenses)})</TableCell></TableRow>
                  <TableRow sx={{ pl: 4 }}><TableCell sx={{ pl: 4 }}>Payroll Expenses</TableCell><TableCell align="right">{formatCurrency(incomeData.payroll_expenses)}</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'action.hover' }}><TableCell><strong>Operating Income</strong></TableCell><TableCell align="right"><strong>{formatCurrency(incomeData.operating_income)}</strong></TableCell></TableRow>
                  <TableRow><TableCell>Other Income/Expenses</TableCell><TableCell align="right">{formatCurrency(incomeData.other_income)}</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'success.dark' }}><TableCell><strong>Net Income</strong></TableCell><TableCell align="right"><strong>{formatCurrency(incomeData.net_income)}</strong></TableCell></TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
          <Grid item xs={12} md={5}>
            <Paper sx={{ p: 2 }}><Typography variant="h6" gutterBottom>Revenue Breakdown</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart><Pie data={revenueBreakdown} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                  {revenueBreakdown.map((entry, index) => (<Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />))}
                </Pie><ChartTooltip /></PieChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        </Grid>
      )}

      {/* Balance Sheet Tab */}
      {tabValue === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead><TableRow><TableCell colSpan={2}><Typography variant="h6">Assets</Typography></TableCell></TableRow></TableHead>
                <TableBody>
                  <TableRow><TableCell><strong>Current Assets</strong></TableCell><TableCell align="right">{formatCurrency(balanceData.current_assets)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Cash</TableCell><TableCell align="right">{formatCurrency(balanceData.cash)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Accounts Receivable</TableCell><TableCell align="right">{formatCurrency(balanceData.accounts_receivable)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Inventory</TableCell><TableCell align="right">{formatCurrency(balanceData.inventory_value)}</TableCell></TableRow>
                  <TableRow><TableCell><strong>Non-Current Assets</strong></TableCell><TableCell align="right">{formatCurrency(balanceData.non_current_assets)}</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'primary.dark' }}><TableCell><strong>Total Assets</strong></TableCell><TableCell align="right"><strong>{formatCurrency(balanceData.total_assets)}</strong></TableCell></TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
          <Grid item xs={12} md={6}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead><TableRow><TableCell colSpan={2}><Typography variant="h6">Liabilities & Equity</Typography></TableCell></TableRow></TableHead>
                <TableBody>
                  <TableRow><TableCell><strong>Current Liabilities</strong></TableCell><TableCell align="right">{formatCurrency(balanceData.current_liabilities)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Accounts Payable</TableCell><TableCell align="right">{formatCurrency(balanceData.accounts_payable)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Accrued Payroll</TableCell><TableCell align="right">{formatCurrency(balanceData.accrued_payroll)}</TableCell></TableRow>
                  <TableRow><TableCell><strong>Long-term Liabilities</strong></TableCell><TableCell align="right">{formatCurrency(balanceData.long_term_liabilities)}</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'error.dark' }}><TableCell><strong>Total Liabilities</strong></TableCell><TableCell align="right"><strong>{formatCurrency(balanceData.total_liabilities)}</strong></TableCell></TableRow>
                  <TableRow><TableCell><strong>Shareholders' Equity</strong></TableCell><TableCell align="right">{formatCurrency(balanceData.shareholders_equity)}</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'primary.dark' }}><TableCell><strong>Total Liab. & Equity</strong></TableCell><TableCell align="right"><strong>{formatCurrency((balanceData.total_liabilities || 0) + (balanceData.shareholders_equity || 0))}</strong></TableCell></TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
        </Grid>
      )}

      {/* Cash Flow Tab */}
      {tabValue === 2 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead><TableRow><TableCell colSpan={2}><Typography variant="h6">Cash Flow Statement</Typography></TableCell></TableRow></TableHead>
            <TableBody>
              <TableRow><TableCell colSpan={2}><strong>Operating Activities</strong></TableCell></TableRow>
              <TableRow><TableCell sx={{ pl: 4 }}>Net Income</TableCell><TableCell align="right">{formatCurrency(cashFlowData.net_income)}</TableCell></TableRow>
              <TableRow><TableCell sx={{ pl: 4 }}>Cash from Sales</TableCell><TableCell align="right">{formatCurrency(cashFlowData.cash_from_sales)}</TableCell></TableRow>
              <TableRow><TableCell sx={{ pl: 4 }}>Payroll Payments</TableCell><TableCell align="right">({formatCurrency(cashFlowData.payroll_payments)})</TableCell></TableRow>
              <TableRow sx={{ bgcolor: 'action.hover' }}><TableCell><strong>Net Operating Cash Flow</strong></TableCell><TableCell align="right"><strong>{formatCurrency(cashFlowData.operating_cash_flow)}</strong></TableCell></TableRow>
              <TableRow><TableCell colSpan={2}><strong>Investing Activities</strong></TableCell></TableRow>
              <TableRow><TableCell sx={{ pl: 4 }}>Inventory Purchases</TableCell><TableCell align="right">({formatCurrency(cashFlowData.inventory_purchases)})</TableCell></TableRow>
              <TableRow sx={{ bgcolor: 'action.hover' }}><TableCell><strong>Net Investing Cash Flow</strong></TableCell><TableCell align="right"><strong>{formatCurrency(cashFlowData.investing_cash_flow)}</strong></TableCell></TableRow>
              <TableRow sx={{ bgcolor: 'success.dark' }}><TableCell><strong>Net Change in Cash</strong></TableCell><TableCell align="right"><strong>{formatCurrency(cashFlowData.net_cash_change)}</strong></TableCell></TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Financial Ratios Tab */}
      {tabValue === 3 && (
        <Box>
          <Typography variant="h6" gutterBottom>Liquidity Ratios</Typography>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={6} md={3}><RatioCard title="Current Ratio" value={ratioData.liquidity?.current_ratio} benchmark="2.0" description="Current Assets / Current Liabilities" /></Grid>
            <Grid item xs={6} md={3}><RatioCard title="Quick Ratio" value={ratioData.liquidity?.quick_ratio} benchmark="1.0" description="(Current Assets - Inventory) / Current Liabilities" /></Grid>
            <Grid item xs={6} md={3}><RatioCard title="Cash Ratio" value={ratioData.liquidity?.cash_ratio} benchmark="0.5" description="Cash / Current Liabilities" /></Grid>
            <Grid item xs={6} md={3}><RatioCard title="Working Capital" value={formatCurrency(ratioData.liquidity?.working_capital)} benchmark="₱0" description="Current Assets - Current Liabilities" /></Grid>
          </Grid>

          <Typography variant="h6" gutterBottom>Profitability Ratios</Typography>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={6} md={3}><RatioCard title="Gross Margin" value={`${((ratioData.profitability?.gross_margin || 0) * 100).toFixed(1)}%`} benchmark="30%" description="Gross Profit / Revenue" /></Grid>
            <Grid item xs={6} md={3}><RatioCard title="Operating Margin" value={`${((ratioData.profitability?.operating_margin || 0) * 100).toFixed(1)}%`} benchmark="15%" description="Operating Income / Revenue" /></Grid>
            <Grid item xs={6} md={3}><RatioCard title="Net Profit Margin" value={`${((ratioData.profitability?.net_margin || 0) * 100).toFixed(1)}%`} benchmark="10%" description="Net Income / Revenue" /></Grid>
            <Grid item xs={6} md={3}><RatioCard title="ROE" value={`${((ratioData.profitability?.roe || 0) * 100).toFixed(1)}%`} benchmark="15%" description="Net Income / Shareholders' Equity" /></Grid>
          </Grid>

          <Typography variant="h6" gutterBottom>Leverage Ratios</Typography>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={6} md={3}><RatioCard title="Debt-to-Equity" value={ratioData.leverage?.debt_to_equity} benchmark="1.5" description="Total Debt / Total Equity" inverse /></Grid>
            <Grid item xs={6} md={3}><RatioCard title="Debt Ratio" value={ratioData.leverage?.debt_ratio} benchmark="0.5" description="Total Debt / Total Assets" inverse /></Grid>
            <Grid item xs={6} md={3}><RatioCard title="Equity Ratio" value={ratioData.leverage?.equity_ratio} benchmark="0.5" description="Total Equity / Total Assets" /></Grid>
          </Grid>

          <Typography variant="h6" gutterBottom>Efficiency Ratios</Typography>
          <Grid container spacing={2}>
            <Grid item xs={6} md={3}><RatioCard title="Asset Turnover" value={ratioData.efficiency?.asset_turnover} benchmark="1.0" description="Revenue / Total Assets" /></Grid>
            <Grid item xs={6} md={3}><RatioCard title="Inventory Turnover" value={ratioData.efficiency?.inventory_turnover} benchmark="6.0" description="COGS / Average Inventory" /></Grid>
            <Grid item xs={6} md={3}><RatioCard title="Days Sales Outstanding" value={`${(ratioData.efficiency?.days_sales_outstanding || 0).toFixed(0)} days`} benchmark="30 days" description="(AR / Revenue) x 365" inverse /></Grid>
          </Grid>
        </Box>
      )}
    </Box>
  );
};

export default FinancialManagement;
