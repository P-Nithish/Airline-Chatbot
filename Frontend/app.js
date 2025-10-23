const API_BASE = "http://127.0.0.1:8000";

const qs = (s) => document.querySelector(s);

function showToast(msg, type = "info", timeout = 3500) {
  const toastContainer = qs("#toast-container");
  if (!toastContainer) return;
  const t = document.createElement("div");
  t.className = `toast ${type}`;
  t.textContent = msg;
  toastContainer.appendChild(t);
  setTimeout(() => t.remove(), timeout);
}

function setActiveTab(tab) {
  const signinTab = qs("#tab-signin");
  const signupTab = qs("#tab-signup");
  const fIn = qs("#form-signin");
  const fUp = qs("#form-signup");
  if (!signinTab || !signupTab || !fIn || !fUp) return;

  if (tab === "signin") {
    signinTab.classList.add("active");
    signupTab.classList.remove("active");
    fIn.classList.remove("hidden");
    fUp.classList.add("hidden");
  } else {
    signupTab.classList.add("active");
    signinTab.classList.remove("active");
    fUp.classList.remove("hidden");
    fIn.classList.add("hidden");
  }
}

async function postJSON(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}

document.addEventListener("DOMContentLoaded", () => {
  // Bind Sign In if the form exists on this page
  const signInForm = qs("#form-signin");
  if (signInForm) {
    signInForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = qs("#si-username")?.value.trim();
      const password = qs("#si-password")?.value;
      if (!username || !password) return showToast("Please enter username and password.", "error");

      const { ok, data, status } = await postJSON(`${API_BASE}/auth/login/`, { username, password });
      if (ok) {
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("username", data.username);
        showToast("Sign in successful!", "success");
        setTimeout(() => (window.location.href = "./chat.html"), 500);
      } else {
        const msg = data?.error || (status === 401 ? "Incorrect username or password." : "Sign in failed.");
        showToast(msg, "error");
      }
    });
  }

  // Bind Sign Up if the form exists on this page
  const signUpForm = qs("#form-signup");
  if (signUpForm) {
    signUpForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = qs("#su-username")?.value.trim();
      const password = qs("#su-password")?.value;
      if (!username || !password) return showToast("Please enter username and password.", "error");

      const { ok, data, status } = await postJSON(`${API_BASE}/auth/signup/`, { username, password });
      if (ok) {
        showToast("Account created successfully!", "success");
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("username", data.username);
        setTimeout(() => (window.location.href = "./chat.html"), 500);
      } else {
        const msg = data?.error || (status === 409 ? "Username already exists." : "Sign up failed.");
        showToast(msg, "error");
      }
    });
  }

  const tabSignin = qs("#tab-signin");
  const tabSignup = qs("#tab-signup");
  if (tabSignin && tabSignup) {
    tabSignin.addEventListener("click", () => setActiveTab("signin"));
    tabSignup.addEventListener("click", () => setActiveTab("signup"));
  }
});
  
