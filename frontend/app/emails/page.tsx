"use client";
import { useState } from "react";
import { Box, Typography, Paper, Button, List, ListItem, ListItemText, TextField, Stack } from "@mui/material";

interface EmailTemplate {
  id: string;
  name: string;
  content: string;
}

const initialTemplates: EmailTemplate[] = [
  { id: "1", name: "Intro Email", content: "Hi, I wanted to connect..." },
  { id: "2", name: "Follow-up", content: "Just checking in..." },
];

export default function EmailsPage() {
  const [templates, setTemplates] = useState<EmailTemplate[]>(initialTemplates);
  const [newName, setNewName] = useState("");
  const [newContent, setNewContent] = useState("");

  const addTemplate = () => {
    if (!newName.trim() || !newContent.trim()) return;
    setTemplates([
      ...templates,
      { id: crypto.randomUUID(), name: newName, content: newContent },
    ]);
    setNewName("");
    setNewContent("");
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" mb={3}>Email Templates</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" spacing={2} mb={2}>
          <TextField label="Template Name" value={newName} onChange={e => setNewName(e.target.value)} fullWidth />
          <TextField label="Content" value={newContent} onChange={e => setNewContent(e.target.value)} fullWidth multiline rows={2} />
          <Button variant="contained" onClick={addTemplate}>Add Template</Button>
        </Stack>
        <List>
          {templates.map(template => (
            <ListItem key={template.id}>
              <ListItemText
                primary={template.name}
                secondary={template.content}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
} 