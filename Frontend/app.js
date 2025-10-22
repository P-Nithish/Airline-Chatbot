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
  function startSeatFlow(){
    seatFlow.active = true;
    seatFlow.step = "pnr";
    seatFlow.data = { pnr:"", flight_id:"", src:"", dst:"", airline_name:"" };
    addMsg(`To search seat availability, you can provide any of the following:<br>
      <code>{ "pnr": &lt;string&gt;, "flight_id": &lt;string&gt;, "src": &lt;string&gt;, "dst": &lt;string&gt;, "airline_name": &lt;string&gt; }</code><br>
      I’ll ask one by one — type your reply or <b>skip</b>.`, "bot");
    addMsg("PNR? (e.g., RWQ248) • or type <b>skip</b>", "bot");
  }

  function proceedSeatFlow(userText){
    const val = userText.trim();
    const lower = val.toLowerCase();

    if (lower === "exit") {
      seatFlow.active = false;
      seatFlow.step = null;
      addMsg("Seat availability flow cancelled.", "bot");
      return;
    }

    switch(seatFlow.step){
      case "pnr":
        if (lower !== "skip") seatFlow.data.pnr = val.toUpperCase();
        seatFlow.step = "flight_id";
        addMsg("Flight ID? (e.g., LH0109) • or <b>skip</b>", "bot");
        break;

      case "flight_id":
        if (lower !== "skip") seatFlow.data.flight_id = val.toUpperCase();
        seatFlow.step = "src";
        addMsg("Source airport (IATA)? (e.g., ATL) • or <b>skip</b>", "bot");
        break;

      case "src":
        if (lower !== "skip") seatFlow.data.src = val.toUpperCase();
        seatFlow.step = "dst";
        addMsg("Destination airport (IATA)? (e.g., MIA) • or <b>skip</b>", "bot");
        break;

      case "dst":
        if (lower !== "skip") seatFlow.data.dst = val.toUpperCase();
        seatFlow.step = "airline_name";
        addMsg("Airline name? (e.g., Lufthansa) • or <b>skip</b>", "bot");
        break;

      case "airline_name":
        if (lower !== "skip") seatFlow.data.airline_name = val;
        seatFlow.step = "done";
        const payload = {};
        Object.entries(seatFlow.data).forEach(([k,v]) => { if (v) payload[k]=v; });

        if (Object.keys(payload).length === 0){
          addMsg("Please provide at least one field (PNR / Flight ID / Route / Airline). Type <b>Seat Availability</b> again to restart.", "bot");
          seatFlow.active = false;
          seatFlow.step = null;
          return;
        }

        addMsg("Searching available seats…", "bot");
        seatFlow.active = false;
        seatFlow.step = null;
        callSeatAPI(payload);
        break;
    }
  }
