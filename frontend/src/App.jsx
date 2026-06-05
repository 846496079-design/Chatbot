import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import ChatWindow from './components/ChatWindow';
import DataPanel from './components/DataPanel';
import WelcomeGuide from './components/WelcomeGuide';
import ConfirmDialog from './components/ConfirmDialog';

const API_BASE = process.env.REACT_APP_API_BASE || 'https://chatbot-0x0v.onrender.com';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [sessionStartTime, setSessionStartTime] = useState(null);
  const [sessionDuration, setSessionDuration] = useState('00:00');
  const [messages, setMessages] = useState([]);
  const [panelData, setPanelData] = useState({
    current_intent: { id: '', name: '', route: '', confidence: 0 },
    emotion_status: { label: 'neutral', history: [] },
    token_consumption: { total_prompt_tokens: 0, total_completion_tokens: 0, total_tokens: 0, round_count: 0 },
    user_profile: {},
    flow_state: { current_flow: '', current_step: '', filled_slots: {}, snapshot_stack: [] },
  });
  const [quickActions, setQuickActions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showGuide, setShowGuide] = useState(true);
  const [sceneLabel, setSceneLabel] = useState('');
  const [confirmDialog, setConfirmDialog] = useState(null);
  const [showDataPanel, setShowDataPanel] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    createSession();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (!sessionStartTime) return;
    const interval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - sessionStartTime) / 1000);
      const mins = Math.floor(elapsed / 60).toString().padStart(2, '0');
      const secs = (elapsed % 60).toString().padStart(2, '0');
      setSessionDuration(`${mins}:${secs}`);
    }, 1000);
    return () => clearInterval(interval);
  }, [sessionStartTime]);

  const createSession = async () => {
    try {
      const res = await axios.post(`${API_BASE}/api/session/create`);
      if (res.data.code === 0) {
        setSessionId(res.data.data.session_id);
        setSessionStartTime(Date.now());
        setSessionDuration('00:00');
      }
    } catch (e) {
      console.error('创建会话失败:', e);
    }
  };

  const fetchPanelData = useCallback(async (sid) => {
    if (!sid) return;
    try {
      const res = await axios.get(`${API_BASE}/api/panel/${sid}`);
      if (res.data.code === 0) {
        setPanelData(res.data.data);
      }
    } catch (e) {
      console.error('获取看板数据失败:', e);
    }
  }, []);

  // 执行下单
  const executeOrder = async (product) => {
    const orderId = `ORD-${new Date().toISOString().slice(0,10).replace(/-/g,'')}-${Math.floor(Math.random()*9000+1000)}`;
    const reply = `好的！已为您成功下单：${product.name}，金额${product.price}元，订单号${orderId}。预计3-5个工作日内发货，请注意查收物流信息哦~很高兴为您服务！`;
    setMessages(prev => [...prev, { role: 'assistant', content: reply }]);
    setQuickActions(['查看订单', '继续咨询', '其他问题']);
  };

  // 执行取消订单
  const executeCancel = async (order) => {
    const reply = `好的！已为您成功取消订单${order.order_id}，商品：${order.product_name}。退款金额${order.amount}元将在3-5个工作日内原路返回您的支付账户，请注意查收~很高兴为您服务！`;
    setMessages(prev => [...prev, { role: 'assistant', content: reply }]);
    setQuickActions(['查看退款进度', '继续咨询', '其他问题']);
  };

  const sendMessage = async (text) => {
    if (!text.trim() || !sessionId || loading) return;

    setShowGuide(false);
    const userMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    const requestBody = {
      session_id: sessionId,
      message: text,
    };

    // 并行调用：分析端点（意图+情绪+槽位+token）+ 流式响应端点
    const analyzePromise = fetch(`${API_BASE}/api/chat/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody),
    }).then(res => res.json()).catch(e => {
      console.error('分析请求失败:', e);
      return null;
    });

    const streamPromise = (async () => {
      try {
        const response = await fetch(`${API_BASE}/api/chat/quick/stream`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestBody),
        });

        if (!response.body) {
          throw new Error('响应体为空');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let buffer = '';
        let assistantMsgId = null;
        let fullContent = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          
          while (buffer.includes('\n\n')) {
            const index = buffer.indexOf('\n\n');
            const line = buffer.substring(0, index);
            buffer = buffer.substring(index + 2);

            if (line.startsWith('data: ')) {
              try {
                const jsonStr = line.substring(6);
                const data = JSON.parse(jsonStr);

                if (data.type === 'text') {
                  fullContent += data.content;
                  if (assistantMsgId === null) {
                    assistantMsgId = messages.length + 1;
                    setMessages(prev => [...prev, { role: 'assistant', content: fullContent }]);
                  } else {
                    setMessages(prev => {
                      const newMessages = [...prev];
                      newMessages[assistantMsgId] = { role: 'assistant', content: fullContent };
                      return newMessages;
                    });
                  }
                } else if (data.type === 'done') {
                  setQuickActions(data.quick_actions || []);
                  if (data.cards && data.card_type && assistantMsgId !== null) {
                    setMessages(prev => {
                      const newMessages = [...prev];
                      newMessages[assistantMsgId] = {
                        ...newMessages[assistantMsgId],
                        cards: data.cards,
                        card_type: data.card_type,
                      };
                      return newMessages;
                    });
                  }
                  // 如果有 pending_action，显示确认弹窗
                  if (data.pending_action) {
                    const action = data.pending_action;
                    if (action.type === 'order') {
                      setConfirmDialog({
                        title: '确认下单',
                        message: `您确定要购买 ${action.product.name} 吗？金额：${action.product.price} 元`,
                        confirmText: '确认下单',
                        cancelText: '再考虑一下',
                        onConfirm: async () => {
                          // 执行下单
                          await executeOrder(action.product);
                          setConfirmDialog(null);
                        },
                        onCancel: () => {
                          setConfirmDialog(null);
                          sendMessage('再考虑一下');
                        }
                      });
                    } else if (action.type === 'cancel') {
                      setConfirmDialog({
                        title: '确认取消订单',
                        message: `您确定要取消订单 ${action.order.order_id} 吗？商品：${action.order.product_name}，退款金额：${action.order.amount} 元`,
                        confirmText: '确认取消',
                        cancelText: '再考虑一下',
                        onConfirm: async () => {
                          // 执行取消订单
                          await executeCancel(action.order);
                          setConfirmDialog(null);
                        },
                        onCancel: () => {
                          setConfirmDialog(null);
                          sendMessage('再考虑一下');
                        }
                      });
                    }
                  }
                } else if (data.type === 'error') {
                  if (assistantMsgId !== null) {
                    setMessages(prev => {
                      const newMessages = [...prev];
                      newMessages[assistantMsgId] = { role: 'assistant', content: data.content };
                      return newMessages;
                    });
                  } else {
                    setMessages(prev => [...prev, { role: 'assistant', content: data.content }]);
                  }
                }
              } catch (e) {
                console.error('解析流式数据失败:', e);
              }
            }
          }
        }
      } catch (e) {
        console.error('流式请求失败:', e);
        setMessages(prev => [...prev, { role: 'assistant', content: '网络连接失败，请检查后端服务是否启动。' }]);
      }
    })();

    // 等待两个请求都完成
    const [analyzeResult] = await Promise.all([analyzePromise, streamPromise]);

    // 处理分析结果：更新意图、情绪、槽位、token
    if (analyzeResult && analyzeResult.code === 0) {
      const ad = analyzeResult.data;
      const intentName = ad.intent?.name || '';
      if (intentName === 'pre_sale') setSceneLabel('售前导购');
      else if (intentName === 'order_query') setSceneLabel('订单查询');
      else if (intentName === 'after_sale') setSceneLabel('售后处理');
      else if (intentName === 'chitchat') setSceneLabel('闲聊');
      else setSceneLabel('');

      // 更新看板数据
      setPanelData(prev => ({
        ...prev,
        current_intent: ad.intent || prev.current_intent,
        emotion_status: {
          label: ad.emotion?.label || 'neutral',
          history: [...prev.emotion_status.history, { round: prev.token_consumption.round_count + 1, label: ad.emotion?.label || 'neutral' }].slice(-5),
        },
        token_consumption: ad.token_usage || prev.token_consumption,
        user_profile: ad.structured_data?.profile_updates 
          ? { ...prev.user_profile, ...ad.structured_data.profile_updates }
          : prev.user_profile,
        flow_state: {
          ...prev.flow_state,
          filled_slots: ad.structured_data?.business_slots || prev.flow_state.filled_slots,
        },
      }));
    }

    // 刷新看板数据
    await fetchPanelData(sessionId);
    setLoading(false);
  };

  const handleQuickAction = (action) => {
    sendMessage(action);
  };

  const handleReset = async () => {
    setMessages([]);
    setPanelData({
      current_intent: { id: '', name: '', route: '', confidence: 0 },
      emotion_status: { label: 'neutral', history: [] },
      token_consumption: { total_prompt_tokens: 0, total_completion_tokens: 0, total_tokens: 0, round_count: 0 },
      user_profile: {},
      flow_state: { current_flow: '', current_step: '', filled_slots: {}, snapshot_stack: [] },
    });
    setQuickActions([]);
    setShowGuide(true);
    setSceneLabel('');
    await createSession();
  };

  return (
    <div className="app-container">
      <div className="app-header">
        <div className="header-left">
          <span className="header-back" onClick={handleReset} style={{ cursor: 'pointer' }}>&#8592; 返回首页</span>
          {sceneLabel && (
            <span className="header-scene">
              场景：<span className="scene-highlight">{sceneLabel}</span>
            </span>
          )}
        </div>
        <div className="header-center">
          <span className="header-duration">会话时长：{sessionDuration}</span>
        </div>
        <div className="header-right">
          <button className="btn-reset" onClick={handleReset}>新会话</button>
        </div>
      </div>

      <div className="app-body">
        <div className="chat-panel">
          {showGuide && messages.length === 0 ? (
            <WelcomeGuide onAction={handleQuickAction} />
          ) : (
            <ChatWindow
              messages={messages}
              loading={loading}
              quickActions={quickActions}
              onAction={handleQuickAction}
              onSend={sendMessage}
              chatEndRef={chatEndRef}
            />
          )}
        </div>

        <div className={`data-panel ${showDataPanel ? 'show' : ''}`}>
          <div className="data-panel-header" onClick={() => setShowDataPanel(false)}>
            B端数据看板<span className="internal-tag">仅内部可见</span>
          </div>
          <DataPanel data={panelData} />
        </div>
      </div>

      {/* 移动端数据面板切换按钮 */}
      <button 
        className="data-panel-toggle" 
        onClick={() => setShowDataPanel(!showDataPanel)}
      >
        <span className="data-panel-toggle-icon">{showDataPanel ? '\u2715' : '\ud83d\udcca'}</span>
        {showDataPanel ? '收起看板' : 'B端看板'}
      </button>

      {/* 确认弹窗 */}
      {confirmDialog && (
        <ConfirmDialog
          title={confirmDialog.title}
          message={confirmDialog.message}
          confirmText={confirmDialog.confirmText}
          cancelText={confirmDialog.cancelText}
          onConfirm={confirmDialog.onConfirm}
          onCancel={confirmDialog.onCancel}
        />
      )}
    </div>
  );
}

export default App;