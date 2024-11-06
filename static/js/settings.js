import feather from "feather-icons";

// THIS FILE IS FOR DEMO PURPOSES ONLY
// AND CAN BE REMOVED AFTER PICKING A STYLE
// JUST BEFORE THE </head> CLOSING TAG

// Set cookie
function setCookie(name, value, days) {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Get cookie
function getCookie(name) {
  const nameEQ = name + "=";
  const ca = document.cookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    const c = ca[i];
    while (c.charAt(0) == " ") c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

// Get query parameter
function getQueryParameter(name) {
  let queryParameter = undefined;
  location.search
    .substr(1)
    .split("&")
    .some(function(item) {
      // returns first occurence and stops
      return (
        item.split("=")[0] == name && (queryParameter = item.split("=")[1])
      );
    });
  return queryParameter;
}

// Get current theme
function getCurrentTheme() {
  const cookie = getCookie("theme");
  const queryParameter = getQueryParameter("theme");

  if (queryParameter) {
    setCookie("theme", queryParameter, 7);
    return queryParameter;
  }

  return cookie ? cookie : "classic";
}

// Append theme style-tag to <head>
const link = document.createElement("link");
link.href = "css/" + getCurrentTheme() + ".css";
link.type = "text/css";
link.rel = "stylesheet";
document.getElementsByTagName("head")[0].appendChild(link);

// Append settings sidebar after page load
document.addEventListener("DOMContentLoaded", function() {
  const html = `<div class="settings">
    <div class="settings-toggle toggle-settings">
      <i class="align-middle" data-feather="settings"></i>
    </div>

    <div class="settings-panel">
      <div class="settings-content js-simplebar">
        <div class="settings-title">
          <button type="button" class="close float-right toggle-settings" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>

          <h4>Settings</h4>
        </div>

        <div class="settings-section">
          <small class="d-block text-uppercase font-weight-bold text-muted mb-2">Layouts</small>

          <ul class="settings-layouts">
            <li>
              <a class="settings-layouts-item" href="layouts-sidebar-sticky.html">
                Sticky Sidebar
                <small class="badge float-right mt-1">
                  <i class="fas fa-angle-right"></i>
                </small>
              </a>
            </li>
            <li>
              <a class="settings-layouts-item" href="layouts-sidebar-collapsed.html">
                Collapsed Sidebar
                <small class="badge float-right mt-1">
                  <i class="fas fa-angle-right"></i>
                </small>
              </a>
            </li>
            <li>
              <a class="settings-layouts-item" href="layouts-boxed.html">
                Boxed Layout
                <small class="badge float-right mt-1">
                  <i class="fas fa-angle-right"></i>
                </small>
              </a>
            </li>
          </ul>
        </div>

        <div class="settings-section">
          <small class="d-block text-uppercase font-weight-bold text-muted mb-2">Themes</small>

          <a class="settings-theme" href="dashboard-analytics.html?theme=classic">
            <img src="img/screenshots/theme-classic-small.png" class="img-fluid" alt="Classic" />
            <span class="d-inline-block mt-1 text-muted">Classic</span>
          </a>

          <a class="settings-theme" href="dashboard-analytics.html?theme=corporate">
            <img src="img/screenshots/theme-corporate-small.png" class="img-fluid" alt="Corporate" />
            <span class="d-inline-block mt-1 text-muted">Corporate</span>
          </a>

          <a class="settings-theme" href="dashboard-analytics.html?theme=modern">
            <img src="img/screenshots/theme-modern-small.png" class="img-fluid" alt="Modern" />
            <span class="d-inline-block mt-1 text-muted">Modern</span>
          </a>

          <a href="https://themes.getbootstrap.com/product/appstack-responsive-admin-template/" target="_blank" class="btn btn-primary btn-block btn-lg"><i class="fas fa-shopping-cart"></i> Buy AppStack</a>
        </div>

      </div>
    </div>
  </div>`;

  // Append html to body
  $("body").append(html);

  // Replace feather icons
  feather.replace();

  // Toggle settings
  $(".toggle-settings").on("click", function(e) {
    e.preventDefault();

    $(".settings").toggleClass("open");
  });
});
