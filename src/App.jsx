// App.jsx
import React from 'react';
import './App.css'

import {
  AppBar, Toolbar, IconButton, Typography, Button, Drawer, List, ListItem, ListItemText,
  Box, Container, CssBaseline, useTheme, useMediaQuery, Grid,
} from '@mui/material';

import { createTheme, ThemeProvider } from '@mui/material/styles';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Validation from './pages/Validation.jsx';
import DetectText from './pages/Check.jsx';
import Home from './pages/Home.jsx';
import Navbar from './components/app_navigation-menu.jsx';


const theme = createTheme({
  typography: {
    fontFamily: '"IBM Plex Sans Thai", sans-serif',
  },
});

function App() {
  return (
    <>
      {/* Navbar */}
      <ThemeProvider theme={theme}>
        {/* พื้นหลังฟองอากาศ */}

        <CssBaseline />

        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={
              <>
                <Home />
                <DetectText />
              </>
            } />
            <Route path="/detectText" element={<DetectText />} /> {/* ✅ ตรงกับ navigate */}
            <Route path="/validation" element={<Validation />} /> {/* ✅ ตรงกับ navigate */}
          </Routes>
        </Router>


      </ThemeProvider>
    </>
  );
}

export default App;
