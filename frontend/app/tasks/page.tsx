"use client";
import { useState } from "react";
import { Box, Typography, Paper, Button, List, ListItem, ListItemText, Checkbox, TextField, Stack } from "@mui/material";

interface Task {
  id: string;
  title: string;
  due: string;
  done: boolean;
}

const initialTasks: Task[] = [
  { id: "1", title: "Follow up with Jane Doe", due: "2024-06-10", done: false },
  { id: "2", title: "Send resume to Acme Corp", due: "2024-06-12", done: false },
  { id: "3", title: "Call John Smith", due: "2024-06-08", done: true },
];

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [newTask, setNewTask] = useState("");
  const [newDue, setNewDue] = useState("");

  const addTask = () => {
    if (!newTask.trim() || !newDue) return;
    setTasks([
      ...tasks,
      { id: crypto.randomUUID(), title: newTask, due: newDue, done: false },
    ]);
    setNewTask("");
    setNewDue("");
  };

  const toggleDone = (id: string) => {
    setTasks(tasks.map(t => t.id === id ? { ...t, done: !t.done } : t));
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" mb={3}>Tasks & Follow-ups</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" spacing={2} mb={2}>
          <TextField label="New Task" value={newTask} onChange={e => setNewTask(e.target.value)} fullWidth />
          <TextField label="Due Date" type="date" value={newDue} onChange={e => setNewDue(e.target.value)} InputLabelProps={{ shrink: true }} />
          <Button variant="contained" onClick={addTask}>Add</Button>
        </Stack>
        <List>
          {tasks.map(task => (
            <ListItem key={task.id} secondaryAction={
              <Checkbox checked={task.done} onChange={() => toggleDone(task.id)} />
            }>
              <ListItemText
                primary={task.title}
                secondary={`Due: ${task.due}`}
                sx={{ textDecoration: task.done ? "line-through" : "none" }}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
} 