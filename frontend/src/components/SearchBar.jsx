import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faSearch, faHeart, faShoppingCart, faHome,
  faUser,
} from '@fortawesome/free-solid-svg-icons';
import { updateQuery, searchProducts } from '../store/searchSlice';
import { fetchSuggestions, clearSuggestions } from '../store/suggestionsSlice';
import { fetchFavoriteCountThunk } from '../store/favoriteSlice';
import { logoutUser } from '../store/userSlice';

const SearchBar = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const [isFavoriteClicked, setIsFavoriteClicked] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const suggestions = useSelector((state) => state.suggestions.suggestions) || [];
  const favoriteCount = useSelector((state) => state.favorites.count);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const isAuthenticated = useSelector((state) => state.user.isAuthenticated);

  useEffect(() => {
    if (searchTerm.trim()) {
      dispatch(fetchSuggestions(searchTerm));
      setShowDropdown(true);
    } else {
      dispatch(clearSuggestions());
      setShowDropdown(false);
    }
  }, [searchTerm, dispatch]);

  useEffect(() => {
    if (isFavoriteClicked) {
      dispatch(fetchFavoriteCountThunk());
    }
  }, [isFavoriteClicked, dispatch]);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setShowDropdown(false);
    if (searchTerm.trim() === '') {
      navigate(`/searchpage?query=${encodeURIComponent(searchTerm)}&error=empty`);
    } else {
      dispatch(updateQuery(searchTerm));
      dispatch(searchProducts(searchTerm))
        .unwrap()
        .then((result) => {
          if (result.length === 0) {
            navigate(`/searchpage?query=${encodeURIComponent(searchTerm)}&error=noresults`);
          } else {
            navigate(`/searchpage?query=${encodeURIComponent(searchTerm)}`);
          }
        })
        .catch(() => {
          navigate(`/searchpage?query=${encodeURIComponent(searchTerm)}&error=noresults`);
        });
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setSearchTerm(suggestion.name);
    setShowDropdown(false);
    navigate(`/searchpage?query=${encodeURIComponent(suggestion.name)}`);
  };

  const handleFavoriteClick = () => {
    setIsFavoriteClicked(true);
  };

  const handleLogout = () => {
    dispatch(logoutUser());
    navigate('/');
  };

  const sortedSuggestions = [...suggestions].sort((a, b) => a.name.localeCompare(b.name));

  return (
    <div className="searchbar">
      <h3>Modern Man</h3>
      <Link to="/">
        <FontAwesomeIcon icon={faHome} className="home-icon" />
        <span className="tooltip-text">Go To Home</span>
      </Link>
      <form className="search-form" onSubmit={handleSearchSubmit}>
        <FontAwesomeIcon icon={faSearch} className="search-icon" />
        <input
          type="text"
          placeholder="Search for Men's Wear and Accessories"
          className="search-input"
          value={searchTerm}
          onChange={handleSearchChange}
          onFocus={() => setShowDropdown(true)}
        />
        {showDropdown && sortedSuggestions.length > 0 && (
          <ul className="suggestions">
            {sortedSuggestions.map((item) => (
              <li key={item.id} className="suggestion-item" onClick={() => handleSuggestionClick(item)}>
                <img src={item.image} alt={item.name} className="suggestion-image" />
                <span className="suggestion-name">{item.name}</span>
              </li>
            ))}
          </ul>
        )}
      </form>
      <div className="user-icons">
        {isAuthenticated && (
        <div
          className="user-icon"
          onMouseEnter={() => setShowUserDropdown(true)}
          onMouseLeave={() => setShowUserDropdown(false)}
        >
          <FontAwesomeIcon icon={faUser} id="user" />
          {showUserDropdown && (
          <div className="user-dropdown">
            <Link to="/profile">Profile</Link>
            <button type="button" onClick={handleLogout}>Logout</button>
          </div>
          )}
        </div>
        )}
        <Link to="/checkout">
          <FontAwesomeIcon icon={faShoppingCart} id="shopping" />
          <span className="tooltip-text">Checkout</span>
        </Link>
        <FontAwesomeIcon icon={faHeart} className="heart" onClick={handleFavoriteClick} />
        <span className="favorite-count">{favoriteCount}</span>
        {favoriteCount > 0 && isFavoriteClicked && <span className="favorite-count">{favoriteCount}</span>}
        <span className="tooltip-text">Favorite</span>
      </div>
    </div>
  );
};

export default SearchBar;
