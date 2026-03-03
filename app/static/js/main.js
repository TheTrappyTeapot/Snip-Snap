import { initUserPromos } from "./components/userPromo.js";

function initSharedComponents() {
	initUserPromos(document);
}

if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", initSharedComponents, { once: true });
} else {
	initSharedComponents();
}
