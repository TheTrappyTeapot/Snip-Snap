import { initDevAuthSwitcher } from "../features/devAuthSwitcher.js";

document.addEventListener("DOMContentLoaded", () => {
  initDevAuthSwitcher({
    selectId: "devUserSelect",
    buttonId: "devUserApplyBtn",
    statusId: "devAuthStatus",
  });
});