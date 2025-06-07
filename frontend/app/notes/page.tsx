"use client";
import { useState } from "react";
import { Box, Typography, Paper, Button, TextField, List, ListItem, ListItemText, Stack } from "@mui/material";

interface Note {
  id: string;
  content: string;
}

const initialNotes: Note[] = [
  { id: "1", content: "Reached out to 5 new people this week. Cold emails worked best." },
  { id: "2", content: "Follow-ups are more effective on Tuesdays." },
];

export default function NotesPage() {
  const [notes, setNotes] = useState<Note[]>(initialNotes);
  const [newNote, setNewNote] = useState("");

  const addNote = () => {
    if (!newNote.trim()) return;
    setNotes([...notes, { id: crypto.randomUUID(), content: newNote }]);
    setNewNote("");
  };

  const deleteNote = (id: string) => {
    setNotes(notes.filter(n => n.id !== id));
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" mb={3} sx={{ color: '#1a2340' }}>Networking Notes</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" spacing={2} mb={2}>
          <TextField label="Add Note" value={newNote} onChange={e => setNewNote(e.target.value)} fullWidth />
          <Button variant="contained" onClick={addNote} sx={{ bgcolor: '#1a2340', '&:hover': { bgcolor: '#22306a' } }}>Add</Button>
        </Stack>
        <List>
          {notes.map(note => (
            <ListItem key={note.id} secondaryAction={
              <Button color="error" onClick={() => deleteNote(note.id)}>Delete</Button>
            }>
              <ListItemText primary={note.content} />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
} 