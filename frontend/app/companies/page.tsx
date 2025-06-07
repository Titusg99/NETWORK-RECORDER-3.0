"use client";
import { useState } from "react";
import { Box, Typography, Paper, Button, List, ListItem, ListItemText, TextField, Stack } from "@mui/material";

interface Company {
  id: string;
  name: string;
  location?: string;
}

const initialCompanies: Company[] = [
  { id: "1", name: "Acme Corp", location: "New York, NY" },
  { id: "2", name: "Beta Inc", location: "San Francisco, CA" },
];

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>(initialCompanies);
  const [newName, setNewName] = useState("");
  const [newLocation, setNewLocation] = useState("");

  const addCompany = () => {
    if (!newName.trim()) return;
    setCompanies([
      ...companies,
      { id: crypto.randomUUID(), name: newName, location: newLocation },
    ]);
    setNewName("");
    setNewLocation("");
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" mb={3}>Companies</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" spacing={2} mb={2}>
          <TextField label="Company Name" value={newName} onChange={e => setNewName(e.target.value)} fullWidth />
          <TextField label="Location" value={newLocation} onChange={e => setNewLocation(e.target.value)} fullWidth />
          <Button variant="contained" onClick={addCompany}>Add Company</Button>
        </Stack>
        <List>
          {companies.map(company => (
            <ListItem key={company.id}>
              <ListItemText
                primary={company.name}
                secondary={company.location}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
} 