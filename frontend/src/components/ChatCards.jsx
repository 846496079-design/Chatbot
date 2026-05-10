import React from 'react';

// 商品推荐卡片
export function ProductCard({ product }) {
  if (!product) return null;
  const discount = product.original_price > product.price
    ? Math.round((1 - product.price / product.original_price) * 100)
    : 0;

  return (
    <div className="card product-card">
      <div className="card-image">
        <div className="card-image-placeholder">
          {product.category?.[0] || '商品'}
        </div>
        {discount > 0 && (
          <span className="card-discount-badge">-{discount}%</span>
        )}
      </div>
      <div className="card-body">
        <div className="card-title" title={product.name}>{product.name}</div>
        <div className="card-meta">
          <span className="card-brand">{product.brand}</span>
          <span className="card-rating">{product.rating}分</span>
        </div>
        <div className="card-price-row">
          <span className="card-price">¥{product.price}</span>
          {product.original_price > product.price && (
            <span className="card-original-price">¥{product.original_price}</span>
          )}
        </div>
        <div className="card-tags">
          <span className="card-tag stock">{product.stock}</span>
          {product.promotion && product.promotion !== '暂无优惠' && (
            <span className="card-tag promo">{product.promotion}</span>
          )}
        </div>
      </div>
    </div>
  );
}

// 订单卡片
export function OrderCard({ order }) {
  if (!order) return null;

  const statusColors = {
    '已签收': '#52c41a',
    '运输中': '#1890ff',
    '派送中': '#722ed1',
    '待发货': '#faad14',
    '已发货': '#13c2c2',
    '待付款': '#ff4d4f',
  };
  const statusColor = statusColors[order.status] || '#999';

  return (
    <div className="card order-card">
      <div className="card-header">
        <span className="card-order-id">{order.order_id}</span>
        <span className="card-status" style={{ color: statusColor, borderColor: statusColor }}>
          {order.status}
        </span>
      </div>
      <div className="card-body">
        <div className="card-title" title={order.product_name}>{order.product_name}</div>
        <div className="card-meta">
          <span>数量：{order.quantity}</span>
          <span>实付：¥{order.paid_amount}</span>
        </div>
        <div className="card-info">
          <div className="card-info-item">
            <span className="card-info-label">下单时间</span>
            <span className="card-info-value">{order.order_time}</span>
          </div>
          <div className="card-info-item">
            <span className="card-info-label">收货人</span>
            <span className="card-info-value">{order.recipient} {order.phone}</span>
          </div>
          <div className="card-info-item">
            <span className="card-info-label">收货地址</span>
            <span className="card-info-value">{order.address}</span>
          </div>
        </div>
        {order.payment_method && (
          <div className="card-payment">
            支付方式：{order.payment_method}
          </div>
        )}
      </div>
    </div>
  );
}

// 物流卡片
export function LogisticsCard({ logistics, orderId }) {
  if (!logistics) return null;

  return (
    <div className="card logistics-card">
      <div className="card-header">
        <span className="card-logistics-title">物流详情</span>
        <span className="card-tracking-no">{logistics.tracking_no}</span>
      </div>
      <div className="card-body">
        <div className="logistics-carrier">
          <span className="carrier-name">{logistics.carrier}</span>
          {logistics.estimated_delivery && (
            <span className="estimated-delivery">预计{logistics.estimated_delivery}送达</span>
          )}
        </div>
        <div className="logistics-current">
          <span className="current-dot"></span>
          <span className="current-text">{logistics.current}</span>
        </div>
        {logistics.trajectory && logistics.trajectory.length > 0 && (
          <div className="logistics-timeline">
            {logistics.trajectory.slice(-3).map((item, idx) => (
              <div key={idx} className={`timeline-item ${idx === 0 ? 'active' : ''}`}>
                <div className="timeline-dot"></div>
                <div className="timeline-content">
                  <div className="timeline-status">{item.status}</div>
                  <div className="timeline-detail">{item.detail}</div>
                  <div className="timeline-time">{item.time}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// 卡片容器 - 用于在消息中展示一组卡片
export function CardContainer({ cards, type }) {
  if (!cards || cards.length === 0) return null;

  return (
    <div className="card-container">
      {cards.map((card, idx) => {
        if (type === 'product') return <ProductCard key={idx} product={card} />;
        if (type === 'order') return <OrderCard key={idx} order={card} />;
        if (type === 'logistics') return <LogisticsCard key={idx} logistics={card} orderId={card.order_id} />;
        return null;
      })}
    </div>
  );
}
