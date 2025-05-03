const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

$("#search-icon").click(function () {
  $(".nav").toggleClass("search");
  $(".nav").toggleClass("no-search");
  $(".search-input").toggleClass("search-active");
});

$('.menu-toggle').click(function () {
  $(".nav").toggleClass("mobile-nav");
  $(this).toggleClass("is-active");
});

const form = document.getElementById("registerForm");

const fields = [
  {
    id: "full-name",
    pattern: /^[A-Za-z\s]+$/,
    error: "Full Name must only contain letters and spaces.",
  },
  {
    id: "register-email",
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    error: "Please enter a valid email address.",
  },
  {
    id: "confirm-email",
    matchWith: "register-email",
    error: "Emails do not match.",
  },
  {
    id: "register-password",
    pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$/,
    error: "Password must be at least 8 characters long, with uppercase, lowercase, and special character.",
  },
  {
    id: "confirm-password",
    matchWith: "register-password",
    error: "Passwords do not match.",
  },
  {
    id: "phone",
    pattern: /^\d{10}$/,
    error: "Please enter a valid 10-digit phone number.",
  },
  {
    id: "college",
    pattern: /^[A-Za-z\s]+$/,
    error: "College Name must only contain letters and spaces.",
  },
  {
    id: "branch",
    pattern: /^[A-Za-z\s]+$/,
    error: "Branch must only contain letters and spaces.",
  },
  {
    id: "passing-year",
    pattern: /^\d{4}$/,
    error: "Passing Year must be a 4-digit number.",
  },
];

fields.forEach((field) => {
  const input = document.getElementById(field.id);
  input.addEventListener("input", () => validateField(field));
});

document.getElementById("terms").addEventListener("change", () => {
  document.getElementById("error-terms").textContent =
    document.getElementById("terms").checked
      ? ""
      : "You must accept the Terms and Conditions.";
});

function validateField(field) {
  const input = document.getElementById(field.id);
  const errorDiv = document.getElementById(`error-${field.id}`);

  if (field.matchWith) {
    const otherVal = document.getElementById(field.matchWith).value;
    errorDiv.textContent = input.value !== otherVal ? field.error : "";
  } else if (field.pattern) {
    errorDiv.textContent = field.pattern.test(input.value) ? "" : field.error;
  }
}

form.addEventListener("submit", function (e) {
  e.preventDefault();
  let isValid = true;

  fields.forEach((field) => {
    validateField(field);
    const errorText = document.getElementById(`error-${field.id}`).textContent;
    if (errorText) isValid = false;
  });

  if (!document.getElementById("terms").checked) {
    document.getElementById("error-terms").textContent =
      "You must accept the Terms and Conditions.";
    isValid = false;
  }

  if (isValid) {
    const email = document.getElementById("register-email").value;

    if (localStorage.getItem(`user-${email}`)) {
      alert("User already registered. You cannot register again.");
    } else {
      localStorage.setItem(
        `user-${email}`,
        JSON.stringify({ registered: true })
      );
      alert("Registration successful!");
      form.reset();
      document
        .querySelectorAll(".error-text")
        .forEach((el) => (el.textContent = ""));
      window.location.href = "newlogin.html";
    }
  }
});
