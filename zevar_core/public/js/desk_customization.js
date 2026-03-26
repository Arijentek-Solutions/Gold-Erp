/**
 * Zevar Core Desk Customization
 *
 * Enhances the standard Frappe desk with:
 * - Keyboard navigation shortcuts
 * - ARIA accessibility improvements
 * - Focus management
 * - High contrast mode support
 *
 * WCAG 2.1 AA compliant
 */

(function () {
	"use strict";

	// Wait for DOM to be ready
	function ready(fn) {
		if (document.readyState !== "loading") {
			fn();
		} else {
			document.addEventListener("DOMContentLoaded", fn);
		}
	}

	ready(function () {
		enhanceDesktopAccessibility();
		setupKeyboardNavigation();
		setupFocusManagement();
		detectAccessibilityPreferences();
		addSkipLink();
	});

	/**
	 * Enhance desktop icons with ARIA attributes
	 */
	function enhanceDesktopAccessibility() {
		// Wait for desktop to fully load
		setTimeout(function () {
			var icons = document.querySelectorAll(".desktop-icon");
			icons.forEach(function (icon, index) {
				// Add ARIA role
				icon.setAttribute("role", "button");
				icon.setAttribute("tabindex", "0");

				// Get label from icon
				var labelEl = icon.querySelector(".icon-title");
				if (labelEl) {
					icon.setAttribute("aria-label", labelEl.textContent.trim());
				}

				// Add description for screen readers
				var descId = "zevar-icon-desc-" + index;
				icon.setAttribute("aria-describedby", descId);

				// Create hidden description element if not exists
				if (!document.getElementById(descId)) {
					var desc = document.createElement("span");
					desc.id = descId;
					desc.className = "sr-only";
					desc.textContent = "Double click or press Enter to open";
					icon.appendChild(desc);
				}

				// Add keyboard activation
				icon.addEventListener("keydown", function (e) {
					if (e.key === "Enter" || e.key === " ") {
						e.preventDefault();
						icon.click();
					}
				});
			});

			// Enhance workspace cards
			var workspaceCards = document.querySelectorAll(".workspace-card");
			workspaceCards.forEach(function (card) {
				card.setAttribute("role", "article");
			});

			// Enhance shortcuts
			var shortcuts = document.querySelectorAll(".workspace-shortcut");
			shortcuts.forEach(function (shortcut) {
				shortcut.setAttribute("role", "button");
				shortcut.setAttribute("tabindex", "0");
			});
		}, 1000);
	}

	/**
	 * Setup keyboard shortcuts for quick navigation
	 */
	function setupKeyboardNavigation() {
		document.addEventListener("keydown", function (e) {
			// Don't trigger if user is typing in an input
			if (
				e.target.tagName === "INPUT" ||
				e.target.tagName === "TEXTAREA" ||
				e.target.isContentEditable
			) {
				return;
			}

			// Alt + key shortcuts for quick access
			if (e.altKey) {
				var key = e.key.toLowerCase();

				// Default Zevar shortcuts
				var defaultShortcuts = {
					p: "/pos", // POS Terminal
					e: "/employee-portal", // Employee Portal
					l: "/app/layaway-contract", // Layaway
					r: "/app/repair-order", // Repairs
					t: "/app/trade-in-record", // Trade-ins
					g: "/app/gift-card", // Gift Cards
					a: "/app/jewelry-appraisal", // Appraisals
					c: "/app/sales-commission-split", // Commissions
					d: "/zevar-desk", // Custom Desk
					h: "/desk", // Home/Standard Desk
				};

				if (defaultShortcuts[key]) {
					e.preventDefault();
					window.location.href = defaultShortcuts[key];
					return;
				}

				// Alt+1 through Alt+9 for quick access to first 9 desktop icons
				if (key >= "1" && key <= "9") {
					e.preventDefault();
					var icons = document.querySelectorAll(".desktop-icon");
					var index = parseInt(key) - 1;
					if (icons[index]) {
						icons[index].click();
					}
				}
			}

			// Escape to close modals
			if (e.key === "Escape") {
				closeAllModals();
			}

			// Focus search with Ctrl+K or Cmd+K
			if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
				e.preventDefault();
				focusSearch();
			}
		});
	}

	/**
	 * Setup focus management for better keyboard UX
	 */
	function setupFocusManagement() {
		// Add visible focus indicators via CSS injection
		var style = document.createElement("style");
		style.textContent = [
			// Screen reader only utility
			".sr-only {",
			"  position: absolute;",
			"  width: 1px;",
			"  height: 1px;",
			"  padding: 0;",
			"  margin: -1px;",
			"  overflow: hidden;",
			"  clip: rect(0, 0, 0, 0);",
			"  white-space: nowrap;",
			"  border: 0;",
			"}",
			"",
			// Focus indicators
			".desktop-icon:focus,",
			".desktop-icon:focus-visible,",
			".workspace-shortcut:focus,",
			".workspace-shortcut:focus-visible {",
			"  outline: 3px solid var(--blue-500, #4f9cff);",
			"  outline-offset: 2px;",
			"  border-radius: 8px;",
			"}",
			"",
			// High contrast mode support
			"@media (prefers-contrast: high) {",
			"  .desktop-icon,",
			"  .workspace-shortcut {",
			"    border: 2px solid currentColor;",
			"  }",
			"}",
			"",
			// Reduced motion support
			"@media (prefers-reduced-motion: reduce) {",
			"  .desktop-icon,",
			"  .desktop-icon *,",
			"  .workspace-shortcut,",
			"  .workspace-shortcut *,",
			"  .modal,",
			"  .modal * {",
			"    transition: none !important;",
			"    animation: none !important;",
			"  }",
			"}",
			"",
			// Minimum touch target size for mobile
			"@media (pointer: coarse) {",
			"  .desktop-icon,",
			"  .workspace-shortcut {",
			"    min-width: 44px;",
			"    min-height: 44px;",
			"  }",
			"}",
		].join("\n");
		document.head.appendChild(style);

		// Trap focus in modals
		$(document).on("shown.bs.modal", ".modal", function () {
			var modal = this;
			var focusableElements = modal.querySelectorAll(
				'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
			);
			if (focusableElements.length > 0) {
				focusableElements[0].focus();
			}
		});
	}

	/**
	 * Detect and respond to accessibility preferences
	 */
	function detectAccessibilityPreferences() {
		// High contrast mode
		if (window.matchMedia("(prefers-contrast: high)").matches) {
			document.body.classList.add("zevar-high-contrast");
		}

		// Reduced motion
		if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
			document.body.classList.add("zevar-reduced-motion");
		}

		// Listen for preference changes
		window.matchMedia("(prefers-contrast: high)").addEventListener("change", function (e) {
			document.body.classList.toggle("zevar-high-contrast", e.matches);
		});

		window
			.matchMedia("(prefers-reduced-motion: reduce)")
			.addEventListener("change", function (e) {
				document.body.classList.toggle("zevar-reduced-motion", e.matches);
			});
	}

	/**
	 * Add skip link for keyboard navigation
	 */
	function addSkipLink() {
		// Check if skip link already exists
		if (document.querySelector(".zevar-skip-link")) {
			return;
		}

		var skipLink = document.createElement("a");
		skipLink.href = "#main-content";
		skipLink.className = "zevar-skip-link";
		skipLink.textContent = "Skip to main content";
		skipLink.style.cssText = [
			"position: absolute;",
			"top: -100%;",
			"left: 50%;",
			"transform: translateX(-50%);",
			"background: #1f2937;",
			"color: white;",
			"padding: 12px 24px;",
			"border-radius: 8px;",
			"text-decoration: none;",
			"font-weight: 500;",
			"z-index: 99999;",
			"transition: top 0.2s ease;",
		].join("");

		skipLink.addEventListener("focus", function () {
			this.style.top = "16px";
		});

		skipLink.addEventListener("blur", function () {
			this.style.top = "-100%";
		});

		document.body.insertBefore(skipLink, document.body.firstChild);

		// Add id to main content if not exists
		var mainContent = document.querySelector("main") || document.querySelector(".desk-body");
		if (mainContent && !mainContent.id) {
			mainContent.id = "main-content";
		}
	}

	/**
	 * Close all open modals
	 */
	function closeAllModals() {
		var modals = document.querySelectorAll(".modal.show, .modal-dialog");
		modals.forEach(function (modal) {
			var closeBtn = modal.querySelector('.close, [data-dismiss="modal"], .modal-close');
			if (closeBtn) {
				closeBtn.click();
			}
		});

		// Close dropdowns
		var dropdowns = document.querySelectorAll(".dropdown.open, .show");
		dropdowns.forEach(function (dropdown) {
			dropdown.classList.remove("open", "show");
		});

		// Close any open overlays
		var overlay = document.querySelector(".modal-backdrop");
		if (overlay) {
			overlay.click();
		}
	}

	/**
	 * Focus the search input
	 */
	function focusSearch() {
		var searchInput = document.querySelector(
			'#search-input, input[type="search"], .search-input'
		);
		if (searchInput) {
			searchInput.focus();
		}
	}

	// Expose utilities globally for custom desk page
	window.ZevarDesk = {
		closeAllModals: closeAllModals,
		focusSearch: focusSearch,
		enhanceAccessibility: enhanceDesktopAccessibility,
	};
})();
