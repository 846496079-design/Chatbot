import React, { useState } from 'react';
import { CardContainer } from './ChatCards';

function ChatWindow({ messages, loading, quickActions, onAction, onSend, chatEndRef }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-avatar-wrapper">
              {msg.role === 'assistant' && (
                <div className="message-avatar assistant-avatar">
                  <span>客服</span>
                </div>
              )}
              {msg.role === 'user' && (
                <div className="message-avatar user-avatar">
                  <span>我</span>
                </div>
              )}
            </div>
            <div className="message-content-wrapper">
              <div className="message-bubble">
                <div className="message-text">{msg.content}</div>
              </div>
              {msg.cards && msg.cards.length > 0 && (
                <CardContainer cards={msg.cards} type={msg.card_type} />
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="message-avatar assistant-avatar">
              <span>客服</span>
            </div>
            <div className="message-bubble">
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {quickActions.length > 0 && (
        <div className="quick-actions-bar">
          {quickActions.map((action, idx) => (
            <button key={idx} className="quick-action-btn" onClick={() => onAction(action)}>
              {action}
            </button>
          ))}
        </div>
      )}

      <form className="chat-input-area" onSubmit={handleSubmit}>
        <input
          type="text"
          className="chat-input"
          placeholder="请输入您的问题..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" className="send-btn" disabled={loading || !input.trim()}>
          发送
        </button>
      </form>
    </div>
  );
}

export default ChatWindow;
