import React from 'react';
import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Forgot from 'pages/Forgot.jsx';

describe('Forgot component', () => {
  it('renders without crashing', () => {
    const { getByText } = render(
      <Router>
        <Forgot />
      </Router>
    );
    expect(getByText(/Forgot Password?/i)).toBeInTheDocument();
  });
});
