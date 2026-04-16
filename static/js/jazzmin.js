// Handling Form Groups (Multiple columns)
document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll(".form-group .row > label.col-sm-3")
    .forEach(function (label) {
      label.classList.remove("col-sm-3");
      label.classList.add("col-sm-1-5");
    });
});

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".form-group .row").forEach(function (row) {
    const children = Array.from(row.children);

    children.forEach((el, index) => {
      if (
        el.tagName === "LABEL" &&
        index > 0 &&
        children[index - 1].classList.contains("fieldBox")
      ) {
        el.style.marginLeft = "80px";
        el.classList.add("col-sm-1-5");
      }
    });
  });
});

// Remove Eye Icon
document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll(".related-widget-wrapper-link.view-related")
    .forEach((el) => el.remove());
});

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("input[type='email']").forEach(function (el) {
    el.classList.add("vTextField");
  });
});
