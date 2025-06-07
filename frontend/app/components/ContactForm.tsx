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
  Chip,
  Stack,
} from '@mui/material';

interface Contact {
  name: string;
  email?: string;
  phone?: string;
  company?: string;
  role?: string;
  tags: string[];
  linkedin?: string;
  website?: string;
  how_met?: string;
  notes?: string;
  location?: string;
  birthday?: string;
}

interface ContactFormProps {
  open: boolean;
  onClose: () => void;
  onSave: (contact: Contact) => void;
  initialData?: Contact;
}

export default function ContactForm({ open, onClose, onSave, initialData }: ContactFormProps) {
  const [formData, setFormData] = useState<Contact>(
    initialData || {
      name: '',
      email: '',
      phone: '',
      company: '',
      role: '',
      tags: [],
      linkedin: '',
      website: '',
      how_met: '',
      notes: '',
      location: '',
      birthday: '',
    }
  );

  const [tagInput, setTagInput] = useState('');

  const handleChange = (field: keyof Contact) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: event.target.value,
    }));
  };

  const handleAddTag = () => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim())) {
      setFormData((prev) => ({
        ...prev,
        tags: [...prev.tags, tagInput.trim()],
      }));
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setFormData((prev) => ({
      ...prev,
      tags: prev.tags.filter((tag) => tag !== tagToRemove),
    }));
  };

  const handleSubmit = () => {
    if (!formData.name.trim()) {
      // TODO: Show error message
      return;
    }
    onSave(formData);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{initialData ? 'Edit Contact' : 'Add New Contact'}</DialogTitle>
      <DialogContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
          <TextField
            required
            label="Name"
            value={formData.name}
            onChange={handleChange('name')}
            fullWidth
          />
          <TextField
            label="Email"
            value={formData.email}
            onChange={handleChange('email')}
            fullWidth
          />
          <TextField
            label="Phone"
            value={formData.phone}
            onChange={handleChange('phone')}
            fullWidth
          />
          <TextField
            label="Company"
            value={formData.company}
            onChange={handleChange('company')}
            fullWidth
          />
          <TextField
            label="Role"
            value={formData.role}
            onChange={handleChange('role')}
            fullWidth
          />
          <Box>
            <TextField
              label="Tags"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddTag();
                }
              }}
              fullWidth
            />
            <Stack direction="row" spacing={1} sx={{ mt: 1, flexWrap: 'wrap', gap: 1 }}>
              {formData.tags.map((tag) => (
                <Chip
                  key={tag}
                  label={tag}
                  onDelete={() => handleRemoveTag(tag)}
                  color="primary"
                  variant="outlined"
                />
              ))}
            </Stack>
          </Box>
          <TextField
            label="LinkedIn"
            value={formData.linkedin}
            onChange={handleChange('linkedin')}
            fullWidth
          />
          <TextField
            label="Website"
            value={formData.website}
            onChange={handleChange('website')}
            fullWidth
          />
          <TextField
            label="How Met"
            value={formData.how_met}
            onChange={handleChange('how_met')}
            fullWidth
          />
          <TextField
            label="Notes"
            value={formData.notes}
            onChange={handleChange('notes')}
            multiline
            rows={4}
            fullWidth
          />
          <TextField
            label="Location"
            value={formData.location}
            onChange={handleChange('location')}
            fullWidth
          />
          <TextField
            label="Birthday"
            value={formData.birthday}
            onChange={handleChange('birthday')}
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