// src/App.js
import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const fileInputRef = useRef();

  const sendMessage = async () => {
    if (!message.trim()) return;

    const newLog = [...chatLog, { sender: 'You', text: message }];
    setChatLog(newLog);

    const formData = new FormData();
    formData.append('message', message);
    for (let f of fileInputRef.current.files) {
      formData.append('attachments', f);
    }

    try {
      const res = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setChatLog([...newLog, { sender: 'Q', text: data.reply }]);
    } catch (err) {
      console.error(err);
      setChatLog([...newLog, { sender: 'Q', text: 'Error: Could not reach backend.' }]);
    }

    setMessage('');
    fileInputRef.current.value = null;
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Amazon Q Chatbot</h2>
      <div style={{
        border: '1px solid #ccc',
        padding: 10,
        height: 300,
        overflowY: 'scroll'
      }}>
        {chatLog.map((m, i) => (
          <div key={i}><strong>{m.sender}:</strong> {m.text}</div>
        ))}
      </div>
      <textarea
        rows={2}
        value={message}
        onChange={e => setMessage(e.target.value)}
        style={{ width: '80%', marginTop: 10 }}
      />
      <div style={{ marginTop: 10 }}>
        <input type="file" multiple ref={fileInputRef} />
      </div>
      <button onClick={sendMessage} style={{ marginTop: 10 }}>Send</button>
    </div>
  );
}

export default App;