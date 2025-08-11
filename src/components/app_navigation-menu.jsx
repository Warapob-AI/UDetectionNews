import React, { useState } from 'react';
import {
  AppBar, Toolbar, Typography, Button, IconButton, Menu, MenuItem,
  CssBaseline, Container, useTheme, useMediaQuery
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import TypewriterTypography from './app_typewriter-typography'; 

const navItems = ['หน้าแรก', 'ตรวจสอบ', 'ข่าวจริง', 'ข่าวปลอม', 'เกี่ยวกับเรา'];

const navButtonStyle = {
  fontWeight: 600,
  mx: 1.5,
  fontSize: '0.85rem',
  transition: '0.3s',
  color: '#FFFFFF',
  '&:hover': {
    backgroundColor: 'rgba(30, 41, 59)',
    color: '#FFFFFF',
  },
};

export default function Navbar() {
  const theme = useTheme();
  const isMobile = useMediaQuery('(max-width:869px)');
  const [anchorEl, setAnchorEl] = useState(null);

  const handleMenuOpen = (event) => setAnchorEl(event.currentTarget);
  const handleMenuClose = () => setAnchorEl(null);

  return (
    <>
      <CssBaseline />
      <AppBar sx={{ background: 'linear-gradient(to right, #101125, #101125)' }}>
        <Container maxWidth="xl">
          <Toolbar>
            <Typography
              variant="h6"
              sx={{ flexGrow: 1, fontFamily: '"IBM Plex Sans Thai", sans-serif', fontWeight: 600 }}
            >
              <TypewriterTypography variant="h6" fontWeight={600} text={'UDetectionNews'} speed={80}/>
            </Typography>

            {/* ถ้าหน้าจอเล็ก แสดง MenuIcon */}
            {isMobile ? (
              <>
                <IconButton color="inherit" onClick={handleMenuOpen}>
                  <MenuIcon />
                </IconButton>
                <Menu
                  anchorEl={anchorEl}
                  open={Boolean(anchorEl)}
                  onClose={handleMenuClose}
                >
                  {navItems.map((item) => (
                    <MenuItem key={item} onClick={handleMenuClose}>
                      {item}
                    </MenuItem>
                  ))}
                </Menu>
              </>
            ) : (
              // ถ้าหน้าจอใหญ่ แสดงปุ่มปกติ
              navItems.map((item) => (
                <Button key={item} color="inherit" sx={navButtonStyle}>
                  {item}
                </Button>
              ))
            )}
          </Toolbar>
        </Container>
      </AppBar>
    </>
  );
}
