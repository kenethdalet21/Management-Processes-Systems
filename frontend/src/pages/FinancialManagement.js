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
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Total Revenue</Typography><Typography variant="h5">₱{(incomeData.total_revenue || 0).toFixed(2)}</Typography></Box>
            <TrendingUpIcon color="success" />
          </Box></CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Net Income</Typography><Typography variant="h5">₱{(incomeData.net_income || 0).toFixed(2)}</Typography></Box>
            <AccountBalanceIcon color="primary" />
          </Box></CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Total Assets</Typography><Typography variant="h5">₱{(balanceData.total_assets || 0).toFixed(2)}</Typography></Box>
            <AssessmentIcon color="info" />
          </Box></CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent><Box display="flex" alignItems="center" justifyContent="space-between">
            <Box><Typography variant="caption" color="text.secondary">Gross Margin</Typography><Typography variant="h5">{((ratioData.profitability?.gross_margin || 0) * 100).toFixed(1)}%</Typography></Box>
            <TrendingUpIcon color="success" />
          </Box></CardContent></Card>
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
                  <TableRow><TableCell><strong>Revenue</strong></TableCell><TableCell align="right">₱{(incomeData.total_revenue || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Sales Revenue</TableCell><TableCell align="right">₱{(incomeData.sales_revenue || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Service Revenue</TableCell><TableCell align="right">₱{(incomeData.service_revenue || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow><TableCell><strong>Cost of Goods Sold</strong></TableCell><TableCell align="right">(₱{(incomeData.cost_of_goods_sold || 0).toFixed(2)})</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'action.hover' }}><TableCell><strong>Gross Profit</strong></TableCell><TableCell align="right"><strong>₱{(incomeData.gross_profit || 0).toFixed(2)}</strong></TableCell></TableRow>
                  <TableRow><TableCell><strong>Operating Expenses</strong></TableCell><TableCell align="right">(₱{(incomeData.operating_expenses || 0).toFixed(2)})</TableCell></TableRow>
                  <TableRow sx={{ pl: 4 }}><TableCell sx={{ pl: 4 }}>Payroll Expenses</TableCell><TableCell align="right">₱{(incomeData.payroll_expenses || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'action.hover' }}><TableCell><strong>Operating Income</strong></TableCell><TableCell align="right"><strong>₱{(incomeData.operating_income || 0).toFixed(2)}</strong></TableCell></TableRow>
                  <TableRow><TableCell>Other Income/Expenses</TableCell><TableCell align="right">₱{(incomeData.other_income || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'success.dark' }}><TableCell><strong>Net Income</strong></TableCell><TableCell align="right"><strong>₱{(incomeData.net_income || 0).toFixed(2)}</strong></TableCell></TableRow>
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
                  <TableRow><TableCell><strong>Current Assets</strong></TableCell><TableCell align="right">₱{(balanceData.current_assets || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Cash</TableCell><TableCell align="right">₱{(balanceData.cash || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Accounts Receivable</TableCell><TableCell align="right">₱{(balanceData.accounts_receivable || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Inventory</TableCell><TableCell align="right">₱{(balanceData.inventory_value || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow><TableCell><strong>Non-Current Assets</strong></TableCell><TableCell align="right">₱{(balanceData.non_current_assets || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'primary.dark' }}><TableCell><strong>Total Assets</strong></TableCell><TableCell align="right"><strong>₱{(balanceData.total_assets || 0).toFixed(2)}</strong></TableCell></TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
          <Grid item xs={12} md={6}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead><TableRow><TableCell colSpan={2}><Typography variant="h6">Liabilities & Equity</Typography></TableCell></TableRow></TableHead>
                <TableBody>
                  <TableRow><TableCell><strong>Current Liabilities</strong></TableCell><TableCell align="right">₱{(balanceData.current_liabilities || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Accounts Payable</TableCell><TableCell align="right">₱{(balanceData.accounts_payable || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow><TableCell sx={{ pl: 4 }}>Accrued Payroll</TableCell><TableCell align="right">₱{(balanceData.accrued_payroll || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow><TableCell><strong>Long-term Liabilities</strong></TableCell><TableCell align="right">₱{(balanceData.long_term_liabilities || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'error.dark' }}><TableCell><strong>Total Liabilities</strong></TableCell><TableCell align="right"><strong>₱{(balanceData.total_liabilities || 0).toFixed(2)}</strong></TableCell></TableRow>
                  <TableRow><TableCell><strong>Shareholders' Equity</strong></TableCell><TableCell align="right">₱{(balanceData.shareholders_equity || 0).toFixed(2)}</TableCell></TableRow>
                  <TableRow sx={{ bgcolor: 'primary.dark' }}><TableCell><strong>Total Liab. & Equity</strong></TableCell><TableCell align="right"><strong>₱{((balanceData.total_liabilities || 0) + (balanceData.shareholders_equity || 0)).toFixed(2)}</strong></TableCell></TableRow>
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
              <TableRow><TableCell sx={{ pl: 4 }}>Net Income</TableCell><TableCell align="right">₱{(cashFlowData.net_income || 0).toFixed(2)}</TableCell></TableRow>
              <TableRow><TableCell sx={{ pl: 4 }}>Cash from Sales</TableCell><TableCell align="right">₱{(cashFlowData.cash_from_sales || 0).toFixed(2)}</TableCell></TableRow>
              <TableRow><TableCell sx={{ pl: 4 }}>Payroll Payments</TableCell><TableCell align="right">(₱{(cashFlowData.payroll_payments || 0).toFixed(2)})</TableCell></TableRow>
              <TableRow sx={{ bgcolor: 'action.hover' }}><TableCell><strong>Net Operating Cash Flow</strong></TableCell><TableCell align="right"><strong>${(cashFlowData.operating_cash_flow || 0).toFixed(2)}</strong></TableCell></TableRow>
              <TableRow><TableCell colSpan={2}><strong>Investing Activities</strong></TableCell></TableRow>
              <TableRow><TableCell sx={{ pl: 4 }}>Inventory Purchases</TableCell><TableCell align="right">(${(cashFlowData.inventory_purchases || 0).toFixed(2)})</TableCell></TableRow>
              <TableRow sx={{ bgcolor: 'action.hover' }}><TableCell><strong>Net Investing Cash Flow</strong></TableCell><TableCell align="right"><strong>${(cashFlowData.investing_cash_flow || 0).toFixed(2)}</strong></TableCell></TableRow>
              <TableRow sx={{ bgcolor: 'success.dark' }}><TableCell><strong>Net Change in Cash</strong></TableCell><TableCell align="right"><strong>${(cashFlowData.net_cash_change || 0).toFixed(2)}</strong></TableCell></TableRow>
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
            <Grid item xs={6} md={3}><RatioCard title="Working Capital" value={`₱${(ratioData.liquidity?.working_capital || 0).toFixed(0)}`} benchmark="₱0" description="Current Assets - Current Liabilities" /></Grid>
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
