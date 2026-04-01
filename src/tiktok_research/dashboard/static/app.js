function debounce(callback, delay) {
  let timer = null;
  return (...args) => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => callback(...args), delay);
  };
}

function initThemeToggle() {
  const themeButtons = Array.from(document.querySelectorAll("[data-theme-option]"));
  if (themeButtons.length === 0) {
    return;
  }

  const storageKey = "researchDashboardTheme";
  const root = document.documentElement;

  const getTheme = () => {
    const currentTheme = root.dataset.theme;
    if (currentTheme === "light" || currentTheme === "dark") {
      return currentTheme;
    }
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  };

  const syncButtons = (theme) => {
    themeButtons.forEach((button) => {
      const isActive = button.dataset.themeOption === theme;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
    });
  };

  const applyTheme = (theme) => {
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    syncButtons(theme);
  };

  applyTheme(getTheme());

  themeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const selectedTheme = button.dataset.themeOption;
      if (selectedTheme !== "light" && selectedTheme !== "dark") {
        return;
      }
      applyTheme(selectedTheme);
      try {
        window.localStorage.setItem(storageKey, selectedTheme);
      } catch (error) {
        console.error(error);
      }
    });
  });
}

function initQueueFilters() {
  const grid = document.getElementById("queue-grid");
  const searchInput = document.getElementById("queue-search");
  const filterButtons = Array.from(document.querySelectorAll("[data-status-filter]"));

  if (!grid || !searchInput || filterButtons.length === 0) {
    return;
  }

  let activeStatus = "all";

  const applyFilters = () => {
    const searchValue = searchInput.value.trim().toLowerCase();
    const cards = Array.from(grid.querySelectorAll(".queue-card"));

    cards.forEach((card) => {
      const matchesStatus = activeStatus === "all" || card.dataset.status === activeStatus;
      const matchesSearch = !searchValue || card.dataset.search.includes(searchValue);
      card.hidden = !(matchesStatus && matchesSearch);
    });
  };

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      activeStatus = button.dataset.statusFilter;
      filterButtons.forEach((item) => item.classList.toggle("is-active", item === button));
      applyFilters();
    });
  });

  searchInput.addEventListener("input", applyFilters);
}

