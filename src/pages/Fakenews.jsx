import { Box, Typography, Button, Grid, Card, CardContent, CardMedia, Container } from '@mui/material';
// You need to import the icon
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import axios from 'axios';


let relatedWebsites = await axios.post('http://localhost:8000/production/get-file-link');
console.log(relatedWebsites.data)

function ScrollingLogos() {
  // ✅ STEP 1: ต่อข้อมูล 2 ชุดเข้าด้วยกันเพื่อให้ไร้รอยต่อ
  const extendedItems = [...relatedWebsites.data];

  const scrollerStyles = {
    display: 'flex', // หรือ 'inline-flex'

    // ✅ STEP 2: Keyframes ที่ถูกต้องสำหรับ "สายพานไร้รอยต่อ"
    animation: 'slide 30s linear infinite', // เพิ่มเวลาเพื่อให้เลื่อนช้าลงและดูง่าย
    '@keyframes slide': {
      'from': {
        transform: 'translateX(0%)',
      },
      'to': {
        // เลื่อนไปแค่ครึ่งเดียว (เท่ากับความยาวของข้อมูล 1 ชุด)
        transform: 'translateX(-50%)',
      }
    }
  };

  return (
    <Box
      sx={{
        width: '100%',
        overflow: 'hidden',
        background: '#1a1a2e', // เพิ่มพื้นหลังเพื่อให้เห็นชัด
        padding: '1rem 0',
        '&:hover .scroller': {
          animationPlayState: 'paused'
        }
      }}
    >
      <Box className="scroller" sx={scrollerStyles}>
        {/* ✅ STEP 3: ใช้ข้อมูลชุดใหม่ที่ต่อกันแล้ว */}
        {extendedItems.map((site, index) => (
          <Box
            key={index}
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              mx: 4,
              flexShrink: 0,
              whiteSpace: 'nowrap'
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <WarningAmberIcon sx={{ color: '#e94560', fontSize: '2.5rem', mr: 1 }} />
              <Typography sx={{ color: '#e94560', fontSize: '2rem', fontWeight: 'bold' }}>
                ข่าวปลอม
              </Typography>
            </Box>
            <Typography sx={{ color: 'white', fontSize: '1.2rem' }}>
              {site.title}
            </Typography>
          </Box>
        ))}
      </Box>
    </Box>
  );
}


// --- UNCHANGED Fakenews Component ---
function Fakenews() {
  return (
    <Box sx={{ width: '100%', backgroundColor: '#101225', color: 'white', py: { xs: 6, md: 8 }, px: 2, }}>

      <ScrollingLogos />

      <Box sx={{ width: '100%', maxWidth: 'lg', mt: 5, mx: 'auto', p: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <WarningAmberIcon sx={{ color: '#e94560', fontSize: '2.5rem', mr: 1 }} />
          <Typography sx={{ color: '#e94560', fontSize: '2rem', fontWeight: 'bold' }}>
            ข่าวปลอม
          </Typography>
        </Box>

        <Grid container spacing={15}> {/* Corrected spacing for better layout */}
          {relatedWebsites.data.map((site, index) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={index}>
              <Card sx={{
                width: '100%',
                height: '100%',
                backgroundColor: '#fff',
                color: '#000',
                borderRadius: '8px',
                display: 'flex',
                flexDirection: 'column',
                boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
                transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
                '&:hover': {
                  transform: 'translateY(-5px)',
                  boxShadow: '0 12px 30px rgba(0,0,0,0.2)'
                }
              }}>
                <CardMedia
                  component="img"
                  height="160"
                  image={site.imageUrl || 'https://via.placeholder.com/400x200.png?text=Image+Not+Found'}
                  alt={site.title}
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent sx={{ flexGrow: 1, p: 2 }}>
                  <Typography gutterBottom variant="h6" component="div" sx={{ fontWeight: 'bold', lineHeight: 1.3 }}>
                    {site.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {site.description ? `${site.description.substring(0, 100)}...` : ''}
                  </Typography>
                </CardContent>
                <Box sx={{ p: 2, pt: 1 }}>
                  <Button
                    component="a"
                    href={site.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    variant="contained"
                    fullWidth
                    sx={{
                      backgroundColor: '#2761aeff',
                      fontWeight: 'bold',
                      '&:hover': {
                        backgroundColor: '#1E4A8C'
                      }
                    }}
                  >
                    รายละเอียดเพิ่มเติม
                  </Button>
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Box>
  );
}

export default Fakenews;