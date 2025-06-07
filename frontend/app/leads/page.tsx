"use client";
import { useState } from "react";
import { Box, Typography, Paper, Button, List, ListItem, ListItemText, TextField, Stack } from "@mui/material";

interface Lead {
  id: string;
  name: string;
  company?: string;
  status: "New" | "Contacted" | "Interested";
}

const initialLeads: Lead[] = [
  { id: "1", name: "Sarah Lee", company: "Acme Corp", status: "New" },
  { id: "2", name: "Tom Brown", company: "Beta Inc", status: "Contacted" },
];

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>(initialLeads);
  const [newName, setNewName] = useState("");
  const [newCompany, setNewCompany] = useState("");

  const addLead = () => {
    if (!newName.trim()) return;
    setLeads([
      ...leads,
      { id: crypto.randomUUID(), name: newName, company: newCompany, status: "New" },
    ]);
    setNewName("");
    setNewCompany("");
  };

  const convertToContact = (id: string) => {
    setLeads(leads.filter(l => l.id !== id));
    // In the future, add to contacts store
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" mb={3}>Leads</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" spacing={2} mb={2}>
          <TextField label="Name" value={newName} onChange={e => setNewName(e.target.value)} fullWidth />
          <TextField label="Company" value={newCompany} onChange={e => setNewCompany(e.target.value)} fullWidth />
          <Button variant="contained" onClick={addLead}>Add Lead</Button>
        </Stack>
        <List>
          {leads.map(lead => (
            <ListItem key={lead.id} secondaryAction={
              <Button variant="outlined" onClick={() => convertToContact(lead.id)}>Convert to Contact</Button>
            }>
              <ListItemText
                primary={lead.name}
                secondary={lead.company ? `Company: ${lead.company} | Status: ${lead.status}` : `Status: ${lead.status}`}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
} 