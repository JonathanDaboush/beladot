
import React, { useEffect, useState } from 'react';
import { getSpecificRefundRequest, approveOrDenyRefund } from '../../api/customerService';
import DecisionFrame from '../../components/DecisionFrame';
import PageHeader from '../../components/PageHeader';
import Button from '../../components/Button';
import Toast from '../../components/Toast';

const RefundRequestDetailPage = ({ refundRequestId }) => {
  const [detail, setDetail] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState('');
  const [refundAmount, setRefundAmount] = useState('');
  const [description, setDescription] = useState('');
  const [preview, setPreview] = useState('');
  const [toast, setToast] = useState({ open: false, kind: 'success', message: '' });

  useEffect(() => {
    getSpecificRefundRequest(refundRequestId).then(setDetail);
  }, [refundRequestId]);

  if (!detail) return <div>Loading...</div>;
  const { order, refund_request, order_items } = detail;

  const handlePreview = () => {
    setPreview(
      <div>
        <div><b>Action:</b> {modalType === 'approve' ? 'Approve Refund' : 'Deny Refund'}</div>
        {modalType === 'approve' && <div><b>Refund Amount:</b> {refundAmount}</div>}
        <div><b>Description:</b> {description}</div>
      </div>
    );
  };

  return (
    <div className="refund-request-detail-page">
      <PageHeader title="Refund Request" subtitle="Review order and decide on refund" />
      <div className="order-summary">
        <div><b>Customer:</b> {order?.customer_name}</div>
        <div><b>Order #:</b> {order?.order_number}</div>
        <div><b>Status:</b> {order?.order_status}</div>
        <div><b>Total:</b> {order?.total_amount}</div>
        <div><b>Created:</b> {order?.created_at}</div>
        <div><b>Updated:</b> {order?.updated_at}</div>
      </div>
      <div className="order-items-slideshow">
        {order_items.map((item, idx) => (
          <div className="order-item-slide" key={idx}>
            <img src={item.product_images?.[0]?.image_url} alt={item.product?.name} />
            <div>{item.product?.name}</div>
            <div>Qty: {item.order_item?.quantity}</div>
            <div>Subtotal: {item.order_item?.subtotal}</div>
          </div>
        ))}
      </div>
      <Button kind="primary" onClick={() => { setShowModal(true); setModalType('approve'); }}>Approve refund</Button>
      <Button kind="danger" onClick={() => { setShowModal(true); setModalType('deny'); }}>Deny refund</Button>
      <DecisionFrame
        visible={showModal}
        onCancel={() => { setShowModal(false); setPreview(''); }}
        onConfirm={async () => {
          await approveOrDenyRefund(refundRequestId, modalType, refundAmount, description);
          setShowModal(false);
          setPreview('');
          setToast({ open: true, kind: 'success', message: modalType === 'approve' ? 'Refund approved' : 'Refund denied' });
        }}
        preview={preview}
        banner={modalType === 'approve' ? 'Approve Refund Request' : 'Deny Refund Request'}
      >
        <h3>{modalType === 'approve' ? 'Approve Refund' : 'Deny Refund'}</h3>
        {modalType === 'approve' && (
          <input placeholder="Refund Amount" value={refundAmount} onChange={e => setRefundAmount(e.target.value)} onBlur={handlePreview} />
        )}
        <textarea placeholder="Reason/Description" value={description} onChange={e => setDescription(e.target.value)} onBlur={handlePreview} />
      </DecisionFrame>
      <Toast open={toast.open} kind={toast.kind} message={toast.message} onClose={() => setToast({ ...toast, open: false })} />
    </div>
  );
};
export default RefundRequestDetailPage;
