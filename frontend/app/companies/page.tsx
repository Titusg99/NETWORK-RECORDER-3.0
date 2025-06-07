"use client";
import { useState } from "react";
import { Box, Typography, Paper, Button, Stack, Grid, Collapse, Card, CardContent, Avatar, TextField, MenuItem, Dialog, DialogTitle, DialogContent, List, ListItem, ListItemText } from "@mui/material";

interface Company {
  id: string;
  name: string;
  location?: string;
  type?: string;
  stage?: string;
  employeeCount?: number;
  industry?: string;
  website?: string;
  employees?: { id: string; name: string; role: string }[];
}

const stageOptions = [
  "Pre-Seed", "Seed", "Series A", "Series B", "Series C", "Series D", "Private", "Public", "Other"
];
const employeeCountOptions = [10, 20, 50, 100, 200, 500, 1000, 5000, 10000];

const initialCompanies: Company[] = [
  {
    id: "1",
    name: "Acme Corp",
    location: "New York, NY",
    type: "Tech",
    stage: "Series B",
    employeeCount: 200,
    industry: "Technology",
    website: "acme.com",
    employees: [
      { id: "1", name: "John Doe", role: "CTO" },
      { id: "2", name: "Jane Smith", role: "Engineer" },
    ],
  },
  {
    id: "2",
    name: "Beta Inc",
    location: "San Francisco, CA",
    type: "VC",
    stage: "Seed",
    employeeCount: 15,
    industry: "Venture Capital",
    website: "betainc.com",
    employees: [
      { id: "3", name: "Alice Brown", role: "Partner" },
    ],
  },
];

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>(initialCompanies);
  const [showAdd, setShowAdd] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
  const [modalCompany, setModalCompany] = useState<Company | null>(null);
  // Add form fields
  const [newName, setNewName] = useState("");
  const [newLocation, setNewLocation] = useState("");
  const [newType, setNewType] = useState("");
  const [newStage, setNewStage] = useState("");
  const [newEmployeeCount, setNewEmployeeCount] = useState<number | "">("");
  const [newIndustry, setNewIndustry] = useState("");
  const [newWebsite, setNewWebsite] = useState("");
  // Filters
  const [filterName, setFilterName] = useState("");
  const [filterType, setFilterType] = useState("");
  const [filterStage, setFilterStage] = useState("");
  const [filterEmployeeCount, setFilterEmployeeCount] = useState<number | "">("");
  const [filterLocation, setFilterLocation] = useState("");
  const [filterIndustry, setFilterIndustry] = useState("");
  const [filterWebsite, setFilterWebsite] = useState("");

  // Filtering logic (mock, to be replaced with backend integration)
  const filteredCompanies = companies.filter(c =>
    (!filterName || c.name.toLowerCase().includes(filterName.toLowerCase())) &&
    (!filterType || (c.type && c.type.toLowerCase().includes(filterType.toLowerCase()))) &&
    (!filterStage || (c.stage && c.stage === filterStage)) &&
    (!filterLocation || (c.location && c.location.toLowerCase().includes(filterLocation.toLowerCase()))) &&
    (!filterEmployeeCount || (c.employeeCount && c.employeeCount === filterEmployeeCount)) &&
    (!filterIndustry || (c.industry && c.industry.toLowerCase().includes(filterIndustry.toLowerCase()))) &&
    (!filterWebsite || (c.website && c.website.toLowerCase().includes(filterWebsite.toLowerCase())))
  );

  const addCompany = () => {
    if (!newName.trim()) return;
    setCompanies([
      ...companies,
      {
        id: crypto.randomUUID(),
        name: newName,
        location: newLocation,
        type: newType,
        stage: newStage,
        employeeCount: newEmployeeCount ? Number(newEmployeeCount) : undefined,
        industry: newIndustry,
        website: newWebsite,
        employees: [],
      },
    ]);
    setNewName("");
    setNewLocation("");
    setNewType("");
    setNewStage("");
    setNewEmployeeCount("");
    setNewIndustry("");
    setNewWebsite("");
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" mb={3} sx={{ color: '#1a2340' }}>Companies</Typography>
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} mb={2}>
        <Paper sx={{ p: 2, flex: 1, minWidth: 200 }}>
          <Typography variant="h6" fontWeight="bold" sx={{ color: '#1a2340' }}>Add Company</Typography>
          <Button variant="contained" sx={{ mt: 2, bgcolor: '#1a2340' }} onClick={() => setShowAdd(v => !v)}>
            {showAdd ? "Hide Add" : "Add Company"}
          </Button>
          <Collapse in={showAdd}>
            <Grid container spacing={2} mt={2}>
              <Grid item xs={12} sm={6}><TextField label="Name" value={newName} onChange={e => setNewName(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Type" value={newType} onChange={e => setNewType(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Industry" value={newIndustry} onChange={e => setNewIndustry(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField select label="Stage" value={newStage} onChange={e => setNewStage(e.target.value)} fullWidth>
                {stageOptions.map(opt => <MenuItem key={opt} value={opt}>{opt}</MenuItem>)}
              </TextField></Grid>
              <Grid item xs={12} sm={6}><TextField select label="Employee Count" value={newEmployeeCount} onChange={e => setNewEmployeeCount(Number(e.target.value))} fullWidth>
                {employeeCountOptions.map(opt => <MenuItem key={opt} value={opt}>{opt}</MenuItem>)}
              </TextField></Grid>
              <Grid item xs={12} sm={6}><TextField label="Location" value={newLocation} onChange={e => setNewLocation(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={6}><TextField label="Website" value={newWebsite} onChange={e => setNewWebsite(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12}><Button variant="contained" sx={{ bgcolor: '#1a2340' }} onClick={addCompany}>Save</Button></Grid>
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
              <Grid item xs={12} sm={4}><TextField label="Name" value={filterName} onChange={e => setFilterName(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={4}><TextField label="Type" value={filterType} onChange={e => setFilterType(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={4}><TextField label="Industry" value={filterIndustry} onChange={e => setFilterIndustry(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={4}><TextField select label="Stage" value={filterStage} onChange={e => setFilterStage(e.target.value)} fullWidth>
                <MenuItem value="">Any</MenuItem>
                {stageOptions.map(opt => <MenuItem key={opt} value={opt}>{opt}</MenuItem>)}
              </TextField></Grid>
              <Grid item xs={12} sm={4}><TextField select label="Employee Count" value={filterEmployeeCount} onChange={e => setFilterEmployeeCount(Number(e.target.value))} fullWidth>
                <MenuItem value="">Any</MenuItem>
                {employeeCountOptions.map(opt => <MenuItem key={opt} value={opt}>{opt}</MenuItem>)}
              </TextField></Grid>
              <Grid item xs={12} sm={4}><TextField label="Location" value={filterLocation} onChange={e => setFilterLocation(e.target.value)} fullWidth /></Grid>
              <Grid item xs={12} sm={4}><TextField label="Website" value={filterWebsite} onChange={e => setFilterWebsite(e.target.value)} fullWidth /></Grid>
            </Grid>
          </Collapse>
        </Paper>
      </Stack>
      <Stack spacing={2}>
        {filteredCompanies.map(company => (
          <Card key={company.id} sx={{ borderRadius: 2, boxShadow: 1, p: 1, display: 'flex', alignItems: 'center', gap: 2, width: '100%', minHeight: 64, cursor: 'pointer', maxWidth: 600 }} onClick={() => setModalCompany(company)}>
            <Avatar sx={{ bgcolor: '#1a2340', width: 40, height: 40 }}>{company.name[0]}</Avatar>
            <CardContent sx={{ flex: 1, p: 0 }}>
              <Typography variant="subtitle1" fontWeight="bold">{company.name}</Typography>
              <Typography variant="body2" color="text.secondary">{company.type} {company.stage ? `| ${company.stage}` : ''} {company.employeeCount ? `| ${company.employeeCount} employees` : ''}</Typography>
              <Typography variant="body2" color="text.secondary">{company.industry}</Typography>
              <Typography variant="body2" color="text.secondary">{company.location}</Typography>
            </CardContent>
          </Card>
        ))}
      </Stack>
      <Dialog open={!!modalCompany} onClose={() => setModalCompany(null)} maxWidth="sm" fullWidth>
        <DialogTitle>{modalCompany?.name} Profile</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary">Type: {modalCompany?.type}</Typography>
          <Typography variant="body2" color="text.secondary">Stage: {modalCompany?.stage}</Typography>
          <Typography variant="body2" color="text.secondary">Employee Count: {modalCompany?.employeeCount}</Typography>
          <Typography variant="body2" color="text.secondary">Industry: {modalCompany?.industry}</Typography>
          <Typography variant="body2" color="text.secondary">Location: {modalCompany?.location}</Typography>
          <Typography variant="body2" color="text.secondary">Website: {modalCompany?.website}</Typography>
          <Typography variant="h6" mt={2}>Associated Employees</Typography>
          <List>
            {modalCompany?.employees?.length ? modalCompany.employees.map(emp => (
              <ListItem key={emp.id}>
                <ListItemText primary={emp.name} secondary={emp.role} />
              </ListItem>
            )) : <ListItem><ListItemText primary="No employees listed." /></ListItem>}
          </List>
        </DialogContent>
      </Dialog>
    </Box>
  );
} 