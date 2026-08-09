(() => {
  'use strict';

  document.documentElement.classList.add('js');

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const header = document.getElementById('header');
  const nav = document.querySelector('.nav');
  const navList = document.getElementById('navList');
  const navToggle = document.getElementById('navToggle');
  const dropdownParents = [...document.querySelectorAll('.has-dropdown')];
  const backToTop = document.getElementById('backToTop');
  const contactModal = document.getElementById('contactModal');
  let modalTrigger = null;

  const setDropdownState = (parent, open) => {
    if (!parent) return;
    parent.classList.toggle('dropdown-open', open);
    parent.querySelector('.dropdown-toggle')?.setAttribute('aria-expanded', String(open));
  };

  const closeDropdowns = (except = null) => {
    dropdownParents.forEach((parent) => {
      if (parent !== except) setDropdownState(parent, false);
    });
  };

  const setNavState = (open) => {
    if (!nav || !navToggle) return;
    nav.classList.toggle('active', open);
    navToggle.classList.toggle('active', open);
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Đóng menu' : 'Mở menu');
    document.body.classList.toggle('nav-open', open);
    if (!open) closeDropdowns();
  };

  navToggle?.addEventListener('click', () => {
    setNavState(!nav?.classList.contains('active'));
  });

  nav?.addEventListener('click', (event) => {
    if (event.target === nav) setNavState(false);
  });

  navList?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 1024) setNavState(false);
    });
  });

  dropdownParents.forEach((parent) => {
    parent.querySelector('.dropdown-toggle')?.addEventListener('click', () => {
      const open = !parent.classList.contains('dropdown-open');
      closeDropdowns(parent);
      setDropdownState(parent, open);
    });
  });

  const updateScrollState = () => {
    const scrolled = window.scrollY > 16;
    header?.classList.toggle('is-scrolled', scrolled);
    backToTop?.classList.toggle('visible', window.scrollY > 600);
  };

  window.addEventListener('scroll', updateScrollState, { passive: true });
  updateScrollState();

  backToTop?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
  });

  const openContactModal = (trigger = null) => {
    if (!contactModal) return;
    modalTrigger = trigger;
    contactModal.inert = false;
    contactModal.classList.add('active');
    contactModal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
    window.setTimeout(() => contactModal.querySelector('input:not([type="hidden"]), select, textarea')?.focus(), 80);
  };

  const closeContactModal = () => {
    if (!contactModal) return;
    contactModal.classList.remove('active');
    contactModal.setAttribute('aria-hidden', 'true');
    contactModal.inert = true;
    document.body.classList.remove('modal-open');
    modalTrigger?.focus?.();
    modalTrigger = null;
  };

  window.openContactModal = openContactModal;
  window.closeContactModal = closeContactModal;

  document.addEventListener('click', (event) => {
    const videoTrigger = event.target.closest('.video-embed');
    if (videoTrigger) {
      event.preventDefault();
      if (videoTrigger.dataset.loaded === 'true') return;

      const youtubeId = videoTrigger.dataset.youtubeId;
      if (!youtubeId) return;

      const iframe = document.createElement('iframe');
      iframe.className = 'video-embed__frame';
      iframe.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(youtubeId)}?autoplay=1&rel=0&hl=vi`;
      iframe.title = videoTrigger.dataset.youtubeTitle || 'Video demo TADIC';
      iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture');
      iframe.setAttribute('allowfullscreen', '');
      videoTrigger.dataset.loaded = 'true';
      videoTrigger.replaceWith(iframe);
      return;
    }

    const trigger = event.target.closest('[data-contact-modal]');
    if (trigger && contactModal) {
      event.preventDefault();
      setNavState(false);
      openContactModal(trigger);
      return;
    }
    if (event.target.closest('[data-modal-close]')) closeContactModal();
    if (!event.target.closest('.has-dropdown')) closeDropdowns();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Tab' && contactModal?.classList.contains('active')) {
      const focusable = [...contactModal.querySelectorAll('button, input, select, textarea, a[href], [tabindex]:not([tabindex="-1"])')]
        .filter((element) => !element.disabled && element.offsetParent !== null);
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      const activeElement = document.activeElement;

      if (first && last && (!contactModal.contains(activeElement)
        || (event.shiftKey && activeElement === first)
        || (!event.shiftKey && activeElement === last))) {
        event.preventDefault();
        (event.shiftKey ? last : first).focus();
      }
    }

    if (event.key === 'Escape') {
      if (contactModal?.classList.contains('active')) closeContactModal();
      if (nav?.classList.contains('active')) setNavState(false);
      closeDropdowns();
    }
  });

  const showFormMessage = (form, message, type) => {
    const alert = form.querySelector('.form-alert');
    if (!alert) return;
    alert.textContent = `${type === 'success' ? '✓' : '!'} ${message}`;
    alert.className = `form-alert alert alert--${type} is-visible`;
    alert.scrollIntoView({ block: 'nearest', behavior: reducedMotion ? 'auto' : 'smooth' });
  };

  const submitContactForm = async (form) => {
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const submitButton = form.querySelector('[type="submit"]');
    const originalButton = submitButton?.innerHTML || '';
    const formData = new FormData(form);
    const csrfToken = formData.get('csrfmiddlewaretoken') || '';
    const payload = {
      name: String(formData.get('name') || '').trim(),
      email: String(formData.get('email') || '').trim(),
      phone: String(formData.get('phone') || '').trim(),
      organization: String(formData.get('organization') || '').trim(),
      product_interest: String(formData.get('product_interest') || 'all'),
      message: String(formData.get('message') || '').trim(),
    };

    if (submitButton) {
      submitButton.disabled = true;
      submitButton.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i><span>Đang gửi...</span>';
    }

    try {
      const response = await fetch(form.dataset.endpoint || '/contact/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Có lỗi xảy ra. Vui lòng thử lại.');
      }

      showFormMessage(form, data.message || 'Cảm ơn! Chúng tôi sẽ liên hệ sớm.', 'success');
      form.reset();
    } catch (error) {
      showFormMessage(form, error.message || 'Không thể kết nối. Vui lòng kiểm tra mạng.', 'error');
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.innerHTML = originalButton;
      }
    }
  };

  document.querySelectorAll('[data-contact-form]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      submitContactForm(form);
    });
  });

  const revealItems = document.querySelectorAll('.reveal');
  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('active'));
  } else {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('active');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -45px' });
    revealItems.forEach((item) => revealObserver.observe(item));
  }

  const animateCounter = (element) => {
    if (element.dataset.animated === 'true') return;
    element.dataset.animated = 'true';
    const target = Number.parseInt(element.dataset.target || '0', 10);
    const suffix = element.dataset.suffix || '';

    if (reducedMotion || !Number.isFinite(target)) {
      element.textContent = `${target}${suffix}`;
      return;
    }

    const duration = 1600;
    const start = performance.now();
    const update = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      element.textContent = `${Math.round(target * eased)}${suffix}`;
      if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
  };

  const counters = document.querySelectorAll('[data-target]');
  if ('IntersectionObserver' in window && !reducedMotion) {
    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.45 });
    counters.forEach((counter) => counterObserver.observe(counter));
  } else {
    counters.forEach(animateCounter);
  }

  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const productCategories = [...document.querySelectorAll('.products-category[data-category]')];
  const filterEmpty = document.querySelector('.filter-empty');

  const applyProductFilter = (filter, updateUrl = false) => {
    if (!filterButtons.length || !productCategories.length) return;
    const available = new Set(productCategories.map((category) => category.dataset.category));
    const activeFilter = filter === 'all' || available.has(filter) ? filter : 'all';
    let visibleCount = 0;

    productCategories.forEach((category) => {
      const visible = activeFilter === 'all' || category.dataset.category === activeFilter;
      category.hidden = !visible;
      if (visible) visibleCount += 1;
    });

    filterButtons.forEach((button) => {
      const active = button.dataset.filter === activeFilter;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });

    if (filterEmpty) filterEmpty.hidden = visibleCount > 0;

    if (updateUrl) {
      const url = new URL(window.location.href);
      if (activeFilter === 'all') url.searchParams.delete('category');
      else url.searchParams.set('category', activeFilter);
      history.replaceState({}, '', `${url.pathname}${url.search}#danh-sach`);
    }
  };

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => applyProductFilter(button.dataset.filter || 'all', true));
  });

  if (filterButtons.length) {
    const requestedFilter = new URLSearchParams(window.location.search).get('category') || 'all';
    applyProductFilter(requestedFilter);
  }

  document.querySelectorAll('[data-tags]').forEach((tagList) => {
    const tags = (tagList.dataset.tags || '').split(',').map((tag) => tag.trim()).filter(Boolean);
    if (tags.length < 2) return;
    const tagElements = tags.map((tag) => {
      const element = document.createElement('span');
      element.textContent = tag;
      return element;
    });
    tagList.replaceChildren(...tagElements);
  });

  document.querySelectorAll('[data-share]').forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const pageUrl = encodeURIComponent(window.location.href);
      const title = encodeURIComponent(document.title);
      const shareUrl = link.dataset.share === 'linkedin'
        ? `https://www.linkedin.com/sharing/share-offsite/?url=${pageUrl}`
        : `https://www.facebook.com/sharer/sharer.php?u=${pageUrl}&quote=${title}`;
      window.open(shareUrl, 'share', 'width=720,height=560,noopener,noreferrer');
    });
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 1024 && nav?.classList.contains('active')) setNavState(false);
  });
})();
