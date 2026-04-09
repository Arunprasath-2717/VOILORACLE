import { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, Bot, User, Loader2, AlertTriangle, ExternalLink } from 'lucide-react';
import * as api from '../../services/api';

const ChatPanel = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '🛰️ **Kronaxis Intelligence Analyst Online.**\n\nAsk me about any global event, geopolitical situation, or sector trend. I have real-time access to the intelligence database.\n\n**Try asking:**\n- "What is happening in India right now?"\n- "Summarize the latest cybersecurity threats"\n- "What sectors are trending bullish?"',
      timestamp: new Date().toISOString(),
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = { role: 'user', content: input.trim(), timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const result = await api.sendChatMessage(userMsg.content);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: result.response,
        sources: result.sources || [],
        matchCount: result.matching_articles || 0,
        timestamp: result.timestamp,
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `⚠️ Intelligence query failed: ${err.message}. The backend may be processing. Try again.`,
        timestamp: new Date().toISOString(),
      }]);
    } finally {
      setLoading(false);
    }
  };

  const formatContent = (text) => {
    return text.split('\n').map((line, i) => {
      // Bold handling
      line = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      // Bullet points
      if (line.trim().startsWith('- ')) {
        return <li key={i} style={{ marginLeft: '1rem', fontSize: '0.82rem', lineHeight: 1.7 }} dangerouslySetInnerHTML={{ __html: line.substring(2) }} />;
      }
      if (line.trim() === '') return <br key={i} />;
      return <p key={i} style={{ margin: '0.25rem 0', fontSize: '0.82rem', lineHeight: 1.7 }} dangerouslySetInnerHTML={{ __html: line }} />;
    });
  };

  return (
    <div className="vo-chat-container">
      <div className="vo-chat-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <MessageCircle size={18} />
          <h3 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 700 }}>Intelligence Analyst Chat</h3>
        </div>
        <span style={{ fontSize: '0.7rem', color: 'var(--color-text-dim)' }}>
          Powered by Gemini AI + Live Database
        </span>
      </div>

      <div className="vo-chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`vo-chat-msg vo-chat-msg--${msg.role}`}>
            <div className="vo-chat-msg-avatar">
              {msg.role === 'assistant' ? <Bot size={16} /> : <User size={16} />}
            </div>
            <div className="vo-chat-msg-body">
              <div className="vo-chat-msg-content">
                {formatContent(msg.content)}
              </div>
              {msg.sources && msg.sources.length > 0 && (
                <div className="vo-chat-sources">
                  <span style={{ fontSize: '0.65rem', fontWeight: 600, color: 'var(--color-text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Sources ({msg.matchCount} matched)
                  </span>
                  {msg.sources.map((s, j) => (
                    <div key={j} className="vo-chat-source-item">
                      <span className={`vo-chat-source-sentiment ${s.sentiment?.toLowerCase()}`}>{s.sentiment}</span>
                      <span className="vo-chat-source-title">{s.title?.substring(0, 80)}</span>
                      {s.url && (
                        <a href={s.url} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--color-primary)', flexShrink: 0 }}>
                          <ExternalLink size={12} />
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
              <span className="vo-chat-msg-time">
                {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        {loading && (
          <div className="vo-chat-msg vo-chat-msg--assistant">
            <div className="vo-chat-msg-avatar"><Bot size={16} /></div>
            <div className="vo-chat-msg-body">
              <div className="vo-chat-typing">
                <Loader2 size={14} className="vo-spinner" />
                <span>Scanning intelligence database...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="vo-chat-input-bar" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about global events..."
          className="vo-chat-input"
          disabled={loading}
        />
        <button type="submit" className="vo-chat-send-btn" disabled={loading || !input.trim()}>
          <Send size={16} />
        </button>
      </form>
    </div>
  );
};

export default ChatPanel;
