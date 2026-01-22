import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Paper, Button, TextField, Dialog, DialogTitle, DialogContent,
  DialogActions, Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  IconButton, Chip, Alert, Grid, Card, CardContent, Tabs, Tab, TablePagination,
  MenuItem, Select, FormControl, InputLabel, Checkbox
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import PaymentIcon from '@mui/icons-material/Payment';
import PersonIcon from '@mui/icons-material/Person';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import api from '../services/api';
import ExcelImportExport from '../components/ExcelImportExport';

const PayrollManagement = () => {
  const [tabValue, setTabValue] = useState(0);
  const [employees, setEmployees] = useState([]);
  const [records, setRecords] = useState([]);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [total, setTotal] = useState(0);
  const [selected, setSelected] = useState([]);
  
  const [openRecord, setOpenRecord] = useState(false);
  const [editingRecord, setEditingRecord] = useState(null);
  const [recordForm, setRecordForm] = useState({
    employee_id: '', pay_period_start: '', pay_period_end: '',
    hours_worked: '', overtime_hours: '0', bonus: '0', deductions: '0', notes: ''
  });

  useEffect(() => {
    fetchEmployees();
    fetchRecords();
    fetchSummary();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, rowsPerPage]);

  const fetchEmployees = async () => {
    try {
      const response = await api.get('/payroll/employees');
      setEmployees(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      console.error('Failed to fetch employees');
      setEmployees([]);
    }
  };

  const fetchRecords = async () => {
    try {
      const response = await api.get(`/payroll/records?page=${page + 1}&per_page=${rowsPerPage}`);
      setRecords(Array.isArray(response.data?.records) ? response.data.records : []);
      setTotal(response.data?.total || 0);
    } catch (err) {
      setError('Failed to fetch payroll records');
      setRecords([]);
    }
  };

  const fetchSummary = async () => {
    try {
      const year = new Date().getFullYear();
      const month = new Date().getMonth() + 1;
      const response = await api.get(`/payroll/summary?year=${year}&month=${month}`);
      setSummary(response.data);
    } catch (err) {
      console.error('Failed to fetch summary');
    }
  };

  const handleOpenRecord = (record = null) => {
    if (record) {
      setEditingRecord(record);
      setRecordForm({
        employee_id: record.employee_id,
        pay_period_start: record.pay_period_start,
        pay_period_end: record.pay_period_end,
        hours_worked: record.hours_worked,
        overtime_hours: record.overtime_hours || 0,
        bonus: record.bonus || 0,
        deductions: record.deductions || 0,
        notes: record.notes || ''
      });
    } else {
      setEditingRecord(null);
      const today = new Date();
      const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split('T')[0];
      const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0).toISOString().split('T')[0];
      setRecordForm({
        employee_id: '', pay_period_start: startOfMonth, pay_period_end: endOfMonth,
        hours_worked: '', overtime_hours: '0', bonus: '0', deductions: '0', notes: ''
      });
    }
    setOpenRecord(true);
  };

  const calculateGross = () => {
    const emp = employees.find(e => e.id === recordForm.employee_id);
    if (!emp) return 0;
    const hours = parseFloat(recordForm.hours_worked) || 0;
    const overtime = parseFloat(recordForm.overtime_hours) || 0;
    const bonus = parseFloat(recordForm.bonus) || 0;
    const baseRate = emp.hourly_rate || (emp.monthly_salary / 160);
    return (hours * baseRate) + (overtime * baseRate * 1.5) + bonus;
  };

  const calculateNet = () => {
    const gross = calculateGross();
    const deductions = parseFloat(recordForm.deductions) || 0;
    return gross - deductions;
  };

  const handleSaveRecord = async () => {
    try {
      const data = {
        ...recordForm,
        hours_worked: parseFloat(recordForm.hours_worked),
        overtime_hours: parseFloat(recordForm.overtime_hours) || 0,
        bonus: parseFloat(recordForm.bonus) || 0,
        deductions: parseFloat(recordForm.deductions) || 0
      };
      if (editingRecord) {
        await api.put(`/payroll/records/${editingRecord.id}`, data);
        setSuccess('Payroll record updated successfully');
      } else {
        await api.post('/payroll/records', data);
        setSuccess('Payroll record created successfully');
      }
      setOpenRecord(false);
      fetchRecords();
      fetchSummary();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save payroll record');
    }
  };

  const handleMarkPaid = async (id) => {
    try {
      await api.post(`/payroll/pay/${id}`);
      setSuccess('Marked as paid');
      fetchRecords();
      fetchSummary();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to mark as paid');
    }
  };

  const handleSelectAll = (event) => {
    if (event.target.checked) {
      const newSelected = records.map((r) => r.id);
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
    if (window.confirm(`Are you sure you want to delete ${selected.length} selected payroll record(s)?`)) {
      try {
        await Promise.all(selected.map(id => api.delete(`/payroll/records/${id}`)));
        setSuccess(`Successfully deleted ${selected.length} payroll record(s)`);
        setSelected([]);
        fetchRecords();
        fetchSummary();
      } catch (err) {
        setError('Failed to delete some payroll records');
      }
    }
  };

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#0088FE'];
  const departmentData = summary?.by_department?.map(d => ({ name: d.department, value: d.total_paid })) || [];
  const monthlyData = summary?.monthly_trend?.map(m => ({ month: m.month, total: m.total_paid })) || [];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Payroll Management</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>{success}</Alert>}

      {/* Excel Import/Export */}
      <ExcelImportExport module="payroll" onImportSuccess={() => { fetchRecords(); fetchSummary(); }} />

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} md={3}>
          <Card><CardContent>
            <Box display="flex" alignItems="center" gap={1} mb={0.5}>
              <PersonIcon color="primary" sx={{ fontSize: 20 }} />
              <Typography variant="caption" color="text.secondary">Employees</Typography>
            </Box>
            <Typography variant="h5" sx={{ fontSize: { xs: '1.1rem', md: '1.4rem' } }}>{Array.isArray(employees) ? employees.length.toLocaleString() : 0}</Typography>
          </CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent>
            <Box display="flex" alignItems="center" gap={1} mb={0.5}>
              <AttachMoneyIcon color="success" sx={{ fontSize: 20 }} />
              <Typography variant="caption" color="text.secondary">Total Payroll (Month)</Typography>
            </Box>
            <Typography variant="h5" sx={{ fontSize: { xs: '0.9rem', md: '1.2rem' }, wordBreak: 'break-word' }}>₱{(summary?.total_gross || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</Typography>
          </CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent>
            <Box display="flex" alignItems="center" gap={1} mb={0.5}>
              <AccessTimeIcon color="warning" sx={{ fontSize: 20 }} />
              <Typography variant="caption" color="text.secondary">Pending Payments</Typography>
            </Box>
            <Typography variant="h5" sx={{ fontSize: { xs: '1.1rem', md: '1.4rem' } }}>{(summary?.pending_count || 0).toLocaleString()}</Typography>
          </CardContent></Card>
        </Grid>
        <Grid item xs={6} md={3}>
          <Card><CardContent>
            <Box display="flex" alignItems="center" gap={1} mb={0.5}>
              <PaymentIcon color="info" sx={{ fontSize: 20 }} />
              <Typography variant="caption" color="text.secondary">Paid This Month</Typography>
            </Box>
            <Typography variant="h5" sx={{ fontSize: { xs: '0.9rem', md: '1.2rem' }, wordBreak: 'break-word' }}>₱{(summary?.total_paid || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</Typography>
          </CardContent></Card>
        </Grid>
      </Grid>

      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => handleOpenRecord()}>Create Payroll Record</Button>
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
        <Tab label="Payroll Records" /><Tab label="Employees" /><Tab label="Analytics" />
      </Tabs>

      {tabValue === 0 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead><TableRow>
              <TableCell padding="checkbox">
                <Checkbox
                  indeterminate={selected.length > 0 && selected.length < records.length}
                  checked={records.length > 0 && selected.length === records.length}
                  onChange={handleSelectAll}
                />
              </TableCell>
              <TableCell>Employee</TableCell><TableCell>Period</TableCell><TableCell align="right">Hours</TableCell>
              <TableCell align="right">Overtime</TableCell><TableCell align="right">Gross</TableCell>
              <TableCell align="right">Net</TableCell><TableCell>Status</TableCell><TableCell align="center">Actions</TableCell>
            </TableRow></TableHead>
            <TableBody>
              {Array.isArray(records) && records.map((record) => {
                const isSelected = selected.indexOf(record.id) !== -1;
                return (
                  <TableRow key={record.id} selected={isSelected}>
                    <TableCell padding="checkbox">
                      <Checkbox
                        checked={isSelected}
                        onChange={() => handleSelectOne(record.id)}
                      />
                    </TableCell>
                    <TableCell>{record.employee?.first_name} {record.employee?.last_name}</TableCell>
                  <TableCell>{record.pay_period_start} - {record.pay_period_end}</TableCell>
                  <TableCell align="right">{record.hours_worked}</TableCell>
                  <TableCell align="right">{record.overtime_hours || 0}</TableCell>
                  <TableCell align="right">₱{record.gross_pay?.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) || '0.00'}</TableCell>
                  <TableCell align="right">₱{record.net_pay?.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) || '0.00'}</TableCell>
                  <TableCell><Chip label={record.is_paid ? 'Paid' : 'Pending'} size="small" color={record.is_paid ? 'success' : 'warning'} /></TableCell>
                  <TableCell align="center">
                    <IconButton size="small" onClick={() => handleOpenRecord(record)}><EditIcon /></IconButton>
                    {!record.is_paid && <IconButton size="small" color="success" onClick={() => handleMarkPaid(record.id)}><PaymentIcon /></IconButton>}
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
            <TableHead><TableRow><TableCell>Name</TableCell><TableCell>Email</TableCell><TableCell>Department</TableCell><TableCell>Position</TableCell><TableCell align="right">Rate</TableCell><TableCell>Status</TableCell></TableRow></TableHead>
            <TableBody>
              {Array.isArray(employees) && employees.map((emp) => (
                <TableRow key={emp.id}>
                  <TableCell>{emp.first_name} {emp.last_name}</TableCell>
                  <TableCell>{emp.email || '-'}</TableCell>
                  <TableCell>{emp.department || '-'}</TableCell>
                  <TableCell>{emp.position || '-'}</TableCell>
                  <TableCell align="right">₱{emp.hourly_rate ? `${emp.hourly_rate?.toLocaleString()}/hr` : `${emp.monthly_salary?.toLocaleString()}/mo`}</TableCell>
                  <TableCell><Chip label={emp.is_active ? 'Active' : 'Inactive'} size="small" color={emp.is_active ? 'success' : 'default'} /></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {tabValue === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}><Typography variant="h6" gutterBottom>Payroll by Department</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart><Pie data={departmentData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} label>
                  {departmentData.map((entry, index) => (<Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />))}
                </Pie><ChartTooltip /></PieChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}><Typography variant="h6" gutterBottom>Monthly Payroll Trend</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={monthlyData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="month" /><YAxis /><ChartTooltip />
                  <Bar dataKey="total" fill="#8884d8" name="Total Paid" />
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        </Grid>
      )}

      {/* Payroll Record Dialog */}
      <Dialog open={openRecord} onClose={() => setOpenRecord(false)} maxWidth="md" fullWidth>
        <DialogTitle>{editingRecord ? 'Edit Payroll Record' : 'Create Payroll Record'}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}><FormControl fullWidth><InputLabel>Employee</InputLabel>
              <Select value={recordForm.employee_id} onChange={(e) => setRecordForm({ ...recordForm, employee_id: e.target.value })} label="Employee" disabled={!!editingRecord}>
                {Array.isArray(employees) && employees.map((emp) => (<MenuItem key={emp.id} value={emp.id}>{emp.first_name} {emp.last_name}</MenuItem>))}
              </Select>
            </FormControl></Grid>
            <Grid item xs={6}><TextField fullWidth label="Pay Period Start" type="date" value={recordForm.pay_period_start} onChange={(e) => setRecordForm({ ...recordForm, pay_period_start: e.target.value })} InputLabelProps={{ shrink: true }} /></Grid>
            <Grid item xs={6}><TextField fullWidth label="Pay Period End" type="date" value={recordForm.pay_period_end} onChange={(e) => setRecordForm({ ...recordForm, pay_period_end: e.target.value })} InputLabelProps={{ shrink: true }} /></Grid>
            <Grid item xs={6}><TextField fullWidth label="Hours Worked" type="number" value={recordForm.hours_worked} onChange={(e) => setRecordForm({ ...recordForm, hours_worked: e.target.value })} required /></Grid>
            <Grid item xs={6}><TextField fullWidth label="Overtime Hours" type="number" value={recordForm.overtime_hours} onChange={(e) => setRecordForm({ ...recordForm, overtime_hours: e.target.value })} /></Grid>
            <Grid item xs={6}><TextField fullWidth label="Bonus" type="number" value={recordForm.bonus} onChange={(e) => setRecordForm({ ...recordForm, bonus: e.target.value })} /></Grid>
            <Grid item xs={6}><TextField fullWidth label="Deductions" type="number" value={recordForm.deductions} onChange={(e) => setRecordForm({ ...recordForm, deductions: e.target.value })} /></Grid>
            <Grid item xs={12}><TextField fullWidth label="Notes" multiline rows={2} value={recordForm.notes} onChange={(e) => setRecordForm({ ...recordForm, notes: e.target.value })} /></Grid>
            {recordForm.employee_id && recordForm.hours_worked && (
              <Grid item xs={12}><Paper sx={{ p: 2, bgcolor: 'success.dark' }}>
                <Typography>Gross Pay: ₱{calculateGross().toFixed(2)} | Net Pay: ₱{calculateNet().toFixed(2)}</Typography>
              </Paper></Grid>
            )}
          </Grid>
        </DialogContent>
        <DialogActions><Button onClick={() => setOpenRecord(false)}>Cancel</Button><Button onClick={handleSaveRecord} variant="contained">{editingRecord ? 'Update' : 'Create'}</Button></DialogActions>
      </Dialog>
    </Box>
  );
};

export default PayrollManagement;
