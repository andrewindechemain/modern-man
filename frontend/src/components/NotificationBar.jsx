import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDiscountedProducts } from '../store/discountsSlice';

const NotificationBar = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { items: discountedProducts, loading, error } = useSelector((state) => state.discount);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    dispatch(fetchDiscountedProducts());
  }, [dispatch]);

  // eslint-disable-next-line consistent-return
  useEffect(() => {
    if (discountedProducts.length > 0) {
      const interval = setInterval(() => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % discountedProducts.length);
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [discountedProducts]);

  const handleLearnMoreClick = () => {
    navigate('/searchpage?discounted=true');
  };

  return (
    <div className="notificationbar">
      {loading && (
      <p>Loading...</p>
      )}
      {error && !loading && (
      <p>
        Error:
        {' '}
        {error}
      </p>
      )}
      {discountedProducts.length > 0 && !loading && !error && (
      <>
        <img src={discountedProducts[currentIndex].image} alt="My Shoes" className="shoes" />
        <p id="notificationbartext">
          Get
          {' '}
          {discountedProducts[currentIndex].discount_percentage}
          % off on
          {' '}
          {discountedProducts[currentIndex].name}
        </p>
        <button type="button" id="notificationbutton" onClick={handleLearnMoreClick}>Learn More</button>
      </>
      )}
      {!loading && !error && discountedProducts.length === 0 && (
      <p>No discount available</p>
      )}
    </div>

  );
};

export default NotificationBar;
