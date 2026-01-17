import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

function App() {
  // UPDATE POINT - backend url
  const backendEndpoint = 'https://congenial-parakeet-qg7jw5gv5xq2xjv6-8000.app.github.dev/chat';
  const [input, setInput] = useState('');
  const [chatLog, setChatLog] = useState([]);

  const sendMessage = async () => {
    const userMessage = { role: 'user', content: input };
    setChatLog((prev) => [...prev, userMessage, { role: 'agent', content: '' }]);
    setInput('');

    try {
      const response = await fetch(backendEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, session_id: 'codespace_user' }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        
        setChatLog((prev) => {
          const newLog = [...prev];
          newLog[newLog.length - 1].content += chunk;
          return newLog;
        });
      }
    } catch (err) {
      console.error("Streaming error:", err);
    }
  };

  return (
    <div style={{ padding: '40px', background: '#1a1a1a', color: 'white', minHeight: '100vh' }}>
      <h2>Agno Agent OS Chat</h2>

      {/* <div style={{ height: '400px', overflowY: 'auto', border: '1px solid #444', padding: '10px', marginBottom: '20px' }}>
        {chatLog.map((msg, i) => (
          <div key={i} style={{ marginBottom: '10px', color: msg.role === 'user' ? '#4af' : '#4f4' }}>
            <strong>{msg.role === 'user' ? 'You: ' : 'Agent: '}</strong>{msg.content}
          </div>
        ))}
      </div> */}

      <div style={{ height: '400px', overflowY: 'auto', border: '1px solid #444', padding: '10px', marginBottom: '20px' }}>
        {chatLog.map((msg, i) => (
          <div key={i} style={{ marginBottom: '10px', color: msg.role === 'user' ? '#4af' : '#4f4' }}>
            <strong>{msg.role === 'user' ? 'You: ' : 'Agent: '}</strong>
            <div style={{ display: 'inline-block', verticalAlign: 'top', marginLeft: '5px', width: '90%' }}>
              {msg.role === 'agent' ? (
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              ) : (
                <span>{msg.content}</span>
              )}
            </div>
          </div>
        ))}
      </div>

      <input 
        value={input} 
        onChange={(e) => setInput(e.target.value)} 
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            sendMessage();
          }
        }}
        style={{ width: '80%', padding: '10px' }} 
        placeholder="Type a message..."
      />
      <button onClick={sendMessage} style={{ padding: '10px 20px', marginLeft: '10px' }}>Send</button>
    </div>
  );
}

export default App;