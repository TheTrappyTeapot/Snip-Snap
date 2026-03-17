const SUPABASE_URL = document.currentScript.getAttribute('data-supabase-url');
const SUPABASE_ANON_KEY = document.currentScript.getAttribute('data-supabase-anon-key');

// Setup Supabase
window.__sb__ = window.__sb__ || window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
const supabase = window.__sb__;

// Get form elements
const signupForm = document.getElementById("signupForm");
const submitBtn = document.getElementById("submitBtn");
const usernameInput = document.getElementById("username");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const usernameError = document.getElementById("usernameError");
const emailError = document.getElementById("emailError");
const passwordError = document.getElementById("passwordError");
const generalError = document.getElementById("generalError");

function clearErrors() {
  usernameError.textContent = "";
  emailError.textContent = "";
  passwordError.textContent = "";
  generalError.textContent = "";
}

function validateForm(username, email, password) {
  clearErrors();
  let isValid = true;

  // Username validation
  if (!username) {
    usernameError.textContent = "Username is required";
    isValid = false;
  } else if (username.length < 2) {
    usernameError.textContent = "Username must be at least 2 characters";
    isValid = false;
  } else if (username.length > 50) {
    usernameError.textContent = "Username must be less than 50 characters";
    isValid = false;
  }

  // Email validation
  if (!email) {
    emailError.textContent = "Email is required";
    isValid = false;
  } else if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
    emailError.textContent = "Please enter a valid email address";
    isValid = false;
  }

  // Password validation
  if (!password) {
    passwordError.textContent = "Password is required";
    isValid = false;
  } else if (password.length < 6) {
    passwordError.textContent = "Password must be at least 6 characters";
    isValid = false;
  } else if (password.length > 128) {
    passwordError.textContent = "Password is too long";
    isValid = false;
  }

  return isValid;
}

async function postTokenToFlask(access_token) {
  const res = await fetch("/auth/callback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ access_token }),
  });
  const json = await res.json();
  if (!json.ok) {
    throw new Error(json.error || "Auth callback failed");
  }
}

if (signupForm) {
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = usernameInput.value.trim();
    const email = emailInput.value.trim().toLowerCase();
    const password = passwordInput.value;

    // Validate form before submitting
    if (!validateForm(username, email, password)) {
      return;
    }

    // Disable submit button during request
    submitBtn.disabled = true;
    submitBtn.textContent = "Creating account…";

    try {
      // Step 1: Create App_User record
      const userRes = await fetch("/api/auth/create-user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, username }),
      });
      const userData = await userRes.json();

      if (!userData.ok) {
        if (userData.error.includes("email")) {
          emailError.textContent = userData.error;
        } else if (userData.error.includes("username")) {
          usernameError.textContent = userData.error;
        } else {
          generalError.textContent = userData.error;
        }
        submitBtn.disabled = false;
        submitBtn.textContent = "Create account";
        return;
      }

      // Step 2: Call Supabase signup
      const { data, error } = await supabase.auth.signUp({ email, password });

      if (error) {
        // Route error to appropriate field
        if (error.message.includes("email")) {
          emailError.textContent = error.message;
        } else if (error.message.includes("password")) {
          passwordError.textContent = error.message;
        } else if (error.message.includes("rate")) {
          generalError.textContent = "Too many signup attempts. Please try again later.";
        } else {
          generalError.textContent = error.message;
        }

        submitBtn.disabled = false;
        submitBtn.textContent = "Create account";
        return;
      }

      if (data.session?.access_token) {
        await postTokenToFlask(data.session.access_token);
        window.location.href = "/discover";
      } else {
        generalError.textContent = "Account created! Check your email to confirm, then log in.";
        submitBtn.disabled = false;
        submitBtn.textContent = "Create account";
      }
    } catch (error) {
      generalError.textContent = "Network error: " + error.message;
      submitBtn.disabled = false;
      submitBtn.textContent = "Create account";
    }
  });
}

// Google signup button
const googleBtn = document.getElementById("googleBtn");
if (googleBtn) {
  googleBtn.addEventListener("click", async () => {
    generalError.textContent = "Redirecting to Google…";
    try {
      await supabase.auth.signInWithOAuth({
        provider: "google",
        options: {
          redirectTo: window.location.origin + "/auth_redirect",
        },
      });
    } catch (error) {
      generalError.textContent = "Error: " + error.message;
    }
  });
}
