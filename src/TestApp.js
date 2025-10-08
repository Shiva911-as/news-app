import React, { useState, useEffect } from 'react';

function TestApp() {
  const [backendStatus, setBackendStatus] = useState('Testing...');

  useEffect(() => {
    // Test backend connection
    fetch('http://localhost:5000/')
      .then(response => response.json())
      .then(data => {
        setBackendStatus('✅ Backend Connected: ' + data.message);
      })
      .catch(error => {
        setBackendStatus('❌ Backend Error: ' + error.message);
      });
  }, []);

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: '#0f0f0f', 
      color: '#ffffff', 
      padding: '20px',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1 style={{ color: '#3b82f6' }}>🚀 NewsHub System Test</h1>
      <p>If you can see this, React is working perfectly!</p>
      
      <div style={{ 
        background: '#1a1a1a', 
        padding: '20px', 
        borderRadius: '8px',
        marginTop: '20px',
        border: '1px solid #333'
      }}>
        <h2 style={{ color: '#10b981' }}>System Status</h2>
        <ul style={{ lineHeight: '1.8' }}>
          <li>✅ React App Loading</li>
          <li>✅ CSS Styles Working</li>
          <li>✅ Components Rendering</li>
          <li>{backendStatus}</li>
        </ul>
      </div>

      <div style={{ 
        background: '#1a1a1a', 
        padding: '20px', 
        borderRadius: '8px',
        marginTop: '20px',
        border: '1px solid #333'
      }}>
        <h3 style={{ color: '#f59e0b' }}>Next Steps</h3>
        <p>If you can see this test page, the React app is working correctly.</p>
        <p>The white screen issue was likely due to component errors in the main App.</p>
        <button 
          onClick={() => window.location.reload()} 
          style={{
            background: '#3b82f6',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            marginTop: '10px'
          }}
        >
          Reload Page
        </button>
      </div>
    </div>
  );
}

export default TestApp;
