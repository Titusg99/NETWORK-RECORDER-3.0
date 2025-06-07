"use client";
import { Box, Typography, Paper } from "@mui/material";

export default function SettingsPage() {
  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" mb={3}>Settings</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="body1">Settings and preferences will be available here. (Data export/import, app preferences, etc.)</Typography>
      </Paper>
    </Box>
  );
} 