import React, { useState } from 'react';

function WelcomeGuide({ onAction }) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onAction(inputValue.trim());
      setInputValue('');
    }
  };
  const scenes = [
    {
      id: 'pre_sale',
      title: '售前导购',
      desc: '想买什么？我帮您挑',
      icon: '🛍',
      actions: ['推荐一款手机', '2000以内的耳机', '有什么优惠活动'],
    },
    {
      id: 'order_query',
      title: '订单查询',
      desc: '查订单、看物流',
      icon: '📦',
      actions: ['我的订单到哪了', '帮我查订单ORD-20260502-002', '物流怎么不动了', '我要取消订单'],
    },
    {
      id: 'after_sale',
      title: '售后处理',
      desc: '退换货、投诉建议',
      icon: '🔧',
      actions: ['我要退货', '收到的商品有问题', '怎么申请退款', '我要投诉'],
    },
  ];

  return (
    <div className="welcome-guide">
      <div className="welcome-content">
        <div className="welcome-hero">
          <div className="welcome-avatar">慧</div>
          <h2>你好，我是小慧</h2>
          <p className="welcome-subtitle">您的智能购物助手，帮您找好物、查订单、解难题！</p>
        </div>

        <div className="scene-cards">
          {scenes.map((scene) => (
            <div key={scene.id} className="scene-card">
              <div className="scene-card-header">
                <span className="scene-icon">{scene.icon}</span>
                <div>
                  <h3>{scene.title}</h3>
                  <p>{scene.desc}</p>
                </div>
              </div>
              <div className="scene-actions">
                {scene.actions.map((action, idx) => (
                  <button key={idx} className="scene-action-btn" onClick={() => onAction(action)}>
                    {action}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="welcome-footer">
          <p>也可以直接在下方输入您的问题，我会智能识别并处理</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="welcome-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="请输入您的问题..."
          className="welcome-input"
        />
        <button type="submit" className="welcome-submit-btn">发送</button>
      </form>
    </div>
  );
}

export default WelcomeGuide;
