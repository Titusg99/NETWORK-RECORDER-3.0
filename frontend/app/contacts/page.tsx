"use client";
import { useState } from "react";
import { Box, Typography, Paper, TextField, Button, Stack } from "@mui/material";
import ContactList from "../components/ContactList";

export default function ContactsPage() {
  const [search, setSearch] = useState("");
  const [showLeads, setShowLeads] = useState(false);
  // Filtering will be implemented with backend integration
  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: { xs: 'flex-start', sm: 'center' }, mb: 3, gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
        <Typography variant="h4" fontWeight="bold" sx={{ color: '#1a2340' }}>Contacts</Typography>
        <Stack direction="row" spacing={2} sx={{ width: { xs: '100%', sm: 'auto' } }}>
          <Button variant={showLeads ? "contained" : "outlined"} sx={{ bgcolor: showLeads ? '#1a2340' : undefined, color: showLeads ? '#fff' : '#1a2340', borderColor: '#1a2340', width: { xs: '100%', sm: 'auto' } }} onClick={() => setShowLeads(!showLeads)}>
            {showLeads ? "Show All" : "Show Leads"}
          </Button>
        </Stack>
      </Box>
      <Paper sx={{ p: { xs: 2, sm: 3 }, mb: 3 }}>
        <TextField
          label="Search Contacts"
          value={search}
          onChange={e => setSearch(e.target.value)}
          fullWidth
          sx={{ mb: 2 }}
        />
        {/* Pass showLeads and search as props for future filtering */}
        <ContactList />
      </Paper>
    </Box>
  );
} 