import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import store from './store/store';
import App from './App';

const appNode = createRoot(document.getElementById('ModernMan'));

appNode.render(
  <React.StrictMode>
    <Provider store={store}>
        <BrowserRouter>
          <App />  
        </BrowserRouter>
    </Provider>
  </React.StrictMode>
  );
