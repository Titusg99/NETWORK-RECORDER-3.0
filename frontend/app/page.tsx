'use client';

import { useState } from 'react';
import { Box, Drawer, List, ListItem, ListItemIcon, ListItemText, AppBar, Toolbar, Typography, IconButton, Button, Divider, Paper, Grid, Avatar, Chip, Stack } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AssignmentIcon from '@mui/icons-material/Assignment';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import PeopleIcon from '@mui/icons-material/People';
import BusinessCenterIcon from '@mui/icons-material/BusinessCenter';
import ContactsIcon from '@mui/icons-material/Contacts';
import ApartmentIcon from '@mui/icons-material/Apartment';
import ListAltIcon from '@mui/icons-material/ListAlt';
import EmailIcon from '@mui/icons-material/Email';
import AdsClickIcon from '@mui/icons-material/AdsClick';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import SettingsIcon from '@mui/icons-material/Settings';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import ContactList from './components/ContactList';
import { useStore } from './store/useStore';

const drawerWidth = 240;

const navItems = [
  { text: 'Dashboard', icon: <DashboardIcon /> },
  { text: 'Task', icon: <AssignmentIcon /> },
  { text: 'Calendar', icon: <CalendarTodayIcon /> },
  { text: 'Leads', icon: <PeopleIcon /> },
  { text: 'Opportunities', icon: <BusinessCenterIcon /> },
  { text: 'Contacts', icon: <ContactsIcon /> },
  { text: 'Companies', icon: <ApartmentIcon /> },
  { text: 'Forms', icon: <ListAltIcon /> },
  { text: 'Emails', icon: <EmailIcon /> },
  { text: 'Social Media Ads', icon: <AdsClickIcon /> },
];

const supportItems = [
  { text: 'Help and Support', icon: <HelpOutlineIcon /> },
  { text: 'Settings', icon: <SettingsIcon /> },
];

export default function DashboardPage() {
  // Mock stats
  const stats = [
    { label: "Total Contacts", value: 42 },
    { label: "New This Month", value: 7 },
    { label: "Overdue Follow-ups", value: 3 },
    { label: "Companies Connected", value: 12 },
  ];
  // Mock tasks
  const tasks = [
    { id: 1, title: "Follow up with Jane Doe", due: "2024-06-10" },
    { id: 2, title: "Send resume to Acme Corp", due: "2024-06-12" },
  ];
  // Mock activity
  const activity = [
    { id: 1, text: "Added new contact: Jane Doe" },
    { id: 2, text: "Added new company: Acme Corp" },
    { id: 3, text: "Completed task: Call John Smith" },
  ];

  return (
    <Box sx={{ width: '100%', maxWidth: '100%', boxSizing: 'border-box', overflow: 'hidden' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3, gap: 2, flexWrap: 'wrap', width: '100%' }}>
        <Typography variant="h4" fontWeight="bold" sx={{ color: '#1a2340', flex: '1 1 100%' }}>Dashboard</Typography>
        <Button variant="contained" startIcon={<AddIcon />} sx={{ bgcolor: '#1a2340', '&:hover': { bgcolor: '#22306a' }, minWidth: 120 }}>Add Company</Button>
        <Button variant="contained" startIcon={<AddIcon />} sx={{ bgcolor: '#1a2340', '&:hover': { bgcolor: '#22306a' }, minWidth: 120 }}>Add Contact</Button>
        <Button variant="outlined" startIcon={<EditIcon />} sx={{ color: '#1a2340', borderColor: '#1a2340', '&:hover': { bgcolor: '#22306a', color: '#fff', borderColor: '#22306a' }, minWidth: 120 }}>Edit Contact</Button>
      </Box>
      <Grid container spacing={3} sx={{ width: '100%', maxWidth: '100%' }}>
        <Grid item xs={12} md={8} sx={{ width: '100%' }}>
          <Paper sx={{ p: { xs: 2, sm: 3 }, mb: 3, width: '100%', boxSizing: 'border-box' }}>
            <Typography variant="h6" fontWeight="bold" mb={2} sx={{ color: '#1a2340' }}>Analytics</Typography>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={3} mb={2} sx={{ width: '100%' }}>
              {stats.map(stat => (
                <Box key={stat.label} sx={{ textAlign: "center", flex: 1, minWidth: 0 }}>
                  <Typography variant="h5" fontWeight="bold" sx={{ color: '#1a2340' }}>{stat.value}</Typography>
                  <Typography variant="body2" color="text.secondary">{stat.label}</Typography>
                </Box>
              ))}
            </Stack>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle1" fontWeight="bold" mb={1} sx={{ color: '#1a2340' }}>Calendar (Coming Soon)</Typography>
            <Paper sx={{ p: 2, bgcolor: '#f5f6fa', borderRadius: 2, minHeight: 120, width: '100%', boxSizing: 'border-box' }}>
              <Typography variant="body2" color="text.secondary">Calendar integration will appear here.</Typography>
            </Paper>
          </Paper>
          <Paper sx={{ p: { xs: 2, sm: 3 }, mb: 3, width: '100%', boxSizing: 'border-box' }}>
            <Typography variant="h6" fontWeight="bold" mb={2} sx={{ color: '#1a2340' }}>Upcoming Tasks</Typography>
            <List>
              {tasks.map(task => (
                <li key={task.id}>
                  <Typography variant="body2">{task.title} (Due: {task.due})</Typography>
                </li>
              ))}
            </List>
          </Paper>
          <Paper sx={{ p: { xs: 2, sm: 3 }, mb: 3, width: '100%', boxSizing: 'border-box' }}>
            <Typography variant="h6" fontWeight="bold" mb={2} sx={{ color: '#1a2340' }}>Recent Activity</Typography>
            <List>
              {activity.map(act => (
                <li key={act.id}>
                  <Typography variant="body2">{act.text}</Typography>
                </li>
              ))}
            </List>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4} sx={{ width: '100%' }}>
          <Paper sx={{ p: { xs: 2, sm: 3 }, mb: 3, width: '100%', boxSizing: 'border-box' }}>
            <Typography variant="h6" fontWeight="bold" mb={2} sx={{ color: '#1a2340' }}>Network Map</Typography>
            <Paper sx={{ p: 2, bgcolor: '#f5f6fa', borderRadius: 2, minHeight: 180, width: '100%', boxSizing: 'border-box' }}>
              <Typography variant="body2" color="text.secondary">Nationwide network distribution map will appear here.</Typography>
            </Paper>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
