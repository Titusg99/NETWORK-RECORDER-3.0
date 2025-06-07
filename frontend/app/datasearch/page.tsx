"use client";
import { useState } from "react";
import { Box, Typography, Paper, Tabs, Tab, TextField, Button, Stack, List, ListItem, ListItemText, Grid } from "@mui/material";

const mockPeople = [
  { id: 1, name: "John Doe", role: "Investment Banker", company: "Goldman Sachs", location: "New York" },
  { id: 2, name: "Jane Smith", role: "VC Partner", company: "Arkansas Ventures", location: "Arkansas" },
];
const mockFirms = [
  { id: 1, name: "Arkansas Ventures", type: "VC", size: 15, location: "Arkansas" },
  { id: 2, name: "Goldman Sachs", type: "Bank", size: 20000, location: "New York" },
];

export default function DataSearchPage() {
  const [tab, setTab] = useState(0);
  // People filters
  const [personRole, setPersonRole] = useState("");
  const [personCompany, setPersonCompany] = useState("");
  const [personLocation, setPersonLocation] = useState("");
  // Firm filters
  const [firmType, setFirmType] = useState("");
  const [firmSize, setFirmSize] = useState("");
  const [firmLocation, setFirmLocation] = useState("");

  // Filter logic (mock, to be replaced with real logic later)
  const filteredPeople = mockPeople.filter(p =>
    (!personRole || p.role.toLowerCase().includes(personRole.toLowerCase())) &&
    (!personCompany || p.company.toLowerCase().includes(personCompany.toLowerCase())) &&
    (!personLocation || p.location.toLowerCase().includes(personLocation.toLowerCase()))
  );
  const filteredFirms = mockFirms.filter(f =>
    (!firmType || f.type.toLowerCase().includes(firmType.toLowerCase())) &&
    (!firmLocation || f.location.toLowerCase().includes(firmLocation.toLowerCase())) &&
    (!firmSize || (f.size >= parseInt(firmSize.split('-')[0] || '0') && f.size <= parseInt(firmSize.split('-')[1] || '99999')))
  );

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" mb={3} sx={{ color: '#1a2340' }}>Data Search</Typography>
      <Paper sx={{ p: { xs: 2, sm: 3 }, mb: 3 }}>
        <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
          <Tab label="People" />
          <Tab label="Firms" />
        </Tabs>
        {tab === 0 && (
          <Box>
            <Grid container spacing={2} mb={2}>
              <Grid item xs={12} sm={4}><TextField label="Role/Title" value={personRole} onChange={e => setPersonRole(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={4}><TextField label="Company" value={personCompany} onChange={e => setPersonCompany(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={4}><TextField label="Location (State/City)" value={personLocation} onChange={e => setPersonLocation(e.target.value)} fullWidth /></Grid>
            </Grid>
            <Button variant="contained" sx={{ bgcolor: '#1a2340', '&:hover': { bgcolor: '#22306a' } }}>Search</Button>
            <List sx={{ mt: 2 }}>
              {filteredPeople.map(p => (
                <ListItem key={p.id}>
                  <ListItemText primary={p.name} secondary={`${p.role} at ${p.company} (${p.location})`} />
                </ListItem>
              ))}
            </List>
          </Box>
        )}
        {tab === 1 && (
          <Box>
            <Grid container spacing={2} mb={2}>
              <Grid item xs={12} sm={4}><TextField label="Firm Type (VC, Bank, etc.)" value={firmType} onChange={e => setFirmType(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={4}><TextField label="Firm Size (e.g. 10-20)" value={firmSize} onChange={e => setFirmSize(e.target.value)} fullWidth placeholder="10-20" /></Grid>
              <Grid item xs={12} sm={4}><TextField label="Location (State/City)" value={firmLocation} onChange={e => setFirmLocation(e.target.value)} fullWidth /></Grid>
            </Grid>
            <Button variant="contained" sx={{ bgcolor: '#1a2340', '&:hover': { bgcolor: '#22306a' } }}>Search</Button>
            <List sx={{ mt: 2 }}>
              {filteredFirms.map(f => (
                <ListItem key={f.id}>
                  <ListItemText primary={f.name} secondary={`${f.type} | ${f.size} people | ${f.location}`} />
                </ListItem>
              ))}
            </List>
          </Box>
        )}
      </Paper>
      <Typography variant="body2" color="text.secondary">
        (You can add more search parameters here later. This page is designed for easy extension.)
      </Typography>
    </Box>
  );
} 