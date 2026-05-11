import React from 'react';

const REALTIME_SLOTS = new Set([
  'gender', 'age_range', 'region', 'income_level',
  'price_sensitivity', 'preferred_categories', 'shopping_motivation',
  'consumption_level', 'brand_affinity', 'decision_cycle',
  'satisfaction_score', 'complaint_tendency',
  'hobbies', 'lifestyle_tags', 'pet_ownership',
  'new_vs_returning', 'device_type', 'promotion_sensitivity',
  'browse_preference', 'customer_lifecycle',
]);

const EMOTION_LABELS = {
  neutral: '中性',
  dissatisfied: '不满',
  angry: '愤怒',
};

const INTENT_SCENES = {
  'pre_sale': '售前导购',
  'order_query': '订单查询',
  'after_sale': '售后处理',
  'chitchat': '闲聊',
  'general': '通用咨询',
  'coupon': '优惠券',
  'product_info': '商品咨询',
  'unknown': '未知意图',
};

const PROFILE_FIELDS = [
  { key: 'gender', label: '性别', category: '基础画像' },
  { key: 'age_range', label: '年龄段', category: '基础画像' },
  { key: 'region', label: '地域', category: '基础画像' },
  { key: 'income_level', label: '收入水平', category: '基础画像' },
  { key: 'occupation', label: '职业', category: '基础画像' },
  { key: 'marital_status', label: '婚姻状况', category: '基础画像' },
  { key: 'has_children', label: '是否有孩子', category: '基础画像' },
  { key: 'living_city_tier', label: '城市等级', category: '基础画像' },
  { key: 'price_sensitivity', label: '价格敏感度', category: '消费特征' },
  { key: 'preferred_categories', label: '偏好品类', category: '消费特征' },
  { key: 'shopping_motivation', label: '购物动机', category: '消费特征' },
  { key: 'consumption_level', label: '消费等级', category: '消费特征' },
  { key: 'brand_affinity', label: '偏好品牌', category: '消费特征' },
  { key: 'decision_cycle', label: '决策周期', category: '消费特征' },
  { key: 'avg_order_value', label: '平均客单价', category: '消费特征' },
  { key: 'purchase_frequency', label: '购买频次', category: '消费特征' },
  { key: 'repurchase_intent', label: '复购意愿', category: '消费特征' },
  { key: 'preferred_payment_method', label: '支付方式', category: '消费特征' },
  { key: 'coupon_usage_rate', label: '优惠券使用率', category: '消费特征' },
  { key: 'promotion_sensitivity', label: '促销敏感度', category: '消费特征' },
  { key: 'satisfaction_score', label: '满意度', category: '服务交互' },
  { key: 'complaint_tendency', label: '投诉倾向', category: '服务交互' },
  { key: 'membership_level', label: '会员等级', category: '服务交互' },
  { key: 'channel_preference', label: '渠道偏好', category: '服务交互' },
  { key: 'device_type', label: '设备类型', category: '服务交互' },
  { key: 'active_time', label: '活跃时段', category: '服务交互' },
  { key: 'preferred_contact_method', label: '联系方式偏好', category: '服务交互' },
  { key: 'response_patience', label: '响应耐心度', category: '服务交互' },
  { key: 'hobbies', label: '兴趣爱好', category: '兴趣生活' },
  { key: 'lifestyle_tags', label: '生活标签', category: '兴趣生活' },
  { key: 'brand_consciousness', label: '品牌意识', category: '兴趣生活' },
  { key: 'tech_savviness', label: '数码能力', category: '兴趣生活' },
  { key: 'pet_ownership', label: '养宠情况', category: '兴趣生活' },
  { key: 'new_vs_returning', label: '新老客', category: '兴趣生活' },
  { key: 'browse_preference', label: '浏览偏好', category: '行为特征' },
  { key: 'search_behavior', label: '搜索习惯', category: '行为特征' },
  { key: 'review_behavior', label: '评价行为', category: '行为特征' },
  { key: 'customer_lifecycle', label: '客户生命周期', category: '行为特征' },
  { key: 'return_rate', label: '退换货率', category: '行为特征' },
  { key: 'service_escalation_count', label: '投诉升级次数', category: '行为特征' },
];

const CATEGORIES = ['基础画像', '消费特征', '服务交互', '兴趣生活', '行为特征'];

