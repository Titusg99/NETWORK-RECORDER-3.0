from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import List, Optional
import json

# Default follow-up intervals (in days) by tag
DEFAULT_FOLLOWUP_INTERVALS = {
    'VC': 60,
    'Banking': 30,
    'Friend': 90,
    'Default': 30,
}

@dataclass
class Interaction:
    date: datetime
    type: str  # e.g., meeting, call, email
    summary: str

    def to_dict(self):
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'type': self.type,
            'summary': self.summary,
        }

    @staticmethod
    def from_dict(data):
        return Interaction(
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            type=data['type'],
            summary=data['summary'],
        )

@dataclass
class Contact:
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    linkedin: Optional[str] = None
    website: Optional[str] = None
    how_met: Optional[str] = None
    notes: Optional[str] = None
    last_interaction: Optional[datetime] = None
    next_followup: Optional[datetime] = None
    location: Optional[str] = None
    birthday: Optional[str] = None
    interactions: List[Interaction] = field(default_factory=list)

    def calculate_next_followup(self, intervals=None):
        intervals = intervals or DEFAULT_FOLLOWUP_INTERVALS
        interval = intervals.get('Default', 30)
        for tag in self.tags:
            if tag in intervals:
                interval = intervals[tag]
                break
        base_date = self.last_interaction or datetime.now()
        self.next_followup = base_date + timedelta(days=interval)

    def log_interaction(self, interaction, intervals=None):
        self.interactions.append(interaction)
        self.last_interaction = interaction.date
        self.calculate_next_followup(intervals)

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'role': self.role,
            'tags': self.tags,
            'linkedin': self.linkedin,
            'website': self.website,
            'how_met': self.how_met,
            'notes': self.notes,
            'last_interaction': self.last_interaction.strftime('%Y-%m-%d') if self.last_interaction else None,
            'next_followup': self.next_followup.strftime('%Y-%m-%d') if self.next_followup else None,
            'location': self.location,
            'birthday': self.birthday,
            'interactions': [i.to_dict() for i in self.interactions],
        }

    @staticmethod
    def from_dict(data):
        c = Contact(
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            company=data.get('company'),
            role=data.get('role'),
            tags=data.get('tags', []),
            linkedin=data.get('linkedin'),
            website=data.get('website'),
            how_met=data.get('how_met'),
            notes=data.get('notes'),
            last_interaction=datetime.strptime(data['last_interaction'], '%Y-%m-%d') if data.get('last_interaction') else None,
            next_followup=datetime.strptime(data['next_followup'], '%Y-%m-%d') if data.get('next_followup') else None,
            location=data.get('location'),
            birthday=data.get('birthday'),
            interactions=[Interaction.from_dict(i) for i in data.get('interactions', [])],
        )
        return c

# Utility functions for saving/loading

def save_contacts(contacts, path):
    with open(path, 'w') as f:
        json.dump([c.to_dict() for c in contacts], f, indent=2)

def load_contacts(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return [Contact.from_dict(c) for c in data]
    except Exception:
        return [] 