function initWorkspaceForm() {
  const form = document.getElementById("rating-form");
  if (!form) {
    return;
  }

  const apiUrl = form.dataset.apiUrl;
  const initialResponses = JSON.parse(form.dataset.initial || "{}");
  const initialMissing = JSON.parse(form.dataset.missing || "[]");
  const saveStatus = document.getElementById("save-status");
  const progressBar = document.getElementById("progress-bar");
  const progressLabel = document.getElementById("progress-label");
  const discernTotalNode = document.getElementById("discern-total");
  const completionModal = document.getElementById("completion-modal");
  const fieldCards = Array.from(document.querySelectorAll("[data-field-card]"));
  const sections = Array.from(document.querySelectorAll("[data-step-section]"));
  let activeStep = 0;
  let lastIsComplete = form.dataset.isComplete === "1";

  const cardIsConditionallyHidden = (card) => card.classList.contains("is-conditionally-hidden");

  const readForm = () => {
    const data = {};
    fieldCards.forEach((card) => {
      if (cardIsConditionallyHidden(card)) {
        return;
      }
      const fieldId = card.dataset.fieldCard;
      const multiInputs = card.querySelectorAll(`input[type="checkbox"][data-field="${fieldId}"]`);
      if (multiInputs.length > 0) {
        data[fieldId] = Array.from(multiInputs)
          .filter((input) => input.checked)
          .map((input) => input.value);
        return;
      }

      const radio = card.querySelector(`input[type="radio"][name="${fieldId}"]:checked`);
      if (radio) {
        data[fieldId] = radio.value;
        return;
      } else if (card.querySelector(`input[type="radio"][name="${fieldId}"]`)) {
        data[fieldId] = "";
        return;
      }

      const textarea = card.querySelector(`textarea[data-field="${fieldId}"]`);
      if (textarea) {
        data[fieldId] = textarea.value.trim();
      }
    });
    return data;
  };

  const writeForm = (responses) => {
    fieldCards.forEach((card) => {
      const fieldId = card.dataset.fieldCard;
      const value = responses[fieldId];
      const radioInputs = card.querySelectorAll(`input[type="radio"][name="${fieldId}"]`);
      radioInputs.forEach((input) => {
        input.checked = value === input.value;
      });

      const checkboxInputs = card.querySelectorAll(`input[type="checkbox"][data-field="${fieldId}"]`);
      checkboxInputs.forEach((input) => {
        input.checked = Array.isArray(value) && value.includes(input.value);
      });

      const textarea = card.querySelector(`textarea[data-field="${fieldId}"]`);
      if (textarea) {
        textarea.value = typeof value === "string" ? value : "";
      }
    });
  };

  const updateConditionalVisibility = () => {
    const current = readForm();
    fieldCards.forEach((card) => {
      const controllingField = card.dataset.conditionalField;
      if (!controllingField) {
        card.classList.remove("is-conditionally-hidden");
        return;
      }

      const allowedValues = (card.dataset.conditionalValues || "")
        .split(",")
        .filter(Boolean);
      card.classList.toggle("is-conditionally-hidden", !allowedValues.includes(current[controllingField]));
    });
  };

  const highlightMissing = (missingIds) => {
    fieldCards.forEach((card) => {
      card.classList.toggle(
        "is-missing",
        missingIds.includes(card.dataset.fieldCard) && !cardIsConditionallyHidden(card),
      );
    });
  };

  const sectionState = (section) => {
    const cards = Array.from(section.querySelectorAll("[data-field-card]"));
    const visibleCards = cards.filter((card) => !cardIsConditionallyHidden(card));
    const requiredCards = visibleCards.filter((card) => {
      return card.dataset.required === "1" || Boolean(card.dataset.conditionalField);
    });
    const responses = readForm();
    const answeredCards = requiredCards.filter((card) => {
      const fieldId = card.dataset.fieldCard;
      const value = responses[fieldId];
      return Array.isArray(value) ? value.length > 0 : Boolean(value);
    });
    return {
      requiredCount: requiredCards.length,
      answeredCount: answeredCards.length,
      complete: requiredCards.length > 0 && answeredCards.length === requiredCards.length,
    };
  };

  const scrollActiveSectionIntoView = () => {
    const activeSection = sections[activeStep];
    if (!activeSection) {
      return;
    }

    window.requestAnimationFrame(() => {
      activeSection.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    });
  };

  const showCompletionModal = () => {
    if (!completionModal) {
      return;
    }
    completionModal.hidden = false;
    completionModal.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-open");
  };

  const hideCompletionModal = () => {
    if (!completionModal) {
      return;
    }
    completionModal.hidden = true;
    completionModal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
  };

  const firstSectionWithMissing = () => {
    const current = readForm();
    const missing = [];
    fieldCards.forEach((card) => {
      if (cardIsConditionallyHidden(card)) {
        return;
      }
      const required = card.dataset.required === "1" || Boolean(card.dataset.conditionalField);
      if (!required) {
        return;
      }
      const fieldId = card.dataset.fieldCard;
      const value = current[fieldId];
      const answered = Array.isArray(value) ? value.length > 0 : Boolean(value);
      if (!answered) {
        missing.push(fieldId);
      }
    });

    if (missing.length === 0) {
      return 0;
    }

    const foundIndex = sections.findIndex((section) => {
      const ids = Array.from(section.querySelectorAll("[data-field-card]")).map((card) => card.dataset.fieldCard);
      return ids.some((id) => missing.includes(id));
    });
    return foundIndex >= 0 ? foundIndex : 0;
  };

  const updateStepUi = () => {
    sections.forEach((section, index) => {
      section.hidden = index !== activeStep;
      section.classList.toggle("is-active", index === activeStep);
    });
  };

  const setSaveState = (status, label) => {
    saveStatus.textContent = label;
    saveStatus.classList.toggle("is-saving", status === "saving");
    saveStatus.classList.toggle("is-error", status === "error");
  };

  const syncSummary = (payload) => {
    progressBar.style.width = `${payload.progress_pct}%`;
    progressLabel.textContent = `This video: ${payload.progress_pct}% complete`;
    discernTotalNode.textContent = payload.discern_total ?? "—";
    highlightMissing(payload.missing_required || []);
    updateStepUi();

    const nowComplete = Boolean(payload.is_complete);
    if (nowComplete && !lastIsComplete) {
      showCompletionModal();
    }
    if (!nowComplete) {
      hideCompletionModal();
    }
    lastIsComplete = nowComplete;
  };

  const sendSave = debounce(async () => {
    const responses = readForm();
    setSaveState("saving", "Saving...");

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ responses }),
      });
      if (!response.ok) {
        throw new Error(`Save failed with status ${response.status}`);
      }
      const payload = await response.json();
      syncSummary(payload);
      setSaveState("saved", payload.is_complete ? "Complete" : "Saved");
    } catch (error) {
      console.error(error);
      setSaveState("error", "Save failed");
    }
  }, 450);

  writeForm(initialResponses);
  updateConditionalVisibility();
  highlightMissing(initialMissing);
  activeStep = firstSectionWithMissing();
  updateStepUi();
  hideCompletionModal();

  form.querySelectorAll("[data-step-prev]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      const currentSection = event.currentTarget.closest("[data-step-section]");
      const currentStep = currentSection ? Number(currentSection.dataset.stepSection) : activeStep;
      activeStep = Math.max(0, currentStep - 1);
      updateStepUi();
      scrollActiveSectionIntoView();
    });
  });

  form.querySelectorAll("[data-step-next]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      const currentSection = event.currentTarget.closest("[data-step-section]");
      const currentStep = currentSection ? Number(currentSection.dataset.stepSection) : activeStep;
      activeStep = Math.min(sections.length - 1, currentStep + 1);
      updateStepUi();
      scrollActiveSectionIntoView();
    });
  });

  const syncFormFlow = () => {
    updateConditionalVisibility();
    updateStepUi();
  };

  form.addEventListener("input", () => {
    syncFormFlow();
    sendSave();
  });

  form.addEventListener("change", (event) => {
    syncFormFlow();
    sendSave();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initThemeToggle();
  initQueueFilters();
  initWorkspaceForm();
});
