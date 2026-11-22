/**
 * Coffee Shop - Modern Interactive Frontend
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Nav Toggle
  const mobileToggle = document.getElementById('mobileNavToggle');
  const navLinks = document.getElementById('navLinks');
  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('show');
    });
  }

  // Toast / Alert Close & Auto-dismiss
  const alertCloses = document.querySelectorAll('.alert-close');
  alertCloses.forEach(btn => {
    btn.addEventListener('click', () => {
      const alert = btn.closest('.alert');
      if (alert) {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 250);
      }
    });
  });

  // Auto dismiss non-error alerts after 6 seconds
  setTimeout(() => {
    document.querySelectorAll('.alert:not(.alert-danger):not(.alert-error)').forEach(alert => {
      alert.style.transition = 'all 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      setTimeout(() => alert.remove(), 400);
    });
  }, 6000);

  // Dynamic Price Calculator for Order / Customizer Page
  const basePriceElem = document.getElementById('dynamicBasePrice');
  const totalPriceElem = document.getElementById('dynamicTotalPrice');
  const sizeSelect = document.getElementById('orderSizeSelect');
  const milkSelect = document.getElementById('orderMilkSelect');
  const qtyInput = document.getElementById('orderQtyInput');
  const qtyMinus = document.getElementById('qtyMinus');
  const qtyPlus = document.getElementById('qtyPlus');

  if (basePriceElem && totalPriceElem) {
    const rawBase = parseFloat(basePriceElem.dataset.basePrice || '4.50');

    function calculateTotal() {
      let currentPrice = rawBase;

      if (sizeSelect) {
        const val = sizeSelect.value;
        if (val === 'large') currentPrice += 0.80;
        else if (val === 'small') currentPrice = Math.max(2.0, currentPrice - 0.50);
      }

      if (milkSelect) {
        const milkVal = milkSelect.value;
        if (milkVal === 'oat' || milkVal === 'almond') currentPrice += 0.60;
        else if (milkVal === 'soy') currentPrice += 0.50;
      }

      const qty = parseInt(qtyInput ? qtyInput.value : '1', 10) || 1;
      const finalTotal = (currentPrice * qty).toFixed(2);
      totalPriceElem.textContent = `$${finalTotal}`;
    }

    if (sizeSelect) sizeSelect.addEventListener('change', calculateTotal);
    if (milkSelect) milkSelect.addEventListener('change', calculateTotal);
    if (qtyInput) qtyInput.addEventListener('input', calculateTotal);

    if (qtyMinus && qtyInput) {
      qtyMinus.addEventListener('click', () => {
        let val = parseInt(qtyInput.value, 10) || 1;
        if (val > 1) {
          qtyInput.value = val - 1;
          calculateTotal();
        }
      });
    }

    if (qtyPlus && qtyInput) {
      qtyPlus.addEventListener('click', () => {
        let val = parseInt(qtyInput.value, 10) || 1;
        if (val < 20) {
          qtyInput.value = val + 1;
          calculateTotal();
        }
      });
    }

    calculateTotal();
  }

  // Live Simulated Progress Tracker on Order Success Page
  const liveOrderTracker = document.getElementById('liveOrderTracker');
  if (liveOrderTracker) {
    const stepNodes = liveOrderTracker.querySelectorAll('.step-node');
    const orderStatusBadge = document.getElementById('orderStatusBadge');
    
    // Animate through brewing steps if received or brewing
    setTimeout(() => {
      if (stepNodes.length >= 2) {
        stepNodes[0].classList.add('completed');
        stepNodes[1].classList.add('active');
        if (orderStatusBadge) {
          orderStatusBadge.textContent = 'Brewing & Crafting ☕';
          orderStatusBadge.style.background = '#d97706';
        }
      }
    }, 4000);
  }
});
