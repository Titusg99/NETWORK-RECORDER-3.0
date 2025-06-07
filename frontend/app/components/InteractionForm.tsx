'use client';

import { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  MenuItem,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { useStore } from '../store/useStore';

interface InteractionFormProps {
  open: boolean;
  onClose: () => void;
  contactId: string;
}

export default function InteractionForm({ open, onClose, contactId }: InteractionFormProps) {
  const [date, setDate] = useState<Date>(new Date());
  const [type, setType] = useState<'Meeting' | 'Call' | 'Email' | 'Other'>('Meeting');
  const [summary, setSummary] = useState('');
  const { addInteraction, updateContact } = useStore();

  const handleSubmit = () => {
    if (!summary.trim()) {
      // TODO: Show error message
      return;
    }

    addInteraction({
      contactId,
      date,
      type,
      summary: summary.trim(),
    });

    // Update contact's last interaction and next followup
    updateContact(contactId, {
      last_interaction: date,
      next_followup: new Date(date.getTime() + 7 * 24 * 60 * 60 * 1000), // 7 days from interaction
    });

    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Log Interaction</DialogTitle>
      <DialogContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
          <DatePicker
            label="Date"
            value={date}
            onChange={(newDate) => newDate && setDate(newDate)}
          />
          <TextField
            select
            label="Type"
            value={type}
            onChange={(e) => setType(e.target.value as typeof type)}
            fullWidth
          >
            <MenuItem value="Meeting">Meeting</MenuItem>
            <MenuItem value="Call">Call</MenuItem>
            <MenuItem value="Email">Email</MenuItem>
            <MenuItem value="Other">Other</MenuItem>
          </TextField>
          <TextField
            label="Summary"
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
            multiline
            rows={4}
            fullWidth
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
} 