'use client';

import { ReactNode, useState } from 'react';
import { Box, Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Typography, Divider, Avatar, AppBar, IconButton, CssBaseline } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AssignmentIcon from '@mui/icons-material/Assignment';
import PeopleIcon from '@mui/icons-material/People';
import BusinessCenterIcon from '@mui/icons-material/BusinessCenter';
import ContactsIcon from '@mui/icons-material/Contacts';
import ApartmentIcon from '@mui/icons-material/Apartment';
import ListAltIcon from '@mui/icons-material/ListAlt';
import EmailIcon from '@mui/icons-material/Email';
import SettingsIcon from '@mui/icons-material/Settings';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import Link from 'next/link';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import './globals.css';

const drawerWidth = 240;
const miniDrawerWidth = 64;

const navItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, href: '/' },
  { text: 'Tasks', icon: <AssignmentIcon />, href: '/tasks' },
  { text: 'Contacts', icon: <ContactsIcon />, href: '/contacts' },
  { text: 'Companies', icon: <ApartmentIcon />, href: '/companies' },
  { text: 'Opportunities', icon: <BusinessCenterIcon />, href: '/opportunities' },
  { text: 'Forms', icon: <InsertDriveFileIcon />, href: '/forms' },
  { text: 'Emails', icon: <EmailIcon />, href: '/emails' },
  { text: 'Notes', icon: <ListAltIcon />, href: '/notes' },
  { text: 'Data Search', icon: <PeopleIcon />, href: '/datasearch' },
];

const supportItems = [
  { text: 'Settings', icon: <SettingsIcon />, href: '/settings' },
];

export default function RootLayout({ children }: { children: ReactNode }) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isMini = useMediaQuery(theme.breakpoints.between('sm', 'md'));
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <div>
      <Toolbar sx={{ minHeight: 64, justifyContent: isMini ? 'center' : 'flex-start' }}>
        <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 'bold', letterSpacing: 1, color: '#fff', display: isMini ? 'none' : 'block' }}>
          My Network
        </Typography>
      </Toolbar>
      <Divider sx={{ bgcolor: 'rgba(255,255,255,0.1)' }} />
      <List>
        {navItems.map((item) => (
          <Link href={item.href} key={item.text} passHref legacyBehavior>
            <ListItem button component="a" sx={{ color: '#fff', '&:hover': { bgcolor: '#22306a' }, justifyContent: 'center', px: 1 }}>
              <ListItemIcon sx={{ color: '#fff', minWidth: 0, justifyContent: 'center', display: 'flex' }}>{item.icon}</ListItemIcon>
              {!isMini && <ListItemText primary={item.text} />}
            </ListItem>
          </Link>
        ))}
      </List>
      <Box sx={{ flexGrow: 1 }} />
      <Divider sx={{ bgcolor: 'rgba(255,255,255,0.1)' }} />
      <List>
        {supportItems.map((item) => (
          <Link href={item.href} key={item.text} passHref legacyBehavior>
            <ListItem button component="a" sx={{ color: '#fff', '&:hover': { bgcolor: '#22306a' }, justifyContent: 'center', px: 1 }}>
              <ListItemIcon sx={{ color: '#fff', minWidth: 0, justifyContent: 'center', display: 'flex' }}>{item.icon}</ListItemIcon>
              {!isMini && <ListItemText primary={item.text} />}
            </ListItem>
          </Link>
        ))}
      </List>
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1, justifyContent: 'center' }}>
        <Avatar sx={{ width: 32, height: 32 }}>J</Avatar>
        {!isMini && <Typography variant="body2">John Marpung</Typography>}
      </Box>
    </div>
  );

  return (
    <html lang="en">
      <body>
        <CssBaseline />
        <Box sx={{ display: 'flex', bgcolor: '#f5f6fa', minHeight: '100vh' }}>
          {/* AppBar for mobile */}
          {isMobile && (
            <AppBar position="fixed" sx={{ bgcolor: '#1a2340', zIndex: theme.zIndex.drawer + 1 }}>
              <Toolbar>
                <IconButton color="inherit" edge="start" onClick={handleDrawerToggle} sx={{ mr: 2 }}>
                  <MenuIcon />
                </IconButton>
                <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 'bold', letterSpacing: 1, color: '#fff' }}>
                  My Network
                </Typography>
              </Toolbar>
            </AppBar>
          )}
          {/* Responsive Drawer */}
          <Box component="nav" sx={{ width: { sm: isMini ? miniDrawerWidth : drawerWidth }, flexShrink: { sm: 0 } }} aria-label="sidebar">
            {/* Mobile drawer */}
            <Drawer
              variant="temporary"
              open={mobileOpen}
              onClose={handleDrawerToggle}
              ModalProps={{ keepMounted: true }}
              sx={{
                display: { xs: 'block', sm: 'none' },
                '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, bgcolor: '#1a2340', color: '#fff', borderRight: 0 },
              }}
            >
              {drawer}
            </Drawer>
            {/* Mini/desktop drawer */}
            <Drawer
              variant="permanent"
              sx={{
                display: { xs: 'none', sm: 'block' },
                '& .MuiDrawer-paper': {
                  boxSizing: 'border-box',
                  width: isMini ? miniDrawerWidth : drawerWidth,
                  bgcolor: '#1a2340',
                  color: '#fff',
                  borderRight: 0,
                  overflowX: 'hidden',
                  transition: 'width 0.2s',
                },
              }}
              open
            >
              {drawer}
            </Drawer>
          </Box>
          {/* Main content */}
          <Box
            component="main"
            sx={{
              flexGrow: 1,
              p: { xs: 1, sm: 4 },
              ml: { sm: isMini ? `${miniDrawerWidth}px` : `${drawerWidth}px`, xs: 0 },
              mt: isMobile ? '56px' : 0,
              minWidth: 0,
              width: '100%',
              maxWidth: '100%',
              minHeight: '100vh',
              boxSizing: 'border-box',
              overflowX: 'hidden',
              transition: 'margin 0.2s',
            }}
          >
            {children}
          </Box>
        </Box>
      </body>
    </html>
  );
}
