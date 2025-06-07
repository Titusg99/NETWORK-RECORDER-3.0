'use client';

import { useState } from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Typography,
  Box,
  Chip,
  Stack,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import { useStore, Contact } from '../store/useStore';
import ContactForm from './ContactForm';
import InteractionForm from './InteractionForm';

export default function ContactList() {
  const { contacts, deleteContact, updateContact } = useStore();
  const [editingContact, setEditingContact] = useState<Contact | null>(null);
  const [isContactFormOpen, setIsContactFormOpen] = useState(false);
  const [isInteractionFormOpen, setIsInteractionFormOpen] = useState(false);
  const [selectedContactId, setSelectedContactId] = useState<string | null>(null);

  const handleEdit = (contact: Contact) => {
    setEditingContact(contact);
    setIsContactFormOpen(true);
  };

  const handleDelete = (id: string) => {
    if (window.confirm('Are you sure you want to delete this contact?')) {
      deleteContact(id);
    }
  };

  const handleLogInteraction = (id: string) => {
    setSelectedContactId(id);
    setIsInteractionFormOpen(true);
  };

  const formatDate = (date?: Date) => {
    if (!date) return 'Never';
    return new Date(date).toLocaleDateString();
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6">Contacts</Typography>
        <IconButton
          color="primary"
          onClick={() => {
            setEditingContact(null);
            setIsContactFormOpen(true);
          }}
        >
          <AddIcon />
        </IconButton>
      </Box>

      <List>
        {contacts.map((contact) => (
          <ListItem
            key={contact.id}
            sx={{
              bgcolor: 'background.paper',
              mb: 1,
              borderRadius: 1,
              '&:hover': {
                bgcolor: 'action.hover',
              },
            }}
          >
            <ListItemText
              primary={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Typography variant="subtitle1">{contact.name}</Typography>
                  {contact.company && (
                    <Typography variant="body2" color="text.secondary">
                      at {contact.company}
                    </Typography>
                  )}
                </Box>
              }
              secondary={
                <Box sx={{ mt: 1 }}>
                  <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
                    {contact.tags.map((tag) => (
                      <Chip
                        key={tag}
                        label={tag}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                    ))}
                  </Stack>
                  <Typography variant="body2" color="text.secondary">
                    Last interaction: {formatDate(contact.last_interaction)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Next follow-up: {formatDate(contact.next_followup)}
                  </Typography>
                </Box>
              }
            />
            <ListItemSecondaryAction>
              <IconButton
                edge="end"
                aria-label="log interaction"
                onClick={() => handleLogInteraction(contact.id)}
                sx={{ mr: 1 }}
              >
                <AddIcon />
              </IconButton>
              <IconButton
                edge="end"
                aria-label="edit"
                onClick={() => handleEdit(contact)}
                sx={{ mr: 1 }}
              >
                <EditIcon />
              </IconButton>
              <IconButton
                edge="end"
                aria-label="delete"
                onClick={() => handleDelete(contact.id)}
              >
                <DeleteIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>

      <ContactForm
        open={isContactFormOpen}
        onClose={() => {
          setIsContactFormOpen(false);
          setEditingContact(null);
        }}
        onSave={(contact) => {
          if (editingContact) {
            updateContact(editingContact.id, contact);
          } else {
            updateContact(contact.id, {
              ...contact,
              last_interaction: new Date(),
              next_followup: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
            });
          }
        }}
        initialData={editingContact || undefined}
      />

      {selectedContactId && (
        <InteractionForm
          open={isInteractionFormOpen}
          onClose={() => {
            setIsInteractionFormOpen(false);
            setSelectedContactId(null);
          }}
          contactId={selectedContactId}
        />
      )}
    </Box>
  );
} 