function DataPanel({ data }) {
  const { current_intent, emotion_status, token_consumption, user_profile, profile_confidence, flow_state } = data;

  const formatValue = (key, value) => {
    if (value === null || value === undefined || value === '') return '-';
    if (Array.isArray(value)) return value.length > 0 ? value.join('、') : '-';
    if (key === 'avg_order_value' && value === 0) return '-';
    if (key === 'satisfaction_score' && value === 0) return '-';
    if (key === 'service_escalation_count' && value === 0) return '-';
    return String(value);
  };

  const getTagClass = (value) => {
    if (value === '高' || value === '是' || value === '积极') return 'tag-high';
    if (value === '中') return 'tag-mid';
    if (value === '低' || value === '否') return 'tag-low';
    return '';
  };

  const formatConfidence = (conf) => {
    if (conf === null || conf === undefined) return null;
    return Math.round(conf * 100);
  };

  const getConfidenceClass = (conf) => {
    if (conf === null || conf === undefined) return '';
    if (conf >= 0.8) return 'conf-high';
    if (conf >= 0.5) return 'conf-mid';
    return 'conf-low';
  };

  const profile = user_profile || {};
  const profConf = profile_confidence || {};
  const intentName = current_intent?.name || '等待中';
  const intentScene = INTENT_SCENES[intentName] || '未分类';
  const businessSlots = flow_state?.filled_slots || {};
  const businessConf = flow_state?.business_confidence || {};

  return (
    <div className="data-panel-content">
      {/* 意图识别 + 情绪状态 并排显示 */}
      <div className="intent-emotion-row">
        <div className="intent-section">
          <div className="section-header">
            <span className="section-icon">&#9679;</span>
            <span>意图识别</span>
          </div>
          <div className="intent-info">
            <div className="intent-main-row">
              <span className="intent-name">{intentScene}</span>
            </div>
            {flow_state?.current_step && (
              <div className="intent-step">{flow_state.current_step}</div>
            )}
            <div className="confidence-bar">
              <div className="confidence-fill" style={{ width: `${(current_intent?.confidence || 0) * 100}%` }}></div>
            </div>
            <div className="confidence-text">置信度 {(current_intent?.confidence ? (current_intent.confidence * 100).toFixed(0) : 0)}%</div>
          </div>
        </div>

        <div className="emotion-section">
          <div className="section-header">
            <span className="section-icon">&#9679;</span>
            <span>情绪状态</span>
          </div>
          <div className="emotion-info">
            <span className={`emotion-label ${emotion_status?.label || 'neutral'}`}>
              {EMOTION_LABELS[emotion_status?.label] || '中性'}
            </span>
            {emotion_status?.confidence > 0 && (
              <span className={`confidence-badge ${getConfidenceClass(emotion_status.confidence)}`}>
                {formatConfidence(emotion_status.confidence)}%
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Token消耗 */}
      <div className="token-section">
        <div className="token-item">
          <span className="token-label">输入</span>
          <span className="token-value">{token_consumption?.total_prompt_tokens || 0}</span>
        </div>
        <div className="token-item">
          <span className="token-label">输出</span>
          <span className="token-value">{token_consumption?.total_completion_tokens || 0}</span>
        </div>
        <div className="token-item total">
          <span className="token-label">总计</span>
          <span className="token-value">{token_consumption?.total_tokens || 0}</span>
        </div>
      </div>

      {/* 用户画像 - 紧凑表格布局 */}
      <div className="profile-section">
        <div className="profile-header">
          <span className="section-icon">&#9679;</span>
          <span>用户画像</span>
          <span className="profile-count">40槽位</span>
        </div>

        {/* 用户卡片 */}
        <div className="user-info-row">
          <div className="user-avatar">U</div>
          <div className="user-details">
            <span className="user-id">用户123</span>
            <span className="user-phone">138****8888</span>
          </div>
          <div className={`member-badge ${getTagClass(profile.membership_level)}`}>
            {profile.membership_level || '普通会员'}
          </div>
        </div>

        {/* 分类展示 */}
        {CATEGORIES.map(cat => {
          const fields = PROFILE_FIELDS.filter(f => f.category === cat);
          return (
            <div key={cat} className="profile-category">
              <div className="category-title">{cat}</div>
              <div className="category-grid">
                {fields.map(field => {
                  const isRealtime = REALTIME_SLOTS.has(field.key);
                  const value = formatValue(field.key, profile[field.key]);
                  const tagClass = getTagClass(value);
                  const conf = profConf[field.key];
                  const confPct = formatConfidence(conf);
                  return (
                    <div key={field.key} className={`profile-item ${isRealtime ? 'realtime' : ''}`}>
                      <span className="item-label">{field.label}</span>
                      <span className="item-value-wrap">
                        <span className={`item-value ${tagClass}`}>{value}</span>
                        {confPct !== null && (
                          <span className={`confidence-badge ${getConfidenceClass(conf)}`}>
                            {confPct}%
                          </span>
                        )}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* 业务槽位 */}
      {Object.keys(businessSlots).length > 0 && (
        <div className="profile-section">
          <div className="profile-header">
            <span className="section-icon">&#9679;</span>
            <span>业务槽位</span>
            <span className="profile-count">{Object.keys(businessSlots).length}槽位</span>
          </div>
          <div className="category-grid">
            {Object.entries(businessSlots).map(([key, value]) => {
              const conf = businessConf[key];
              const confPct = formatConfidence(conf);
              const displayValue = Array.isArray(value) ? value.join('、') : String(value);
              return (
                <div key={key} className="profile-item realtime">
                  <span className="item-label">{key}</span>
                  <span className="item-value-wrap">
                    <span className="item-value">{displayValue}</span>
                    {confPct !== null && (
                      <span className={`confidence-badge ${getConfidenceClass(conf)}`}>
                        {confPct}%
                      </span>
                    )}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

export default DataPanel;