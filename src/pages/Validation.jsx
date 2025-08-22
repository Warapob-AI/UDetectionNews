import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Box, Typography, Button, Paper, Tooltip, tooltipClasses, Stack, Grid, Card, CardContent, CardMedia } from '@mui/material';
import { styled } from '@mui/material/styles';
import CircularProgressWithLabel from '../components/validation_circular.jsx';
import { TypeAnimation } from 'react-type-animation';

// CustomTooltip และ cleanConfidence (คงเดิม)
const CustomTooltip = styled(({ className, ...props }) => (
    <Tooltip {...props} classes={{ popper: className }} />
))(({ theme }) => ({
    [`& .${tooltipClasses.tooltip}`]: {
        backgroundColor: '#34495e',
        color: 'white',
        maxWidth: '1000px',
        fontSize: theme.typography.pxToRem(14),
        border: '1px solid #4a637a',
        borderRadius: '8px',
        padding: '16px',
    },
    [`& .${tooltipClasses.arrow}`]: {
        color: '#34495e',
    },
}));

function cleanConfidence(value) {
    if (typeof value === 'string') {
        return parseInt(value, 10);
    } else if (typeof value === 'number') {
        return value;
    }
    return NaN;
}


function ResultPage() {
    const location = useLocation();
    const navigate = useNavigate();
    // --- 1. สร้าง State สำหรับควบคุมคิว Animation ---
    const [typingHeaderIndex, setTypingHeaderIndex] = useState(0);
    const [typingDescIndex, setTypingDescIndex] = useState(-1); // เริ่มที่ -1 คือยังไม่มีรายละเอียดไหนเริ่มพิมพ์
    const [allTypingFinished, setAllTypingFinished] = useState(false);

    const rawStringFromApi = location.state?.result;
    const analyzedText = location.state?.textToAnalyze;

    useEffect(() => {
        if (!rawStringFromApi) {
            navigate('/');
        }
    }, [rawStringFromApi, navigate]);

    if (!rawStringFromApi) {
        return null;
    }

    let result;
    try {
        const startIndex = rawStringFromApi.indexOf('{');
        const endIndex = rawStringFromApi.lastIndexOf('}');
        const cleanJsonString = rawStringFromApi.substring(startIndex, endIndex + 1);
        result = JSON.parse(cleanJsonString);
    } catch (error) {
        console.error("Error parsing JSON string:", error);
        return <p>Error parsing data, redirecting...</p>;
    }

    // --- จุดที่แก้ไข: ดึงข้อมูลที่ครบถ้วนมาใช้โดยตรง ---
    // ไม่ต้อง fetch เพิ่มแล้ว!
    // ตรวจสอบว่าเป็น Array จริงๆ ก่อนนำไปใช้
    console.log("testtesttest"+ location.state.searchResult)
    const relatedWebsites = Array.isArray(location.state.searchResult) 
  ? location.state.searchResult 
  : [];

    const confidencePercentage = cleanConfidence(result.confidence);
    let predictionText = result.conclusion || "ไม่สามารถระบุได้";
    const uniqueTexts = [...new Set(result.analysis_points.map(p => p.header).filter(Boolean))];
    const uniqueTextsDes = [...new Set(result.analysis_points.map(p => p.description).filter(Boolean))];
    const analysisDetails = uniqueTexts.map((header, index) => ({
        header: header,
        description: uniqueTextsDes[index] || 'ไม่มีรายละเอียดเพิ่มเติม'
    }));
    let color_text = '';
    let color_stop_1 = '';
    let color_stop_2 = '';

    if (predictionText.includes('ข่าวจริง') || predictionText.toLowerCase().includes('true')) {
        color_text = '#2ecc71';
        color_stop_1 = '#00ffb3ff';
        color_stop_2 = '#00ff88ff';
        predictionText = 'ข่าวจริง'
    } else if (predictionText.includes('ข่าวปลอม') || predictionText.toLowerCase().includes('fake')) {
        color_text = '#e74c3c';
        color_stop_1 = '#ff0000ff';
        color_stop_2 = '#ff0000ff';
        predictionText = 'ข่าวปลอม'
    } else if (predictionText.includes('ไม่เพียงพอ')) {
        color_text = '#dce73cff';
        color_stop_1 = '#ffee00ff';
        color_stop_2 = '#ffee00ff';
    }

    return (
        <Box
            sx={{
                minHeight: '100vh', display: 'flex', flexDirection: 'column',
                alignItems: 'center', py: 4, px: 2, backgroundColor: '#1d2c3d',
                gap: 3,
            }}
        >
            {/* ส่วนหัวและผลลัพธ์ (คงเดิม) */}
            <Typography variant="h4" color="white" fontWeight={500} marginTop={10} gutterBottom>ผลการวิเคราะห์</Typography>
            <Paper elevation={6} sx={{ p: 3, borderRadius: '16px', backgroundColor: '#2c3e50', width: '100%', maxWidth: '800px', textAlign: 'center' }}>
                <Typography variant="h6" sx={{ color: 'white', mb: 1 }}>หัวข้อข่าวที่นำมาวิเคราะห์</Typography>
                <Typography sx={{ color: 'rgba(255,255,255,0.8)' }}>"{analyzedText}"</Typography>
            </Paper>
            <Paper
                elevation={6}
                sx={{
                    display: 'flex',
                    flexDirection: { xs: 'column', md: 'row' },
                    alignItems: 'center',
                    gap: { xs: 3, md: 5 },
                    p: 4,
                    borderRadius: '16px',
                    backgroundColor: '#2c3e50',
                    width: '100%',
                    maxWidth: '800px'
                }}
            >
                {/* === คอลัมน์ซ้าย (วงกลม) === */}
                <Box sx={{ flex: 'none', textAlign: 'center' }}>
                    <CircularProgressWithLabel value={confidencePercentage} color_stop_1={color_stop_1} color_stop_2={color_stop_2} />
                    {/* เปลี่ยนข้อความให้เหมาะสม เพราะไม่ต้องชี้แล้ว */}
                    <Typography sx={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '0.8rem', mt: 1 }}>
                        ผลการวิเคราะห์
                    </Typography>
                </Box>

                {/* === คอลัมน์ขวา (ผลลัพธ์และเหตุผล) === */}
                <Box sx={{ flex: 1, width: '100%', display: 'flex', flexDirection: 'column', gap: 2 }}>

                    {/* ส่วนแสดงผลลัพธ์ (บนสุดของคอลัมน์ขวา) */}
                    <Box sx={{ color: 'white', textAlign: { xs: 'center', md: 'left' } }}>
                        <Typography variant="h4">
                            ผลลัพธ์: <span style={{ color: color_text, fontWeight: 'bold' }}>{predictionText}</span>
                        </Typography>
                        <Typography variant="h6" sx={{ mt: 1, color: 'rgba(255,255,255,0.8)' }}>
                            ความเชื่อมั่น {confidencePercentage.toFixed(2)}%
                        </Typography>
                    </Box>

                    {/* ส่วนแสดงเหตุผล (รองลงมา) */}
                    <Box
                        sx={{
                            backgroundColor: 'rgba(0, 0, 0, 0.2)',
                            borderRadius: '8px',
                            p: 2.5,
                            color: 'white'
                        }}
                    >
                        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                            ทำไมถึงเป็น{predictionText}?
                        </Typography>
                        <Stack component="ul" spacing={1} sx={{ pl: 2, mt: 1, listStyleType: 'none', m: 0 }}>
                            {uniqueTexts.map((text, index) => (
                                <Typography component="li" key={index} sx={{ color: 'rgba(255,255,255,0.9)' }}>
                                    {`${index + 1}. ${text}`}
                                </Typography>
                            ))}
                        </Stack>
                    </Box>

                </Box>
            </Paper>




            <Paper
                elevation={6}
                sx={{
                    p: { xs: 2, md: 4 },
                    borderRadius: '16px',
                    backgroundColor: '#2c3e50',
                    width: '100%',
                    maxWidth: '800px',
                    minHeight: '250px'
                }}
            >
                <Typography variant="h5" sx={{ color: 'white', mb: 3, fontWeight: 'bold', textAlign: 'center' }}>
                    รายละเอียดเชิงลึก
                </Typography>

                <Stack spacing={3}>
                    {analysisDetails.map((item, index) => {
                        const hasFinished = index < typingHeaderIndex;
                        const isHeaderTyping = index === typingHeaderIndex;
                        const isDescTyping = index === typingDescIndex;
                        const isLastItem = index === analysisDetails.length - 1;

                        return (
                            <Box key={index}>
                                {/* --- ส่วนของหัวข้อ (ปรับปรุง Logic) --- */}
                                <Typography variant="h6" sx={{ color: 'white', minHeight: '32px' }}>
                                    {
                                        hasFinished ? `${index + 1}. ${item.header}` // 1. ถ้าพิมพ์เสร็จแล้ว: แสดงข้อความเต็ม
                                            : isHeaderTyping ? ( // 2. ถ้ากำลังพิมพ์: แสดง Animation
                                                <TypeAnimation
                                                    key={`header-${index}`}
                                                    sequence={[
                                                        `${index + 1}. ${item.header}`,
                                                        () => setTypingDescIndex(index)
                                                    ]}
                                                    speed={60}
                                                    wrapper="span"
                                                    cursor={false}
                                                />
                                            ) : null // 3. ถ้ายังไม่ถึงคิว: ไม่ต้องแสดงอะไร
                                    }
                                </Typography>

                                {/* --- ส่วนของรายละเอียด (ปรับปรุง Logic) --- */}
                                {(hasFinished || isDescTyping) && (
                                    <Typography
                                        variant="body1"
                                        sx={{
                                            color: 'rgba(255,255,255,0.8)',
                                            pl: 4,
                                            position: 'relative',
                                            minHeight: '48px',
                                            '&::before': {
                                                content: '"•"',
                                                position: 'absolute',
                                                left: '16px',
                                                color: '#2ecc71',
                                                fontWeight: 'bold'
                                            }
                                        }}
                                    >
                                        {
                                            hasFinished ? item.description // 1. ถ้าพิมพ์เสร็จแล้ว: แสดงข้อความเต็ม
                                                : isDescTyping ? ( // 2. ถ้ากำลังพิมพ์: แสดง Animation
                                                    <TypeAnimation
                                                        key={`desc-${index}`}
                                                        sequence={[
                                                            item.description,
                                                            500,
                                                            () => {
                                                                // เมื่อพิมพ์เสร็จ ถ้าเป็นรายการสุดท้าย ให้หยุด
                                                                if (!isLastItem) {
                                                                    setTypingHeaderIndex(prevIndex => prevIndex + 1);
                                                                }
                                                            }
                                                        ]}
                                                        speed={80}
                                                        wrapper="span"
                                                        cursor={false}
                                                    />
                                                ) : null // 3. ถ้ายังไม่ถึงคิว: ไม่ต้องแสดงอะไร
                                        }
                                    </Typography>
                                )}
                            </Box>
                        );
                    })}
                </Stack>
            </Paper>
            {/* === ส่วนเว็บไซต์ที่ใกล้เคียง (อัปเกรดเป็นการ์ดข่าว) === */}
            <Box sx={{ width: '100%', maxWidth: 'lg', mt: 3 }}>
                <Typography variant="h5" color="white" gutterBottom sx={{ textAlign: 'center', mb: 5 }}>
                    แหล่งข้อมูลที่ใกล้เคียง
                </Typography>
                <Grid container maxWidth='lg' spacing={3}>
                    {relatedWebsites.slice(0, 3).map((site, index) => (
                        <Grid size={{ xs: 12, sm: 6, md: 4 }} sx={{ px: '2rem' }} key={index}>
                            <Card sx={{
                                width: '100%',
                                height: '100%',
                                backgroundColor: '#fff',
                                color: '#000',
                                borderRadius: '1px',
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
                                    <Typography gutterBottom variant="h6" component="div" sx={{ fontWeight: 'bold', lineHeight: 1.3, height: 'auto', overflow: 'hidden' }}>
                                        {site.title}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary" sx={{ height: 'auto', overflow: 'hidden' }}>
                                        {site.description}
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
                                                backgroundColor: '#229954'
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




            <Button variant="contained" onClick={() => navigate('/')} sx={{ mt: 4 }}>
                กลับไปหน้าแรก
            </Button>
        </Box >
    );
}

export default ResultPage;