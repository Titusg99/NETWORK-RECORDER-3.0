import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface Contact {
  id: string;
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
  last_interaction?: Date;
  next_followup?: Date;
}

export interface Interaction {
  id: string;
  contactId: string;
  date: Date;
  type: 'Meeting' | 'Call' | 'Email' | 'Other';
  summary: string;
}

interface Store {
  contacts: Contact[];
  interactions: Interaction[];
  addContact: (contact: Omit<Contact, 'id'>) => void;
  updateContact: (id: string, contact: Partial<Contact>) => void;
  deleteContact: (id: string) => void;
  addInteraction: (interaction: Omit<Interaction, 'id'>) => void;
  deleteInteraction: (id: string) => void;
}

export const useStore = create<Store>()(
  persist(
    (set) => ({
      contacts: [],
      interactions: [],
      addContact: (contact) =>
        set((state) => ({
          contacts: [
            ...state.contacts,
            { ...contact, id: crypto.randomUUID() },
          ],
        })),
      updateContact: (id, contact) =>
        set((state) => ({
          contacts: state.contacts.map((c) =>
            c.id === id ? { ...c, ...contact } : c
          ),
        })),
      deleteContact: (id) =>
        set((state) => ({
          contacts: state.contacts.filter((c) => c.id !== id),
          interactions: state.interactions.filter((i) => i.contactId !== id),
        })),
      addInteraction: (interaction) =>
        set((state) => ({
          interactions: [
            ...state.interactions,
            { ...interaction, id: crypto.randomUUID() },
          ],
        })),
      deleteInteraction: (id) =>
        set((state) => ({
          interactions: state.interactions.filter((i) => i.id !== id),
        })),
    }),
    {
      name: 'network-tracker-storage',
    }
  )
); 