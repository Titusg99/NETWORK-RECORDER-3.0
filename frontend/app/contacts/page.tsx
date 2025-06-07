"use client";
import { useState } from "react";
import { Box, Typography, Paper, Button, Stack, Grid, Collapse, Card, CardContent, Avatar, TextField, Slider } from "@mui/material";

// Mock contacts for demo
const mockContacts = [
  { id: 1, name: "John Doe", role: "Investment Banker", profession: "Finance", company: "Goldman Sachs", location: "New York", tags: ["lead", "finance"], connectionScore: 80 },
  { id: 2, name: "Jane Smith", role: "VC Partner", profession: "Venture Capital", company: "Arkansas Ventures", location: "Arkansas", tags: ["vc"], connectionScore: 60 },
];

export default function ContactsPage() {
  const [showSearch, setShowSearch] = useState(false);
  const [showAdd, setShowAdd] = useState(false);
  // Advanced filters
  const [search, setSearch] = useState("");
  const [role, setRole] = useState("");
  const [profession, setProfession] = useState("");
  const [company, setCompany] = useState("");
  const [affiliatedCompany, setAffiliatedCompany] = useState("");
  const [location, setLocation] = useState("");
  const [tags, setTags] = useState("");
  const [connectionScore, setConnectionScore] = useState([0, 100]);

  // Filtering logic (mock, to be replaced with backend integration)
  const filteredContacts = mockContacts.filter(c =>
    (!search || c.name.toLowerCase().includes(search.toLowerCase())) &&
    (!role || c.role.toLowerCase().includes(role.toLowerCase())) &&
    (!profession || (c.profession && c.profession.toLowerCase().includes(profession.toLowerCase()))) &&
    (!company || c.company.toLowerCase().includes(company.toLowerCase())) &&
    (!affiliatedCompany || c.company.toLowerCase().includes(affiliatedCompany.toLowerCase())) &&
    (!location || c.location.toLowerCase().includes(location.toLowerCase())) &&
    (!tags || c.tags.some(t => t.toLowerCase().includes(tags.toLowerCase()))) &&
    (c.connectionScore >= connectionScore[0] && c.connectionScore <= connectionScore[1])
  );

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" sx={{ color: '#1a2340', mb: 3 }}>Contacts</Typography>
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} mb={2}>
        <Paper sx={{ p: 2, flex: 1, minWidth: 200 }}>
          <Typography variant="h6" fontWeight="bold" sx={{ color: '#1a2340' }}>Add Person</Typography>
          <Button variant="contained" sx={{ mt: 2, bgcolor: '#1a2340' }} onClick={() => setShowAdd(v => !v)}>
            {showAdd ? "Hide Add" : "Add New"}
          </Button>
          <Collapse in={showAdd}>
            <Grid container spacing={2} mt={2}>
              <Grid item xs={12} sm={6}><TextField label="Name" fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Role/Title" fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Profession" fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Company" fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Affiliated Company" fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Location" fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Tags" fullWidth /></Grid>
              <Grid item xs={12} sm={6}>
                <Typography gutterBottom>Connection Score</Typography>
                <Slider value={[0, 100]} valueLabelDisplay="auto" min={0} max={100} />
              </Grid>
              <Grid item xs={12}><Button variant="contained" sx={{ bgcolor: '#1a2340' }}>Save</Button></Grid>
            </Grid>
          </Collapse>
        </Paper>
        <Paper sx={{ p: 2, flex: 1, minWidth: 200 }}>
          <Typography variant="h6" fontWeight="bold" sx={{ color: '#1a2340' }}>Search</Typography>
          <Button variant="outlined" sx={{ mt: 2, color: '#1a2340', borderColor: '#1a2340' }} onClick={() => setShowSearch(v => !v)}>
            {showSearch ? "Hide Search" : "Show Search"}
          </Button>
          <Collapse in={showSearch}>
            <Grid container spacing={2} mt={2}>
              <Grid item xs={12} sm={6}><TextField label="Name" value={search} onChange={e => setSearch(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Role/Title" value={role} onChange={e => setRole(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Profession" value={profession} onChange={e => setProfession(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Company" value={company} onChange={e => setCompany(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Affiliated Company" value={affiliatedCompany} onChange={e => setAffiliatedCompany(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Location" value={location} onChange={e => setLocation(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Tags" value={tags} onChange={e => setTags(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}>
                <Typography gutterBottom>Connection Score</Typography>
                <Slider
                  value={connectionScore}
                  onChange={(_, v) => setConnectionScore(v as number[])}
                  valueLabelDisplay="auto"
                  min={0}
                  max={100}
                />
              </Grid>
            </Grid>
          </Collapse>
        </Paper>
      </Stack>
      <Stack spacing={2}>
        {filteredContacts.map(contact => (
          <Card key={contact.id} sx={{ borderRadius: 3, boxShadow: 2, p: 2, display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
            <Avatar sx={{ bgcolor: '#1a2340', width: 56, height: 56 }}>{contact.name[0]}</Avatar>
            <CardContent sx={{ flex: 1, p: 0 }}>
              <Typography variant="h6" fontWeight="bold">{contact.name}</Typography>
              <Typography variant="body2" color="text.secondary">{contact.role} at {contact.company}</Typography>
              <Typography variant="body2" color="text.secondary">{contact.profession}</Typography>
              <Typography variant="body2" color="text.secondary">{contact.location}</Typography>
              <Typography variant="body2" color="text.secondary">Connection Score: {contact.connectionScore}</Typography>
              <Stack direction="row" spacing={1} mt={1}>
                {contact.tags.map(tag => (
                  <Paper key={tag} sx={{ px: 1, py: 0.5, borderRadius: 2, bgcolor: '#e6f7e6', color: '#1a2340', fontSize: 12 }}>{tag}</Paper>
                ))}
              </Stack>
            </CardContent>
          </Card>
        ))}
      </Stack>
    </Box>
  );
} 