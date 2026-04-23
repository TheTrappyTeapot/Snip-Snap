/* Script for app/static/js/pages/signup.js. */

console.log("signup.js script loading");

// Prevent double-loading
if (window.__signupJsLoaded) {
  console.warn("signup.js already loaded, skipping");
} else {
  window.__signupJsLoaded = true;

  // Get data attributes from the script tag
  let SUPABASE_URL = '';
  let SUPABASE_ANON_KEY = '';

  try {
    const scriptTag = document.currentScript;
    if (scriptTag) {
      SUPABASE_URL = scriptTag.getAttribute('data-supabase-url');
      SUPABASE_ANON_KEY = scriptTag.getAttribute('data-supabase-anon-key');
      console.log("Script attributes found - SUPABASE_URL:", SUPABASE_URL ? "loaded" : "missing");
    } else {
      console.error("document.currentScript is not available");
    }
  } catch (e) {
    console.error("Error reading script attributes:", e);
  }

  // Setup Supabase
  let supabase = null;
  try {
    if (!window.supabase) {
      console.error("Supabase library not loaded");
    } else if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      window.__sb__ = window.__sb__ || window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
      supabase = window.__sb__;
      console.log("Supabase client initialized");
    } else {
      console.error("Supabase credentials missing");
    }
  } catch (e) {
    console.error("Error initializing Supabase:", e);
  }

  // Initialize form when DOM is ready
  function initializeForm() {
  console.log("Initializing form...");
  
  const signupForm = document.getElementById("signupForm");
  const submitBtn = document.getElementById("submitBtn");
  const usernameInput = document.getElementById("username");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const usernameError = document.getElementById("usernameError");
  const emailError = document.getElementById("emailError");
  const passwordError = document.getElementById("passwordError");
  const accountTypeError = document.getElementById("accountTypeError");
  const generalError = document.getElementById("generalError");
  const googleBtn = document.getElementById("googleBtn");
  
  console.log("Form elements found:", {
    signupForm: !!signupForm,
    submitBtn: !!submitBtn,
    usernameInput: !!usernameInput,
    emailInput: !!emailInput,
    passwordInput: !!passwordInput
  });
  
  if (!signupForm) {
    console.error("Signup form not found in the page");
    return;
  }

  /**
   * Clears all visible validation and general error messages.
   */
  function clearErrors() {
    usernameError.textContent = "";
    emailError.textContent = "";
    passwordError.textContent = "";
    accountTypeError.textContent = "";
    generalError.textContent = "";
  }

  /**
   * Validates signup inputs and returns true when the form is valid.
   */
  function validateForm(username, email, password, accountType) {
    clearErrors();
    let isValid = true;

    // Account type validation
    if (!accountType) {
      accountTypeError.textContent = "Please select an account type";
      isValid = false;
    }

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

  // Attach form submit handler
  signupForm.addEventListener("submit", async (e) => {
    console.log("Form submit event triggered");
    e.preventDefault();
    console.log("Form submission prevented, proceeding with async signup");

    const username = usernameInput.value.trim();
    const email = emailInput.value.trim().toLowerCase();
    const password = passwordInput.value;
    const accountType = document.querySelector('input[name="accountType"]:checked')?.value || '';

    console.log("Form values:", { username, email, accountType, passwordLength: password.length });

    // Validate form before submitting
    if (!validateForm(username, email, password, accountType)) {
      console.log("Form validation failed");
      return;
    }

    // Disable submit button during request
    submitBtn.disabled = true;
    submitBtn.textContent = "Creating account…";

    try {
      // Step 1: Create App_User record
      console.log("Attempting to create user:", { email, username, role: accountType });
      const userRes = await fetch("/api/auth/create-user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, username, role: accountType }),
      });
      const userData = await userRes.json();
      console.log("User creation response:", userData, "Status:", userRes.status);

      if (!userRes.ok || !userData.ok) {
        const errorMsg = userData.error || "Failed to create user account";
        console.log("User creation failed:", errorMsg);
        if (errorMsg.toLowerCase().includes("email")) {
          emailError.textContent = errorMsg;
        } else if (errorMsg.toLowerCase().includes("username")) {
          usernameError.textContent = errorMsg;
        } else {
          generalError.textContent = errorMsg;
        }
        submitBtn.disabled = false;
        submitBtn.textContent = "Create account";
        return;
      }

      // Step 2: Call Supabase signup
      if (!supabase) {
        throw new Error("Supabase client not initialized");
      }

      console.log("Calling Supabase signup...");
      const { data, error } = await supabase.auth.signUp({ email, password });
      console.log("Supabase signup response:", { data, error });

      if (error) {
        console.log("Supabase signup error:", error);
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

      console.log("Signup successful, session:", data.session?.access_token ? "Has token" : "No token");
      if (data.session?.access_token) {
        await postTokenToFlask(data.session.access_token);
        console.log("Token posted to Flask, redirecting to profile page...");
        window.location.href = "/profile";
      } else {
        generalError.textContent = "Account created! Check your email to confirm, then log in.";
        submitBtn.disabled = false;
        submitBtn.textContent = "Create account";
      }
    } catch (error) {
      console.error("Signup error:", error);
      generalError.textContent = "Network error: " + error.message;
      submitBtn.disabled = false;
      submitBtn.textContent = "Create account";
    }
  });

  // Google signup button
  if (googleBtn) {
    googleBtn.addEventListener("click", async () => {
      try {
        if (!supabase) {
          throw new Error("Supabase not initialized");
        }
        const { data, error } = await supabase.auth.signInWithOAuth({
          provider: 'google',
          options: {
            redirectTo: window.location.origin + '/auth/callback',
          },
        });
        if (error) throw error;
      } catch (error) {
        console.error("Google signup error:", error);
        generalError.textContent = "Google signup failed: " + error.message;
      }
    });
  }
  
  console.log("Form initialization complete");
}

// Wait for DOM to be ready
if (document.readyState === 'loading') {
  console.log("DOM still loading, waiting for DOMContentLoaded event");
  document.addEventListener('DOMContentLoaded', initializeForm);
} else {
  console.log("DOM already loaded, initializing form immediately");
  initializeForm();
}
} // End of if (!window.__signupJsLoaded) block
