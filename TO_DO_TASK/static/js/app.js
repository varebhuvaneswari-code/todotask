(() => {
  const storageKey = "todoflow-theme";
  const root = document.documentElement;

  function preferredTheme() {
    const saved = localStorage.getItem(storageKey);
    if (saved === "dark" || saved === "light") return saved;
    if (document.body?.classList.contains("theme-dark")) return "dark";
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function applyTheme(theme) {
    const isDark = theme === "dark";
    root.dataset.theme = theme;
    document.body.classList.toggle("theme-dark", isDark);
    document.body.classList.toggle("theme-light", !isDark);
    localStorage.setItem(storageKey, theme);

    const toggle = document.querySelector("#themeToggle");
    if (toggle) {
      toggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
      toggle.setAttribute("title", isDark ? "Light mode" : "Dark mode");
      toggle.innerHTML = isDark ? '<i class="bi bi-sun"></i>' : '<i class="bi bi-moon-stars"></i>';
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    applyTheme(preferredTheme());

    document.querySelector("#themeToggle")?.addEventListener("click", () => {
      applyTheme(root.dataset.theme === "dark" ? "light" : "dark");
    });
    window.todoFlowThemeReady = true;

    document.querySelectorAll("[data-password-toggle]").forEach((button) => {
      button.addEventListener("click", () => {
        const input = button.parentElement.querySelector("input");
        if (!input) return;
        input.type = input.type === "password" ? "text" : "password";
        button.innerHTML = input.type === "password" ? '<i class="bi bi-eye"></i>' : '<i class="bi bi-eye-slash"></i>';
      });
    });

    document.querySelectorAll("[data-confirm]").forEach((form) => {
      form.addEventListener("submit", (event) => {
        if (!confirm(form.dataset.confirm)) event.preventDefault();
      });
    });

    document.querySelectorAll("[data-toggle-form]").forEach((form) => {
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const card = form.closest("[data-task-card]");
        const icon = form.querySelector("i");
        try {
          const response = await fetch(form.action, {
            method: "POST",
            headers: {
              "X-Requested-With": "XMLHttpRequest",
              "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
            },
          });
          if (!response.ok) throw new Error("Toggle failed");
          const data = await response.json();
          card.classList.toggle("is-complete", data.completed);
          card.classList.add("complete-pulse");
          icon.className = data.completed ? "bi bi-check-circle-fill" : "bi bi-circle";
          setTimeout(() => card.classList.remove("complete-pulse"), 650);
        } catch {
          form.submit();
        }
      });
    });

    document.querySelectorAll(".needs-validation input").forEach((input) => {
      input.addEventListener("blur", () => input.classList.toggle("is-valid", input.value.trim().length > 0));
    });

    document.querySelectorAll(".todo-card, .stat-card, .task-preview, .panel").forEach((item, index) => {
      item.style.setProperty("--delay", `${Math.min(index * 45, 360)}ms`);
      item.classList.add("reveal-item");
    });

    if (window.bootstrap?.Tooltip) {
      document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => new bootstrap.Tooltip(el));
    }
  });
})();
