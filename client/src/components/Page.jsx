import * as React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

export default function Page({title, children}) {
  return (
    <Box sx={{ height: 640, width: '100%' }}>
    <Typography
      variant="h2"
      align="left"
      sx={{
        color: 'text.secondary',
      }}
    >{ title }
    </Typography>
    {children}
    </Box>
  );
}