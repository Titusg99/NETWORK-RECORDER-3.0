"use client";
import { useState } from "react";
import { Box, Typography, Paper, Button, List, ListItem, ListItemText, TextField, Stack } from "@mui/material";

interface Opportunity {
  id: string;
  title: string;
  date: string;
  company?: string;
  contact?: string;
}

const initialOpportunities: Opportunity[] = [
  { id: "1", title: "Interview at Acme Corp", date: "2024-06-15", company: "Acme Corp", contact: "Sarah Lee" },
  { id: "2", title: "Coffee with Tom Brown", date: "2024-06-20", contact: "Tom Brown" },
];

export default function OpportunitiesPage() {
  const [opps, setOpps] = useState<Opportunity[]>(initialOpportunities);
  const [newTitle, setNewTitle] = useState("");
  const [newDate, setNewDate] = useState("");
  const [newCompany, setNewCompany] = useState("");
  const [newContact, setNewContact] = useState("");

  const addOpp = () => {
    if (!newTitle.trim() || !newDate) return;
    setOpps([
      ...opps,
      { id: crypto.randomUUID(), title: newTitle, date: newDate, company: newCompany, contact: newContact },
    ]);
    setNewTitle("");
    setNewDate("");
    setNewCompany("");
    setNewContact("");
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" mb={3}>Opportunities</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" spacing={2} mb={2}>
          <TextField label="Title" value={newTitle} onChange={e => setNewTitle(e.target.value)} fullWidth />
          <TextField label="Date" type="date" value={newDate} onChange={e => setNewDate(e.target.value)} InputLabelProps={{ shrink: true }} />
          <TextField label="Company" value={newCompany} onChange={e => setNewCompany(e.target.value)} fullWidth />
          <TextField label="Contact" value={newContact} onChange={e => setNewContact(e.target.value)} fullWidth />
          <Button variant="contained" onClick={addOpp}>Add</Button>
        </Stack>
        <List>
          {opps.map(opp => (
            <ListItem key={opp.id}>
              <ListItemText
                primary={opp.title}
                secondary={`Date: ${opp.date}${opp.company ? ` | Company: ${opp.company}` : ""}${opp.contact ? ` | Contact: ${opp.contact}` : ""}`}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
} 