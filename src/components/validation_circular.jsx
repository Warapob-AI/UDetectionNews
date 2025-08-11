import React from 'react';
import PropTypes from 'prop-types';
import { CircularProgress, Typography, Box } from '@mui/material';

function CircularProgressWithLabel(props) {
    const sizeCircle = 340;
    const strokeWidth = 10; // กำหนดความหนาของเส้นที่นี่
    const radius = (sizeCircle - strokeWidth) / 2;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (props.value / 100) * circumference;

    return (
        <Box
            sx={{
                position: 'relative',
                display: 'inline-flex',
                filter: 'drop-shadow(0px 8px 10px rgba(0, 0, 0, 0.4))'
            }}
        >
            {/* 1. วงกลมพื้นหลัง (Track) ทำให้เข้มและเบลอเล็กน้อย */}
            <CircularProgress
                variant="determinate"
                value={100}
                sx={{
                    color: 'rgba(0, 0, 0, 0.2)', // สีพื้นหลังเข้มๆ
                    filter: 'blur(1px)',
                }}
                size={sizeCircle}
                thickness={strokeWidth}
            />

            {/* 2. สร้าง SVG Layer สำหรับวาดเส้น Gradient */}
            <svg
                width={sizeCircle}
                height={sizeCircle}
                style={{
                    position: 'absolute',
                    left: 0,
                    transform: 'rotate(-90deg)', // หมุนให้เริ่มจากด้านบน
                }}
            >
                <defs>
                    {/* ✅ กำหนดสี Gradient ที่นี่ */}
                    <linearGradient id="progressGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor={props.color_stop_1} /> 
                        <stop offset="50%" stopColor={props.color_stop_1} />
                    </linearGradient>
                </defs>
                <circle
                    cx={sizeCircle / 2}
                    cy={sizeCircle / 2}
                    r={radius}
                    fill="none"
                    stroke="url(#progressGradient)" // ✅ ใช้ Gradient ที่สร้างไว้
                    strokeWidth={strokeWidth}
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    strokeLinecap="round" // ✅ ทำให้ปลายเส้นโค้งมน
                    style={{
                        transition: 'stroke-dashoffset 0.5s ease-out',
                    }}
                />
            </svg>

            {/* ตัวเลขเปอร์เซ็นต์ (อยู่บนสุด) */}
            <Box
                sx={{
                    top: 0, left: 0, bottom: 0, right: 0,
                    position: 'absolute',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <Typography
                    variant="h3"
                    component="div"
                    color="white"
                    fontWeight="bold"
                    sx={{
                        textShadow: '0px 2px 5px rgba(0, 0, 0, 0.5)'
                    }}
                >
                    {`${Math.round(props.value)}%`}
                </Typography>
            </Box>
        </Box>
    );
}

CircularProgressWithLabel.propTypes = {
    value: PropTypes.number.isRequired,
};

export default CircularProgressWithLabel;