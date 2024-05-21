import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDiscountedProducts } from '../store/discountsSlice';
import { css, keyframes } from '@emotion/react';
import shoes from '../images/shoes.webp';

const NotificationBar = () => {
    const navigate = useNavigate();

    const handleLearnMoreClick = () => {
        navigate('/searchpage?discounted=true');
    };

    return (
        <div className="notificationbar">
            <img src={shoes} alt="My Shoes" className='shoes' />
            <p>Get 50% off Selected Shoes</p>
            <button id="notificationbutton" onClick={handleLearnMoreClick}>Learn More</button>
        </div>
    );
}

export default NotificationBar;