// 📁 src/pages/detectText.jsx (ที่แก้ไขแล้ว)

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
// ✅ 1. เพิ่ม Grid เข้าไปใน import
import { Box, Typography, TextField, Button, CircularProgress, Grid, Container } from '@mui/material';
import axios from 'axios';
// เพิ่ม State สำหรับสลับโหมด


// ตรวจสอบว่ามี import เหล่านี้แล้ว
import { ToggleButton, ToggleButtonGroup } from '@mui/material';
// ✅ 2. ย้ายข้อมูลและ Component ออกมาไว้นอก DetectText
// สร้าง Array ของข้อมูลไว้นอก Component เพราะเป็นข้อมูลที่ไม่เปลี่ยนแปลง
const statsData = [
  {
    value: 'Google Search',
    label: 'เราใช้ Google Search ในการช่วยตัดสิน',
  },
  {
    value: 'AI : LLM',
    label: 'เราใช้ AI LLM ในการช่วยประมวลผล',
  },
  {
    value: 'Deep Learning',
    label: 'เราเทรน Deep Learning จาก Dataset',
  },
];

// สร้าง StatsSection Component แยกออกมาเป็นของตัวเอง
const StatsSection = () => {

  return (

    <Box
      sx={{
        width: '100%',
        backgroundColor: '#101125',
        color: 'white',
        py: { xs: 6, md: 8 },
        px: 2,
      }}
    >
      <Container maxWidth='lg' >
        <Grid container spacing={{ xs: 5, md: 3 }} justifyContent="center" data-aos="fade-up" data-aos-delay="200">
          {statsData.map((stat, index) => (
            <Grid size={{ xs: 12, sm: 4 }} key={index} sx={{ textAlign: 'center' }}>
              <Typography
                component="p"
                variant="h6"
                fontWeight={700}
                sx={{ fontSize: { xs: '2.5rem', md: '2rem' } }}
              >
                {stat.value}
              </Typography>
              <Typography
                variant="body1"
                sx={{ color: '#42bdffff', fontWeight: 500 }}
              >
                {stat.label}
              </Typography>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

// Component หลักของคุณ
const DetectText = React.forwardRef((props, ref) => {
  const [newsText, setNewsText] = useState('');
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const [inputType, setInputType] = useState('text');

  const handleAnalyzeClick = async () => {
    if (!newsText.trim()) {
      const alertMessage = inputType === 'text' ? 'กรุณาป้อนข้อความก่อนครับ' : 'กรุณาวางลิงก์ก่อนครับ';
      alert(alertMessage);
      return;
    }
    setIsLoading(true);

    try {
      let textToAnalyze = newsText;

      // ขั้นตอนที่ 1: ถ้าเป็นลิงก์ ให้ดึงหัวข้อข่าวจากเว็บมาก่อน
      if (inputType === 'link') {
        setStatus('กำลังตรวจจับหัวข้อเว็บไซต์...')
        const titleResponse = await axios.post('http://localhost:8000/production/news-website-title', { url: newsText });

        textToAnalyze = titleResponse.data;
        console.log(textToAnalyze)
      }

      setStatus('กำลังค้นหาข้อมูลที่เกี่ยวข้อง...')
      const searchResponse = await axios.post('http://localhost:8000/production/news-title-search', { task: textToAnalyze });

      setStatus('กำลังวิเคราะห์...')
      const finalResponse = await axios.post('http://localhost:8000/production/news-title-check', {
        task: textToAnalyze,
        search: JSON.stringify(searchResponse.data)
      });

      console.log(searchResponse.data)


      // ขั้นตอนสุดท้าย: ส่งผลลัพธ์ไปหน้า validation
      navigate('/validation', {
        state: {
          result: finalResponse.data,
          textToAnalyze: textToAnalyze, // <-- เพิ่มบรรทัดนี้เข้ามา
          searchResult: searchResponse.data
        }
      });

    } catch (error) {
      console.error("Error fetching data:", error);
      alert("เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <> {/* ✅ ใช้ Fragment ครอบเพื่อ return สองอย่างพร้อมกัน */}

      <StatsSection />


      <Box
        ref={ref}
        id="detectText"
        sx={{
          minHeight: '680px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          scrollSnapAlign: 'start',
          backgroundColor: '#101125',
          p: 4,
          gap: 2,
          pb: 5
        }}
      >
        <Typography variant="h3" color="white" fontWeight={600} gutterBottom data-aos="fade-up">
          ตรวจจับข้อความ
        </Typography>
        <Typography color="white" sx={{ mb: 1 }} data-aos="fade-up" data-aos-delay="100">
          วางข้อความข่าวที่ต้องการวิเคราะห์ลงในช่องด้านล่าง
        </Typography>

        <ToggleButtonGroup
          value={inputType}
          exclusive
          onChange={(event, newType) => {
            if (newType !== null) {
              setInputType(newType);
            }
          }}
          aria-label="Input type"
          size="small"
          sx={{
            mb: 1.5,
            width: '100%',
            maxWidth: '300px',

            // สไตล์เริ่มต้นสำหรับปุ่มทุกอัน
            '& .MuiToggleButton-root': {
              backgroundColor: '#283481', // สีพื้นหลังเริ่มต้น
              color: '#FFFFFF',
              flex: 1,
              transition: 'background 0.4s ease-in-out, color 0.4s ease-in-out',
            },

            // ✅ 1. กำหนด hover effect ให้ทำงาน "เฉพาะปุ่มที่ยังไม่ถูกเลือก"
            '& .MuiToggleButton-root:not(.Mui-selected):hover': {
              background: 'linear-gradient(90deg,rgba(166, 227, 255, 1) 0%, rgba(106, 170, 251, 1) 100%)',
              color: '#FFFFFF'
            },

            // ✅ 2. กำหนดให้ปุ่มที่ "ถูกเลือก" มีสไตล์ gradient ค้างไว้เลย
            '& .Mui-selected': {
              background: 'linear-gradient(90deg,rgba(166, 227, 255, 1) 0%, rgba(106, 170, 251, 1) 100%)',
              color: '#FFFFFF'
            },

            // สไตล์ borderRadius ยังคงเหมือนเดิม
            '& .MuiToggleButton-root:first-of-type': {
              borderRadius: '20px 0 0 0',
            },
            '& .MuiToggleButton-root:last-of-type': {
              borderRadius: '0 20px 0 0',
            },
          }}
          data-aos="fade-up"
          data-aos-delay="200"
        >
          <ToggleButton value="text">ข้อความ</ToggleButton>
          <ToggleButton value="link">ลิงก์</ToggleButton>
        </ToggleButtonGroup>

        {/* ✅ TextField เหมือนเดิมทุกอย่าง แค่เปลี่ยน placeholder */}
        <TextField
          value={newsText}
          onChange={(e) => setNewsText(e.target.value)}
          multiline
          rows={8}
          placeholder={
            inputType === 'text'
              ? "วางเนื้อหาข่าวของคุณที่นี่..."
              : "วางลิงก์ (URL) ของคุณที่นี่..."
          }
          variant="filled"
          fullWidth
          sx={{
            maxWidth: '980px',
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '4px',
            textarea: { color: 'white' }
          }}
          data-aos="fade-up"
          data-aos-delay="200"
        />

        <Button
          onClick={handleAnalyzeClick}
          disabled={isLoading}
          variant="contained"
          size="large"
          sx={{ mt: 1 }}
          data-aos="fade-up"
          data-aos-delay="300"
        >
          {isLoading ? 'กำลังวิเคราะห์...' : 'วิเคราะห์ข่าว'}
        </Button>
        <Box sx={{ pb: 5 }}></Box>
        {isLoading && (
          <Box sx={{ width: '100%', maxWidth: '700px', mt: 2, display: 'flex', justifyContent: 'center' }}>
            <CircularProgress />
            <Typography sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
              {status}
            </Typography>
          </Box>
        )}
      </Box>

    </>
  );
});

export default DetectText;