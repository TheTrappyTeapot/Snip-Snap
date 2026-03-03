import { supabase } from "../services/supabaseClient.js";

const DEV_USERS = {
  customer: { email: "customer_test@snipsnap.local", password: "ChangeMe123!" },
  barber: { email: "barber_test@snipsnap.local", password: "ChangeMe123!" },
};

async function fetchBackendSession() {
  const { data } = await supabase.auth.getSession();
  const token = data?.session?.access_token;

  const res = await fetch("/api/session", {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });

  return res.json();
}

export function initDevAuthSwitcher({ selectId, buttonId, statusId }) {
  const selectEl = document.getElementById(selectId);
  const buttonEl = document.getElementById(buttonId);
  const statusEl = document.getElementById(statusId);

  async function renderStatus() {
    try {
      const info = await fetchBackendSession();
      statusEl.textContent = JSON.stringify(info);
    } catch (e) {
      statusEl.textContent = "Error reading session";
    }
  }

  buttonEl.addEventListener("click", async () => {
    const choice = selectEl.value;

    if (choice === "guest") {
      await supabase.auth.signOut();
      await renderStatus();
      return;
    }

    const creds = DEV_USERS[choice];
    if (!creds) return;

    // Sign in (dev only)
    const { error } = await supabase.auth.signInWithPassword({
      email: creds.email,
      password: creds.password,
    });

    if (error) {
      statusEl.textContent = `Sign-in failed: ${error.message}`;
      return;
    }

    await renderStatus();
  });

  // keep status live when auth changes in another tab too
  supabase.auth.onAuthStateChange(() => {
    renderStatus();
  });

  renderStatus();
}