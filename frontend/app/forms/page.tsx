"use client";
import { useState } from "react";
import { Box, Typography, Paper, Button, List, ListItem, ListItemText, Stack } from "@mui/material";

interface FileItem {
  id: string;
  name: string;
}

const initialFiles: FileItem[] = [
  { id: "1", name: "Resume.pdf" },
  { id: "2", name: "CoverLetter.docx" },
];

export default function FormsPage() {
  const [files, setFiles] = useState<FileItem[]>(initialFiles);

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      setFiles([...files, { id: crypto.randomUUID(), name: file.name }]);
    }
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" mb={3}>Forms & Documents</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" spacing={2} mb={2}>
          <Button variant="contained" component="label">
            Upload File
            <input type="file" hidden onChange={handleUpload} />
          </Button>
        </Stack>
        <List>
          {files.map(file => (
            <ListItem key={file.id}>
              <ListItemText primary={file.name} />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
} 